import pytest

from snapfind import db, embed, search

DOCS = {
    "ticket.png": ("RailBook E-Ticket PNR 4521876630\nTrain 12952 Rajdhani Express\n"
                   "Date of Journey: 14/12/2026 Coach B2", "december dec 2026"),
    "bus.png": ("CityBus booking confirmed\nSeat 14 Pune to Mumbai\n02/08/2026",
                "august aug 2026"),
    "error.png": ("Error: listen EADDRINUSE: address already in use :::3000", ""),
    "chat.png": ("Riya: are we still meeting for dinner tonight?\nme: yes 8pm at the cafe", ""),
}


def fill(con, docs=DOCS, sha=None):
    for name, (text, dates) in docs.items():
        vec = embed.embed(embed.chunks(text)).tobytes()
        db.put(con, f"/shots/{name}", 1.0, 1, sha or name, vec, text, dates)
    con.commit()


@pytest.mark.parametrize("q", ['"', "*", "AND", "-", "NEAR(", "a\"b OR", "", "   ", "日本 ₹"])
def test_hostile_queries_do_not_crash(con, q):
    fill(con)
    for mode in ("keyword", "semantic", "hybrid"):
        search.search(con, q, mode=mode)


def test_rrf_rewards_agreement():
    assert search.rrf([1, 2, 3], [2, 9, 8])[:2] == [2, 1]  # in both lists beats first in one
    assert search.rrf([], [5, 6]) == [5, 6]


def test_modes_find_the_right_image(con):
    fill(con)
    top = lambda q, m: search.search(con, q, mode=m)[0]["path"]  # noqa: E731
    assert top("EADDRINUSE", "keyword") == "/shots/error.png"
    assert top("train ticket december", "keyword") == "/shots/ticket.png"
    assert top("port is already taken by another server", "semantic") == "/shots/error.png"
    assert top("friend asking about evening plans", "hybrid") == "/shots/chat.png"


def test_keyword_snippet_is_highlighted(con):
    fill(con)
    hit = search.search(con, "rajdhani", mode="keyword")[0]
    assert "\x02Rajdhani\x03" in hit["snippet"]


def test_same_screenshot_in_two_folders_is_one_result(con):
    text = "Order #88812 delivered to your door"
    vec = embed.embed([text]).tobytes()
    db.put(con, "/pc/order.png", 1.0, 1, "same", vec, text, "")
    db.put(con, "/phone/order.png", 1.0, 1, "same", vec, text, "")
    con.commit()
    hits = search.search(con, "order delivered")
    assert len(hits) == 1 and len(hits[0]["copies"]) == 1


def test_vector_cache_sees_new_rows(con):
    fill(con, {"a.png": ("weather forecast rain tomorrow", "")})
    search.search(con, "rain", mode="semantic")
    fill(con, {"b.png": ("electricity bill due amount", "")})
    paths = [h["path"] for h in search.search(con, "power bill payment", mode="semantic")]
    assert paths[0] == "/shots/b.png"
