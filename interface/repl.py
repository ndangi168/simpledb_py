from core.db_engine import Database

def run_repl():
    db = Database()
    print("SimpleDB v1 (type 'exit' to quit)")

    while True:
        cmd = input("SQL> ").strip()
        if cmd.lower() == "exit":
            break
        elif cmd.lower().startswith("create table"):
            # For now: CREATE TABLE users id,name
            parts = cmd.split()
            table_name = parts[2]
            columns = parts[3].split(",")
            print(db.create_table(table_name, columns))
        elif cmd.lower().startswith("insert into"):
            # Example: INSERT INTO users 1,Alice
            parts = cmd.split()
            table_name = parts[2]
            values = parts[3].split(",")
            print(db.insert_data(table_name, values))
        elif cmd.lower().startswith("select"):
            # Example: SELECT * FROM users
            parts = cmd.split()
            table_name = parts[-1]
            result = db.select_data(table_name)
            print(result)
        else:
            print("Unknown command")