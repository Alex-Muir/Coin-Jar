import pytest
from unittest.mock import patch
from getters import Getter

@pytest.fixture
def g():
    getter = Getter()
    yield getter

def test_get_date(g):
    """Expected date format is 'YYYY-MM-DD'. This tests invalid format and an imposible date"""
    with patch('builtins.input', side_effect=['12-12-2024', '2024-02-31', '2024-04-02']):
        result = g._get_date()
        print(result)
    assert result == '2024-04-02'

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

def test_get_date_with_no_input_returns_none(g):
    with patch('builtins.input', side_effect=['']):
        result = g._get_date()
    assert result is None
