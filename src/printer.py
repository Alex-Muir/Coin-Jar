class Printer:
    """A class for printing long bitd of text"""
    def __init__(self):
        """Nothing happens here"""
        pass

    def print_greeting(self):
        """Print the greeting when the program begins"""
        print("Welcome to Coin Jar! A budgeting and financial tracking "
              "application written in Python")

    def print_menu(self):
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

    def print_date_format_requirement(self):
        """Print date format requirements"""
        print("\nPlease enter dates as 'yyyy-mm-dd' format (include the hyphens)."
              "\nYou can leace this blank if you would like to use today's date")

    def print_income_categories(self):
        """Print the categories for income"""
        print("\nIncome categories and ids")
        print("\nSalary: 9\nPay Check: 10\nMisc Income: 11")

    def print_expenses_categories(self):
        """Print the categories for expenses"""
        print("\nExpense categories and ids")
        print("\nRent: 1\nGroceries: 2\nEating Out: 3\nTransportation: 4")
        print("Entertainment & Leisure: 5\nUtilities: 6\nHealth & Wellness: 7")
        print("Misc Expense: 8")

    def print_select(self, data):
        """Print the returned data from a database query"""
        print(data)