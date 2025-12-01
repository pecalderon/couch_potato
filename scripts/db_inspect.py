#!/usr/bin/env python3
"""
Print unique titles and counts from the SQLite DB (couch_potato.db).
Usage: python3 scripts/db_inspect.py
"""
import sqlite3
import os

DB = os.getenv('SQLITE_DB_PATH', 'couch_potato.db')

if not os.path.exists(DB):
    print(f"Database '{DB}' not found. Run the app to create it first.")
    raise SystemExit(1)

conn = sqlite3.connect(DB)
cur = conn.cursor()
cur.execute("SELECT title, COUNT(*) as cnt, MIN(id) as sample_id FROM watch_items GROUP BY title ORDER BY cnt DESC, title ASC")
rows = cur.fetchall()
print('Unique titles (title, count, sample_id):')
for r in rows:
    print(r)
conn.close()
