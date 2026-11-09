"""Ranking: FTS5 BM25 for words, MiniLM cosine for meaning, fused with Reciprocal Rank Fusion."""

import re
from functools import lru_cache

import numpy as np

from snapfind.dates import expand_terms

POOL = 50  # candidates taken from each ranker before fusing
RRF_K = 60  # the standard RRF constant; fixed, never tuned on the eval set
HL = ("\x02", "\x03")  # highlight markers in snippets; the CLI and web UI turn them into styling


def fts_query(q: str) -> str:
    """Any user text -> a safe FTS5 query: every word quoted, joined with OR."""
    terms = expand_terms(re.findall(r"\w+", q.lower()))
    return " OR ".join(f'"{t}"' for t in terms)


def keyword(con, q: str, k: int = POOL) -> list[int]:
    match = fts_query(q)
    if not match:
        return []
    rows = con.execute("SELECT rowid FROM fts WHERE fts MATCH ? "
                       "ORDER BY bm25(fts, 1.0, 0.5) LIMIT ?", (match, k))
    return [r for (r,) in rows]


_vectors: dict = {}


def _matrix(con):
    """All chunk vectors, cached in memory until the database changes."""
    key = (id(con), con.execute("PRAGMA data_version").fetchone()[0], con.total_changes)
    if _vectors.get("key") != key:
        ids, starts, blocks, n = [], [], [], 0
        rows = con.execute("SELECT id, emb FROM images WHERE emb IS NOT NULL ORDER BY id")
        for rid, blob in rows:
            m = np.frombuffer(blob, dtype=np.float32).reshape(-1, 384)
            ids.append(rid)
            starts.append(n)
            blocks.append(m)
            n += len(m)
        mat = np.vstack(blocks) if blocks else np.zeros((0, 384), np.float32)
        _vectors.update(key=key, ids=np.array(ids), starts=np.array(starts, dtype=np.int64),
                        mat=mat)
    return _vectors["ids"], _vectors["starts"], _vectors["mat"]


@lru_cache(maxsize=256)
def _query_vector(q: str) -> np.ndarray:
    from snapfind.embed import embed

    return embed([q])[0]


def semantic(con, q: str, k: int = POOL) -> list[tuple[int, int]]:
    """[(image id, index of its best chunk)], best first."""
    ids, starts, mat = _matrix(con)
    if not q.strip() or not len(ids):
        return []
    scores = mat @ _query_vector(q)
    best = np.maximum.reduceat(scores, starts)
    order = np.argsort(-best)[:k]
    ends = np.append(starts[1:], len(scores))
    return [(int(ids[i]), int(np.argmax(scores[starts[i]:ends[i]]))) for i in order]


def rrf(*rankings: list[int], k: int = RRF_K) -> list[int]:
    score: dict[int, float] = {}
    for ranking in rankings:
        for rank, rid in enumerate(ranking, 1):
            score[rid] = score.get(rid, 0.0) + 1.0 / (k + rank)
    return sorted(score, key=lambda r: -score[r])  # stable: ties keep first-ranker order


def search(con, q: str, n: int = 10, mode: str = "hybrid") -> list[dict]:
    kw = keyword(con, q) if mode in ("hybrid", "keyword") else []
    sem = semantic(con, q) if mode in ("hybrid", "semantic") else []
    best_chunk = dict(sem)
    ranked = rrf(kw, [r for r, _ in sem]) if mode == "hybrid" else kw or [r for r, _ in sem]
    kw_hits = set(kw)

    results, seen = [], {}
    for rid in ranked:
        path, sha1 = con.execute("SELECT path, sha1 FROM images WHERE id=?", (rid,)).fetchone()
        if sha1 in seen:  # same screenshot in two folders: one result, "+1 copy"
            seen[sha1]["copies"].append(path)
            continue
        hit = {"id": rid, "path": path, "copies": [],
               "snippet": _snippet(con, rid, q, rid in kw_hits, best_chunk.get(rid))}
        seen[sha1] = hit
        results.append(hit)
        if len(results) == n:
            break
    return results


def _snippet(con, rid: int, q: str, is_kw: bool, chunk: int | None) -> str:
    if is_kw:
        (s,) = con.execute("SELECT snippet(fts, 0, ?, ?, '…', 14) FROM fts "
                           "WHERE fts MATCH ? AND rowid = ?", (*HL, fts_query(q), rid)).fetchone()
        if s.strip():
            return " ".join(s.split())
    (text,) = con.execute("SELECT text FROM fts WHERE rowid=?", (rid,)).fetchone()
    from snapfind.embed import chunks

    parts = chunks(text)
    part = parts[chunk] if chunk is not None and chunk < len(parts) else " ".join(text.split())
    return part[:160] + ("…" if len(part) > 160 else "")
