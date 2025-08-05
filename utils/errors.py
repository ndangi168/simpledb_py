# simpledb/utils/errors.py

"""
Custom exception classes for SimpleDB.
"""

class SimpleDBError(Exception):
    """Base class for all custom SimpleDB errors."""
    pass

class TableNotFoundError(SimpleDBError):
    """Raised when a table doesn't exist."""
    pass

class InvalidQueryError(SimpleDBError):
    """Raised when a SQL query is invalid or unsupported."""
    pass

class ColumnMismatchError(SimpleDBError):
    """Raised when INSERT values don't match table schema."""
    pass