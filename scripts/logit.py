#!/usr/bin/env python3

import logging
from logging import DEBUG
import sys

COLORS = {
    "red": "\x1b[31m",
    "green": "\x1b[32m",
    "yellow": "\x1b[33m",
    "reset": "\x1b[0m",
}


def main():
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    logging.log(DEBUG, f"{COLORS.get('green')}Updating Origin One{COLORS.get('reset')}")
    logging.log(
        DEBUG,
        f"Without colors: {COLORS.get('red')}Red Logging asdf{COLORS.get('reset')}",
    )
    logging.log(
        DEBUG,
        f"Without colors: {COLORS.get('yellow')}Yellow Logging{COLORS.get('reset')}",
    )


if __name__ == "__main__":
    main()
