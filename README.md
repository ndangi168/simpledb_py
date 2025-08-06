This project is under construction.

This Database project somehow will look like this


simpledb/
├── main.py                         
├── config.py                       
├── core/                           # Core database logic
│   ├── db_engine.py                # Database class (holds all tables)
│   ├── table.py                    # Table class & schema 
├── commands/                       # Separate dir for logic for each SQL command
│   ├── create_table.py             
│   ├── insert.py                   
│   ├── select.py                   
│   ├── update.py               
│   ├── delete.py            
├── parser/                     
│   ├── tokenizer.py                # Used for breaking SQL string into tokens
│   ├── parser.py                   # Converts tokens into command and arguments
├── indexes/                       
│   ├── btree.py                    # Basic B-Tree indexing (same as sqlite)
│   ├── hash_index.py               # Basic Hash index
├── storage/                    
│   ├── file_manager.py             # Save and load tables from disk
│   ├── wal.py                      # Write-Ahead Log for durability and transactions and recovery
├── transactions/                  
│   ├── transaction.py              # For ACID properties
├── interface/
│   └── repl.py                     # For CLI which runs SQL prompt
├── utils/
│   ├── errors.py                   # Custom errors
│   └── helpers.py                  # Helping commands
└── tests/
    └── test                        # Some Testing files



Phase 1: (Currently here)
    Some basic flow and functions building and brainstorming directly using python dictionary.