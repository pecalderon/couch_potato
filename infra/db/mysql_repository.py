import os, pymysql
from typing import List, Dict
from dotenv import load_dotenv
from domain.ports import Repository
from domain.models import WatchItem, TitleMetadata
load_dotenv()
def _conn():
    return pymysql.connect(
        host=os.getenv('MYSQL_HOST', '127.0.0.1'),
        port=int(os.getenv('MYSQL_PORT', '3306')),
        user=os.getenv('MYSQL_USER', 'root'),
        password=os.getenv('MYSQL_PASSWORD', ''),
        database=os.getenv('MYSQL_DB', 'couch_potato'),
        cursorclass=pymysql.cursors.DictCursor)
class MySQLRepository(Repository):
    def save(self, item: WatchItem, meta: TitleMetadata) -> int:
        with _conn() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO watch_items (title, status, note, year, runtime, poster_url, plot, imdb_rating) "
                    "VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
                    (item.title, item.status, item.note, item.year, item.runtime, item.poster_url, item.plot, item.imdb_rating))
                conn.commit(); return cur.lastrowid
    def find(self, q: str) -> List[WatchItem]:
        with _conn() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT id, title, status, note, year, runtime, poster_url, plot, imdb_rating "
                    "FROM watch_items WHERE title LIKE %s ORDER BY id DESC", (f"%{q}%",))
                rows = cur.fetchall()
        return [WatchItem(**r) for r in rows]
    def update_status(self, item_id: int, status: str) -> None:
        with _conn() as conn:
            with conn.cursor() as cur:
                cur.execute("UPDATE watch_items SET status=%s WHERE id=%s", (status, item_id)); conn.commit()
    def remove(self, item_id: int) -> None:
        with _conn() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM watch_items WHERE id=%s", (item_id,)); conn.commit()
    def summary(self) -> Dict[str, float]:
        with _conn() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT status, COUNT(*) c FROM watch_items GROUP BY status")
                counts = {r['status']: r['c'] for r in cur.fetchall()}
                cur.execute("SELECT AVG(imdb_rating) avg FROM watch_items WHERE status='finished' AND imdb_rating IS NOT NULL")
                avg = cur.fetchone()['avg']
        return {**{k: counts.get(k, 0) for k in ('to_watch','watching','finished')},
                'avg_rating_finished': float(avg) if avg is not None else None}
