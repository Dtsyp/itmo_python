import csv
import json
from typing import Any, Callable

Row = dict[str, str]

COMPARATORS = {
    ">": float.__gt__,
    "<": float.__lt__,
    ">=": float.__ge__,
    "<=": float.__le__,
    "==": float.__eq__,
    "!=": float.__ne__,
}


def pipe(*fns: Callable) -> Callable:
    """Применяет функции последовательно слева направо."""
    def _pipe(x: Any) -> Any:
        for f in fns:
            x = f(x)
        return x
    return _pipe


def compose(*fns: Callable) -> Callable:
    """Композиция функций справа налево (математическая запись)."""
    return pipe(*reversed(fns))


def read_csv(path: str) -> list[Row]:
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _split_expr(expr: str) -> tuple[Callable, float]:
    # сначала двусимвольные, потом односимвольные
    for op in (">=", "<=", "!=", "==", ">", "<"):
        if expr.startswith(op):
            return COMPARATORS[op], float(expr[len(op):])
    raise ValueError(f"не могу разобрать условие: {expr}")


def filter_by(**conds: str) -> Callable[[list[Row]], list[Row]]:
    """Фильтрует строки по условиям: filter_by(age=">18")."""
    checks = {col: _split_expr(expr) for col, expr in conds.items()}

    def _do(rows: list[Row]) -> list[Row]:
        result = []
        for row in rows:
            if all(op(float(row[col]), val) for col, (op, val) in checks.items()):
                result.append(row)
        return result
    return _do


def sort_by(field: str, reverse: bool = False) -> Callable[[list[Row]], list[Row]]:
    """Сортирует по заданному полю."""
    return lambda rows: sorted(rows, key=lambda r: r[field], reverse=reverse)


def take(n: int) -> Callable[[list], list]:
    """Оставляет первые n элементов."""
    return lambda rows: rows[:n]


def to_json(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2)
