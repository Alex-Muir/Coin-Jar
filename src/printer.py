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
        7) Print Coin Jar
        0) Exit                                                                     
        """)

    def print_date_format_requirement(self):
        """Print date format requirements"""
        print("\nPlease enter dates as 'yyyy-mm-dd' format (include the hyphens)."
              "\nYou can leave this blank if you would like to use today's date")

    def print_income_categories(self, valid_ids_names):
        """Print the categories for income"""
        for item in valid_ids_names:
            print(f"{item[1]} - {item[0]}")

    def print_expenses_categories(self, valid_ids_names):
        """Print the categories for expenses"""
        for item in valid_ids_names:
            print(f"{item[1]} - {item[0]}")

    def print_select(self, data):
        """Print the returned data from a database query"""
        print(data)
