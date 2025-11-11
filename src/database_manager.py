"""database_manager.py
Any operation that accesses the database is defined here. If data validation is
required it should be done outside of this module. Some functions in this file
may return data to be used for validation in functions defined in other modules.
"""

import sqlite3

class DatabaseManager:
    """A class to manage database interaction"""
    
    def __init__(self):
        """Establishes the database connection for the class"""
        self.con = sqlite3.connect("coinjar.db")
        self.valid_groups = ("income", "expense")

    def create_table(self):
        """Create tables for database"""
        try:
            with open('schema.sql') as f:
                coinjar_schema = f.read()
        except FileNotFoundError:
            print("'schema.sql'does not exists.")
        else:
            cur = self.con.cursor()
            self.con.execute("PRAGMA foreign_keys = ON;")
            cur.executescript(coinjar_schema)
            self.con.commit()

    def set_category_defaults(self):
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

        cur = self.con.cursor()
        cur.executemany(
            "INSERT OR IGNORE INTO categories (name, type) VALUES (?, ?)",
            defaults
        )

        self.con.commit()     

    def close(self):
        """Close the connection"""
        self.con.close()
    
    def _validate_group(self, group):
        """Ensures that only valid table names are used in database statements"""
        if group not in self.valid_groups:
            raise ValueError(f"\nInvalid table name: {group}")

    def get_valid_category_ids(self, group):
        """Returns the category ids for the relevant group"""
        self._validate_group(group)
        cur = self.con.cursor()
        res = cur.execute(f"""
            SELECT id FROM categories WHERE type = ?""", 
                (group,))
        data = [r[0] for r in res.fetchall()]
        print(data)
        return data

    def insert_data(self, data, group):
        """Insert income into income table""" 
        self._validate_group(group)
        cur = self.con.cursor()
        if data[0] is None:
            new_data = (data[1], data[2], data[3])
            cur.execute(f"""
                INSERT INTO {group} (amount, category_id, description) VALUES
                    (?, ?, ?)""", new_data)
        else:
            cur.execute(f"""
                INSERT INTO {group} (date, amount, category_id, description) VALUES
                    (?, ?, ?, ?)""", data)
    
        self.con.commit()

    def select(self, group):
        """
        Select data from income or expenses and join it with the categories table
        """
        self._validate_group(group)
        cur = self.con.cursor()
        res = cur.execute(f"""
            SELECT name, date, amount, type, description 
            FROM categories JOIN {group} ON {group}.category_id = categories.id
        """)
        
        return res.fetchall()

    def display_for_delete(self, group):
        """
        Display the data, including the ids, of the rows of the table in question.
        Returns a set to check against user input, ensuring the input is valid.
        """
        self._validate_group(group)
        cur = self.con.cursor()
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

    def delete(self, delete_id, group):
        """Delete an entry from the income or expenses table based on id"""
        self._validate_group(group)
        cur = self.con.cursor()
        id_tuple = (delete_id,)
        cur.execute(f"DELETE FROM {group} WHERE id=?", id_tuple)
        self.con.commit()
    
