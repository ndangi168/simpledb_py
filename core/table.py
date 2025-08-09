"""
Represents a database table with schema definition and data storage.
"""

from typing import List, Dict, Any, Optional, Tuple
from ..utils.errors import TableError, ColumnError, ValidationError
from ..utils.helpers import convert_value, validate_column_name
from ..config import SUPPORTED_TYPES


class Column:
    def __init__(self, name: str, data_type: str, nullable: bool = True, primary_key: bool = False):
        self.name = name
        self.data_type = data_type.upper()
        self.nullable = nullable
        self.primary_key = primary_key
        
        # Validate column name
        if not validate_column_name(name):
            raise ColumnError(f"Invalid column name: {name}")
        
        # Validate data type
        if self.data_type not in SUPPORTED_TYPES:
            raise ColumnError(f"Unsupported data type: {data_type}")
    
    def validate_value(self, value: Any) -> bool:
        if value is None:
            return self.nullable
        
        expected_type = SUPPORTED_TYPES[self.data_type]
        return isinstance(value, expected_type)
    
    def convert_value(self, value: str) -> Any:
        # Convert a string value to the column's data type.
        return convert_value(value, self.data_type)
    
    def __repr__(self):
        constraints = []
        if not self.nullable:
            constraints.append("NOT NULL")
        if self.primary_key:
            constraints.append("PRIMARY KEY")
        
        constraint_str = " ".join(constraints)
        return f"{self.name} {self.data_type}{' ' + constraint_str if constraint_str else ''}"


