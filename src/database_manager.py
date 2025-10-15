"""database_manager.py
Any operation that accesses the database is defined here. If data validation is
required it should be done outside of this module. Some functions in this file
may return data to be used for validation in functions defined in other modules.
"""

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

def insert_data(con, data, group):
    """Insert income into income table""" 
    cur = con.cursor()
    if data[0] is None:
        new_data = (data[1], data[2], data[3])
        cur.execute(f"""
            INSERT INTO {group} (amount, category_id, description) VALUES
                (?, ?, ?)""", new_data)
    else:
        cur.execute(f"""
            INSERT INTO {group} (date, amount, category_id, description) VALUES
                (?, ?, ?, ?)""", data)
    
    con.commit()

def select(con, group):
    """
    Select data from income or expenses and join it with the categories table
    """
    cur = con.cursor()
    res = cur.execute(f"""
        SELECT name, date, amount, type, description 
        FROM categories JOIN {group} ON {group}.category_id = categories.id
    """)
    data = res.fetchall()
    print(data) 

def display_for_delete(con, group):
    """
    Display the data, including the ids, of the rows of the table in question.
    Returns a set to check against user input, ensuring the input is valid.
    """
    cur = con.cursor()
    res = cur.execute(f"""
        SELECT {group}.id, name, date, amount, type, description
        FROM categories JOIN {group} ON {group}.category_id = categories.id
    """)
    id_set = set()
    for row in res.fetchall():
        id = row[0]
        id_set.add(id)
        print(row)
    return id_set

def delete(con, delete_id, group):
    """Delete an entry from the income or expenses table based on id"""
    cur = con.cursor()
    cur.execute(f"DELETE FROM {group} WHERE id=?", str(delete_id))
    con.commit()
    
