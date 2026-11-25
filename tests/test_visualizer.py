import pytest
from visualizer import Visualizer

@pytest.fixture
def v():
    visualizer = Visualizer()
    yield visualizer
