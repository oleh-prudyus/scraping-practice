import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone

from .config import DB_PATH


@contextmanager
def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db():
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS quotes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL,
                author TEXT NOT NULL,
                scraped_at TEXT NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS run_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                started_at TEXT NOT NULL,
                finished_at TEXT,
                status TEXT NOT NULL,
                message TEXT
            )
            """
        )


def get_setting(key, default=None):
    with get_connection() as conn:
        row = conn.execute("SELECT value FROM settings WHERE key = ?", (key,)).fetchone()
        return row["value"] if row else default


def set_setting(key, value):
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO settings (key, value) VALUES (?, ?) "
            "ON CONFLICT(key) DO UPDATE SET value = excluded.value",
            (key, value),
        )


def save_quotes(quotes):
    now = datetime.now(timezone.utc).isoformat()
    with get_connection() as conn:
        conn.execute("DELETE FROM quotes")
        conn.executemany(
            "INSERT INTO quotes (text, author, scraped_at) VALUES (?, ?, ?)",
            [(text, author, now) for text, author in quotes],
        )


def get_quotes(limit=200):
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT text, author, scraped_at FROM quotes ORDER BY id LIMIT ?", (limit,)
        ).fetchall()
        return [dict(row) for row in rows]


def start_run():
    now = datetime.now(timezone.utc).isoformat()
    with get_connection() as conn:
        cursor = conn.execute(
            "INSERT INTO run_log (started_at, status) VALUES (?, ?)", (now, "running")
        )
        return cursor.lastrowid


def finish_run(run_id, status, message=""):
    now = datetime.now(timezone.utc).isoformat()
    with get_connection() as conn:
        conn.execute(
            "UPDATE run_log SET finished_at = ?, status = ?, message = ? WHERE id = ?",
            (now, status, message, run_id),
        )


def get_last_run():
    with get_connection() as conn:
        row = conn.execute(
            "SELECT started_at, finished_at, status, message FROM run_log ORDER BY id DESC LIMIT 1"
        ).fetchone()
        return dict(row) if row else None
