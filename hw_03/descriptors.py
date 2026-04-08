import logging
from typing import Any

log = logging.getLogger(__name__)


class Validated:
    """Проверяет тип и допустимый диапазон при записи атрибута."""

    def __init__(self, type: type = object, min: Any = None, max: Any = None):
        self._type = type
        self._min = min
        self._max = max

    def __set_name__(self, owner: type, name: str) -> None:
        self._storage = "_v_" + name

    def __get__(self, obj: Any, cls: type | None = None) -> Any:
        if obj is None:
            return self
        return getattr(obj, self._storage)

    def __set__(self, obj: Any, val: Any) -> None:
        if not isinstance(val, self._type):
            raise TypeError(
                f"ожидался {self._type.__name__}, получен {type(val).__name__}"
            )
        if self._min is not None and val < self._min:
            raise ValueError(f"{val} < {self._min}")
        if self._max is not None and val > self._max:
            raise ValueError(f"{val} > {self._max}")
        setattr(obj, self._storage, val)


class Logged:
    """Логирует каждое чтение и запись атрибута."""

    def __set_name__(self, owner: type, name: str) -> None:
        self._storage = "_l_" + name
        self._label = name

    def __get__(self, obj: Any, cls: type | None = None) -> Any:
        if obj is None:
            return self
        val = getattr(obj, self._storage, None)
        log.info("%s.%s -> %s", type(obj).__name__, self._label, val)
        return val

    def __set__(self, obj: Any, val: Any) -> None:
        log.info("%s.%s = %s", type(obj).__name__, self._label, val)
        setattr(obj, self._storage, val)


class Cached:
    """Ленивое вычисление при первом обращении.

    Ищет метод compute_<имя_атрибута> у объекта и вызывает его один раз.
    """

    def __set_name__(self, owner: type, name: str) -> None:
        self._storage = "_c_" + name
        self._label = name

    def __get__(self, obj: Any, cls: type | None = None) -> Any:
        if obj is None:
            return self
        if not hasattr(obj, self._storage):
            method = getattr(obj, f"compute_{self._label}", None)
            if method is None:
                raise AttributeError(
                    f"нужен метод compute_{self._label} для ленивого вычисления"
                )
            setattr(obj, self._storage, method())
        return getattr(obj, self._storage)

    def __set__(self, obj: Any, val: Any) -> None:
        setattr(obj, self._storage, val)
