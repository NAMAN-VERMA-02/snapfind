"""snapfind command line. `snapfind "train ticket december"` is short for `snapfind search ...`."""

import argparse
import json
import os
import sys
import time
from pathlib import Path

from snapfind import __version__, db

COMMANDS = {"index", "search", "watch", "forget", "reset"}
AUTO_UPDATE_LIMIT = 20  # before a search, OCR at most this many new screenshots


def _progress(i: int, total: int, secs: float) -> None:
    rate = i / secs if secs else 0.0
    eta = (total - i) / rate if rate else 0.0
    print(f"\r  {i}/{total}  {rate:.2f} img/s  ETA {eta / 60:.0f} min ", end="", file=sys.stderr,
          flush=True)
    if i == total:
        print(file=sys.stderr)


def _remember(con, paths: list[str]) -> list[Path]:
    roots = []
    for p in paths:
        root = Path(p).expanduser().resolve()
        if not root.is_dir():
            sys.exit(f"snapfind: not a folder: {p}")
        con.execute("INSERT OR IGNORE INTO folders(path) VALUES (?)", (str(root),))
        roots.append(root)
    con.commit()
    return roots


def cmd_index(con, args) -> int:
    from snapfind import indexer

    _remember(con, args.paths)
    for pat in args.exclude:
        con.execute("INSERT OR IGNORE INTO excludes(pattern) VALUES (?)", (pat,))
    con.commit()
    roots = indexer.folders(con)
    if not roots:
        sys.exit("snapfind: no Screenshots folder found. Pass one: snapfind index <folder>")
    print("Folders:\n  " + "\n  ".join(map(str, roots)), file=sys.stderr)
    r = indexer.update(con, roots, progress=_progress)
    total = con.execute("SELECT count(*) FROM images").fetchone()[0]
    print(f"{r['indexed']} new or changed ({r['ocr']} needed OCR, the rest came from the cache), "
          f"{r['removed']} removed, {total} in the index.", file=sys.stderr)
    return 0


def _highlight(s: str) -> str:
    on, off = ("\x1b[1;33m", "\x1b[0m") if sys.stdout.isatty() else ("[", "]")
    return s.replace("\x02", on).replace("\x03", off)


def cmd_search(con, args) -> int:
    from snapfind import indexer, search

    if not args.no_update:
        r = indexer.update(con, limit=AUTO_UPDATE_LIMIT)
        if r["skipped"]:
            print(f"({r['new']} new screenshots are not indexed yet. Run: snapfind index)",
                  file=sys.stderr)
    t = time.perf_counter()
    hits = search.search(con, " ".join(args.query), n=args.n, mode=args.mode)
    ms = (time.perf_counter() - t) * 1000
    if args.json:
        for h in hits:
            h["snippet"] = h["snippet"].replace("\x02", "").replace("\x03", "")
        print(json.dumps(hits, ensure_ascii=False, indent=2))
        return 0
    if not hits:
        print("No matches.", file=sys.stderr)
        return 1
    for i, h in enumerate(hits, 1):
        extra = f"  (+{len(h['copies'])} copy)" if h["copies"] else ""
        print(f"{i:2}. {h['path']}{extra}\n    {_highlight(h['snippet'])}")
    print(f"({len(hits)} results in {ms:.0f} ms)", file=sys.stderr)
    return 0


def cmd_watch(con, args) -> int:
    from snapfind import indexer

    _remember(con, args.paths)
    print(f"Watching {len(indexer.folders(con))} folder(s), every {args.every}s. Ctrl+C stops.",
          file=sys.stderr)
    try:
        while True:
            r = indexer.update(con, progress=_progress)
            if r["indexed"] or r["removed"]:
                print(f"{time.strftime('%H:%M:%S')}  +{r['indexed']} -{r['removed']}",
                      file=sys.stderr)
            time.sleep(args.every)
    except KeyboardInterrupt:
        return 0


def cmd_forget(con, args) -> int:
    target = str(Path(args.path).expanduser().resolve())
    rows = [p for (p,) in con.execute("SELECT path FROM images")
            if p == target or p.startswith(os.path.join(target, ""))]
    db.delete(con, rows)
    con.execute("DELETE FROM folders WHERE path=?", (target,))
    for pat in (target, os.path.join(target, "*")):
        con.execute("INSERT OR IGNORE INTO excludes(pattern) VALUES (?)", (pat,))
    con.commit()
    print(f"Removed {len(rows)} image(s) from the index; {target} will be skipped from now on.",
          file=sys.stderr)
    return 0


def cmd_reset(con, args) -> int:
    path = db.default_path() if args.db is None else Path(args.db)
    if not args.yes and input(f"Delete the whole index at {path}? [y/N] ").strip().lower() != "y":
        return 1
    con.close()
    for suffix in ("", "-wal", "-shm"):
        Path(f"{path}{suffix}").unlink(missing_ok=True)
    print("Index deleted.", file=sys.stderr)
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="snapfind",
                                description="Search your screenshots by the text in them, offline.")
    p.add_argument("--version", action="version", version=f"snapfind {__version__}")
    p.add_argument("--db", help="index file (default: %%LOCALAPPDATA%%\\snapfind\\index.db)")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("index", help="OCR new screenshots into the index")
    s.add_argument("paths", nargs="*", help="extra folders to index and remember")
    s.add_argument("--exclude", action="append", default=[], metavar="GLOB",
                   help="skip paths matching this pattern (remembered)")
    s.set_defaults(fn=cmd_index)

    s = sub.add_parser("search", help="search the index (the default command)")
    s.add_argument("query", nargs="+")
    s.add_argument("-n", type=int, default=10, help="number of results")
    s.add_argument("--mode", choices=["hybrid", "keyword", "semantic"], default="hybrid")
    s.add_argument("--json", action="store_true")
    s.add_argument("--no-update", action="store_true", help="don't index new screenshots first")
    s.set_defaults(fn=cmd_search)

    s = sub.add_parser("watch", help="keep indexing new screenshots")
    s.add_argument("paths", nargs="*")
    s.add_argument("--every", type=float, default=5.0, help="seconds between scans")
    s.set_defaults(fn=cmd_watch)

    s = sub.add_parser("forget", help="remove a file or folder from the index and skip it")
    s.add_argument("path")
    s.set_defaults(fn=cmd_forget)

    s = sub.add_parser("reset", help="delete the whole index")
    s.add_argument("--yes", action="store_true")
    s.set_defaults(fn=cmd_reset)
    return p


def default_to_search(argv: list[str]) -> list[str]:
    """`snapfind train ticket` -> `snapfind search train ticket`."""
    argv, i = list(argv), 0
    while i < len(argv) and argv[i].startswith("-"):  # skip global options and --db's value
        i += 2 if argv[i] == "--db" else 1
    if i < len(argv) and argv[i] not in COMMANDS:
        argv.insert(i, "search")
    return argv


def main(argv: list[str] | None = None) -> int:
    # Windows consoles default to cp1252; OCR text would crash print() without this.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    args = build_parser().parse_args(default_to_search(sys.argv[1:] if argv is None else argv))
    con = db.connect(args.db)
    try:
        return args.fn(con, args)
    finally:
        try:
            con.close()
        except Exception:
            pass
