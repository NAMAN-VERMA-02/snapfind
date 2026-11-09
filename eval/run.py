"""Run the eval: index eval/images, run every query in eval/cases.jsonl in three modes.

    python eval/run.py                         # synthetic set -> eval/results.json
    python eval/run.py --base-db real.db --out eval/results_scale.json
        # scale test: the same queries, with an already-built index of other screenshots as
        # distractors. Only target ranks are recorded, never paths or text from that index.

Top-k hit rate = share of queries whose target image is in the first k results.
"""

import argparse
import json
import math
import os
import platform
import shutil
import statistics
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT))
from snapfind import __version__, db, embed, indexer, ocr, search  # noqa: E402

MODES = ("keyword", "semantic", "hybrid")


def wilson(hits: int, n: int, z: float = 1.96) -> tuple[float, float]:
    if not n:
        return (0.0, 0.0)
    p = hits / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (round(c - h, 3), round(c + h, 3))


def cpu_name() -> str:
    if sys.platform == "win32":
        import winreg

        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                            r"HARDWARE\DESCRIPTION\System\CentralProcessor\0") as k:
            return winreg.QueryValueEx(k, "ProcessorNameString")[0].strip()
    try:
        for line in open("/proc/cpuinfo", encoding="utf-8"):
            if line.startswith("model name"):
                return line.split(":", 1)[1].strip()
    except OSError:
        pass
    return platform.processor() or platform.machine()


def git_commit() -> str:
    try:
        return subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, capture_output=True,
                              text=True).stdout.strip()
    except OSError:
        return ""


def summarize(rows: list[dict], pred) -> dict:
    sel = [r for r in rows if pred(r)]
    out = {"n": len(sel)}
    for m in MODES:
        top1 = sum(1 for r in sel if r[m] == 1)
        top3 = sum(1 for r in sel if r[m] and r[m] <= 3)
        out[m] = {"top1": top1, "top3": top3, "top3_ci95": wilson(top3, len(sel))}
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=str(HERE / "_work" / "eval.db"))
    ap.add_argument("--base-db", help="copy this index first and add the eval images to it")
    ap.add_argument("--out", default=str(HERE / "results.json"))
    args = ap.parse_args()

    dbp = Path(args.db)
    dbp.parent.mkdir(parents=True, exist_ok=True)
    for suffix in ("", "-wal", "-shm"):
        Path(f"{dbp}{suffix}").unlink(missing_ok=True)
    if args.base_db:
        shutil.copy(args.base_db, dbp)
    con = db.connect(dbp)
    base_count = con.execute("SELECT count(*) FROM images").fetchone()[0]

    t = time.perf_counter()
    ocr._get()
    embed._load()
    load_s = time.perf_counter() - t

    images = HERE / "images"
    def timed_update():  # wall time including the folder scan, not just the OCR loop
        t = time.perf_counter()
        r = indexer.update(con, [images])
        return r, time.perf_counter() - t

    first, first_s = timed_update()
    again, again_s = timed_update()  # nothing changed: shows what the cache saves
    total = con.execute("SELECT count(*) FROM images").fetchone()[0]

    cases = [json.loads(line) for line in (HERE / "cases.jsonl").read_text("utf-8").splitlines()
             if line.strip()]
    rows, latencies = [], []
    for c in cases:
        target = str(images / c["file"])
        row = {"id": c["id"], "query": c["query"], "kind": c["kind"], "hard": c.get("hard")}
        for m in MODES:
            t = time.perf_counter()
            hits = search.search(con, c["query"], n=10, mode=m)
            if m == "hybrid":
                latencies.append((time.perf_counter() - t) * 1000)
            paths = [h["path"] for h in hits]
            row[m] = paths.index(target) + 1 if target in paths else None
        rows.append(row)

    def hit3(r, m):
        return bool(r[m] and r[m] <= 3)

    result = {
        "date": time.strftime("%Y-%m-%d"),
        "snapfind": __version__, "commit": git_commit(),
        "cpu": cpu_name(), "threads": os.cpu_count(), "python": platform.python_version(),
        "os": platform.platform(terse=True),
        "corpus": {"eval_images": first["indexed"], "distractor_images": base_count,
                   "total_indexed": total},
        "speed": {"model_load_s": round(load_s, 2),
                  "first_index_s": round(first_s, 2),
                  "images_per_s": round(first["indexed"] / first_s, 3),
                  "cached_reindex_ms": round(again_s * 1000, 1),
                  "search_ms_p50": round(statistics.median(latencies), 1)},
        "buckets": {
            "all": summarize(rows, lambda r: True),
            "exact": summarize(rows, lambda r: r["kind"] == "exact"),
            "paraphrase": summarize(rows, lambda r: r["kind"] == "paraphrase"),
            "hard_images": summarize(rows, lambda r: bool(r["hard"])),
        },
        "hybrid_vs_keyword_top3": {
            "fixed": sum(1 for r in rows if hit3(r, "hybrid") and not hit3(r, "keyword")),
            "broken": sum(1 for r in rows if hit3(r, "keyword") and not hit3(r, "hybrid"))},
        "queries": rows,
    }
    Path(args.out).write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", "utf-8")

    print(f"{result['cpu']}, {result['corpus']}")
    print("| bucket | n | " + " | ".join(f"{m} top-3" for m in MODES) + " |")
    for name, b in result["buckets"].items():
        cells = [f"{b[m]['top3']}/{b['n']}" for m in MODES]
        print(f"| {name} | {b['n']} | " + " | ".join(cells) + " |")
    print(json.dumps(result["speed"]), json.dumps(result["hybrid_vs_keyword_top3"]))


if __name__ == "__main__":
    main()
