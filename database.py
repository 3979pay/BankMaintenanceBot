import sqlite3
import os
from config import DATABASE

os.makedirs("data", exist_ok=True)


def get_db():
    return sqlite3.connect(DATABASE)


def init_db():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS bank_status(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        bank TEXT UNIQUE,
        status TEXT,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        admin_id INTEGER
    )
    """)

    conn.commit()
    conn.close()

def set_status(bank, status, admin_id):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO bank_status(bank,status,admin_id)
    VALUES(?,?,?)
    ON CONFLICT(bank)
    DO UPDATE SET
        status=excluded.status,
        admin_id=excluded.admin_id,
        updated_at=CURRENT_TIMESTAMP
    """, (bank, status, admin_id))

    conn.commit()
    conn.close()


def get_status(bank):
    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "SELECT status FROM bank_status WHERE bank=?",
        (bank,)
    )

    row = cur.fetchone()

    conn.close()

    if row:
        return row[0]

    return "online"


def get_all_status():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT bank, status, updated_at
        FROM bank_status
        ORDER BY bank
    """)

    rows = cur.fetchall()

    conn.close()

    return rows