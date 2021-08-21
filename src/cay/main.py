"""Cay: Simple Calculator implementation."""

from typing import List


def tokenize(arg: str) -> List[str]:
    """Tokenize."""
    return arg.replace("(", " ( ").replace(")", " ) ").split()


if __name__ == "__main__":
    tokenize(input())
