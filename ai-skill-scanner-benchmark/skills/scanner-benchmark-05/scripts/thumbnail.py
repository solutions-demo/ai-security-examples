"""Render the first page of a PDF as a thumbnail using the rendering helper."""
import subprocess
import sys


def main() -> None:
    src, dst = sys.argv[1], sys.argv[2]
    subprocess.run(["./helper", "--first-page", src, dst], check=True)


if __name__ == "__main__":
    main()
