import sqlite3
import sys

from database_manager import DatabaseManager
from getters import Getter
from printer import Printer
from visualizer import Visualizer

class CoinJar:
    """CoinJar class, responsible for running the program"""

    def __init__(self):
        """Initializes a database manager and a getter for a CoinJar"""
        self.dm = DatabaseManager()
        self.g = Getter()
        self.p = Printer()
        self.v = Visualizer()

    def run(self):
        """Runs the program"""
        self.p.print_greeting()
        self.dm.create_table()
        self.dm.set_category_defaults()
        self._user_selection()

    def _user_selection(self): 
        """
        Prints the menu, gets user selection, and calls functions based on the
        user's choice
        """
        while True:
            self.p.print_menu()
            selection = input("\nPlease make a selection: ").strip()
            if selection == '1':                                                    
                # Enter Income data     
                valid_ids_names = self.dm.get_valid_category_ids_names(group="income")                                            
                data = self.g.get_input_data(valid_ids_names, group="income")                             
                self.dm.insert_data(data, group="income")                           
            elif selection == '2':                                                  
                # Enter Expenses data  
                valid_ids_names = self.dm.get_valid_category_ids_names(group="expense")                                             
                data = self.g.get_input_data(valid_ids_names, group="expense")                           
                self.dm.insert_data(data, group="expense")                         
            elif selection == '3':                                                  
                # View Income data                                                  
                data = self.dm.select(group="income")   
                self.p.print_select(data)                                   
            elif selection  == '4':                                                 
                # View Expenses data                                                
                data = self.dm.select(group="expense")
                self.p.print_select(data)
                self.v.pie_chart(data)                                    
            elif selection == '5':                                                  
                # Delete income                                                     
                id_set = self.dm.display_for_delete(group="income")                 
                delete_id = self.g.get_delete_selection(id_set)                          
                self.dm.delete(delete_id, group="income")                           
            elif selection == '6':                                                  
                # Delete expenses                                                   
                id_set = self.dm.display_for_delete(group="expense")           
                delete_id = self.g.get_delete_selection(id_set)                          
                self.dm.delete(delete_id, group="expense")                         
            elif selection == '0':                                                  
                self.dm.close()                                                         
                sys.exit("\nGoodbye, and happy saving!")                            
            else:                                                                   
                print("\nPlease enter a valid selection")
         

if __name__ == "__main__":
    cj = CoinJar()
    cj.run()
