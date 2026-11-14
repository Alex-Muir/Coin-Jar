import pytest
from printer import Printer

@pytest.fixture
def p():
    printer = Printer()
    yield printer

def test_print_greeting(p, capsys):
    p.print_menu()
    capture = capsys.readouterr()
    for label in ["1)", "2)", "3)", "4)", "5)", "6)", "7)", "0)"]:
        assert label in capture.out, f"menu is missing {label}"
