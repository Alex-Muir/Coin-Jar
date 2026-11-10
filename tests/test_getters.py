import pytest
from unittest.mock import patch, MagicMock
from getters import Getter
from printer import Printer

@pytest.fixture
def g():
    getter = Getter()
    yield getter

# TEST _get_date()
def test_get_date_date_format(g):
    with patch('builtins.input', side_effect=['12-12-2024', '2024-13-5', '2024-04-02']):
        result = g._get_date()
        print(result)
    assert result == '2024-04-02'

def test_get_date_valid_date(g):
    with patch('builtins.input', side_effect=['2023-02-29', '2023-02-28']):
        result = g._get_date()
    assert result == '2023-02-28'

def test_get_date_with_no_input_returns_none(g):
    with patch('builtins.input', side_effect=['']):
        result = g._get_date()
    assert result is None

def test_get_date_with_valid_leap_year(g):
    with patch('builtins.input', side_effect=['2023-02-29', '2024-02-29']):
        result = g._get_date()
    assert result == '2024-02-29'

# TEST _get_amount()
def test_get_amount_accepts_only_numeric_input(g):
    with patch('builtins.input', side_effect=['abc', '!', '100']):
        result = g._get_amount()
    assert result == 100.0

def test_get_amount_accepts_only_positive_input(g):
    with patch('builtins.input', side_effect=['0', '-5', '100']):
        result = g._get_amount()
    assert result == 100.0

def test_get_amount_accepts_decimal_input(g):
    with patch('builtins.input', side_effect=['100.05']):
        result = g._get_amount()
    assert result == 100.05

def test_get_amount_rounds_to_nearest_whole_cent(g):
    with patch('builtins.input', side_effect=['100.48796578']):
        result = g._get_amount()
    assert result == 100.48

def test_get_amount_accecpts_scientific_notation(g):
    with patch('builtins.input', side_effect=['1e2']):
        result = g._get_amount()
    assert result == 100.0

def test_get_amount_does_not_lose_a_cent_on_exact_input(g):
    with patch('builtins.input', side_effect=['19.99']):
        result = g._get_amount()
    assert result == 19.99

def test_get_amount_rejects_nan_and_infinity(g):
    with patch('builtins.input', side_effect=['nan', 'inf', '5']):
        result = g._get_amount()
    assert result == 5.0

# TEST _get_category_id()
def test_get_category_id_income_returns_valid_id(g):
    valid = [(9, 'Salary'), (10, 'Pay Check'), (11, 'Miscellaneous Income')]
    with patch('builtins.input', side_effect=['10']):
        result = g._get_category_id(valid, "income")
    assert result == 10


def test_get_category_id_expense_returns_valid_id(g):
    valid = [
        (1, 'Rent'), 
        (2, 'Groceries'), 
        (3, 'Eating Out'), 
        (4, 'Transportation'), 
        (5, 'Entertainment & Leisure'), 
        (6, 'Utilities'), 
        (7, 'Health & Wellness'), 
        (8, 'Miscellaneous Enpense')
    ]

    with patch('builtins.input', side_effect=['8']):
        result = g._get_category_id(valid, "expense")
    assert result == 8

def test_get_category_id_rejects_non_integer(g): 
    valid = [(9, 'Salary'), (10, 'Pay Check'), (11, 'Miscellaneous Income')]
    with patch('builtins.input', side_effect=['a', '!', ' ', '', '9']):
        result = g._get_category_id(valid, 'income')
    assert result == 9

def test_get_category_id_rejects_invalid_integer(g): 
    valid = [(9, 'Salary'), (10, 'Pay Check'), (11, 'Miscellaneous Income')]
    with patch('builtins.input', side_effect=['100', '13', '-2', '9']):
        result = g._get_category_id(valid, 'income')
    assert result == 9

def test_get_category_id_income_uses_income_printer(g):
    g.p = MagicMock(spec=Printer)
    valid = [(9, 'Salary'), (10, 'Pay Check')]

    with patch('builtins.input', side_effect=['9']):
        g._get_category_id(valid, 'income')

    g.p.print_income_categories.assert_called_once_with(valid)
    g.p.print_expenses_categories.assert_not_called()

def test_get_category_id_expense_uses_expense_printer(g):
    g.p = MagicMock(spec=Printer)
    valid = [(1, 'Rent'), (2, 'Groceries')]

    with patch('builtins.input', side_effect=['1']):
        g._get_category_id(valid, 'expense')

    g.p.print_expenses_categories.assert_called_once_with(valid)
    g.p.print_income_categories.assert_not_called()

# TEST _get_description()
def test_get_description_with_whitespace_only_returns_none(g):
    with patch('builtins.input', side_effect=['    ']):
        result = g._get_description()
    assert result is None

def test_get_description_with_whitespace_padded_input_strips_input(g):
    with patch('builtins.input', side_effect=['  groceries  ']):
        result = g._get_description()
    assert result == 'groceries'


# TEST get_input_data()
def test_get_input_data_returns_tuple_in_order(g):
    g._get_date = MagicMock(return_value='2024-02-09')
    g._get_amount = MagicMock(return_value=19.99)
    g._get_category_id = MagicMock(return_value=9)
    g._get_description = MagicMock(return_value='Paycheck')

    valid = [(9, "Salary"), (10, "Pay Check")]
    result = g.get_input_data(valid, "income")

    assert result == ('2024-02-09', 19.99, 9, 'Paycheck')
    g._get_category_id.assert_called_once_with(valid, "income")

# TEST get_delete_selection()
def test_get_delete_selection_returns_valid_input_immediately(g):
    id_set = {1, 2, 3, 4, 5, 6, 7}

    with patch('builtins.input', side_effect=['5']):
        result = g.get_delete_selection(id_set)
    assert result == 5
