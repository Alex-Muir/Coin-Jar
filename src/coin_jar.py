import sqlite3

import database_manager as dm

con = dm.get_connection()
dm.create_table(con)
dm.set_category_defaults(con)

# TEST
dm.test_table_exists(con)
dm.test_select(con)

