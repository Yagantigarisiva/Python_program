import sqlite3, os

APP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(APP_DIR, "data", "site.db")

def main():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    con = sqlite3.connect(DB_PATH)
    with open(os.path.join(APP_DIR, "data", "schema.sql"), "r", encoding="utf-8") as f:
        con.executescript(f.read())
    with open(os.path.join(APP_DIR, "data", "seed.sql"), "r", encoding="utf-8") as f:
        con.executescript(f.read())
    con.commit()
    con.close()
    print("Database initialized at", DB_PATH)

if __name__ == "__main__":
    main()
