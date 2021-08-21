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


def test_main():
    assert 1 == 1
    assert __version__ == "0.1.0"
