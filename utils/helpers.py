"""
Contains functions for formatting, type conversion, and data validation.
"""

import json
from typing import Any, List, Dict, Union
from ..config import SUPPORTED_TYPES

def convert_value(value: str, target_type: str) -> Any:
    # Convert a string value to the specified data type.
    if value.upper() == "NULL":
        return None
    
    type_class = SUPPORTED_TYPES.get(target_type.upper())
    if not type_class:
        raise ValueError(f"Unsupported data type: {target_type}")
    
    try:
        if type_class == bool:
            # Handle boolean conversion
            if value.lower() in ('true', '1', 'yes'):
                return True
            elif value.lower() in ('false', '0', 'no'):
                return False
            else:
                raise ValueError(f"Cannot convert '{value}' to boolean")
        else:
            return type_class(value)
    except (ValueError, TypeError) as e:
        raise ValueError(f"Cannot convert '{value}' to {target_type}: {e}")


def validate_column_name(name: str) -> bool:
    if not name or len(name) > 32:
        return False
    
    # Check if name starts with a letter or underscore
    if not (name[0].isalpha() or name[0] == '_'):
        return False
    
    # Check if name contains only letters, digits, and underscores
    return all(c.isalnum() or c == '_' for c in name)


def validate_table_name(name: str) -> bool:
    if not name or len(name) > 64:
        return False
    
    # Check if name starts with a letter or underscore
    if not (name[0].isalpha() or name[0] == '_'):
        return False
    
    # Check if name contains only letters, digits, and underscores
    return all(c.isalnum() or c == '_' for c in name)