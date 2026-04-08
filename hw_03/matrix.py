from __future__ import annotations
from typing import Any

from hw_03.descriptors import Validated, Logged, Cached


class Matrix:
    """Матрица с арифметикой, хэшированием и контекстным менеджером."""

    rows = Validated(type=int, min=1)
    cols = Validated(type=int, min=1)
    data = Logged()
    determinant = Cached()

    def __init__(self, vals: list[list[float]]) -> None:
        self.rows = len(vals)
        self.cols = len(vals[0])
        self.data = [r[:] for r in vals]
        self._src = None  # для контекстного менеджера

    def _check_size(self, other: Matrix) -> None:
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("размеры не совпадают")

    def compute_determinant(self) -> float:
        d = self.data
        n = self.rows
        if n != self.cols:
            raise ValueError("определитель только для квадратных матриц")
        if n == 1:
            return d[0][0]
        if n == 2:
            return d[0][0] * d[1][1] - d[0][1] * d[1][0]
        # разложение по первой строке
        result = 0.0
        for col in range(n):
            sub = [[d[i][j] for j in range(n) if j != col] for i in range(1, n)]
            result += ((-1) ** col) * d[0][col] * Matrix(sub).determinant
        return result

    def __add__(self, other: Matrix) -> Matrix:
        self._check_size(other)
        return Matrix([
            [self.data[i][j] + other.data[i][j] for j in range(self.cols)]
            for i in range(self.rows)
        ])

    def __sub__(self, other: Matrix) -> Matrix:
        self._check_size(other)
        return Matrix([
            [self.data[i][j] - other.data[i][j] for j in range(self.cols)]
            for i in range(self.rows)
        ])

    def __mul__(self, k: float) -> Matrix:
        return Matrix([
            [self.data[i][j] * k for j in range(self.cols)]
            for i in range(self.rows)
        ])

    def __rmul__(self, k: float) -> Matrix:
        return self * k

    def __matmul__(self, other: Matrix) -> Matrix:
        if self.cols != other.rows:
            raise ValueError("несовместимые размеры для умножения")
        return Matrix([
            [sum(self.data[i][t] * other.data[t][j] for t in range(self.cols))
             for j in range(other.cols)]
            for i in range(self.rows)
        ])

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Matrix):
            return NotImplemented
        return self.data == other.data

    def __hash__(self) -> int:
        # кортеж кортежей — простой и надёжный способ
        return hash(tuple(tuple(r) for r in self.data))

    def __repr__(self) -> str:
        return f"Matrix({self.data!r})"

    def __str__(self) -> str:
        return "\n".join("\t".join(str(v) for v in row) for row in self.data)

    def __format__(self, spec: str) -> str:
        return "\n".join(
            "\t".join(format(v, spec) for v in row) for row in self.data
        )

    @classmethod
    def from_file(cls, path: str) -> Matrix:
        f = open(path, encoding="utf-8")
        rows = []
        for line in f:
            stripped = line.strip()
            if stripped:
                rows.append([float(x) for x in stripped.split()])
        m = cls(rows)
        m._src = f
        return m

    def __enter__(self) -> Matrix:
        return self

    def __exit__(self, *exc: Any) -> None:
        if self._src:
            self._src.close()
            self._src = None
