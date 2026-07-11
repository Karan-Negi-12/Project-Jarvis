import sqlite3
from datetime import datetime, timedelta


class ShortTermMemory:
    """Recent commands & interactions, persisted in SQLite."""

    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn
        self._create_table()

    def _create_table(self):
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS short_term (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role TEXT,
                content TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        self.conn.commit()

    def add(self, role: str, content: str):
        self.conn.execute(
            "INSERT INTO short_term (role, content) VALUES (?, ?)",
            (role, content),
        )
        self.conn.commit()

    def get_recent(self, days: int = 2, limit: int = 15):
        cutoff = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d %H:%M:%S")
        rows = self.conn.execute(
            """
            SELECT role, content, created_at
            FROM short_term
            WHERE created_at >= ?
            ORDER BY created_at DESC
            LIMIT ?
            """,
            (cutoff, limit),
        ).fetchall()
        # Return oldest-first so it reads naturally
        return list(reversed(rows))

    def clear(self):
        self.conn.execute("DELETE FROM short_term")
        self.conn.commit()