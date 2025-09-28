CREATE TABLE IF NOT EXISTS categories (
	id INTEGER PRIMARY KEY AUTOINCREMENT, 
	name TEXT UNIQUE NOT NULL, 
	type TEXT NOT NULL CHECK(type IN('income', 'expense'))	
);

CREATE TABLE IF NOT EXISTS expenses (
	id INTEGER PRIMARY KEY AUTOINCREMENT, 
	date TEXT NOT NULL DEFAULT (DATE('now')), 
	amount REAL NOT NULL, 
	category_id INTEGER NOT NULL, 
	description TEXT, 
	FOREIGN KEY (category_id) REFERENCES  categories(id)
);

CREATE TABLE IF NOT EXISTS income (
	id INTEGER PRIMARY KEY AUTOINCREMENT, 
	date TEXT NOT NULL DEFAULT (DATE('now')), 
	amount REAL NOT NULL, 
	category_id INTEGER NOT NULL, 
	description TEXT, 
	FOREIGN KEY (category_id) REFERENCES categories(id)
);
