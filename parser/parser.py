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
    
    def __init__(self):
        self.tokenizer = Tokenizer()
        self.current_tokens = []
        self.current_index = 0
    
    def parse(self, sql: str) -> Command:
        tokens = self.tokenizer.tokenize(sql)
        self.current_tokens = tokens
        self.current_index = 0
        
        if not tokens:
            raise SyntaxError("Empty SQL statement")
        
        command = self._parse_command()
        
        # Check for trailing tokens
        if self.current_index < len(tokens):
            raise SyntaxError(f"Unexpected tokens after command: {tokens[self.current_index:]}")
        
        return command
    
    def _parse_command(self) -> Command:
        """Parse the main command based on the first keyword."""
        if self.current_index >= len(self.current_tokens):
            raise SyntaxError("Unexpected end of statement")
        
        token = self.current_tokens[self.current_index]
        
        if token.type != "KEYWORD":
            raise SyntaxError(f"Expected keyword, got {token.type}")
        
        if token.value == "CREATE":
            return self._parse_create_table()
        elif token.value == "INSERT":
            return self._parse_insert()
        elif token.value == "SELECT":
            return self._parse_select()
        elif token.value == "UPDATE":
            return self._parse_update()
        elif token.value == "DELETE":
            return self._parse_delete()
        elif token.value in ("BEGIN", "COMMIT", "ROLLBACK"):
            return self._parse_transaction()
        else:
            raise SyntaxError(f"Unsupported command: {token.value}")
    
    def _parse_create_table(self) -> CreateTableCommand:
        """Parse CREATE TABLE statement."""
        # CREATE TABLE table_name (column_definitions)
        self._expect_keyword("CREATE")
        self._expect_keyword("TABLE")
        
        table_name = self._expect_identifier()
        self._expect_punctuation("(")
        
        columns = []
        while self.current_index < len(self.current_tokens):
            column_def = self._parse_column_definition()
            columns.append(column_def)
            
            if self._peek_punctuation() == ")":
                break
            
            self._expect_punctuation(",")
        
        self._expect_punctuation(")")
        
        return CreateTableCommand(table_name, columns)
    
    def _parse_column_definition(self) -> Dict[str, Any]:
        """Parse a column definition in CREATE TABLE."""
        column_name = self._expect_identifier()
        data_type = self._expect_identifier()
        
        column_def = {
            "name": column_name,
            "type": data_type,
            "nullable": True,
            "primary_key": False
        }
        
        # Parse additional constraints
        while self.current_index < len(self.current_tokens):
            token = self._peek_token()
            if token.type == "PUNCTUATION" and token.value in (",", ")"):
                break
            
            if token.type == "KEYWORD":
                if token.value == "NOT":
                    self._advance()
                    self._expect_keyword("NULL")
                    column_def["nullable"] = False
                elif token.value == "PRIMARY":
                    self._advance()
                    self._expect_keyword("KEY")
                    column_def["primary_key"] = True
                else:
                    break
            else:
                break
        
        return column_def
    
    def _parse_insert(self) -> InsertCommand:
        """Parse INSERT INTO statement."""
        # INSERT INTO table_name (columns) VALUES (values)
        self._expect_keyword("INSERT")
        self._expect_keyword("INTO")
        
        table_name = self._expect_identifier()
        
        # Parse column list (optional)
        columns = []
        if self._peek_punctuation() == "(":
            self._advance()
            while self.current_index < len(self.current_tokens):
                columns.append(self._expect_identifier())
                if self._peek_punctuation() == ")":
                    break
                self._expect_punctuation(",")
            self._expect_punctuation(")")
        
        self._expect_keyword("VALUES")
        
        # Parse values
        values = []
        while self.current_index < len(self.current_tokens):
            self._expect_punctuation("(")
            row_values = []
            while self.current_index < len(self.current_tokens):
                value = self._parse_value()
                row_values.append(value)
                if self._peek_punctuation() == ")":
                    break
                self._expect_punctuation(",")
            self._expect_punctuation(")")
            values.append(row_values)
            
            if self._peek_punctuation() != "(":
                break
            self._expect_punctuation(",")
        
        return InsertCommand(table_name, columns, values)
    
    def _parse_select(self) -> SelectCommand:
        """Parse SELECT statement."""
        # SELECT columns FROM table_name [WHERE condition] [ORDER BY] [LIMIT]
        self._expect_keyword("SELECT")
        
        # Parse column list
        columns = []
        if self._peek_token().value == "*":
            self._advance()
            columns = ["*"]
        else:
            while self.current_index < len(self.current_tokens):
                columns.append(self._expect_identifier())
                if self._peek_punctuation() != ",":
                    break
                self._advance()
        
        self._expect_keyword("FROM")
        table_name = self._expect_identifier()
        
        # Parse WHERE clause
        where_clause = None
        if self._peek_keyword() == "WHERE":
            where_clause = self._parse_where_clause()
        
        # Parse ORDER BY
        order_by = None
        if self._peek_keyword() == "ORDER":
            order_by = self._parse_order_by()
        
        # Parse LIMIT
        limit = None
        if self._peek_keyword() == "LIMIT":
            limit = self._parse_limit()
        
        return SelectCommand(columns, table_name, where_clause, order_by, limit)
    