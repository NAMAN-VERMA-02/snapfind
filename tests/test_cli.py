import json
import os
import subprocess
import sys

from snapfind import cli, db, embed


def run(*args, encoding="utf-8"):
    env = {**os.environ, "PYTHONIOENCODING": encoding}
    return subprocess.run([sys.executable, "-m", "snapfind", *args], capture_output=True,
                          env=env, timeout=300)


def test_bare_query_means_search():
    d = cli.default_to_search
    assert d(["train", "ticket"]) == ["search", "train", "ticket"]
    assert d(["--db", "x.db", "train"]) == ["--db", "x.db", "search", "train"]
    assert d(["index", "D:/phone"]) == ["index", "D:/phone"]
    assert d(["--version"]) == ["--version"]


def test_unicode_ocr_text_prints_on_a_cp1252_console(tmp_path):
    path = tmp_path / "i.db"
    con = db.connect(path)
    text = "Paid ₹1,499 → Riya ✓ 東京"
    db.put(con, "C:/s/upi.png", 1.0, 1, "x", embed.embed([text]).tobytes(), text, "")
    con.commit()
    con.close()
    out = run("--db", str(path), "paid riya", "--no-update", encoding="cp1252")
    assert out.returncode == 0, out.stderr.decode("utf-8", "replace")
    assert "upi.png" in out.stdout.decode("utf-8")


def test_json_output(tmp_path):
    path = tmp_path / "i.db"
    con = db.connect(path)
    db.put(con, "/s/a.png", 1.0, 1, "a", embed.embed(["wifi password"]).tobytes(),
           "wifi password", "")
    con.commit()
    con.close()
    out = run("--db", str(path), "search", "wifi", "--json", "--no-update")
    hits = json.loads(out.stdout)
    assert hits[0]["path"] == "/s/a.png" and "\x02" not in hits[0]["snippet"]
