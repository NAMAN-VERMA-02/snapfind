"""Indexing and search must work with no network at all.

A fresh Python process makes every socket call raise before snapfind (or RapidOCR, onnxruntime,
tokenizers) is even imported, then OCRs real images and searches them. In CI the same test also
runs inside a Linux network namespace with no interfaces (SNAPFIND_EXPECT_NO_NET=1), which
catches native code that would bypass Python's socket module.
"""

import os
import subprocess
import sys
import textwrap

from tests.conftest import make_shot

SCRIPT = textwrap.dedent(r"""
    import os, socket, sys

    if os.environ.get("SNAPFIND_EXPECT_NO_NET"):
        # Sanity check that the sandbox is real: an unpatched connect must fail.
        try:
            socket.create_connection(("1.1.1.1", 443), timeout=3).close()
            sys.exit("sandbox has network access")
        except OSError:
            pass

    def blocked(*a, **k):
        raise OSError("network access attempted: " + repr(a[:2]))

    socket.socket.connect = socket.socket.connect_ex = blocked
    socket.create_connection = socket.getaddrinfo = blocked

    from snapfind import db, indexer, search

    con = db.connect(sys.argv[1])
    r = indexer.update(con, [sys.argv[2]])
    assert r["ocr"] == 3, r
    for q, want in [("train ticket december", "ticket.png"),
                    ("EADDRINUSE", "error.png"),
                    ("someone inviting me to dinner", "chat.png")]:
        top = search.search(con, q)[0]["path"]
        assert top.endswith(want), (q, top)
    print("OFFLINE OK")
""")


def test_index_and_search_with_network_blocked(tmp_path):
    shots = tmp_path / "shots"
    shots.mkdir()
    make_shot(shots / "ticket.png", ["RailBook E-Ticket", "Train 12952 Rajdhani Express",
                                     "Date of Journey: 14/12/2026", "Coach B2 Berth 34"])
    make_shot(shots / "error.png", ["$ npm run dev", "Error: listen EADDRINUSE: address",
                                    "already in use :::3000"])
    make_shot(shots / "chat.png", ["Riya", "Are you free for dinner on Friday?",
                                   "Let's try the new place near the station"])
    env = {**os.environ, "HF_HUB_OFFLINE": "1"}
    out = subprocess.run([sys.executable, "-c", SCRIPT, str(tmp_path / "i.db"), str(shots)],
                         capture_output=True, text=True, env=env, timeout=900)
    assert out.returncode == 0, out.stdout + out.stderr
    assert "OFFLINE OK" in out.stdout
