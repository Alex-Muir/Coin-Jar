import pytest
from database_manager import DatabaseManager

@pytest.fixture
def db():
    db_manager = DatabaseManager(db_path=":memory:")
    db_manager.create_table()
    db_manager.set_category_defaults()
    yield db_manager
    db_manager.close()

def test_if_working():
    print("It's working!!!!")
