"""getters.py
This module contains functions defined specifically for the purpose of getting
data from the user. Functions defined here should be longer than one line, and 
can also perform input validation if required.
"""

from printer import Printer

class Getter:
    """A class for getting"""

    def __init__(self):
        """Nothing happens here"""
        self.p = Printer()

    def _get_date(self):
        """Get the date for income or expenses"""

        self.p.print_date_format_requirement()
        date = input("\nEnter the date: ").strip()
        if not date:
            return None
        return date

    def _get_amount(self):
        """Get amount for income or expenses"""

        while True:
            try:
                amount = float(input("\nEnter the amount: ").strip())
            except ValueError:
                print("\nPlease enter a number")
            else:
                if amount < 0:
                    print("\nThe amount must be greater than 0")
                    continue
                return amount

    def _get_category_id(self, valid_ids, group):
        """Get the category id for the type of income or expense"""
        print(valid_ids)
        if group == "income":
            self.p.print_income_categories()

        if group == "expense":
            self.p.print_expenses_categories()

        while True:
            try:
                category_id = int(input("Enter the category id: ").strip())
            except ValueError:
                print("\nPlease enter an integer listed above")
            else:
                if category_id not in valid_ids:
                    print("\nPlease enter a valid number")
                    continue
                return category_id
    
    def _get_description(self):
        """Get an optional description for the income or expense"""
        description = input("\nEnter a description (you can leave this blank): ").strip()
        if description:
            return description
        return None

    def get_input_data(self, valid_ids, group):
        print(valid_ids)
        date = self._get_date()
        amount = self._get_amount()
        category_id = self._get_category_id(valid_ids, group)
        description = self._get_description()

        return (date, amount, category_id, description)

    def get_delete_selection(self, id_set):
        """
        Get the user's selection for which row to delete. Check validity by 
        comparing against the set passed to the function. Ensure input is valid.
        """
        if id_set:
            while True:
                try:
                    selection = int(input("\nEnter the id of the row you'd like to delete: ").strip())
                except ValueError:
                    print("\nPlease ensure your selection is an integer")
                else:
                    if selection not in id_set:
                        print("\nPlease ensure your selection is listed in the output " 
                              "of possible rows to be deleted")
                        continue
                    return selection    
        else:
            print("\nNothing to delete")            
