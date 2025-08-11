"""
Represents a database table with schema definition and data storage.
"""

from typing import List, Dict, Any, Optional, Tuple
from ..utils.errors import TableError, ColumnError, ValidationError
from ..utils.helpers import convert_value, validate_column_name, validate_table_name
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


class Table:
    def __init__(self, name: str, columns: List[Dict[str, Any]]):
        if not validate_table_name(name):
            raise TableError(f"Invalid table name: {name}")
        
        self.name = name
        self.columns = []
        self.data = []
        self.indexes = {}
        self.next_row_id = 1
        
        # Create column objects
        for col_def in columns:
            column = Column(
                name=col_def["name"],
                data_type=col_def["type"],
                nullable=col_def.get("nullable", True),
                primary_key=col_def.get("primary_key", False)
            )
            self.columns.append(column)
        
        # Validate schema
        self._validate_schema()
    
    def _validate_schema(self):
        if not self.columns:
            raise TableError("Table must have at least one column")
        
        # Check for duplicate column names
        column_names = [col.name for col in self.columns]
        if len(column_names) != len(set(column_names)):
            raise TableError("Duplicate column names are not allowed")
        
        # Check primary key constraints
        primary_keys = [col for col in self.columns if col.primary_key]
        if len(primary_keys) > 1:
            raise TableError("Only one primary key column is supported")
    
    def get_column_by_name(self, name: str) -> Optional[Column]:
        for column in self.columns:
            if column.name.lower() == name.lower():
                return column
        return None
    
    def get_column_index(self, name: str) -> int:
        for i, column in enumerate(self.columns):
            if column.name.lower() == name.lower():
                return i
        
        raise ColumnError(f"Column '{name}' not found in table '{self.name}'")
    
    def validate_row(self, row_data: List[Any]) -> bool:
        if len(row_data) != len(self.columns):
            return False
        
        for i, (value, column) in enumerate(zip(row_data, self.columns)):
            if not column.validate_value(value):
                return False
        
        return True
    
    def insert_row(self, row_data: List[Any]) -> int:
        if not self.validate_row(row_data):
            raise ValidationError(f"Invalid row data for table '{self.name}'")
        
        # Add row ID as the first column
        row_with_id = [self.next_row_id] + row_data
        self.data.append(row_with_id)
        
        # Update indexes
        self._update_indexes(row_with_id)
        
        row_id = self.next_row_id
        self.next_row_id += 1
        
        return row_id
    
    def update_row(self, row_id: int, updates: Dict[str, Any]) -> bool:
        # Find the row
        row_index = self._find_row_by_id(row_id)
        if row_index is None:
            return False
        
        # Create new row data
        new_row = self.data[row_index].copy()
        
        # Apply updates
        for column_name, new_value in updates.items():
            column = self.get_column_by_name(column_name)
            if column is None:
                raise ColumnError(f"Column '{column_name}' not found")
            
            if not column.validate_value(new_value):
                raise ValidationError(f"Invalid value for column '{column_name}'")
            
            col_index = self.get_column_index(column_name)
            new_row[col_index + 1] = new_value  # +1 for row_id
        
        # Replace the row
        self.data[row_index] = new_row
        
        # Update indexes
        self._update_indexes(new_row)
        
        return True
    
    def delete_row(self, row_id: int) -> bool:
        row_index = self._find_row_by_id(row_id)
        if row_index is None:
            return False
        
        # Remove from data
        deleted_row = self.data.pop(row_index)
        
        # Update indexes (remove the row)
        self._remove_from_indexes(deleted_row)
        
        return True
    
    def select_rows(self, columns: List[str] = None, where_clause: Dict = None,
                   order_by: List[Dict] = None, limit: int = None) -> List[List[Any]]:
        # Determine which columns to select
        if columns is None or columns == ["*"]:
            select_columns = [col.name for col in self.columns]
        else:
            select_columns = columns
        
        # Get column indices
        select_indices = []
        for col_name in select_columns:
            col_index = self.get_column_index(col_name)
            select_indices.append(col_index + 1)  # +1 for row_id
        
        # Filter rows based on WHERE clause
        filtered_rows = self._filter_rows(where_clause)
        
        # Apply ORDER BY
        if order_by:
            filtered_rows = self._sort_rows(filtered_rows, order_by)
        
        # Apply LIMIT
        if limit:
            filtered_rows = filtered_rows[:limit]
        
        # Select specified columns
        result = []
        for row in filtered_rows:
            selected_row = [row[i] for i in select_indices]
            result.append(selected_row)
        
        return result
    
    def _find_row_by_id(self, row_id: int) -> Optional[int]:
        for i, row in enumerate(self.data):
            if row[0] == row_id:
                return i
        return None
    
    def _filter_rows(self, where_clause: Dict = None) -> List[List[Any]]:
        if where_clause is None:
            return self.data.copy()
        
        filtered = []
        for row in self.data:
            if self._evaluate_condition(row, where_clause):
                filtered.append(row)
        
        return filtered
    
    def _evaluate_condition(self, row: List[Any], condition: Dict) -> bool:
        if condition["type"] == "comparison":
            left = condition["left"]
            operator = condition["operator"]
            right = condition["right"]
            
            # Handle column references
            if isinstance(left, str) and self.get_column_by_name(left):
                col_index = self.get_column_index(left)
                left = row[col_index + 1]  # +1 for row_id
            
            if isinstance(right, str) and self.get_column_by_name(right):
                col_index = self.get_column_index(right)
                right = row[col_index + 1]  # +1 for row_id
            
            # Perform comparison
            if operator == "=":
                return left == right
            elif operator == "<>":
                return left != right
            elif operator == "<":
                return left < right
            elif operator == ">":
                return left > right
            elif operator == "<=":
                return left <= right
            elif operator == ">=":
                return left >= right
            else:
                return False
        
        return False
    
    def _sort_rows(self, rows: List[List[Any]], order_by: List[Dict]) -> List[List[Any]]:
        def sort_key(row):
            key_parts = []
            for order_spec in order_by:
                col_name = order_spec["column"]
                direction = order_spec["direction"]
                col_index = self.get_column_index(col_name)
                value = row[col_index + 1]  # +1 for row_id
                
                # Handle None values
                if value is None:
                    value = float('-inf') if direction == "ASC" else float('inf')
                
                key_parts.append(value)
            
            return tuple(key_parts)
        
        reverse = any(spec["direction"] == "DESC" for spec in order_by)
        return sorted(rows, key=sort_key, reverse=reverse)
    
    def _update_indexes(self, row: List[Any]):
        for index_name, index in self.indexes.items():
            index.insert(row)
    
    def _remove_from_indexes(self, row: List[Any]):
        for index_name, index in self.indexes.items():
            index.delete(row)
    
    def create_index(self, index_name: str, column_name: str, index_type: str = "btree"):
        column = self.get_column_by_name(column_name)
        if column is None:
            raise ColumnError(f"Column '{column_name}' not found")
        
        if index_type == "btree":
            from ..indexes.btree import BTreeIndex
            index = BTreeIndex(column_name, self.get_column_index(column_name))
        elif index_type == "hash":
            from ..indexes.hash_index import HashIndex
            index = HashIndex(column_name, self.get_column_index(column_name))
        else:
            raise IndexError(f"Unsupported index type: {index_type}")
        
        # Build index from existing data
        for row in self.data:
            index.insert(row)
        
        self.indexes[index_name] = index
    
    def get_table_info(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "columns": [str(col) for col in self.columns],
            "row_count": len(self.data),
            "indexes": list(self.indexes.keys())
        }
    
    def __repr__(self):
        return f"Table('{self.name}', {len(self.columns)} columns, {len(self.data)} rows)" 
    

