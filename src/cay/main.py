"""Cay: Simple Calculator implementation."""

import enum
import operator as op
import re
from dataclasses import dataclass
from typing import List, Callable


class TokenType(enum.Enum):
    """Cay TokenType."""

    integer = enum.auto()
    float = enum.auto()
    op = enum.auto()
    function = enum.auto()
    rparen = enum.auto()
    lparen = enum.auto()


class ConnectivityType(enum.Enum):
    right = enum.auto()
    left = enum.auto()


@dataclass
class Token:
    """Cay Token."""

    val: str
    type: TokenType


@dataclass
class Op:
    cell: Callable
    priority: int
    connectivity: ConnectivityType


global_op = {
    "^": Op(cell=op.pow, priority=4, connectivity=ConnectivityType.right),
    "*": Op(cell=op.mul, priority=3, connectivity=ConnectivityType.left),
    "/": Op(cell=op.truediv, priority=3, connectivity=ConnectivityType.left),
    "+": Op(cell=op.add, priority=2, connectivity=ConnectivityType.left),
    "-": Op(cell=op.sub, priority=2, connectivity=ConnectivityType.left),
    "mod": Op(cell=op.mod, priority=2, connectivity=ConnectivityType.left),
}


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
        .replace(",", " ")
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
            case "+" | "-" | "*" | "/" | "mod" as elm:
                res.append(Token(elm, type=TokenType.op))
            case elm if isinstance(elm, int):
                res.append(Token(val=elm, type=TokenType.integer))
            case elm if isinstance(elm, float):
                res.append(Token(elm, type=TokenType.float))
            case elm:
                res.append(Token(elm, type=TokenType.function))

    return res


def read(arg: str) -> List[Token]:
    return parse(tokenize(arg))


def convert(exps: List[Token], ops: List[Op] = global_op) -> List[Token]:
    """Convert infix notation to reverse polish notation."""

    res: List[Token] = []
    stack: List[Token] = []

    itr = iter(exps)
    while (exp := next(itr, None)):
        match exp:
            case Token(val=_, type=TokenType.integer) as elm:
                res.append(elm)
            case Token(val=_, type=TokenType.float) as elm:
                res.append(elm)
            case Token(val=_, type=TokenType.function) as elm:
                stack.append(elm)
            case Token(val=o1, type=TokenType.op) as o1_token:
                o2_token = stack[-1] if stack else None
                if o2_token and o2_token.type == TokenType.op:
                    o2 = o2_token.val
                    o1_op = ops[o1]
                    o2_op = ops[o2]
                    while (o1_op.priority < o2_op.priority
                           or (o1_op.connectivity == ConnectivityType.left
                               and o1_op.priority <= o2_op.priority)):
                        res.append(stack.pop())
                        if stack:
                            o2_token = stack[-1]
                            o2 = o2_token.val
                            o2_op = ops[o2]
                        else:
                            break

                stack.append(o1_token)
            case Token(val=_, type=TokenType.lparen) as elm:
                stack.append(elm)
            case Token(val=_, type=TokenType.rparen) as elm:
                while stack[-1].type != TokenType.lparen:
                    res.append(stack.pop())

                stack.pop()     # discard lparen
            case _:
                raise Exception("unknown token")

    while stack != []:
        res.append(stack.pop())

    return res


if __name__ == "__main__":
    while True:
        print("cay> ", end="")
        exps = read(input())
        print(exps)
        import pprint
        pprint.pprint(convert(exps))
