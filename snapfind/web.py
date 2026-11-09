"""A tiny local web UI. Stdlib only, bound to 127.0.0.1, no external assets (works offline)."""

import json
import mimetypes
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

from snapfind import indexer, search

PAGE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>snapfind</title>
<style>
:root { --bg:#f7f7f5; --fg:#1d1d1f; --muted:#6b6b70; --card:#fff; --line:#e3e3e0; --hl:#ffe58a; }
@media (prefers-color-scheme: dark) {
  :root { --bg:#141416; --fg:#ececef; --muted:#9a9aa2; --card:#1e1e22; --line:#2e2e34; --hl:#6b5a12; }
}
* { box-sizing: border-box; }
body { margin:0; font:15px/1.45 system-ui, "Segoe UI", sans-serif; background:var(--bg); color:var(--fg); }
main { max-width: 1100px; margin: 0 auto; padding: 24px 16px 48px; }
h1 { font-size: 20px; margin: 0 0 12px; letter-spacing: -0.01em; }
h1 span { color: var(--muted); font-weight: 400; font-size: 14px; margin-left: 8px; }
form { display:flex; gap:8px; margin-bottom: 8px; }
input[type=search] { flex:1; font:inherit; font-size:17px; padding:10px 14px; border-radius:10px;
  border:1px solid var(--line); background:var(--card); color:var(--fg); }
select, button { font:inherit; padding:8px 12px; border-radius:10px; border:1px solid var(--line);
  background:var(--card); color:var(--fg); }
#status { color: var(--muted); font-size: 13px; min-height: 20px; margin-bottom: 12px; }
#results { display:grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap:14px; }
.hit { background:var(--card); border:1px solid var(--line); border-radius:12px; overflow:hidden; }
.hit a { display:block; background:#0001; }
.hit img { display:block; width:100%; height:190px; object-fit:cover; object-position:top; }
.meta { padding:10px 12px; }
.path { font-size:12px; color:var(--muted); word-break:break-all; }
.snip { margin-top:6px; font-size:14px; }
mark { background: var(--hl); color: inherit; border-radius: 3px; padding: 0 2px; }
</style></head>
<body><main>
<h1>snapfind <span>offline screenshot search</span></h1>
<form id="f"><input type="search" id="q" placeholder="train ticket december" autofocus
  aria-label="Search screenshots">
<select id="mode" aria-label="Ranking"><option>hybrid</option><option>keyword</option>
<option>semantic</option></select><button>Search</button></form>
<div id="status" role="status"></div>
<div id="results"></div>
</main>
<script>
const $ = (id) => document.getElementById(id);
const esc = (s) => s.replace(/[&<>"]/g, (c) => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const mark = (s) => esc(s).replaceAll("\\u0002", "<mark>").replaceAll("\\u0003", "</mark>");
async function run(e) {
  if (e) e.preventDefault();
  const q = $("q").value.trim();
  if (!q) return;
  history.replaceState(null, "", "?q=" + encodeURIComponent(q));
  $("status").textContent = "Searching…";
  const t = performance.now();
  const r = await fetch("/api/search?mode=" + $("mode").value + "&q=" + encodeURIComponent(q));
  const hits = await r.json();
  $("status").textContent = hits.length + " results in " + Math.round(performance.now() - t) + " ms";
  $("results").innerHTML = hits.map((h) => `<div class="hit">
    <a href="/img?id=${h.id}" target="_blank" rel="noopener"><img loading="lazy" alt="" src="/img?id=${h.id}"></a>
    <div class="meta"><div class="path">${esc(h.path)}${h.copies.length ? " (+" + h.copies.length + " copy)" : ""}</div>
    <div class="snip">${mark(h.snippet)}</div></div></div>`).join("");
}
$("f").addEventListener("submit", run);
const q0 = new URLSearchParams(location.search).get("q");
if (q0) { $("q").value = q0; run(); }
</script></body></html>
"""


def make_handler(con, port: int):
    lock = threading.Lock()  # one sqlite connection, shared by the server's threads
    allowed_hosts = {f"127.0.0.1:{port}", f"localhost:{port}"}

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *a):
            pass

        def _send(self, code: int, body: bytes, ctype: str) -> None:
            self.send_response(code)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("X-Content-Type-Options", "nosniff")
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self):
            # Blocks DNS rebinding: a web page can't read results through another hostname.
            if self.headers.get("Host") not in allowed_hosts:
                return self._send(403, b"forbidden host", "text/plain")
            url = urlparse(self.path)
            qs = parse_qs(url.query)
            if url.path == "/":
                return self._send(200, PAGE.encode(), "text/html; charset=utf-8")
            if url.path == "/api/search":
                q = qs.get("q", [""])[0]
                mode = qs.get("mode", ["hybrid"])[0]
                if mode not in ("hybrid", "keyword", "semantic"):
                    mode = "hybrid"
                with lock:
                    indexer.update(con, limit=20)
                    hits = search.search(con, q, n=24, mode=mode) if q.strip() else []
                return self._send(200, json.dumps(hits).encode(), "application/json")
            if url.path == "/img":
                # Only ids that are in the index: there is no path parameter to abuse.
                rid = qs.get("id", [""])[0]
                with lock:
                    row = con.execute("SELECT path FROM images WHERE id=?",
                                      (rid,)).fetchone() if rid.isdigit() else None
                if row:
                    try:
                        with open(row[0], "rb") as f:
                            body = f.read()
                    except OSError:
                        body = None
                    if body is not None:
                        ctype = mimetypes.guess_type(row[0])[0] or "application/octet-stream"
                        return self._send(200, body, ctype)
            return self._send(404, b"not found", "text/plain")

    return Handler


def make_server(con, port: int) -> ThreadingHTTPServer:
    return ThreadingHTTPServer(("127.0.0.1", port), make_handler(con, port))


def serve(con, port: int = 8765) -> None:
    server = make_server(con, port)
    print(f"snapfind UI: http://127.0.0.1:{port}  (Ctrl+C stops)", file=sys.stderr)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
