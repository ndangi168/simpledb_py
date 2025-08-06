from core.table import Table

class Database:
    def __init__(self):
        self.tables = {}

    def create_table(self, table_name, columns):
        if table_name in self.tables:
            raise Exception(f"Table {table_name} already exists")
        self.tables[table_name] = Table(table_name, columns)
        return f"Table '{table_name}' created."

    def insert_data(self, table_name, values):
        if table_name not in self.tables:
            raise Exception(f"Table {table_name} not found")
        self.tables[table_name].insert_row(values)
        return f"1 row inserted into '{table_name}'."

    def select_data(self, table_name):
        if table_name not in self.tables:
            raise Exception(f"Table {table_name} not found")
        rows = self.tables[table_name].select_rows()
        return {
            "columns": self.tables[table_name].columns,
            "rows": rows
        }