import argparse
import sys
from typing import TextIO


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="nl — нумерация строк")
    p.add_argument("file", nargs="?", help="путь к файлу (без аргумента читает stdin)")
    p.add_argument("-b", default="t", choices=["a", "t", "n"],
                   help="режим нумерации (a=все, t=непустые, n=нет)")
    p.add_argument("-s", default="\t", help="разделитель после номера")
    p.add_argument("-w", type=int, default=6, help="ширина колонки с номером")
    return p.parse_args()


def number_lines(src: TextIO, mode: str, sep: str, width: int) -> None:
    num = 0
    for raw in src:
        text = raw.rstrip("\n")

        need_num = (mode == "a") or (mode == "t" and text.strip())
        if need_num:
            num += 1
            print(f"{num:>{width}}{sep}{text}")
        else:
            print(" " * width + sep + text)


def main() -> None:
    args = parse_args()

    if args.file:
        try:
            with open(args.file, encoding="utf-8") as f:
                number_lines(f, args.b, args.s, args.w)
        except FileNotFoundError:
            print(f"nl: {args.file}: файл не найден", file=sys.stderr)
            sys.exit(1)
        except PermissionError:
            print(f"nl: {args.file}: отказано в доступе", file=sys.stderr)
            sys.exit(1)
    else:
        number_lines(sys.stdin, args.b, args.s, args.w)


if __name__ == "__main__":
    main()
