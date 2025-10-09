import sqlite3

def get_connection():
    """Create a connection to the database"""
    return sqlite3.connect("coinjar.db")

def create_table(con):
    """Create tables for database"""
    try:
        with open('schema.sql') as f:
            coinjar_schema = f.read()
    except FileNotFoundError:
        print("'schema.sql'does not exists.")
    else:
        cur = con.cursor()
        con.execute("PRAGMA foreign_keys = ON;")
        cur.executescript(coinjar_schema)
        con.commit

def set_category_defaults(con):
    """Sets the default categories for tracking expenses and income"""
    defaults = [
        ("Rent", "expense"), 
        ("Groceries", "expense"),
        ("Eating Out", "expense"), 
        ("Transportation", "expense"), 
        ("Entertainment & Leisure", "expense"), 
        ("Utilities", "expense"), 
        ("Health & Wellness", "expense"), 
        ("Miscellaneous Expense", "expense"), 
        ("Salary", "income"), 
        ("Pay Check", "income"), 
        ("Miscellaneous Income", "income")
    ]

    cur = con.cursor()
    cur.executemany(
        "INSERT OR IGNORE INTO categories (name, type) VALUES (?, ?)",
        defaults
    )

    con.commit()     

def insert_income(con):
    """Insert income into income table""" 
    cur = con.cursor()
    cur.execute("""
        INSERT INTO income (amount, category_id, description) VALUES
            (1032.64, 10, 'Camellia Coffee Roasters')
    """)
    
    con.commit()

# TEST
def select_income(con):
    cur = con.cursor()
    res = cur.execute("""
        SELECT name, type, date, amount, description 
        FROM categories JOIN income ON income.category_id = categories.id
    """)
    print(res.fetchall()) 
    
 
# TEST
def test_table_exists(con):
    cur = con.cursor()
    res = cur.execute("SELECT name FROM sqlite_master")
    tables = res.fetchall()
    print(tables)

# TEST
def test_select(con):
    cur = con.cursor()
    res = cur.execute("SELECT * FROM categories")
    tables = res.fetchall()
    print(tables)
