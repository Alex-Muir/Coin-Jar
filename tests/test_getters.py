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

def test_get_amount(g):
    """
    Expected input should be a an integer or float. The method does allow the user to 
    enter more than two numbers after the decimal point, but the result will be rounded 
    down to the nearest whole cent
    """ 
    # Accepts numeric and positive input
    with patch('builtins.input', side_effect=['abc', '!', '0', '-5', '100']):
        result1 = g._get_amount()
        print(result1)
    assert result1 == 100.0

    # Accepts decimal input
    with patch('builtins.input', side_effect=['100.05']):
        result2 = g._get_amount()
        print(result2)
    assert result2 == 100.05

    # Result rounds to the nearest whole cent
    with patch('builtins.input', side_effect=['100.48796578']):
        result3 = g._get_amount()
        print(result3)
    assert result3 == 100.48

