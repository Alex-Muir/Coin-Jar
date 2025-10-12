import sqlite3
import sys

import database_manager as dm

def print_menu():
    """Print the menu to display potential selections"""
    print("""
    1) Enter Income
    2) Enter expenses
    3) View Income
    4) View Expenses
    0) Exit
    """)

def _get_date():
    """Get the date for income or expenses"""

    print("\nPlease enter dates as 'yyyy-mm-dd' format (include the hyphens)."
          "\nYou can leace this blank if you would like to use today's date")
    date = input("\nEnter the date of this income: ")
    if not date:
        return None
    return date

def _get_amount():
    """Get amount for income or expenses"""

    while True:
        try:
            amount = float(input("\nEnter the amount: "))
        except ValueError:
            print("\nPlease enter a number")
        else:
            if amount < 0:
                print("\nThe amount must be greater than 0")
                continue
            return amount

def _get_category_id(group):
    """Get the category id for the type of income or expense"""
    # THIS WILL BE REPLACED WITH A GRAPHICAL MENU. THE USER WILL NOT NEED TO
    # KNOW THE ACTUAL ID OF THE CATEGORY

    # MAKE THE CHECKS DYNAMIC EX: SELECT COUNT(*) from CATEGORIES WHERE type = 'expense
    # TO CHECK IF ID IS VALID

    # CAN CURRENTLY ENTER AN EXPENSE ID FOR INCOME (AND VICE VERSA) AND IT WILL 
    # COUNT AS VALID INPUT

    if group == "income":
        print("\nIncome categories and ids")
        print("\nSalary: 9\nPay Check: 10\nMisc Income: 11")

    if group == "expense":
        print("\nExpense categories and ids")
        print("\nRent: 1\nGroceries: 2\n Eating Out: 3\nTransportation: 4")
        print("Entertainment & Leisure: 5\nUtilities: 6\nHealth & Wellness: 7")
        print("Misc Expense: 8")

    while True:
        try:
            category_id = int(input("Enter the category id: "))
        except ValueError:
            print("\nPlease enter an integer listed above")
        else:
            if category_id < 1 or category_id > 11:
                print("\nPlease enter a valid number")
                continue
        return category_id
    
def _get_description():
    """Get an optional description for the income or expense"""
    description = input("\nEnter a description (you can leave this blank): ")
    if description:
        return description
    return None

def get_input_data(group):
    date = _get_date()
    amount = _get_amount()
    category_id = _get_category_id(group)
    description = _get_description()

    return (date, amount, category_id, description) 
         

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
        selection = input("\nPlease make a selection:")
        if selection == '1':
            data = get_input_data(group="income")
            dm.insert_income(con, data) 
        elif selection == '2':
            pass
        elif selection == '3':
            pass
        elif selection  == '4':
            pass
        elif selection == '0':
            con.close()
            sys.exit()
        else:
            print("\nPlease enter a valid selection")

if __name__ == "__main__":
    main()

