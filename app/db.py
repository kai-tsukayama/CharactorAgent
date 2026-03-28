import sqlite3
from pathlib import Path

DB_PATH = Path("data/chara_agent.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS characters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            role TEXT NOT NULL,
            tone TEXT NOT NULL,
            personality TEXT NOT NULL,
            speaking_style TEXT NOT NULL
        )
        """
    )

    conn.commit()
    conn.close()