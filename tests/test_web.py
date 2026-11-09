import json
import threading
import urllib.error
import urllib.request

import pytest

from snapfind import db, embed, indexer, web


@pytest.fixture
def server(tmp_path, monkeypatch):
    monkeypatch.setattr(indexer, "default_folders", lambda: [])  # never scan the real folder
    img = tmp_path / "shot.png"
    img.write_bytes(b"\x89PNG fake")
    con = db.connect(tmp_path / "i.db")
    text = "Payment successful Rs 1,499 to Riya"
    db.put(con, str(img), 1.0, 1, "s", embed.embed([text]).tobytes(), text, "")
    con.commit()
    srv = web.make_server(con, 0)  # port 0: any free port
    port = srv.server_address[1]
    srv.RequestHandlerClass = web.make_handler(con, port)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    yield port
    srv.shutdown()
    srv.server_close()
    con.close()


def get(port, path, host=None):
    req = urllib.request.Request(f"http://127.0.0.1:{port}{path}")
    req.add_header("Host", host or f"127.0.0.1:{port}")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()


def test_page_and_search(server):
    status, body = get(server, "/")
    assert status == 200 and b"snapfind" in body
    status, body = get(server, "/api/search?q=riya+payment&mode=keyword")
    hits = json.loads(body)
    assert status == 200 and hits[0]["path"].endswith("shot.png")


def test_images_only_by_indexed_id(server):
    assert get(server, "/img?id=1") == (200, b"\x89PNG fake")
    assert get(server, "/img?id=999")[0] == 404
    assert get(server, "/img?id=../../etc/passwd")[0] == 404
    assert get(server, "/img?path=C:/Windows/win.ini")[0] == 404


def test_other_hostnames_are_refused(server):
    # A DNS-rebinding page would arrive with its own hostname in the Host header.
    assert get(server, "/api/search?q=riya", host=f"evil.example:{server}")[0] == 403
