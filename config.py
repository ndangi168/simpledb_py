'''
    Config
'''

import os

# getcwd (current working directory) join it with simpledb_data file
DATA_DIR = os.path.join(os.getcwd(), "simpledb_data")

# Create one if not
os.makedirs(DATA_DIR, exist_ok=True)

BUFFER_SIZE = 4096 #in bytes