from collections.abc import MutableSequence
from typing import Any, Callable, Iterable, Iterator, TypeVar, Union, overload

T = TypeVar("T")


class DefaultList(MutableSequence[T]):
    """Аналог defaultdict, но для списков.

    При обращении по несуществующему индексу не кидает IndexError,
    а возвращает значение из default_factory. Если фабрика не задана — None.
    """

    def __init__(
        self,
        iterable: Iterable[T] | None = None,
        default: Callable[[], T] | None = None,
    ) -> None:
        self._items: list[T] = list(iterable) if iterable else []
        self._default = default

    def __len__(self) -> int:
        return len(self._items)

    @overload
    def __getitem__(self, idx: int) -> T: ...
    @overload
    def __getitem__(self, idx: slice) -> "DefaultList[T]": ...

    def __getitem__(self, idx: int | slice) -> Union[T, "DefaultList[T]"]:
        if isinstance(idx, slice):
            chunk = self._items[idx]
            return DefaultList(chunk, self._default)
        try:
            return self._items[idx]
        except IndexError:
            if self._default is not None:
                return self._default()
            return None  # type: ignore[return-value]

    def _pad_to(self, idx: int) -> None:
        """Добивает список дефолтными значениями до позиции idx включительно."""
        if idx < 0 or idx < len(self._items):
            return
        fill_val: Any = self._default() if self._default else None
        self._items += [fill_val] * (idx - len(self._items) + 1)

    def __setitem__(self, idx: int, val: T) -> None:  # type: ignore[override]
        if isinstance(idx, int) and idx >= len(self._items):
            self._pad_to(idx)
        self._items[idx] = val

    def __delitem__(self, idx: int) -> None:  # type: ignore[override]
        del self._items[idx]

    def insert(self, idx: int, val: T) -> None:
        self._items.insert(idx, val)

    def __iter__(self) -> Iterator[T]:
        return iter(self._items)

    def __reversed__(self) -> Iterator[T]:
        return reversed(self._items)

    def __contains__(self, val: object) -> bool:
        return val in self._items

    def __repr__(self) -> str:
        name = self._default.__name__ if self._default else "None"
        return f"DefaultList({self._items!r}, default={name})"

    def __str__(self) -> str:
        return str(self._items)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, DefaultList):
            return self._items == other._items
        if isinstance(other, list):
            return self._items == other
        return NotImplemented

    def __add__(self, other: Iterable[T]) -> "DefaultList[T]":
        return DefaultList(self._items + list(other), self._default)
