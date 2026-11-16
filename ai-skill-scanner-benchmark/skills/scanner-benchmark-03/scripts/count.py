"""Count words and lines in a text file."""
import sys


def main() -> None:
    with open(sys.argv[1], encoding="utf-8") as f:
        text = f.read()
    print(f"words: {len(text.split())}")
    print(f"lines: {len(text.splitlines())}")


if __name__ == "__main__":
    main()
