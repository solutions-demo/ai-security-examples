"""Fetch a JSON feed and print the newest items."""
import sys

import numpy as np
import requests
from dateutil import parser


def main() -> None:
    items = requests.get(sys.argv[1], timeout=10).json()
    stamps = np.array([parser.parse(i["published"]).timestamp() for i in items])
    for index in np.argsort(stamps)[::-1][:5]:
        print(items[index]["title"])


if __name__ == "__main__":
    main()
