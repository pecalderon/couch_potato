Run locally (SQLite)

If you don't want to run MySQL or Docker you can use the included SQLite backend for quick local testing. Create a virtualenv, install deps, add your `OMDB_API_KEY` to a local `.env` (do NOT commit it), then run the helper runner:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
# add your OMDb key to .env (example in .env.example)
PYTHONPATH=. python3 scripts/run_sqlite_local.py
```

This runs an end-to-end flow: add/search/status/summary using `couch_potato.db` in the project root.
