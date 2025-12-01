import os
import sqlite3
from typing import List, Dict, Optional
from domain.ports import Repository
from domain.models import WatchItem, TitleMetadata


DB_PATH = os.getenv('SQLITE_DB_PATH', 'couch_potato.db')


def _conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def _ensure_schema():
    with _conn() as conn:
        cur = conn.cursor()
        cur.execute('''
        CREATE TABLE IF NOT EXISTS watch_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'to_watch',
            note TEXT,
            year TEXT,
            runtime TEXT,
            poster_url TEXT,
            plot TEXT,
            imdb_rating REAL
        )
        ''')
        conn.commit()


class SQLiteRepository(Repository):
    def __init__(self):
        _ensure_schema()

    def save(self, item: WatchItem, meta: TitleMetadata) -> int:
        with _conn() as conn:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO watch_items (title, status, note, year, runtime, poster_url, plot, imdb_rating) VALUES (?,?,?,?,?,?,?,?)",
                (item.title, item.status, item.note, item.year, item.runtime, item.poster_url, item.plot, item.imdb_rating)
            )
            conn.commit()
            return cur.lastrowid

    def find(self, q: str) -> List[WatchItem]:
        with _conn() as conn:
            cur = conn.cursor()
            cur.execute(
                "SELECT id, title, status, note, year, runtime, poster_url, plot, imdb_rating FROM watch_items WHERE title LIKE ? ORDER BY id DESC",
                (f"%{q}%",)
            )
            rows = cur.fetchall()
        return [WatchItem(**dict(r)) for r in rows]

    def update_status(self, item_id: int, status: str) -> None:
        with _conn() as conn:
            cur = conn.cursor()
            cur.execute("UPDATE watch_items SET status=? WHERE id=?", (status, item_id))
            conn.commit()

    def remove(self, item_id: int) -> None:
        with _conn() as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM watch_items WHERE id=?", (item_id,))
            conn.commit()

    def summary(self) -> Dict[str, float]:
        with _conn() as conn:
            cur = conn.cursor()
            cur.execute("SELECT status, COUNT(*) c FROM watch_items GROUP BY status")
            counts = {r[0]: r[1] for r in cur.fetchall()}
            cur.execute("SELECT AVG(imdb_rating) FROM watch_items WHERE status='finished' AND imdb_rating IS NOT NULL")
            avg = cur.fetchone()[0]
        return {**{k: counts.get(k, 0) for k in ('to_watch', 'watching', 'finished')}, 'avg_rating_finished': float(avg) if avg is not None else None}
