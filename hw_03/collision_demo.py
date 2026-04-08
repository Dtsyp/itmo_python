from hw_03.matrix import Matrix


class BadHashMatrix(Matrix):
    """Матрица, у которой хэш всегда одинаковый — для демонстрации коллизий."""
    def __hash__(self) -> int:
        return 7


def main() -> None:
    # матрицы как ключи set и dict
    a = Matrix([[1, 0], [0, 1]])
    b = Matrix([[2, 3], [4, 5]])
    c = Matrix([[1, 0], [0, 1]])  # такая же как a

    print(f"a == c: {a == c}, hash совпал: {hash(a) == hash(c)}")
    print(f"set(a, b, c) -> len = {len({a, b, c})}")  # 2, т.к. a == c

    scores = {a: "identity", b: "random"}
    print(f"scores[a] = {scores[a]}")
    print(f"scores[c] = {scores[c]}")  # c == a, поэтому тот же ключ
    print()

    # искусственная коллизия
    m1 = BadHashMatrix([[1, 2], [3, 4]])
    m2 = BadHashMatrix([[9, 9], [9, 9]])

    print(f"hash(m1) = {hash(m1)}, hash(m2) = {hash(m2)}")
    print(f"m1 == m2: {m1 == m2}")

    both = {m1, m2}
    print(f"обе в set: len = {len(both)}")
    assert len(both) == 2, "коллизия не должна приводить к потере элементов"

    mapping = {m1: "first", m2: "second"}
    print(f"mapping[m1] = {mapping[m1]}, mapping[m2] = {mapping[m2]}")
    print("коллизия разрешена корректно")


# Почему a == b обязывает hash(a) == hash(b):
#
# dict и set ищут элемент в два шага: сначала по хэшу находят
# нужную корзину, и только потом сравнивают через __eq__.
# Если равные объекты попадут в разные корзины (из-за разных хэшей),
# то __eq__ вообще не вызовется и они будут считаться разными.
# Результат — дубли в set и «потерянные» ключи в dict.
#
# Обратное неверно: одинаковый хэш у неравных объектов — это просто
# коллизия. Python честно проверит __eq__ и сохранит оба объекта
# в одной корзине. Единственный минус — поиск в корзине за O(n),
# но на корректность это не влияет.


if __name__ == "__main__":
    main()
