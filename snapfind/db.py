"""The index: one SQLite file with FTS5 for text and a float32 blob of chunk vectors per image."""

import os
import sqlite3
from pathlib import Path

SCHEMA = """
CREATE TABLE IF NOT EXISTS images(
    id INTEGER PRIMARY KEY,
    path TEXT UNIQUE NOT NULL,
    mtime REAL NOT NULL,
    size INTEGER NOT NULL,
    sha1 TEXT NOT NULL,
    emb BLOB                       -- float32 (n_chunks, 384), NULL when the image has no text
);
CREATE INDEX IF NOT EXISTS images_sha1 ON images(sha1);
-- rowid = images.id; dates = month words for the capture date and dates found in the text
CREATE VIRTUAL TABLE IF NOT EXISTS fts USING fts5(
    text, dates, tokenize='porter unicode61 remove_diacritics 2'
);
CREATE TABLE IF NOT EXISTS folders(path TEXT PRIMARY KEY);
CREATE TABLE IF NOT EXISTS excludes(pattern TEXT PRIMARY KEY);
"""


def default_path() -> Path:
    if p := os.environ.get("SNAPFIND_DB"):
        return Path(p)
    base = os.environ.get("LOCALAPPDATA") or os.path.expanduser("~/.local/share")
    return Path(base) / "snapfind" / "index.db"


def connect(path: str | os.PathLike | None = None) -> sqlite3.Connection:
    path = Path(path or default_path())
    path.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(path, check_same_thread=False)
    con.execute("PRAGMA journal_mode=WAL")  # search while `watch` or `index` is writing
    con.executescript(SCHEMA)
    return con


def put(con, path: str, mtime: float, size: int, sha1: str, emb: bytes | None,
        text: str, dates: str) -> None:
    con.execute(
        "INSERT INTO images(path, mtime, size, sha1, emb) VALUES (?,?,?,?,?) "
        "ON CONFLICT(path) DO UPDATE SET mtime=excluded.mtime, size=excluded.size, "
        "sha1=excluded.sha1, emb=excluded.emb",
        (path, mtime, size, sha1, emb),
    )
    (rid,) = con.execute("SELECT id FROM images WHERE path=?", (path,)).fetchone()
    con.execute("DELETE FROM fts WHERE rowid=?", (rid,))
    con.execute("INSERT INTO fts(rowid, text, dates) VALUES (?,?,?)", (rid, text, dates))


def delete(con, paths) -> None:
    for p in paths:
        row = con.execute("SELECT id FROM images WHERE path=?", (p,)).fetchone()
        if row:
            con.execute("DELETE FROM fts WHERE rowid=?", row)
            con.execute("DELETE FROM images WHERE id=?", row)
