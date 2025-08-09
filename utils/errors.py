"""
Error types for different database operations.
"""


class SimpleDBError(Exception):
    """Base exception class for all SimpleDB errors."""
    pass


class TableError(SimpleDBError):
    """Raised when there are issues with table operations."""
    pass


class TableExistsError(TableError):
    """Raised when trying to create a table that already exists."""
    pass


class TableNotFoundError(TableError):
    """Raised when trying to access a table that doesn't exist."""
    pass


class ColumnError(SimpleDBError):
    """Raised when there are issues with column operations."""
    pass


class ColumnNotFoundError(ColumnError):
    """Raised when trying to access a column that doesn't exist."""
    pass


class ColumnTypeError(ColumnError):
    """Raised when there's a type mismatch for a column."""
    pass


class ParserError(SimpleDBError):
    """Raised when there are issues parsing SQL statements."""
    pass

class TransactionError(SimpleDBError):
    """Raised when there are issues with transactions."""
    pass

class StorageError(SimpleDBError):
    """Raised when there are issues with file storage operations."""
    pass


class IndexError(SimpleDBError):
    """Raised when there are issues with index operations."""
    pass


class ValidationError(SimpleDBError):
    """Raised when data validation fails."""
    pass 




class SyntaxError(ParserError):
    """Raised when SQL syntax is invalid."""
    pass



class NoActiveTransactionError(TransactionError):
    """Raised when trying to commit/rollback without an active transaction."""
    pass


class TransactionInProgressError(TransactionError):
    """Raised when trying to start a transaction while one is already active."""
    pass