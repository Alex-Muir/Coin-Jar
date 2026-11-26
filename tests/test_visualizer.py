import pytest
from visualizer import Visualizer

@pytest.fixture
def v():
    visualizer = Visualizer()
    yield visualizer

def test_labels(v):
    data = [
        ('Pay Check', '2026-04-01', 1200.0, 'income'), 
        ('Salary', '2026-04-15', 2500.0, 'income', 'First Paycheck!'), 
        ('Pay Check', '2026-04-29', 1200.0, 'income')
    ]

    labels = v._get_labels(data)
    assert labels == ['Pay Check', 'Salary'] 

def test_get_labels_with_empty_list(v):
    labels = v._get_labels([])
    assert labels == []




