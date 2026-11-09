import time

from snapfind.dates import expand_terms, taken_words, text_date_words


def test_capture_date_from_windows_and_android_names():
    assert taken_words("C:/s/Screenshot 2024-08-11 181943.png", 0) == "august aug 2024"
    assert taken_words("/x/Screenshot_20241018-123456_Chrome.jpg", 0) == "october oct 2024"


def test_capture_date_falls_back_to_mtime():
    mtime = time.mktime((2025, 12, 3, 12, 0, 0, 0, 0, -1))
    assert taken_words("Screenshot (12).png", mtime) == "december dec 2025"


def test_numeric_dates_in_text_become_month_words():
    assert text_date_words("Date of Journey: 14/12/2026") == "december dec 2026"
    assert text_date_words("paid on 2026-03-05") == "march mar 2026"
    assert text_date_words("due 12/14/26") == "december dec 2026"  # only month-first is valid
    assert text_date_words("version 1.2.3 and 45/67/2020") == ""


def test_query_month_aliases():
    assert expand_terms(["train", "december"]) == ["train", "december", "dec"]
    assert expand_terms(["dec"]) == ["dec", "december"]
