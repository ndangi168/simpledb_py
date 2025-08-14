"""
Converts tokens into structured command objects for execution.
"""

from typing import List, Dict, Any, Optional
from .tokenizer import Token, Tokenizer
from ..utils.errors import ParserError, SyntaxError


class Command:
    def __init__(self, command_type: str):
        self.type = command_type


class CreateTableCommand(Command):
    def __init__(self, table_name: str, columns: List[Dict[str, Any]]):
        super().__init__("CREATE_TABLE")
        self.table_name = table_name
        self.columns = columns


class InsertCommand(Command):
    def __init__(self, table_name: str, columns: List[str], values: List[List[Any]]):
        super().__init__("INSERT")
        self.table_name = table_name
        self.columns = columns
        self.values = values


class SelectCommand(Command):
    def __init__(self, columns: List[str], table_name: str, where_clause: Optional[Dict] = None,
                 order_by: Optional[List[Dict]] = None, limit: Optional[int] = None):
        super().__init__("SELECT")
        self.columns = columns
        self.table_name = table_name
        self.where_clause = where_clause
        self.order_by = order_by
        self.limit = limit


class UpdateCommand(Command):
    def __init__(self, table_name: str, set_clause: Dict[str, Any], where_clause: Optional[Dict] = None):
        super().__init__("UPDATE")
        self.table_name = table_name
        self.set_clause = set_clause
        self.where_clause = where_clause


class DeleteCommand(Command):
    def __init__(self, table_name: str, where_clause: Optional[Dict] = None):
        super().__init__("DELETE")
        self.table_name = table_name
        self.where_clause = where_clause


class TransactionCommand(Command):
    def __init__(self, transaction_type: str):
        super().__init__("TRANSACTION")
        self.transaction_type = transaction_type


class Parser:
    """
    Parses SQL tokens into command objects.
    
    Supports:
    - CREATE TABLE
    - INSERT INTO
    - SELECT
    - UPDATE
    - DELETE
    - BEGIN/COMMIT/ROLLBACK
    """
  