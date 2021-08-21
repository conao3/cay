"""Cay: Simple Calculator implementation."""

import enum
import re
from dataclasses import dataclass
from typing import List


class TokenType(enum.Enum):
    """Cay TokenType."""

    integer = enum.auto()
    float = enum.auto()
    op = enum.auto()
    function = enum.auto()
    rparen = enum.auto()
    lparen = enum.auto()
    comma = enum.auto()


@dataclass
class Token:
    """Cay Token."""

    val: str
    type: TokenType


def tokenize(arg: str) -> List[str]:
    """
    Tokenize.

    >>> tokenize("1+2+42")
    ['1', '+', '2', '+', '42']

    >>> tokenize("(1 + 2) * 3")
    ['(', '1', '+', '2', ')', '*', '3']
    """
    return (
        re.sub("([0-9]+)", r" \1 ", arg)
        .replace("(", " ( ")
        .replace(")", " ) ")
        .split()
    )


def parse(exps: List[str]) -> List[Token]:
    """
    Parse.

    >>> parse(tokenize("1+2"))
    [Token(val=1, type=<TokenType.integer: 1>),
     Token(val='+', type=<TokenType.op: 3>),
     Token(val=2, type=<TokenType.integer: 1>)]
    """
    res = []
    for exp in exps:
        try:
            exp = int(exp)
        except ValueError:
            try:
                exp = float(exp)
            except ValueError:
                exp = exp

        match exp:
            case "(":
                res.append(Token(val="(", type=TokenType.lparen))
            case ")":
                res.append(Token(val=")", type=TokenType.rparen))
            case ",":
                res.append(Token(val=",", type=TokenType.comma))
            case "+" | "-" | "*" | "/" | "mod" as elm:
                res.append(Token(elm, type=TokenType.op))
            case elm if isinstance(elm, int):
                res.append(Token(val=elm, type=TokenType.integer))
            case elm if isinstance(elm, float):
                res.append(Token(elm, type=TokenType.float))
            case elm:
                res.append(Token(elm, type=TokenType.function))

    return res


if __name__ == "__main__":
    while True:
        print("cay> ", end="")
        print(parse(tokenize(input())))
