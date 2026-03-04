import sqlite3
from datetime import datetime

DB_NAME = "me_pdfs.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # PDF Sessions
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pdf_sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT,
        extracted_text TEXT,
        created_at TEXT
    )
    """)

    # Chat Messages
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chat_messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id INTEGER,
        role TEXT,
        message TEXT,
        created_at TEXT,
        FOREIGN KEY(session_id) REFERENCES pdf_sessions(id)
    )
    """)

    conn.commit()
    conn.close()