"""Render the eval screenshots: eval/screens.py -> HTML -> PNG with headless Edge (or Chrome).

    python eval/make_dataset.py [--browser PATH]

Writes eval/images/<id>.png (targets) and <id>_d.png (twins, the hard negatives). Hard cases get
post-processed: JPEG artifacts, blur from downscaling, or a tall scroll capture.
"""

import argparse
import copy
import shutil
import subprocess
import sys
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from PIL import Image

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from screens import S  # noqa: E402
from templates import RENDER, page  # noqa: E402

BROWSERS = [r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            "/usr/bin/google-chrome", "/usr/bin/chromium"]
PHONE_TEMPLATES = {"chat", "sms", "post"}
FILLER_CHAT = [("them", "ok"), ("me", "haha"), ("them", "send the notes pls"), ("me", "sent"),
               ("them", "who's coming tomorrow?"), ("me", "me"), ("them", "same"),
               ("me", "what time?"), ("them", "around 5"), ("them", "👍"), ("me", "fine")] * 3
FILLER_PARAS = ["This page is part of the student handbook and is updated every semester.",
                "Read the full section before contacting the office with questions."] * 9


def variants(spec: dict) -> list[dict]:
    base = {k: v for k, v in spec.items() if k != "twin"}
    if "from_" in base:
        base["from"] = base.pop("from_")
    twin = {**copy.deepcopy(base), **spec["twin"], "id": spec["id"] + "_d"}
    return [base, twin]


def pad_tall(s: dict) -> dict:
    s = copy.deepcopy(s)
    if s["t"] == "chat":
        s["msgs"] = [(w, t, "1:0" + str(i % 10) + " PM") for i, (w, t) in enumerate(FILLER_CHAT)] + s["msgs"]
    elif s["t"] == "notes":
        s["items"] = [f"Topic {i}: revise class notes" for i in range(1, 46)] + s["items"]
    elif s["t"] == "sheet":
        s["rows"] = [[f"Student {i:02}", "-", "-"] for i in range(1, 70)] + s["rows"]
    elif s["t"] == "doc":
        s["paras"] = FILLER_PARAS + s["paras"]
    return s


def capture(cmd: list[str], png: Path, timeout: float = 240) -> None:
    """Run a headless browser until the screenshot file appears. Headless Edge on Windows can
    keep running after writing it, so don't wait for the process to exit."""
    proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    deadline = time.monotonic() + timeout
    try:
        while time.monotonic() < deadline:
            if png.exists() and png.stat().st_size > 0:
                time.sleep(0.5)  # let the write finish
                return
            if proc.poll() is not None:
                time.sleep(2)  # helper processes may still be writing the file
                if png.exists():
                    continue
                raise RuntimeError(f"browser exited without a screenshot: {png.name}")
            time.sleep(0.2)
        raise TimeoutError(png.name)
    finally:
        proc.kill()


def render(browser: str, s: dict, out_dir: Path, work: Path) -> Path:
    phone = s["t"] in PHONE_TEMPLATES or s.get("phone")
    hard = s.get("hard")
    if hard == "tall":
        s = pad_tall(s)
    cls = " ".join(c for c, on in [("dark", s.get("dark")), ("lowc", hard == "lowc"),
                                   ("small", hard == "small")] if on)
    html = work / f"{s['id']}.html"
    html.write_text(page(RENDER[s["t"]](s), cls), encoding="utf-8")
    # Headless Chromium has a minimum window width (about 500 px); a narrower phone window gets
    # laid out wider than it is captured and the right edge is cut off. 540 x 2 = 1080 px wide.
    w, h, scale = (540, 1200, 2.0) if phone else (1280, 800, 1.0)
    if hard == "tall":
        h = w * 4
    png = work / f"{s['id']}.png"
    for attempt in range(3):  # a launch occasionally stalls on a busy machine; try again
        # A fresh profile each attempt: a killed browser's helpers can keep the old one locked.
        cmd = [browser, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--no-first-run",
               "--disable-extensions", "--disable-component-update",
               "--disable-background-networking",
               f"--user-data-dir={work / ('profile-' + s['id'] + '-' + str(attempt))}",
               f"--window-size={w},{h}",
               f"--force-device-scale-factor={scale}", f"--screenshot={png}", html.as_uri()]
        try:
            capture(cmd, png)
            break
        except (TimeoutError, RuntimeError):
            if attempt == 2:
                raise
    img = Image.open(png).convert("RGB")
    if hard == "blur":
        small = img.resize((int(img.width * 0.4), int(img.height * 0.4)), Image.BILINEAR)
        img = small.resize(img.size, Image.BILINEAR)
    if hard == "jpeg":  # e.g. a screenshot forwarded through a chat app
        out = out_dir / f"{s['id']}.jpg"
        img.save(out, quality=22)
    else:
        out = out_dir / f"{s['id']}.png"
        img.save(out, optimize=True)
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--browser", default=next((b for b in BROWSERS if Path(b).exists()), None))
    ap.add_argument("--only", nargs="*", help="render just these ids")
    ap.add_argument("--force", action="store_true", help="re-render images that already exist")
    args = ap.parse_args()
    if not args.browser:
        sys.exit("No Edge/Chrome found; pass --browser")
    out_dir = HERE / "images"
    out_dir.mkdir(exist_ok=True)
    (HERE / "_work").mkdir(exist_ok=True)
    work = Path(tempfile.mkdtemp(prefix="render-", dir=HERE / "_work"))
    jobs = [v for spec in S for v in variants(spec)
            if (not args.only or v["id"].removesuffix("_d") in args.only)
            and (args.force or not any(out_dir.glob(v["id"] + ".*")))]
    try:
        with ThreadPoolExecutor(2) as pool:
            for out in pool.map(lambda s: render(args.browser, s, out_dir, work), jobs):
                print(out.name)
    finally:
        shutil.rmtree(work, ignore_errors=True)
    print(f"{len(jobs)} images in {out_dir}")


if __name__ == "__main__":
    main()
