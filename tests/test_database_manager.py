import sqlite3
from datetime import date
import pytest
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
def test_tables_are_created(db):
    cur = db.con.cursor()
    res = cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = {row[0] for row in res.fetchall()}
    assert {"categories", "income", "expense"} <= tables

def test_calling_create_table_twice_doesnt_wipe_existing_rows(db):
    cur = db.con.cursor()
    cur.execute("INSERT INTO income (amount, category_id) VALUES (100, 11)")
    db.create_table()
    res = cur.execute("SELECT date, amount, category_id FROM income").fetchall()
    assert res == [(date.today().isoformat(), 100.0, 11),]

def test_raises_integrity_error_on_bad_category_id(db):
    with pytest.raises(sqlite3.IntegrityError):
        db.insert_data((None, 50, 999, 'Test'), 'income')

def test_raises_integrity_error_on_bad_category_type(db):
    cur = db.con.cursor()
    with pytest.raises(sqlite3.IntegrityError):
       cur.execute("INSERT INTO categories (name, type) VALUES ('Vacation', 'savings')")

def test_rasises_integrity_error_on_categories_with_same_name(db):
    cur = db.con.cursor()
    with pytest.raises(sqlite3.IntegrityError):
        cur.execute("INSERT INTO categories (name, type) VALUES ('Rent', 'expense')")

def test_category_count_after_set_category_defaults_call(db):
    cur = db.con.cursor()
    category_count = cur.execute("SELECT COUNT(*) FROM categories").fetchone()[0]
    # Adjust if additional categories are added
    assert category_count == 11

def test_category_count_is_the_same_after_second_set_category_defaults_call(db):
    db.set_category_defaults()
    cur = db.con.cursor()
    category_count = cur.execute("SELECT COUNT(*) FROM categories").fetchone()[0]
    assert category_count == 11

def test_close_actually_closes_database_connection(db):
    cur = db.con.cursor()
    db.close()
    with pytest.raises(sqlite3.ProgrammingError):
        cur.execute("SELECT 1")

def test_insert_data_raises_value_error_on_bad_group(db):
    with pytest.raises(ValueError):
        db.insert_data((None, 3, 90, "Test"), group="bogus")

def test_description_is_none(db):
    db.insert_data((None, 50, 9, None), "income")
    res = db.con.execute("SELECT description FROM income").fetchone()
    assert res[0] is None

def test_insert_data_increments_id(db):
    cur = db.con.cursor()
    db.insert_data((None, 50, 9, 'First'), 'income')
    res = cur.execute("SELECT id FROM income WHERE description='First'")
    first_id = res.fetchone()[0]
    
    db.insert_data((None, 75, 9, 'Second'), 'income')
    res = cur.execute("SELECT id FROM income WHERE description='Second' ")
    second_id = res.fetchone()[0]

    assert second_id != first_id
    assert second_id > first_id

def test_select_invalid_group_raises_value_error(db):
    with pytest.raises(ValueError):
        db.select("bogus")

def test_select_empty_group_table_returns_empty_list(db):
    assert db.select("income") == []

def test_display_for_deletes_returned_set(db):
    cur = db.con.cursor()
    cur.execute("""
        INSERT INTO income (amount, category_id, description)
        VALUES (55, 9, 'Test'), (100, 10, 'Test2'), (20, 9, 'Test3')
    """)
    assert db.display_for_delete('income') == {1, 2, 3}

def test_display_for_delete_returns_a_set(db):
    assert isinstance(db.display_for_delete('income'), set) == True

def test_display_for_delete_raises_value_error_on_invlaid_group(db):
    with pytest.raises(ValueError):
        db.display_for_delete("bogus") 

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
    assert data == ('2026-04-01', 50.0, 9, 'Test')

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

def test_delete_removes_correct_row_from_expense(db):
    cur = db.con.cursor()
    cur.execute("INSERT INTO expense (amount, category_id) VALUES (100, 2)")
    cur.execute("INSERT INTO expense (amount, category_id) VALUES (25, 3)")
    cur.execute("INSERT INTO expense (amount, category_id) VALUES (350, 4)")
    db.delete(2, 'expense')
    ids = [row[0] for row in cur.execute("SELECT id FROM expense").fetchall()]
    print(f"set: {ids}")
    assert (2 not in ids)

def test_delete_removes_correct_row_from_income(db):
    cur = db.con.cursor()
    data = [(100, 9), (200, 10), (300, 11)]
    cur.executemany("INSERT INTO income (amount, category_id) VALUES(?, ?)", data)
    db.delete(2, 'income')
    ids = [row[0] for row in cur.execute("SELECT id FROM income").fetchall()]
    assert 2 not in ids

def test_delete_invalid_id_leaves_row_count_unchanged(db):
    cur = db.con.cursor()                                                       
    data = [(100, 9), (200, 10), (300, 11)]                                     
    cur.executemany("INSERT INTO income (amount, category_id) VALUES(?, ?)", data)
    db.delete(5, 'income')                                                      
    data = cur.execute("SELECT id FROM income").fetchall()
    assert len(data) == 3

def test_delete_raises_value_error_on_invalid_group(db):
    cur = db.con.cursor()
    cur.execute("INSERT INTO income (amount, category_id) VALUES(100, 9)")
    with pytest.raises(ValueError):
        db.delete(1, 'bogus')

def test_get_total_savings_returns_negative_number_when_expenses_exceed_income(db):
    cur = db.con.cursor()
    cur.execute("INSERT INTO income (amount, category_id) VALUES (50, 11)")
    cur.execute("INSERT INTO expense (amount, category_id) VALUES (80, 3)")
    assert db.get_total_savings() == -30

def test_line_graph_data_all_positive_total_values(db):
    cur = db.con.cursor()
    date_and_amount_income = [
        ('2024-02-09', 50, 9), 
        ('2024-02-10', 100, 9), 
        ('2024-02-15', 25, 9), 
        ('2024-02-20', 25, 9)
    ]
    date_and_amount_expense = [
        ('2024-02-09', 20, 1),
        ('2024-02-11', 60, 1),
        ('2024-02-15', 40, 1),
        ('2024-02-18', 30, 1)
    ]

    cur.executemany("""
        INSERT INTO income (date, amount, category_id) 
        VALUES(?, ?, ?)""", date_and_amount_income
    )
    cur.executemany(
        """INSERT INTO expense (date, amount, category_id) 
        VALUES(?, ?, ?)""", date_and_amount_expense
    )

    data = db.get_line_data()

    assert data['line_graph_data'] == {
        '2024-02-09': 30, 
        '2024-02-10': 130, 
        '2024-02-11': 70, 
        '2024-02-15': 55, 
        '2024-02-18': 25, 
        '2024-02-20': 50,
    }, "Line graph data is not correct"

    assert data['low'] == 25, "The low value is incorrect"
    assert data['high'] == 130, "The high value is incorrect"

def test_line_graph_data_all_negative_total_values(db):
    cur = db.con.cursor()
    date_and_amount_income = [
        ('2024-02-09', 50, 9),
        ('2024-02-10', 10, 9),
        ('2024-02-15', 25, 9),
        ('2024-02-20', 25, 9)
    ]
    date_and_amount_expense = [
        ('2024-02-09', 70, 1),
        ('2024-02-11', 60, 1),
        ('2024-02-15', 40, 1),
        ('2024-02-18', 30, 1)
    ]

    cur.executemany("""
        INSERT INTO income (date, amount, category_id)
        VALUES(?, ?, ?)""", date_and_amount_income
    )
    cur.executemany(
        """INSERT INTO expense (date, amount, category_id)
        VALUES(?, ?, ?)""", date_and_amount_expense
    )
    
    data = db.get_line_data()

    assert data['line_graph_data'] == {
        '2024-02-09': -20,
        '2024-02-10': -10,
        '2024-02-11': -70,
        '2024-02-15': -85,
        '2024-02-18': -115,
        '2024-02-20': -90,
    }, "Line graph data is not correct"

    assert data['low'] == -115, "The low value is incorrect"
    assert data['high'] == -10, "The high value is incorrect"

def test_get_line_data_empty_tables(db):
    data = db.get_line_data()
    assert data['line_graph_data'] == {}
    assert data['high'] is None
    assert data['low'] is None

def test_get_line_data_singl_day_income_and_expense(db):
    cur = db.con.cursor()
    cur.execute("""
        INSERT INTO income (date, amount, category_id) 
        VALUES ('2024-02-09', 50, 9)
    """)

    cur.execute("""
        INSERT INTO expense (date, amount, category_id)
        VALUES ('2024-02-09', 20, 1)
    """)

    data = db.get_line_data()
    assert data['line_graph_data'] == {'2024-02-09': 30}
    assert data['high'] == 30
    assert data['low'] == 30

def test_get_line_datapositive_then_negative(db):
    cur = db.con.cursor()
    cur.execute("""
        INSERT INTO income (date, amount, category_id)
        VALUES ('2024-02-09', 50, 9)
    """)
    cur.execute("""
        INSERT INTO expense (date, amount, category_id)
        VALUES ('2024-02-11', 100, 1)
    """)

    data = db.get_line_data()
    assert data['line_graph_data'] == {'2024-02-09': 50, '2024-02-11': -50}
    assert data['high'] == 50
    assert data['low'] == -50

def test_get_line_data_zero_then_negative(db):
    cur = db.con.cursor()
    cur.execute("""
        INSERT INTO income (date, amount, category_id)
        VALUES ('2024-02-09', 50, 9)
    """)
    expense_input = [
        ('2024-02-09', 50, 1),
        ('2024-02-11', 50, 1)
    ]
    cur.executemany("""
        INSERT INTO expense (date, amount, category_id)
        VALUES (?, ?, ?)
    """, expense_input)

    data = db.get_line_data()

    assert data['line_graph_data'] == {'2024-02-09': 0, '2024-02-11': -50}
    assert data['high'] == 0
    assert data['low'] == -50

def test_get_line_data_only_income(db):
    cur = db.con.cursor()
    income_data = [
        ('2024-02-09', 50, 9),
        ('2024-02-11', 100, 10),
        ('2024-02-13', 20, 9)
    ]

    cur.executemany("""
        INSERT INTO income (date, amount, category_id)
        VALUES (?, ?, ?)
    """, income_data)

    data = db.get_line_data()

    assert data['line_graph_data'] == {
        '2024-02-09': 50, 
        '2024-02-11': 150, 
        '2024-02-13': 170
    }
    assert data['high'] == 170
    assert data['low'] == 50

def test_get_line_data_only_expense(db):
    cur = db.con.cursor()
    expense_data = [
        ('2024-02-09', 50, 9),
        ('2024-02-11', 100, 10),
        ('2024-02-13', 20, 9)
    ]

    cur.executemany("""
        INSERT INTO expense (date, amount, category_id)
        VALUES (?, ?, ?)
    """, expense_data)

    data = db.get_line_data()

    assert data['line_graph_data'] == {
        '2024-02-09': -50, 
        '2024-02-11': -150, 
        '2024-02-13': -170
    }
    assert data['high'] == -50
    assert data['low'] == -170

def test_validate_group_raises_ValueError_on_invalid_group(db):
    with pytest.raises(ValueError):
        db._validate_group("invalid_group")

def test_validate_groups_succeeds_with_valid_group(db):
    for group in db.valid_groups:
        db._validate_group(group)

def test_get_valid_category_ids_names(db):
    cur = db.con.cursor()
    res = cur.execute("SELECT id, name FROM categories WHERE type = 'income'")
    income_ids_and_names = res.fetchall()
    res = cur.execute("SELECT id, name FROM categories WHERE type = 'expense'")
    expense_ids_and_names = res.fetchall()
    # Only income ids and names
    assert db.get_valid_category_ids_names('income') == income_ids_and_names
    # Only expense ids and names
    assert db.get_valid_category_ids_names('expense') == expense_ids_and_names
