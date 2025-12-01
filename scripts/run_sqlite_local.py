"""Run full app locally using SQLite (no Docker) and real OMDb API.
Usage: PYTHONPATH=. python3 scripts/run_sqlite_local.py
Requires: `OMDB_API_KEY` set in `.env` file in repo root.
"""
import os
from dotenv import load_dotenv
from infra.db.sqlite_repository import SQLiteRepository
from infra.web.provider_factory import get_provider
from services.app_service import AppService


def main():
    load_dotenv('.env')
    repo = SQLiteRepository()
    provider = get_provider()
    svc = AppService(repo=repo, provider=provider)

    title = os.getenv('OMDB_TITLE', 'Guardians of the Galaxy Vol. 2')
    print('Adding title:', title)
    new_id = svc.add_title(title)
    print('Added id=', new_id)

    print('\nSearch results for "guardians":')
    rows = svc.search('guardians')
    for r in rows:
        print(r)

    print('\nUpdating status of id 1 to finished')
    svc.update_status(1, 'finished')

    print('\nSummary:')
    print(svc.summary())


if __name__ == '__main__':
    main()
