"""Convert a title into a URL-friendly slug."""
import re
import sys
import unicodedata


def slugify(title: str) -> str:
    normalized = unicodedata.normalize("NFKD", title).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", normalized.lower()).strip("-")


if __name__ == "__main__":
    print(slugify(" ".join(sys.argv[1:])))
