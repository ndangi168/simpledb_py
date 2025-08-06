# Global configuration file for SimpleDB
# Stores constants, file paths, and settings used across the project

import os

# Database file paths
DATA_DIR = "simpledb_data" # Folder for db
WAL_FILE = os.path.join(DATA_DIR, "wal.log") # For transactions and crash recovery
METADATA_FILE = os.path.join(DATA_DIR, "metadata.json") # For schemas

# Table and storage settings
DEFAULT_BUFFER_SIZE = 1024  # bytes (1kb, mostly used 4kb like by sqlite)
MAX_TABLE_NAME_LENGTH = 64
MAX_COLUMN_NAME_LENGTH = 32

# Index settings
BTREE_ORDER = 4  # Number of children per node
HASH_TABLE_SIZE = 1000  # Initial size for hash tables

# Transaction settings
MAX_TRANSACTION_ID = 999999 # To avoid overflow
TRANSACTION_TIMEOUT = 30  # seconds

# Parser settings
MAX_SQL_LENGTH = 10000  # characters
MAX_TOKENS = 1000

# Error messages
ERROR_MESSAGES = {
    "table_exists": "Table '{}' already exists",
    "table_not_found": "Table '{}' not found",
    "column_not_found": "Column '{}' not found in table '{}'",
    "invalid_syntax": "Invalid SQL syntax",
    "type_mismatch": "Type mismatch for column '{}'",
    "transaction_not_found": "No active transaction",
    "transaction_exists": "Transaction already in progress"
}

# Supported data types
SUPPORTED_TYPES = {
    "INT": int,
    "INTEGER": int,
    "TEXT": str,
    "STRING": str,
    "FLOAT": float,
    "REAL": float,
    "BOOLEAN": bool,
    "BOOL": bool
}

# SQL keywords for tokenizer
SQL_KEYWORDS = {
    "CREATE", "TABLE", "INSERT", "INTO", "VALUES", "SELECT", "FROM", "WHERE",
    "UPDATE", "SET", "DELETE", "BEGIN", "COMMIT", "ROLLBACK", "INDEX",
    "PRIMARY", "KEY", "FOREIGN", "REFERENCES", "NOT", "NULL", "DEFAULT",
    "ORDER", "BY", "ASC", "DESC", "LIMIT", "OFFSET", "AND", "OR"
} 