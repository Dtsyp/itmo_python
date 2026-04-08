import functools
import inspect
from typing import Any, Callable, TypeVar

F = TypeVar("F", bound=Callable)


def validate_types(func: F) -> F:
    """Декоратор для runtime-проверки типов по аннотациям функции."""
    sig = inspect.signature(func)
    ann = func.__annotations__

    @functools.wraps(func)
    def inner(*a: Any, **kw: Any) -> Any:
        params = sig.bind(*a, **kw)
        params.apply_defaults()

        for pname, pval in params.arguments.items():
            if pname not in ann:
                continue
            if not isinstance(pval, ann[pname]):
                raise TypeError(
                    f"argument '{pname}' expected {ann[pname].__name__}, "
                    f"got {type(pval).__name__}"
                )

        res = func(*a, **kw)

        ret_type = ann.get("return")
        if ret_type and not isinstance(res, ret_type):
            raise TypeError(
                f"return value expected {ret_type.__name__}, "
                f"got {type(res).__name__}"
            )
        return res

    return inner  # type: ignore[return-value]


def curry(func: F) -> Callable:
    """Каррирование: превращает f(a, b, c) в f(a)(b)(c).

    Аргументы можно передавать и группами — f(a, b)(c).
    """
    params = inspect.signature(func).parameters
    required = 0
    for p in params.values():
        if p.default is p.empty and p.kind in (p.POSITIONAL_ONLY, p.POSITIONAL_OR_KEYWORD):
            required += 1

    @functools.wraps(func)
    def step(*got: Any) -> Any:
        if len(got) >= required:
            return func(*got)

        @functools.wraps(func)
        def next_step(*more: Any) -> Any:
            return step(*got, *more)
        return next_step

    return step


def memoize(func: F) -> F:
    """Запоминает результаты вызовов в словаре."""
    memo: dict = {}

    @functools.wraps(func)
    def inner(*a: Any, **kw: Any) -> Any:
        k = a + tuple(sorted(kw.items()))
        if k not in memo:
            memo[k] = func(*a, **kw)
        return memo[k]

    inner.cache = memo  # type: ignore[attr-defined]
    return inner  # type: ignore[return-value]
