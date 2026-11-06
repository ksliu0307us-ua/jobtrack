# Roadmap

Rough order of what I want to do next. Nothing here is set in stone.

## Soon

- [ ] `edit` command to fix a typo in company/role/url without deleting and re-adding
- [ ] `delete` command (with a confirmation prompt)
- [ ] `--json` flag on `list` and `show` so output can be piped to `jq` or scripts
- [ ] Validate dates on input (`--date`, `--follow-up`) and give a clear error instead of storing junk
- [ ] Mark the current status change with a timestamp so I can see how long each stage took

## Next

- [ ] Status history table (every transition with a date) instead of one `status` column
- [ ] `export` to CSV, and `import` from CSV for people coming from a spreadsheet
- [ ] Tags / labels (e.g. `remote`, `referral`, `dream-job`) and `list --tag`
- [ ] `stats` improvements: response rate, average days from applied to first reply, applications per week
- [ ] Config file for defaults (default follow-up interval, db location)
- [ ] Colour in the terminal output when stdout is a TTY, off when piped

## Later / maybe

- [ ] Interactive TUI mode (`jobtrack ui`) using `curses` or `textual`
- [ ] Reminders: a `jobtrack due` summary that can run from cron and print or notify
- [ ] Attach files to an application (the resume version you sent, the job post as PDF)
- [ ] Publish to PyPI
- [ ] Shell completion for bash/zsh

## Housekeeping

- [ ] Tests for the CLI layer, not just `db.py`
- [ ] GitHub Actions workflow running `pytest` on push
- [ ] Type hints throughout and a `mypy` pass
- [ ] CHANGELOG.md once there's a 0.2.0
