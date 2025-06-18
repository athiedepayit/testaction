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


def colorprint(color, text):
    mycolor = COLORS.get("green")
    if COLORS.get(color) is not None:
        mycolor = COLORS.get(color)
    return f"{mycolor}{text}{COLORS.get('reset')}"


def main():
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    logging.log(DEBUG, colorprint("green", "green text!"))
    logging.log(DEBUG, colorprint("yellow", "yellow text!"))
    logging.log(DEBUG, colorprint("red", "red text!"))


if __name__ == "__main__":
    main()
