import sqlite3
import json
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "trace.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS investigations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            inv_type TEXT NOT NULL,
            target TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            status TEXT NOT NULL,
            summary TEXT,
            data_json TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def save_investigation(inv_type: str, target: str, status: str, summary: str, data: dict) -> int:
    conn = get_connection()
    cursor = conn.cursor()
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        INSERT INTO investigations (inv_type, target, timestamp, status, summary, data_json)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (inv_type, target, now_str, status, summary, json.dumps(data)))
    inv_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return inv_id

def get_all_investigations(limit: int = 50):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, inv_type, target, timestamp, status, summary
        FROM investigations
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))
    rows = cursor.fetchall()
    results = [dict(row) for row in rows]
    conn.close()
    return results

def get_investigation_by_id(inv_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, inv_type, target, timestamp, status, summary, data_json
        FROM investigations
        WHERE id = ?
    """, (inv_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return None
    res = dict(row)
    res["data"] = json.loads(res["data_json"])
    conn.close()
    return res

def delete_investigation(inv_id: int) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM investigations WHERE id = ?", (inv_id,))
    deleted = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return deleted

def clear_all_investigations():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM investigations")
    conn.commit()
    conn.close()

def get_stats():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM investigations")
    total = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM investigations WHERE inv_type = 'username'")
    total_usernames = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM investigations WHERE inv_type = 'domain'")
    total_domains = cursor.fetchone()[0]
    
    cursor.execute("""
        SELECT id, inv_type, target, timestamp, status, summary
        FROM investigations
        ORDER BY id DESC
        LIMIT 5
    """)
    recent = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return {
        "total_investigations": total,
        "total_usernames": total_usernames,
        "total_domains": total_domains,
        "recent_activity": recent,
        "supported_sources_count": 10
    }

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully at:", DB_PATH)
