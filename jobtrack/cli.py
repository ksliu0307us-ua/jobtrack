import argparse
import sys
from datetime import date

from . import db


def fmt_row(r):
    follow = f"  follow-up {r['follow_up']}" if r["follow_up"] else ""
    return f"#{r['id']:<3} {r['status']:<10} {r['company']} - {r['role']}  (applied {r['applied_on']}){follow}"


def cmd_add(conn, args):
    app_id = db.add(conn, args.company, args.role, args.date, args.follow_up, args.url)
    print(f"added #{app_id}: {args.company} - {args.role}")


def cmd_list(conn, args):
    rows = db.list_all(conn, args.status)
    if not rows:
        print("nothing here yet. try: jobtrack add <company> <role>")
        return
    for r in rows:
        print(fmt_row(r))


def cmd_show(conn, args):
    r = db.get(conn, args.id)
    print(fmt_row(r))
    if r["url"]:
        print(f"  {r['url']}")
    if r["notes"]:
        print()
        print(r["notes"])


def cmd_status(conn, args):
    db.set_status(conn, args.id, args.status)
    print(f"#{args.id} -> {args.status}")


def cmd_note(conn, args):
    db.add_note(conn, args.id, " ".join(args.text))
    print(f"note added to #{args.id}")


def cmd_followup(conn, args):
    db.set_follow_up(conn, args.id, args.date)
    print(f"#{args.id} follow-up set to {args.date}")


def cmd_due(conn, args):
    rows = db.due(conn)
    if not rows:
        print("nothing due. nice.")
        return
    today = date.today().isoformat()
    for r in rows:
        late = " (overdue)" if r["follow_up"] < today else ""
        print(f"{fmt_row(r)}{late}")


def cmd_stats(conn, args):
    c = db.counts(conn)
    total = sum(c.values())
    if not total:
        print("no applications yet")
        return
    print(f"total: {total}")
    for s in db.STATUSES:
        if s in c:
            print(f"  {s:<10} {c[s]}")


def build_parser():
    p = argparse.ArgumentParser(prog="jobtrack", description="keep track of job applications")
    p.add_argument("--db", default=None, help="path to the sqlite file (default: ~/.jobtrack.db)")
    sub = p.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("add", help="log a new application")
    a.add_argument("company")
    a.add_argument("role")
    a.add_argument("--date", help="YYYY-MM-DD, defaults to today")
    a.add_argument("--follow-up", dest="follow_up", help="YYYY-MM-DD to check back")
    a.add_argument("--url")
    a.set_defaults(fn=cmd_add)

    l = sub.add_parser("list", help="list applications")
    l.add_argument("--status", choices=db.STATUSES)
    l.set_defaults(fn=cmd_list)

    s = sub.add_parser("show", help="details and notes for one application")
    s.add_argument("id", type=int)
    s.set_defaults(fn=cmd_show)

    st = sub.add_parser("status", help="change status")
    st.add_argument("id", type=int)
    st.add_argument("status", choices=db.STATUSES)
    st.set_defaults(fn=cmd_status)

    n = sub.add_parser("note", help="append a dated note")
    n.add_argument("id", type=int)
    n.add_argument("text", nargs="+")
    n.set_defaults(fn=cmd_note)

    f = sub.add_parser("followup", help="set or change the follow-up date")
    f.add_argument("id", type=int)
    f.add_argument("date", help="YYYY-MM-DD")
    f.set_defaults(fn=cmd_followup)

    d = sub.add_parser("due", help="what needs a follow-up today")
    d.set_defaults(fn=cmd_due)

    x = sub.add_parser("stats", help="count by status")
    x.set_defaults(fn=cmd_stats)

    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    conn = db.connect(args.db) if args.db else db.connect()
    try:
        args.fn(conn, args)
    except (KeyError, ValueError) as e:
        msg = e.args[0] if e.args else str(e)
        print(f"error: {msg}", file=sys.stderr)
        return 1
    finally:
        conn.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
