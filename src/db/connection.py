import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # pasta /src
DB_PATH = os.path.join(BASE_DIR, "vendas.db")

def get_connection():
    if not os.path.exists(DB_PATH):
        raise FileNotFoundError(f"Banco não encontrado em: {DB_PATH}")

    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn







# DEBUG opcional:
#if __name__ == "__main__":
    print("DB_PATH:", DB_PATH)
    print("Exists?", os.path.exists(DB_PATH))
    print("Size:", os.path.getsize(DB_PATH) if os.path.exists(DB_PATH) else "N/A")

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    print(cur.fetchall())
