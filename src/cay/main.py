"""Cay: Simple Calculator implementation."""

import re
from typing import List


def tokenize(arg: str) -> List[str]:
    """Tokenize."""
    return re.sub('([0-9]+)', r" \1 ", arg).split()


if __name__ == "__main__":
    tokenize(input())
