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
    