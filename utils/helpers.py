# simpledb/utils/helpers.py

"""
Helper functions for formatting, casting, etc.
"""

def cast_value(value_str):
    """Try to cast string input into int or leave as string."""
    try:
        return int(value_str)
    except ValueError:
        return value_str.strip("'\"")  # remove quotes if it's a string

def print_table(rows, columns):
    """Prints table in a formatted way."""
    if not rows:
        print("[INFO] No rows found.")
        return

    col_widths = [len(col) for col in columns]

    for row in rows:
        for i, val in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(val)))

    def print_row(row):
        print("| " + " | ".join(str(val).ljust(col_widths[i]) for i, val in enumerate(row)) + " |")

    print("+", "+".join("-" * (w + 2) for w in col_widths), "+", sep="")
    print_row(columns)
    print("+", "+".join("-" * (w + 2) for w in col_widths), "+", sep="")
    for row in rows:
        print_row(row)
    print("+", "+".join("-" * (w + 2) for w in col_widths), "+", sep="")