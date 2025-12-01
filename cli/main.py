import argparse
from infra.db.mysql_repository import MySQLRepository
from infra.web.provider_factory import get_provider
from services.app_service import AppService
def build_service():
    return AppService(repo=MySQLRepository(), provider=get_provider())
def cmd_add(args):
    svc = build_service(); new_id = svc.add_title(args.title); print(f"Added: id={new_id}")
def cmd_search(args):
    svc = build_service(); rows = svc.search(args.q)
    for r in rows: print(vars(r))
def cmd_status(args):
    svc = build_service(); svc.update_status(args.id, args.status); print("OK")
def cmd_remove(args):
    svc = build_service(); svc.remove(args.id); print("OK")
def cmd_summary(args):
    svc = build_service(); print(svc.summary())
def main():
    p = argparse.ArgumentParser(prog='couch_potato', description='Couch Potato CLI')
    sub = p.add_subparsers(dest='cmd', required=True)
    a = sub.add_parser('add'); a.add_argument('title'); a.set_defaults(func=cmd_add)
    s = sub.add_parser('search'); s.add_argument('q'); s.set_defaults(func=cmd_search)
    u = sub.add_parser('status'); u.add_argument('id', type=int); u.add_argument('status', choices=['to_watch','watching','finished']); u.set_defaults(func=cmd_status)
    r = sub.add_parser('remove'); r.add_argument('id', type=int); r.set_defaults(func=cmd_remove)
    m = sub.add_parser('summary'); m.set_defaults(func=cmd_summary)
    args = p.parse_args(); args.func(args)
if __name__ == '__main__':
    main()
