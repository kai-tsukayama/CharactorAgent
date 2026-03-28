from app.db import get_connection

def get_all_characters():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM characters")
    rows = cursor.fetchall()

    conn.close()
    return rows