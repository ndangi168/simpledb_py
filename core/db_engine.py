# simpledb/core/db_engine.py

"""
Basic skeleton of the in-memory database engine.
"""

class Database:
    def __init__(self):
        self.tables = {}  # Dictionary to hold table name → Table object

    def __repr__(self):
        return f"<Database: {len(self.tables)} tables>"