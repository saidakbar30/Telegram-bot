import sqlite3
from contextlib import closing
from datetime import datetime

from config import DB_PATH, DEFAULT_TEXTS, LATITUDE, LONGITUDE


def _conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with closing(_conn()) as c:
        c.execute(
            "CREATE TABLE IF NOT EXISTS users ("
            "user_id INTEGER PRIMARY KEY, full_name TEXT, username TEXT, "
            "joined_at TEXT, active INTEGER DEFAULT 1)"
        )
        c.execute(
            "CREATE TABLE IF NOT EXISTS texts (key TEXT PRIMARY KEY, value TEXT)"
        )
        for key, value in DEFAULT_TEXTS.items():
            c.execute(
                "INSERT OR IGNORE INTO texts (key, value) VALUES (?, ?)", (key, value)
            )
        c.commit()


# ----- Foydalanuvchilar -----
def add_user(user_id: int, full_name: str, username: str | None):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with closing(_conn()) as c:
        c.execute(
            "INSERT OR IGNORE INTO users (user_id, full_name, username, joined_at) "
            "VALUES (?, ?, ?, ?)",
            (user_id, full_name, username, now),
        )
        c.execute("UPDATE users SET active = 1 WHERE user_id = ?", (user_id,))
        c.commit()


def set_active(user_id: int, active: bool):
    with closing(_conn()) as c:
        c.execute(
            "UPDATE users SET active = ? WHERE user_id = ?",
            (1 if active else 0, user_id),
        )
        c.commit()


def get_active_user_ids() -> list[int]:
    with closing(_conn()) as c:
        rows = c.execute("SELECT user_id FROM users WHERE active = 1").fetchall()
    return [r["user_id"] for r in rows]


def get_stats() -> dict:
    today = datetime.now().strftime("%Y-%m-%d")
    with closing(_conn()) as c:
        total = c.execute("SELECT COUNT(*) FROM users").fetchone()[0]
        active = c.execute("SELECT COUNT(*) FROM users WHERE active = 1").fetchone()[0]
        today_cnt = c.execute(
            "SELECT COUNT(*) FROM users WHERE joined_at LIKE ?", (today + "%",)
        ).fetchone()[0]
    return {
        "total": total,
        "active": active,
        "blocked": total - active,
        "today": today_cnt,
    }


# ----- Matnlar -----
def get_text(key: str) -> str:
    with closing(_conn()) as c:
        row = c.execute("SELECT value FROM texts WHERE key = ?", (key,)).fetchone()
    if row:
        return row["value"]
    return DEFAULT_TEXTS.get(key, "")


def set_text(key: str, value: str):
    with closing(_conn()) as c:
        c.execute(
            "INSERT INTO texts (key, value) VALUES (?, ?) "
            "ON CONFLICT(key) DO UPDATE SET value = excluded.value",
            (key, value),
        )
        c.commit()


# ----- Lokatsiya -----
def get_location() -> tuple[float, float]:
    raw = get_text("location")
    try:
        lat, lon = raw.split(",")
        return float(lat), float(lon)
    except Exception:
        return LATITUDE, LONGITUDE


def set_location(lat: float, lon: float):
    set_text("location", f"{lat},{lon}")
