import sqlite3
import sys

import database_manager as dm
import getters as g

def print_menu():
    """Print the menu to display potential selections"""
    print("""
    1) Enter Income
    2) Enter expenses
    3) View Income
    4) View Expenses
    5) Delete Income
    6) Delete Expenses
    0) Exit
    """)

def main():

    # Greeting
    print("\nWelcome to Coin Jar. A budgeting and financial tracking application"
          " written in Python.")

    # Set up
    con = dm.get_connection()
    dm.create_table(con)
    dm.set_category_defaults(con)

    # User selection
    while True:
        print_menu()
        selection = input("\nPlease make a selection: ")
        if selection == '1':
            # Enter Income data
            data = g.get_input_data(group="income")
            dm.insert_data(con, data, group="income") 
        elif selection == '2':
            # Enter Expenses data
            data = g.get_input_data(group="expenses")
            dm.insert_data(con, data, group="expenses")
        elif selection == '3':
            # View Income data
            dm.select(con, group="income")
        elif selection  == '4':
            # View Expenses data
            dm.select(con, group="expenses")
        elif selection == '5':
            # Delete income
            id_set = dm.display_for_delete(con, group="income")
            delete_id = g.get_delete_selection(id_set)
            dm.delete(con, delete_id, group="income") 
        elif selection == '6':
            # Delete expenses
            id_set = dm.display_for_delete(con, group="expenses")
            delete_id = g.get_delete_selection(id_set)
            dm.delete(con, delete_id, group="expenses") 
        elif selection == '0':
            con.close()
            sys.exit("\nGoodbye, and happy saving!")
        else:
            print("\nPlease enter a valid selection")

if __name__ == "__main__":
    main()

