# Couch Potato
Lightweight movie & series tracker (save titles, mark status, enrich with OMDb: year/poster/plot/runtime/rating).

## Quick start (macOS)
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
mysql -h  -P  -u  -p  < schema.sql
python -m cli.main add "Inception"
python -m cli.main search "incep"
python -m cli.main status 1 finished
python -m cli.main summary
