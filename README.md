# jobtrack

A small command-line tool for keeping track of job applications. I got tired of
the spreadsheet, so this lives in the terminal instead: log an application,
move it through the stages, jot down notes after calls, and ask "what do I
need to follow up on today?"

Everything is stored in a single SQLite file in your home directory
(`~/.jobtrack.db`). No accounts, no sync, nothing leaves your machine.

## Who it's for

Me, mostly. But anyone who's job hunting and prefers the terminal to a
spreadsheet should find it useful.

## Built with

- Python 3.9+
- Standard library only (`argparse`, `sqlite3`). No dependencies to install.
- `pytest` for the tests.

## Install

```sh
git clone https://github.com/kslu0307us-ua/jobtrack.git
cd jobtrack
pip install -e .
```

That gives you a `jobtrack` command. If you'd rather not install anything,
`python -m jobtrack.cli` works the same from the repo folder.

## Usage

```sh
# log an application (date defaults to today)
jobtrack add "Acme" "Backend Engineer" --follow-up 2026-11-14 --url https://acme.example/jobs/42

# see everything, newest first
jobtrack list
jobtrack list --status interview

# move it along
jobtrack status 1 screening
jobtrack status 1 interview

# notes get a date stamp and stack up
jobtrack note 1 recruiter call went well, take-home due Friday

# details and notes for one application
jobtrack show 1

# set or change when to check back
jobtrack followup 1 2026-11-20

# what needs attention today (overdue items are marked)
jobtrack due

# counts by status
jobtrack stats
```

Statuses: `applied`, `screening`, `interview`, `offer`, `rejected`, `withdrawn`.

Use `--db path/to/file.db` before the subcommand to point at a different
database, which is handy for testing or keeping separate searches apart.

## Running the tests

```sh
pip install pytest
pytest
```

## Roadmap

See [ROADMAP.md](ROADMAP.md) for what I'm planning next. Issues and PRs welcome.

## License

MIT. See [LICENSE](LICENSE).
