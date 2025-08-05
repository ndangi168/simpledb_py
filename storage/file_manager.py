# simpledb/storage/file_manager.py

"""
Handles saving and loading the database from disk.
"""

import os

class FileManager:
    def __init__(self, data_dir):
        self.data_dir = data_dir

    def load_database(self):
        # Just simulate loading
        return None

    def save_database(self, db):
        # Simulate saving
        print("[INFO] Database saved to disk.")