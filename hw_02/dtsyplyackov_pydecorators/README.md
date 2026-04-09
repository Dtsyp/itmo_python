# dtsyplyackov-pydecorators

Декораторы для Python: проверка типов, каррирование, мемоизация.

## Установка

```bash
pip install --index-url https://test.pypi.org/simple/ dtsyplyackov-pydecorators
```

## Примеры

```python
from dtsyplyackov_pydecorators import validate_types, curry, memoize

@validate_types
def add(a: int, b: int) -> int:
    return a + b

add(1, 2)    # 3
add("1", 2)  # TypeError

@curry
def mul(a, b, c):
    return a * b * c

mul(2)(3)(4)   # 24

@memoize
def fib(n: int) -> int:
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)

fib(100)  # быстро за счёт кеша
```

Декораторы можно стекировать:

```python
@curry
@validate_types
def safe_add(a: int, b: int) -> int:
    return a + b

safe_add(1)(2)    # 3
safe_add("x")(2)  # TypeError
```
