import pytest
from printer import Printer

@pytest.fixture
def p():
    printer = Printer()
    yield printer

def test_print_greeting(p, capsys):
    p.print_greeting()
    capture = capsys.readouterr()
    assert "Welcome to Coin Jar!" in capture.out

def test_print_menu(p, capsys):
    p.print_menu()
    capture = capsys.readouterr()
    for label in ["1)", "2)", "3)", "4)", "5)", "6)", "7)", "0)"]:
        assert label in capture.out, f"menu is missing {label}"

def test_print_date_format_requirement(p, capsys):
    p.print_date_format_requirement()
    capture = capsys.readouterr()
    assert "Please enter dates as 'yyyy-mm-dd'" in capture.out

def test_print_income_categories(p, capsys):
    categories = [(9, 'Salary'), (10, 'Pay Check')]
    p.print_income_categories(categories)
    capture = capsys.readouterr()
    for item in categories:
        assert f"{item[1]} - {item[0]}" in capture.out

def test_print_expenses_categories(p, capsys):
    categories = [(1, 'Rent'), (2, 'Groceries')]
    p.print_expenses_categories(categories)
    capture = capsys.readouterr()
    for item in categories:
        assert f"{item[1]} - {item[0]}" in capture.out

def test_print_select(p, capsys):
    data = [('Pay Check', '2026-01-28', 200.0, 'income', 'Test income')]
    p.print_select(data)
    capture = capsys.readouterr()
    assert str(data) in capture.out
