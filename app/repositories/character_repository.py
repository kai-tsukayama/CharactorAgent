from app.db import get_connection
from app.models import Character

def get_all_characters():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM characters")
    rows = cursor.fetchall()

    conn.close()
    return [
        Character(
            id = row["id"],
            name = row["name"],
            role = row["role"],
            tone = row["tone"],
            personality = row["personality"],
            speaking_style = row["speaking_style"],
        )
        for row in rows
    ]