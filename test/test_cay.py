import cay.main as main
from cay import __version__


class TestTokenize:
    def test_simple(self):
        assert main.tokenize("1 + 2") == ["1", "+", "2"]
        assert main.tokenize("1 + 2 * 3") == ["1", "+", "2", "*", "3"]

    def test_paren(self):
        assert main.tokenize("(1 + 2) * 3") == ["(", "1", "+", "2", ")", "*", "3"]

    def test_2digits(self):
        assert main.tokenize("1 + 2 + 42") == ["1", "+", "2", "+", "42"]


class TestParse:
    def test_simple(self):
        assert main.parse(main.tokenize("1+2")) == [
            main.Token(val=1, type=main.TokenType.integer),
            main.Token(val='+', type=main.TokenType.op),
            main.Token(val=2, type=main.TokenType.integer),
        ]

    def test_paren(self):
        assert main.parse(main.tokenize("(1+2)*3")) == [
            main.Token(val='(', type=main.TokenType.lparen),
            main.Token(val=1, type=main.TokenType.integer),
            main.Token(val='+', type=main.TokenType.op),
            main.Token(val=2, type=main.TokenType.integer),
            main.Token(val=')', type=main.TokenType.rparen),
            main.Token(val='*', type=main.TokenType.op),
            main.Token(val=3, type=main.TokenType.integer),
        ]


def test_main():
    assert 1 == 1
    assert __version__ == "0.1.0"
