import pytest
from datetime import date
from database_manager import DatabaseManager

# FIXTURES
@pytest.fixture
def db():
    db_manager = DatabaseManager(db_path=':memory:')
    db_manager.create_table()
    db_manager.set_category_defaults()
    yield db_manager
    db_manager.close()

# TESTS
def test_get_total_savings_returns_zero_when_tables_empty(db):
    assert db.get_total_savings() == 0

def test_get_total_savings_correctly_computes_total(db):
    cur = db.con.cursor()
    cur.execute("INSERT INTO income (amount, category_id) VALUES (100, 11)")
    cur.execute("INSERT INTO expense (amount, category_id) VALUES (80, 3)")
    assert db.get_total_savings() == 20

def test_default_date_insert(db):
    db.insert_data((None, 50, 9, 'Test'), 'income')
    cur = db.con.cursor()
    data = cur.execute("""
        SELECT date, amount, category_id, description 
        FROM income""").fetchone()
    print(f"Data: {data}")
    assert data == (date.today().isoformat(), 50.0, 9, 'Test')

def test_explicit_date_insert(db):
    db.insert_data(('2026-04-01', 50, 9, 'Test'), 'income')
    cur = db.con.cursor()
    data = cur.execute("""
        SELECT date, amount, category_id, description 
        FROM income""").fetchone()
    print(f"Data: {data}")
    assert data == ("2026-04-01", 50.0, 9, "Test")

def test_select_with_default_date(db):
    """
    The select method joins the relevant group table with the
    categories table, which is why data in res may look unexpected 
    given the seeded data inserted into the group table
    """  
    cur = db.con.cursor()
    cur.execute("""
        INSERT INTO income (amount, category_id, description) 
        VALUES (100, 9, 'Test')
    """)
    cur.execute("INSERT INTO income (amount, category_id) VALUES (25, 11)")
    res = db.select('income')
    print(res)
    assert res == [
        ('Salary', date.today().isoformat(), 100.0, 'income', 'Test'),
        ('Miscellaneous Income', date.today().isoformat(), 25.0, 'income', None)
    ]

def test_select_with_explicit_date(db):
    """
    The select method joins the relevant group table with the
    categories table, which is why data in res may look unexpected 
    given the seeded data inserted into the group table
    """  
    cur = db.con.cursor()
    cur.execute("""
        INSERT INTO expense (date, amount, category_id) 
        VALUES ('2026-04-01', 100, 2)
    """)
    cur.execute("""
        INSERT INTO expense (date, amount, category_id, description) 
        VALUES ('2026-04-01', 25, 3, 'Test')
    """)
    res = db.select("expense")
    print(res)
    assert res == [
        ('Groceries', '2026-04-01', 100.0, 'expense', None),
        ('Eating Out', '2026-04-01', 25, 'expense', 'Test')
    ]

def test_delete_removes_correct_row(db):
    cur = db.con.cursor()
    cur.execute("INSERT INTO expense (amount, category_id) VALUES (100, 2)")
    cur.execute("INSERT INTO expense (amount, category_id) VALUES (25, 3)")
    cur.execute("INSERT INTO expense (amount, category_id) VALUES (350, 4)")
    db.delete(2, 'expense')
    ids = [row[0] for row in cur.execute("SELECT id FROM expense").fetchall()]
    print(f"set: {ids}")
    assert (2 not in ids)

def test_validate_group_raises_ValueError_on_invalid_group(db):
    with pytest.raises(ValueError):
        db._validate_group("invalid_group")

