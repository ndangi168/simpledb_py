"""
Breaks SQL strings into individual tokens for parsing.
"""

from typing import List, Tuple
from ..config import SQL_KEYWORDS, MAX_SQL_LENGTH, MAX_TOKENS
from ..utils.errors import ParserError


class Token:
    def __init__(self, token_type: str, value: str, position: int):
        self.type = token_type
        self.value = value
        self.position = position
    
    def __repr__(self):
        return f"Token({self.type}, '{self.value}', pos={self.position})"


class Tokenizer:
    def __init__(self):
        self.keywords = SQL_KEYWORDS
        self.operators = {
            '=', '<', '>', '<=', '>=', '<>', '!=',
            '+', '-', '*', '/', 'AND', 'OR', 'NOT'
        }
        self.punctuation = {
            '(', ')', ',', ';', '.', '*'
        }
    
    def tokenize(self, sql: str) -> List[Token]:
        if len(sql) > MAX_SQL_LENGTH:
            raise ParserError(f"SQL statement too long (max {MAX_SQL_LENGTH} characters)")
        
        tokens = []
        position = 0
        i = 0
        
        while i < len(sql):
            char = sql[i]
            
            # Skip whitespace
            if char.isspace():
                i += 1
                continue
            
            # Handle comments (simple -- style)
            if char == '-' and i + 1 < len(sql) and sql[i + 1] == '-':
                # Skip to end of line
                while i < len(sql) and sql[i] != '\n':
                    i += 1
                continue
            
            # Handle string literals
            if char == "'" or char == '"':
                token, new_i = self._tokenize_string(sql, i, char)
                tokens.append(token)
                i = new_i
                continue
            
            # Handle numbers
            if char.isdigit() or char == '-':
                token, new_i = self._tokenize_number(sql, i)
                tokens.append(token)
                i = new_i
                continue
            
            # Handle identifiers and keywords
            if char.isalpha() or char == '_':
                token, new_i = self._tokenize_identifier(sql, i)
                tokens.append(token)
                i = new_i
                continue
            
            # Handle operators and punctuation
            if char in self.operators or char in self.punctuation:
                token, new_i = self._tokenize_operator(sql, i)
                tokens.append(token)
                i = new_i
                continue
            
            # Unknown character
            raise ParserError(f"Unexpected character '{char}' at position {i}")
        
        if len(tokens) > MAX_TOKENS:
            raise ParserError(f"Too many tokens (max {MAX_TOKENS})")
        
        return tokens
    
    def _tokenize_string(self, sql: str, start: int, quote_char: str) -> Tuple[Token, int]:
        value = ""
        i = start + 1  # Skip opening quote
        
        while i < len(sql):
            char = sql[i]
            if char == quote_char:
                # Check for escaped quote
                if i + 1 < len(sql) and sql[i + 1] == quote_char:
                    value += char
                    i += 2
                else:
                    i += 1
                    break
            elif char == '\\':
                # Handle escape sequences
                if i + 1 < len(sql):
                    i += 1
                    value += sql[i]
                i += 1
            else:
                value += char
                i += 1
        else:
            raise ParserError(f"Unterminated string literal starting at position {start}")
        
        return Token("LITERAL", value, start), i
    
    def _tokenize_number(self, sql: str, start: int) -> Tuple[Token, int]:
        value = ""
        i = start
        
        # Handle negative numbers
        if sql[i] == '-':
            value += sql[i]
            i += 1
        
        # Integer part
        while i < len(sql) and sql[i].isdigit():
            value += sql[i]
            i += 1
        
        # Decimal part
        if i < len(sql) and sql[i] == '.':
            value += sql[i]
            i += 1
            while i < len(sql) and sql[i].isdigit():
                value += sql[i]
                i += 1
        
        return Token("LITERAL", value, start), i
    
    def _tokenize_identifier(self, sql: str, start: int) -> Tuple[Token, int]:
        value = ""
        i = start
        
        while i < len(sql) and (sql[i].isalnum() or sql[i] == '_'):
            value += sql[i]
            i += 1
        
        # Check if it's a keyword
        if value.upper() in self.keywords:
            return Token("KEYWORD", value.upper(), start), i
        else:
            return Token("IDENTIFIER", value, start), i
    
    def _tokenize_operator(self, sql: str, start: int) -> Tuple[Token, int]:
        char = sql[start]
        
        # Try two-character operators first
        if start + 1 < len(sql):
            two_char = char + sql[start + 1]
            if two_char in ('<=', '>=', '<>', '!='):
                return Token("OPERATOR", two_char, start), start + 2
        
        # Single character operators and punctuation
        if char in self.operators:
            return Token("OPERATOR", char, start), start + 1
        elif char in self.punctuation:
            return Token("PUNCTUATION", char, start), start + 1
        
        raise ParserError(f"Unknown operator '{char}' at position {start}")
    
    def filter_tokens(self, tokens: List[Token], exclude_types: List[str] = None) -> List[Token]:
        """
        Filter tokens by type, excluding specified types.
        """
        if exclude_types is None:
            exclude_types = ["WHITESPACE"]
        
        return [token for token in tokens if token.type not in exclude_types] 