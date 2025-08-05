'''
    Inititalize the database and starts the REPL (Read-Eval-Print Loop)
'''

from interface.repl import start_repl
from core.db_engine import Database
from storage.file_manager import FileManager 
import config

def main():
    print("\nWelcome! This is SimpleDB made in Python\n")

    # Load database
    file_manager = FileManager(config.DATA_DIR)
    db = file_manager.load_database()
    
    if db is None:
        print("## No existing DB, create a new one.\n\n")
        db = Database()

    start_repl(db, file_manager)

# Start REPL when run direct main.py (not from test)
if __name__ == "__main__":
    main()
