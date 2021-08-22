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
            main.Token(val="+", type=main.TokenType.op),
            main.Token(val=2, type=main.TokenType.integer),
        ]

    def test_paren(self):
        assert main.parse(main.tokenize("(1+2)*3")) == [
            main.Token(val="(", type=main.TokenType.lparen),
            main.Token(val=1, type=main.TokenType.integer),
            main.Token(val="+", type=main.TokenType.op),
            main.Token(val=2, type=main.TokenType.integer),
            main.Token(val=")", type=main.TokenType.rparen),
            main.Token(val="*", type=main.TokenType.op),
            main.Token(val=3, type=main.TokenType.integer),
        ]

    def test_function(self):
        assert main.parse(main.tokenize("fn(1, 2)+42")) == [
            main.Token(val="fn", type=main.TokenType.function),
            main.Token(val="(", type=main.TokenType.lparen),
            main.Token(val=1, type=main.TokenType.integer),
            main.Token(val=2, type=main.TokenType.integer),
            main.Token(val=")", type=main.TokenType.rparen),
            main.Token(val="+", type=main.TokenType.op),
            main.Token(val=42, type=main.TokenType.integer),
        ]


class TestConvert:
    def test_simple(self):
        assert main.convert(main.parse(main.tokenize("3+4"))) == [
            main.Token(val=3, type=main.TokenType.integer),
            main.Token(val=4, type=main.TokenType.integer),
            main.Token(val="+", type=main.TokenType.op),
        ]

    def test_complex(self):
        assert main.convert(main.parse(main.tokenize("3+4*2/(1-5)^2^3"))) == [
            main.Token(val=3, type=main.TokenType.integer),
            main.Token(val=4, type=main.TokenType.integer),
            main.Token(val=2, type=main.TokenType.integer),
            main.Token(val='*', type=main.TokenType.op),
            main.Token(val=1, type=main.TokenType.integer),
            main.Token(val=5, type=main.TokenType.integer),
            main.Token(val='-', type=main.TokenType.op),
            main.Token(val=2, type=main.TokenType.integer),
            main.Token(val=3, type=main.TokenType.integer),
            main.Token(val='^', type=main.TokenType.function),
            main.Token(val='^', type=main.TokenType.function),
            main.Token(val='/', type=main.TokenType.op),
            main.Token(val='+', type=main.TokenType.op)
        ]


def test_main():
    assert 1 == 1
    assert __version__ == "0.1.0"
