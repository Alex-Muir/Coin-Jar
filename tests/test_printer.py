import pytest
from printer import Printer

@pytest.fixture
def p():
    printer = Printer()
    yield p
