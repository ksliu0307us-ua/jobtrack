import pytest

from jobtrack import db


@pytest.fixture
def conn(tmp_path):
    c = db.connect(tmp_path / "test.db")
    yield c
    c.close()


def test_add_and_list(conn):
    db.add(conn, "Acme", "Backend Engineer", applied_on="2026-11-01")
    db.add(conn, "Globex", "SWE Intern", applied_on="2026-11-03")
    rows = db.list_all(conn)
    assert [r["company"] for r in rows] == ["Globex", "Acme"]  # newest first


def test_status_change(conn):
    app_id = db.add(conn, "Acme", "Backend Engineer")
    db.set_status(conn, app_id, "interview")
    assert db.get(conn, app_id)["status"] == "interview"


def test_bad_status_rejected(conn):
    app_id = db.add(conn, "Acme", "Backend Engineer")
    with pytest.raises(ValueError):
        db.set_status(conn, app_id, "ghosted")


def test_missing_id(conn):
    with pytest.raises(KeyError):
        db.get(conn, 999)


def test_notes_accumulate(conn):
    app_id = db.add(conn, "Acme", "Backend Engineer")
    db.add_note(conn, app_id, "recruiter call went fine")
    db.add_note(conn, app_id, "sent take-home")
    notes = db.get(conn, app_id)["notes"]
    assert "recruiter call went fine" in notes
    assert "sent take-home" in notes
    assert notes.count("\n") == 1


def test_due_skips_closed(conn):
    a = db.add(conn, "Acme", "SWE", follow_up="2026-01-01")
    b = db.add(conn, "Globex", "SWE", follow_up="2026-01-01")
    db.set_status(conn, b, "rejected")
    ids = [r["id"] for r in db.due(conn, on="2026-06-01")]
    assert ids == [a]


def test_due_respects_date(conn):
    db.add(conn, "Acme", "SWE", follow_up="2026-12-25")
    assert db.due(conn, on="2026-12-01") == []
    assert len(db.due(conn, on="2026-12-25")) == 1


def test_counts(conn):
    db.add(conn, "A", "x")
    db.add(conn, "B", "y")
    c = db.add(conn, "C", "z")
    db.set_status(conn, c, "offer")
    assert db.counts(conn) == {"applied": 2, "offer": 1}
