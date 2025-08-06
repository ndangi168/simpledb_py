class Table:
    def __init__(self, name, columns):
        self.name = name
        self.columns = columns
        self.rows = []

    def insert_row(self, values):
        if len(values) != len(self.columns):
            raise ValueError("Column count does not match values count")
        self.rows.append(values)

    def select_rows(self):
        return self.rows

    def get_table_info(self):
        return {
            "name": self.name,
            "columns": self.columns,
            "row_count": len(self.rows)
        }