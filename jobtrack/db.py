import sqlite3
from datetime import date
from pathlib import Path

DEFAULT_DB = Path.home() / ".jobtrack.db"

STATUSES = ["applied", "screening", "interview", "offer", "rejected", "withdrawn"]

# statuses where there's nothing left to follow up on
CLOSED = ("offer", "rejected", "withdrawn")

SCHEMA = """
CREATE TABLE IF NOT EXISTS applications (
    id         INTEGER PRIMARY KEY,
    company    TEXT NOT NULL,
    role       TEXT NOT NULL,
    status     TEXT NOT NULL DEFAULT 'applied',
    applied_on TEXT NOT NULL,
    follow_up  TEXT,
    url        TEXT,
    notes      TEXT NOT NULL DEFAULT ''
);
"""


def connect(path=DEFAULT_DB):
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA)
    return conn


def add(conn, company, role, applied_on=None, follow_up=None, url=None):
    applied_on = applied_on or date.today().isoformat()
    cur = conn.execute(
        "INSERT INTO applications (company, role, applied_on, follow_up, url)"
        " VALUES (?, ?, ?, ?, ?)",
        (company, role, applied_on, follow_up, url),
    )
    conn.commit()
    return cur.lastrowid


def get(conn, app_id):
    row = conn.execute("SELECT * FROM applications WHERE id = ?", (app_id,)).fetchone()
    if row is None:
        raise KeyError(f"no application with id {app_id}")
    return row


def list_all(conn, status=None):
    if status:
        q = "SELECT * FROM applications WHERE status = ? ORDER BY applied_on DESC, id DESC"
        return conn.execute(q, (status,)).fetchall()
    q = "SELECT * FROM applications ORDER BY applied_on DESC, id DESC"
    return conn.execute(q).fetchall()


def set_status(conn, app_id, status):
    if status not in STATUSES:
        raise ValueError(f"unknown status '{status}' (try one of: {', '.join(STATUSES)})")
    get(conn, app_id)  # raises if missing
    conn.execute("UPDATE applications SET status = ? WHERE id = ?", (status, app_id))
    conn.commit()


def set_follow_up(conn, app_id, when):
    get(conn, app_id)
    conn.execute("UPDATE applications SET follow_up = ? WHERE id = ?", (when, app_id))
    conn.commit()


def add_note(conn, app_id, text):
    row = get(conn, app_id)
    stamp = date.today().isoformat()
    existing = row["notes"]
    notes = f"{existing}\n[{stamp}] {text}" if existing else f"[{stamp}] {text}"
    conn.execute("UPDATE applications SET notes = ? WHERE id = ?", (notes, app_id))
    conn.commit()


def due(conn, on=None):
    """Applications with a follow-up date on or before `on` that are still open."""
    on = on or date.today().isoformat()
    placeholders = ", ".join("?" for _ in CLOSED)
    q = (
        "SELECT * FROM applications"
        " WHERE follow_up IS NOT NULL AND follow_up <= ?"
        f" AND status NOT IN ({placeholders})"
        " ORDER BY follow_up, id"
    )
    return conn.execute(q, (on, *CLOSED)).fetchall()


def counts(conn):
    rows = conn.execute(
        "SELECT status, COUNT(*) AS n FROM applications GROUP BY status"
    ).fetchall()
    return {r["status"]: r["n"] for r in rows}
