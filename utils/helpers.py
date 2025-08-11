"""
Contains functions for formatting, type conversion, and data validation.
"""

import json
from typing import Any, List, Dict, Union
from ..config import SUPPORTED_TYPES


def format_table_output(headers: List[str], rows: List[List[Any]]) -> str:
    if not rows:
        return "No rows returned."
    
    # Calculate column widths
    col_widths = []
    for i, header in enumerate(headers):
        max_width = len(str(header))
        for row in rows:
            if i < len(row):
                max_width = max(max_width, len(str(row[i])))
        col_widths.append(max_width + 2)  # Add padding
    
    # Create separator line
    separator = "+" + "+".join("-" * width for width in col_widths) + "+"
    
    # Build the table
    result = [separator]
    
    # Header row
    header_row = "|"
    for i, header in enumerate(headers):
        header_row += f" {str(header):<{col_widths[i]-1}}|"
    result.append(header_row)
    result.append(separator)
    
    # Data rows
    for row in rows:
        data_row = "|"
        for i, cell in enumerate(row):
            data_row += f" {str(cell):<{col_widths[i]-1}}|"
        result.append(data_row)
    
    result.append(separator)
    return "\n".join(result)


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


def format_success_message(message: str) -> str:
    return f"✓ {message}"


def format_error_message(message: str) -> str:
    return f"✗ {message}"


def format_info_message(message: str) -> str:
    return f"ℹ {message}"


def safe_json_dumps(obj: Any) -> str:
    def default_converter(o):
        if hasattr(o, '__dict__'):
            return o.__dict__
        return str(o)
    
    return json.dumps(obj, default=default_converter, indent=2)


def safe_json_loads(s: str) -> Any:
    try:
        return json.loads(s)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON: {e}")


def truncate_string(s: str, max_length: int = 50) -> str:
    if len(s) <= max_length:
        return s
    return s[:max_length-3] + "..." 