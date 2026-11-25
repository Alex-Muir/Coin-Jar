import pytest
from visualizer import Visualizer

@pytest.fixture
def v():
    visualizer = Visualizer()
    yield visualizer

def test_get_labels(v):
    labels = v._get_labels([])
    assert labels == []
