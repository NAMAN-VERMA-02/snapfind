import os
import shutil
import sys

import pytest

from snapfind import indexer, ocr
from tests.conftest import age


@pytest.fixture
def fake_ocr(monkeypatch):
    """OCR stand-in: returns the file's bytes as text and records every call."""
    calls = []

    def read_text(path):
        calls.append(os.path.basename(path))
        with open(path, encoding="utf-8") as f:
            return f.read()

    monkeypatch.setattr(ocr, "read_text", read_text)
    return calls


def write(folder, name, text, seconds_ago=3600):
    p = folder / name
    p.write_text(text, encoding="utf-8")
    age(p, seconds_ago)
    return p


def paths(con):
    return sorted(os.path.basename(p) for (p,) in con.execute("SELECT path FROM images"))


def test_only_new_or_changed_files_are_ocrd(con, tmp_path, fake_ocr):
    shots = tmp_path / "shots"
    shots.mkdir()
    write(shots, "a.png", "alpha invoice")
    b = write(shots, "b.png", "beta receipt")
    write(shots, "notes.txt", "not an image")

    indexer.update(con, [shots])
    assert sorted(fake_ocr) == ["a.png", "b.png"]

    indexer.update(con, [shots])  # nothing changed: no OCR at all
    assert len(fake_ocr) == 2

    b.write_text("beta receipt, edited", encoding="utf-8")
    age(b, 100)
    indexer.update(con, [shots])
    assert fake_ocr[2:] == ["b.png"]

    os.remove(shots / "a.png")
    r = indexer.update(con, [shots])
    assert r["removed"] == 1 and paths(con) == ["b.png"]


def test_copies_and_renames_reuse_the_cache(con, tmp_path, fake_ocr):
    shots, export = tmp_path / "shots", tmp_path / "export"
    shots.mkdir()
    export.mkdir()
    write(shots, "orig.png", "boarding pass gate 22")
    indexer.update(con, [shots])
    shutil.copy2(shots / "orig.png", export / "IMG_0001.png")
    r = indexer.update(con, [shots, export])
    assert fake_ocr == ["orig.png"] and r["indexed"] == 1 and r["ocr"] == 0
    texts = [t for (t,) in con.execute("SELECT text FROM fts")]
    assert texts == ["boarding pass gate 22"] * 2


def test_newest_first_and_resumable(con, tmp_path, monkeypatch):
    shots = tmp_path / "shots"
    shots.mkdir()
    for i in range(25):
        write(shots, f"s{i:02}.png", f"shot {i}", seconds_ago=10_000 - i * 10)
    calls = []

    def flaky(path):
        calls.append(os.path.basename(path))
        if len(calls) == 15:
            raise KeyboardInterrupt  # the user hits Ctrl+C mid-run
        return "text"

    monkeypatch.setattr(ocr, "read_text", flaky)
    with pytest.raises(KeyboardInterrupt):
        indexer.update(con, [shots])
    assert calls[:3] == ["s24.png", "s23.png", "s22.png"]  # newest first
    con.rollback()
    assert len(paths(con)) == 10  # committed every 10 images

    monkeypatch.setattr(ocr, "read_text", lambda p: "text")
    r = indexer.update(con, [shots])
    assert r["indexed"] == 15 and len(paths(con)) == 25


def test_limit_skips_big_backlogs(con, tmp_path, fake_ocr):
    shots = tmp_path / "shots"
    shots.mkdir()
    for i in range(5):
        write(shots, f"{i}.png", f"text {i}")
    r = indexer.update(con, [shots], limit=3)
    assert r["skipped"] and r["new"] == 5 and fake_ocr == []


def test_half_written_and_excluded_files_are_skipped(con, tmp_path, fake_ocr):
    shots = tmp_path / "shots"
    (shots / "private").mkdir(parents=True)
    write(shots, "ok.png", "fine")
    write(shots, "fresh.png", "still being saved", seconds_ago=0)
    write(shots / "private", "bank.png", "balance")
    con.execute("INSERT INTO excludes VALUES (?)", (str(shots / "private" / "*"),))
    indexer.update(con, [shots])
    assert fake_ocr == ["ok.png"]


def test_rows_survive_when_their_folder_is_not_scanned(con, tmp_path, fake_ocr):
    a, b = tmp_path / "a", tmp_path / "b"
    a.mkdir()
    b.mkdir()
    write(a, "1.png", "one")
    write(b, "2.png", "two")
    indexer.update(con, [a, b])
    indexer.update(con, [a])  # b is unplugged / not passed: keep its rows
    assert paths(con) == ["1.png", "2.png"]


@pytest.mark.skipif(sys.platform != "win32", reason="Windows file attributes")
def test_onedrive_cloud_only_files_are_not_read(con, tmp_path, fake_ocr):
    import ctypes

    shots = tmp_path / "shots"
    shots.mkdir()
    write(shots, "local.png", "here")
    cloud = write(shots, "cloud.png", "in the cloud")
    assert ctypes.windll.kernel32.SetFileAttributesW(str(cloud), 0x1000)  # OFFLINE
    try:
        indexer.update(con, [shots])
    finally:
        ctypes.windll.kernel32.SetFileAttributesW(str(cloud), 0x80)
    assert fake_ocr == ["local.png"]


def test_tall_images_are_sliced_to_cover_everything():
    assert ocr.slice_tops(1080, 1920) == [0]
    for w, h in [(1080, 8000), (1000, 2001), (720, 30000)]:
        tops = ocr.slice_tops(w, h)
        assert tops[0] == 0 and tops[-1] + 2 * w == h  # last slice ends at the bottom
        assert all(b - a <= 1.8 * w for a, b in zip(tops, tops[1:], strict=False))  # 10% overlap


def test_glued_labels_are_split():
    assert ocr.split_joined("RailBook E-TicketPNR 4521") == "Rail Book Ticket PNR"
