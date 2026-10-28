import sqlite3
from pathlib import Path

DB_path = Path(__file__).with_name("taskdb.db")

def get_db():
    conn = sqlite3.connect(DB_path)
    conn.row_factory = sqlite3.Row

    try:
        yield conn
    finally:
        conn.close()


def create_table():
    conn = sqlite3.connect(DB_path)

    try:
        conn.execute("""
        CREATE TABLE  IF NOT EXISTS tasks(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Title TEXT  NOT NULL CHECK(length(Title)>0),
        Description TEXT NOT NULL DEFAULT '',
        Priority TEXT NOT NULL CHECK(Priority IN ('low','medium','high')),
        Taskstatus TEXT NOT NULL CHECK(Taskstatus IN ('pending','in progress','completed')))        
""")

        conn.commit()
    finally:
        conn.close()

create_table()
