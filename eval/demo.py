"""Make docs/demo.gif and docs/cli.png from real searches on the eval index (never real data).

    python eval/demo.py   # needs eval/_work/eval.db from eval/run.py, and Edge or Chrome
"""

import html
import os
import subprocess
import sys
import tempfile
import threading
from pathlib import Path

from PIL import Image

HERE = Path(__file__).parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(HERE))
from make_dataset import BROWSERS, capture  # noqa: E402

from snapfind import db, indexer, web  # noqa: E402

QUERIES = ["train ticket december", "port already in use", "wifi password", "money I owe for the trip"]
PORT = 8766


def shot(browser: str, url: str, out: Path, work: Path, w=1280, h=760) -> Image.Image:
    capture([browser, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--no-first-run",
             f"--user-data-dir={work / ('profile-' + out.stem)}", f"--window-size={w},{h}",
             "--virtual-time-budget=15000", f"--screenshot={out}", url], out)
    return Image.open(out).convert("RGB")


def main() -> None:
    browser = next(b for b in BROWSERS if Path(b).exists())
    dbp = HERE / "_work" / "eval.db"
    docs = ROOT / "docs"
    docs.mkdir(exist_ok=True)
    work = Path(tempfile.mkdtemp(prefix="demo-", dir=HERE / "_work"))

    indexer.default_folders = lambda: []  # the demo must never touch a real Screenshots folder
    con = db.connect(dbp)
    srv = web.make_server(con, PORT)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    frames = []
    for i, q in enumerate(QUERIES):
        url = f"http://127.0.0.1:{PORT}/?q={q.replace(' ', '+')}"
        frames.append(shot(browser, url, work / f"f{i}.png", work))
    srv.shutdown()
    frames[0].save(docs / "web-ui.png", optimize=True)
    small = [f.resize((960, int(f.height * 960 / f.width)), Image.LANCZOS) for f in frames]
    pal = [f.quantize(colors=128, method=Image.Quantize.MEDIANCUT) for f in small]
    pal[0].save(docs / "demo.gif", save_all=True, append_images=pal[1:], duration=2600, loop=0,
                optimize=True)

    out = subprocess.run([sys.executable, "-m", "snapfind", "--db", str(dbp), QUERIES[0],
                          "--no-update", "-n", "3"], capture_output=True, text=True,
                         encoding="utf-8", cwd=ROOT)
    text = f"> snapfind \"{QUERIES[0]}\"\n" + out.stdout + out.stderr
    text = text.replace(str(ROOT) + os.sep, "")  # the real path, shown relative: eval\images\...
    page = ('<html><body style="margin:0;background:#16161a;color:#e6e6ea;'
            'font:17px/1.5 Consolas,monospace;padding:22px;white-space:pre-wrap">'
            + html.escape(text).replace("[", '<b style="color:#ffd75e">').replace("]", "</b>")
            + "</body></html>")
    (work / "cli.html").write_text(page, encoding="utf-8")
    img = shot(browser, (work / "cli.html").as_uri(), work / "cli.png", work, 1100, 330)
    img.save(docs / "cli.png", optimize=True)
    print("wrote docs/demo.gif, docs/web-ui.png, docs/cli.png")


if __name__ == "__main__":
    main()
