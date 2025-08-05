# simpledb/interface/repl.py

def start_repl(database, file_manager):
    while True:
        try:
            user_input = input("SimpleDB > ").strip()

            if not user_input:
                continue

            if user_input.upper() in ("EXIT;", "QUIT;"):
                print("[INFO] Exiting SimpleDB. Goodbye!")
                file_manager.save_database(database)
                break

            print(f"[DEBUG] You entered: {user_input}")
            print("[WARN] SQL parser not yet implemented.")

        except KeyboardInterrupt:
            print("\n[INFO] Interrupted. Type 'EXIT;' to quit.")
        except Exception as e:
            print(f"[ERROR] {e}")