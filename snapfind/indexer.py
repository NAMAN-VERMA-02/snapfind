"""Find screenshots, OCR the new ones (newest first), and keep the index in step with the disk."""

import fnmatch
import hashlib
import os
import sys
import time
from collections.abc import Callable
from pathlib import Path

from snapfind import db, embed, ocr
from snapfind.dates import taken_words, text_date_words

EXTS = {".png", ".jpg", ".jpeg", ".webp", ".bmp"}
# OneDrive "online-only" placeholders: reading one makes OneDrive download it.
CLOUD_ONLY = 0x400000 | 0x40000 | 0x1000  # RECALL_ON_DATA_ACCESS | RECALL_ON_OPEN | OFFLINE
SETTLE_SECONDS = 2  # skip files written in the last 2 s; they may still be half-saved


def default_folders() -> list[Path]:
    """Windows' real Screenshots folder (it can be OneDrive\\Pictures\\Screenshots 1),
    then ~/Pictures/Screenshots."""
    found = []
    if sys.platform == "win32":
        import winreg

        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows"
                                r"\CurrentVersion\Explorer\User Shell Folders") as key:
                value, _ = winreg.QueryValueEx(key, "{B7BEDE81-DF94-4682-A7D8-57A52620B86F}")
                found.append(Path(os.path.expandvars(value)))
        except OSError:
            pass
    found.append(Path.home() / "Pictures" / "Screenshots")
    return [p for p in dict.fromkeys(found) if p.is_dir()]


def folders(con) -> list[Path]:
    saved = [Path(p) for (p,) in con.execute("SELECT path FROM folders")]
    return [p for p in dict.fromkeys(default_folders() + saved) if p.is_dir()]


def excluded(con) -> list[str]:
    return [p for (p,) in con.execute("SELECT pattern FROM excludes")]


def scan(roots: list[Path], excludes: list[str]) -> dict[str, tuple[float, int]]:
    """path -> (mtime, size) for every image under roots that is safe to read now."""
    now = time.time()
    out = {}
    for root in roots:
        for dirpath, _, names in os.walk(root):
            for name in names:
                if os.path.splitext(name)[1].lower() not in EXTS:
                    continue
                path = os.path.join(dirpath, name)
                if any(fnmatch.fnmatch(path, pat) for pat in excludes):
                    continue
                try:
                    st = os.stat(path)
                except OSError:
                    continue
                if getattr(st, "st_file_attributes", 0) & CLOUD_ONLY:
                    continue
                if now - st.st_mtime < SETTLE_SECONDS:
                    continue
                out[path] = (st.st_mtime, st.st_size)
    return out


def pending(con, roots: list[Path]) -> tuple[list[str], list[str], dict]:
    """(new or changed paths, newest first; paths gone from disk; scan result)."""
    found = scan(roots, excluded(con))
    known = {p: (m, s) for p, m, s in con.execute("SELECT path, mtime, size FROM images")}
    todo = sorted((p for p, ms in found.items() if known.get(p) != ms),
                  key=lambda p: found[p][0], reverse=True)
    # Only drop rows under a root we just scanned, so an unplugged drive keeps its index.
    prefixes = tuple(os.path.join(str(r), "") for r in roots)
    gone = [p for p in known if p not in found and p.startswith(prefixes)]
    return todo, gone, found


def _sha1(path: str) -> str:
    h = hashlib.sha1()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def index_file(con, path: str, mtime: float, size: int) -> bool:
    """Index one file. Returns True if it needed OCR, False if the content-hash cache hit."""
    sha1 = _sha1(path)
    hit = con.execute("SELECT f.text, i.emb FROM images i JOIN fts f ON f.rowid = i.id "
                      "WHERE i.sha1 = ? LIMIT 1", (sha1,)).fetchone()
    if hit:
        text, emb = hit
    else:
        text = ocr.read_text(path)
        extra = ocr.split_joined(text)
        text = f"{text}\n{extra}" if extra else text
        parts = embed.chunks(text)
        emb = embed.embed(parts).tobytes() if parts else None
    dates = f"{taken_words(path, mtime)} {text_date_words(text)}".strip()
    db.put(con, path, mtime, size, sha1, emb, text, dates)
    return not hit


def update(con, roots: list[Path] | None = None, limit: int | None = None,
           progress: Callable[[int, int, float], None] | None = None) -> dict:
    """Bring the index in line with the disk. With `limit`, do nothing if more than `limit`
    files are new (used before each search so it never starts a long OCR run by surprise)."""
    roots = folders(con) if roots is None else roots
    todo, gone, found = pending(con, roots)
    if gone:
        db.delete(con, gone)
        con.commit()
    if limit is not None and len(todo) > limit:
        return {"new": len(todo), "indexed": 0, "ocr": 0, "removed": len(gone), "skipped": True}
    t0, n_ocr = time.perf_counter(), 0
    for i, path in enumerate(todo, 1):
        try:
            n_ocr += index_file(con, path, *found[path])
        except Exception as e:  # one unreadable file must not stop the run
            print(f"\nskipped {path}: {e}", file=sys.stderr)
        if i % 10 == 0:
            con.commit()  # resumable: Ctrl+C loses at most 10 images of work
        if progress:
            progress(i, len(todo), time.perf_counter() - t0)
    con.commit()
    return {"new": len(todo), "indexed": len(todo), "ocr": n_ocr, "removed": len(gone),
            "skipped": False, "seconds": time.perf_counter() - t0}
