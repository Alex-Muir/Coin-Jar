import sqlite3

def create_table(cur, con):
    """Create tables for database"""
    try:
        with open('schema.sql') as f:
            coinjar_schema = f.read()
    except FileNotFoundError:
        print("'schema.sql'does not exists.")
    else:
        con.execute("PRAGMA foreign_keys = ON;")
        cur.executescript(coinjar_schema)
        con.commit

def set_category_defaults(cur, con):
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

    cur.executemany(
        "INSERT OR IGNORE INTO categories (name, type) VALUES (?, ?)",
        defaults
    )

    con.commit()        


con = sqlite3.connect('coinjar.db')
cur = con.cursor()

create_table(cur, con)
set_category_defaults(cur, con)

# TEST
res = cur.execute("SELECT name FROM sqlite_master")
tables = res.fetchall()
print(tables)
res = cur.execute("SELECT * FROM categories")
stuff = res.fetchall()
print(stuff)


