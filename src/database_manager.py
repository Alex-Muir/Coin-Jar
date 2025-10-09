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
