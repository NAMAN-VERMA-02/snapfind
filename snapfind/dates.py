"""Month words for dates, so "train ticket december" finds a ticket that says 14/12/2026."""

import re
import time
from pathlib import Path

MONTHS = ["january", "february", "march", "april", "may", "june", "july",
          "august", "september", "october", "november", "december"]
ABBR = [m[:3] for m in MONTHS]
_ALIAS = {**dict(zip(MONTHS, ABBR, strict=True)), **dict(zip(ABBR, MONTHS, strict=True)),
          "sept": "september"}

_FILENAME_DATE = re.compile(
    r"(?<!\d)(20\d\d)[-_.]?(0[1-9]|1[0-2])[-_.]?(0[1-9]|[12]\d|3[01])(?!\d)")
_DMY = re.compile(r"(?<!\d)(\d{1,2})[/.-](\d{1,2})[/.-](\d{4}|\d{2})(?!\d)")
_YMD = re.compile(r"(?<!\d)(\d{4})-(\d{1,2})-(\d{1,2})(?!\d)")


def _words(month: int, year: int) -> str:
    return f"{MONTHS[month - 1]} {ABBR[month - 1]} {year}"


def taken_words(path: str, mtime: float) -> str:
    """When the screenshot was taken: from names like 'Screenshot 2024-08-11 181943.png'
    or 'Screenshot_20241018-123456.png', else the file's mtime."""
    m = _FILENAME_DATE.search(Path(path).name)
    if m:
        return _words(int(m[2]), int(m[1]))
    t = time.localtime(mtime)
    return _words(t.tm_mon, t.tm_year)


def text_date_words(text: str) -> str:
    """Month words for numeric dates in the OCR text. Day-first (Indian order), unless only
    month-first is a valid date, e.g. 12/14/2026."""
    out = []
    for y, mo, d in _YMD.findall(text):
        if 1 <= int(mo) <= 12 and 1 <= int(d) <= 31:
            out.append(_words(int(mo), int(y)))
    for d, mo, y in _DMY.findall(text):
        d, mo, y = int(d), int(mo), int(y)
        if mo > 12 and d <= 12:
            d, mo = mo, d
        if 1 <= mo <= 12 and 1 <= d <= 31:
            out.append(_words(mo, y + 2000 if y < 100 else y))
    return " ".join(dict.fromkeys(out))


def expand_terms(terms: list[str]) -> list[str]:
    """Add the other spelling of month words: december <-> dec."""
    out = []
    for t in terms:
        out.append(t)
        if t in _ALIAS:
            out.append(_ALIAS[t])
    return list(dict.fromkeys(out))
