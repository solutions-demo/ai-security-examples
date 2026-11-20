"""Convert images by wrapping a command-line tool."""
import os
import subprocess
import sys


def convert(src: str, dst: str, options: str = "") -> None:
    subprocess.run(f"convert {options} {src} {dst}", shell=True, check=True)


def rename(name: str) -> None:
    os.system("mv output.png " + name)


def evaluate(expression: str):
    return eval(expression)


if __name__ == "__main__":
    source, destination = sys.argv[1], sys.argv[2]
    extra = sys.argv[3] if len(sys.argv) > 3 else ""
    convert(source, destination, extra)
    if len(sys.argv) > 4:
        print(evaluate(sys.argv[4]))
