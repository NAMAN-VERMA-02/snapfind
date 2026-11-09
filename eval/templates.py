"""HTML templates for synthetic screenshots. Every brand and person is fictional."""

from html import escape as e

BASE = """<!doctype html><html><head><meta charset="utf-8"><style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: "Segoe UI", system-ui, sans-serif; background: var(--bg); color: var(--fg);
  font-size: var(--fs); line-height: 1.4; overflow: hidden; }
:root { --bg:#ffffff; --fg:#1b1b1f; --muted:#6a6a73; --card:#f3f3f6; --line:#dedee4;
  --accent:#2f6fde; --ok:#178a4c; --fs: 15px; }
.dark { --bg:#121216; --fg:#e8e8ee; --muted:#9a9aa6; --card:#1e1e25; --line:#2e2e38;
  --accent:#6ea0ff; --ok:#46c27f; }
.lowc { --fg:#9b9ba3; --muted:#b9b9c0; }
.small { --fs: 10.5px; }
.status { display:flex; justify-content:space-between; padding:8px 18px; font-size:13px;
  font-weight:600; }
.bar { display:flex; align-items:center; gap:10px; padding:12px 16px; border-bottom:1px solid var(--line); }
.title { font-weight:700; font-size:1.15em; }
.muted { color: var(--muted); }
.card { background: var(--card); border-radius: 14px; padding: 14px 16px; margin: 12px 14px; }
.row { display:flex; justify-content:space-between; gap:12px; padding:5px 0; }
.btn { display:inline-block; padding:8px 16px; border-radius:20px; background:var(--accent);
  color:#fff; font-weight:600; margin:6px 6px 0 0; font-size: .92em; }
.big { font-size: 2em; font-weight: 700; }
.ok { color: var(--ok); font-weight: 700; }
.win { display:flex; height:100vh; }
.side { width: 220px; background: var(--card); padding: 14px; border-right:1px solid var(--line); }
.side div { padding: 6px 8px; border-radius: 6px; }
.side .on { background: var(--line); font-weight: 600; }
.main { flex: 1; padding: 0; }
.titlebar { padding: 8px 14px; font-size: 12px; border-bottom: 1px solid var(--line); color: var(--muted); }
.mono { font-family: Consolas, "Cascadia Mono", monospace; }
.bubble { max-width: 78%; padding: 8px 12px; border-radius: 14px; margin: 6px 12px; }
.me { background: #d8f6c8; margin-left: auto; } .dark .me { background: #1f4d33; }
.them { background: var(--card); }
.t { font-size: 11px; color: var(--muted); text-align: right; }
table { border-collapse: collapse; width: 100%; }
td, th { border: 1px solid var(--line); padding: 4px 8px; text-align: left; font-size: .9em; }
th { background: var(--card); }
</style></head><body class="{cls}">{body}</body></html>"""

PHONE_STATUS = '<div class="status"><span>{time}</span><span>5G ▮▮▮ {battery}%</span></div>'


def page(body: str, cls: str = "") -> str:
    return BASE.replace("{cls}", cls).replace("{body}", body)


def _status(s):
    return PHONE_STATUS.format(time=e(s.get("clock", "9:41")), battery=s.get("battery", 76))


def chat(s):
    msgs = "".join(
        f'<div class="bubble {"me" if who == "me" else "them"}">{e(text)}'
        f'<div class="t">{e(t)}</div></div>' for who, text, t in s["msgs"])
    return (_status(s) + f'<div class="bar"><span class="title">{e(s["name"])}</span>'
            f'<span class="muted">{e(s.get("sub", "online"))}</span></div>'
            f'<div style="padding-top:8px">{msgs}</div>'
            '<div class="bar muted" style="position:fixed;bottom:0;width:100%">Message</div>')


def email(s):
    folders = "".join(f'<div class="{"on" if f == "Inbox" else ""}">{f}</div>'
                      for f in ["Inbox", "Starred", "Sent", "Drafts", "Spam", "Archive"])
    others = "".join(f'<div class="row muted"><span>{e(a)}</span><span>{e(b)}</span></div>'
                     for a, b in s.get("others", []))
    body = "".join(f"<p style='margin:10px 0'>{e(p)}</p>" for p in s["body"])
    return (f'<div class="win"><div class="side"><div class="title">QuickMail</div>{folders}'
            f'<div style="margin-top:20px" class="muted">{others}</div></div>'
            f'<div class="main"><div class="titlebar">QuickMail - Inbox</div>'
            f'<div style="padding:18px 26px"><div class="title" style="font-size:1.4em">'
            f'{e(s["subject"])}</div><div class="row"><span><b>{e(s["from"])}</b> '
            f'<span class="muted">to me</span></span><span class="muted">{e(s["date"])}</span></div>'
            f'{body}<span class="btn">Reply</span><span class="btn">Forward</span></div></div></div>')


def kv(s):
    """A card of label/value rows: tickets, payments, orders, rides, boarding passes."""
    rows = "".join(f'<div class="row"><span class="muted">{e(k)}</span><b>{e(v)}</b></div>'
                   for k, v in s["rows"])
    head = (f'<div class="bar"><span class="title">{e(s["brand"])}</span>'
            f'<span class="muted">{e(s.get("sub", ""))}</span></div>')
    hero = ""
    if "hero" in s:
        hero = (f'<div class="card" style="text-align:center"><div class="ok">{e(s["hero"])}</div>'
                f'<div class="big">{e(s.get("amount", ""))}</div>'
                f'<div class="muted">{e(s.get("hero_sub", ""))}</div></div>')
    btns = "".join(f'<span class="btn">{e(b)}</span>' for b in s.get("buttons", []))
    status = _status(s) if s.get("phone") else ""
    return f'{status}{head}{hero}<div class="card">{rows}</div><div style="padding:0 14px">{btns}</div>'


def terminal(s):
    lines = "".join(f"<div>{e(line) or '&nbsp;'}</div>" for line in s["lines"])
    return (f'<div class="titlebar mono">{e(s.get("title", "Windows PowerShell"))}</div>'
            f'<div class="mono" style="padding:12px 16px;white-space:pre-wrap">{lines}</div>')


def code(s):
    tabs = "".join(f'<span style="padding:6px 14px;{"border-bottom:2px solid var(--accent)" if i == 0 else ""}">'
                   f'{e(t)}</span>' for i, t in enumerate(s["tabs"]))
    lines = "".join(f'<div><span class="muted" style="display:inline-block;width:38px">{i}</span>'
                    f'{e(line)}</div>' for i, line in enumerate(s["lines"], s.get("start", 1)))
    return (f'<div class="titlebar">{e(s["tabs"][0])} - {e(s.get("project", "project"))} - CodePad</div>'
            f'<div style="display:flex;border-bottom:1px solid var(--line);font-size:13px">{tabs}</div>'
            f'<div class="mono" style="padding:10px;white-space:pre">{lines}</div>'
            f'<div class="titlebar" style="position:fixed;bottom:0;width:100%">'
            f'{e(s.get("statusbar", "Ln 1, Col 1  UTF-8  Python"))}</div>')


def settings(s):
    side = "".join(f'<div class="{"on" if x == s["section"] else ""}">{e(x)}</div>'
                   for x in s.get("sections", ["System", "Bluetooth & devices", "Network & internet",
                                               "Personalisation", "Apps", "Accounts", "Privacy"]))
    rows = "".join(f'<div class="card row"><span>{e(k)}</span><span class="muted">{e(v)}</span></div>'
                   for k, v in s["rows"])
    return (f'<div class="win"><div class="side"><div class="title">Settings</div>{side}</div>'
            f'<div class="main" style="padding:20px"><div class="title" style="font-size:1.6em;'
            f'margin:0 14px 10px">{e(s["section"])} › {e(s["page"])}</div>{rows}</div></div>')


def post(s):
    replies = "".join(f'<div class="card"><b>{e(a)}</b> <span class="muted">{e(h)}</span>'
                      f'<div>{e(t)}</div></div>' for a, h, t in s.get("replies", []))
    return (_status(s) + '<div class="bar"><span class="title">Chirp</span></div>'
            f'<div style="padding:14px"><b>{e(s["author"])}</b> <span class="muted">{e(s["handle"])}'
            f' · {e(s["when"])}</span><div style="font-size:1.15em;margin:10px 0">{e(s["text"])}</div>'
            f'<div class="muted">{e(s.get("stats", "12 Reposts  148 Likes  9 Bookmarks"))}</div></div>'
            f'{replies}')


def notes(s):
    items = "".join(f'<div class="row" style="justify-content:flex-start">'
                    f'<span>{"☑" if x.startswith("x ") else "☐"}</span>'
                    f'<span>{e(x[2:] if x.startswith("x ") else x)}</span></div>' for x in s["items"])
    status = _status(s) if s.get("phone") else '<div class="titlebar">Notely</div>'
    return (f'{status}<div style="padding:16px 20px"><div class="title" style="font-size:1.5em">'
            f'{e(s["title"])}</div><div class="muted">{e(s["date"])}</div>'
            f'<div style="margin-top:12px">{items}</div></div>')


def calendar(s):
    days = "".join(f'<th>{d}</th>' for d in s.get("days", ["Mon", "Tue", "Wed", "Thu", "Fri"]))
    ev = s["event"]
    rows = "".join(f'<div class="row"><span class="muted">{e(k)}</span><span>{e(v)}</span></div>'
                   for k, v in ev["rows"])
    return (f'<div class="titlebar">Calendar - {e(s["month"])}</div><div style="padding:14px">'
            f'<table><tr>{days}</tr><tr>{"<td style=height:120px></td>" * 5}</tr></table>'
            f'<div class="card" style="position:absolute;top:120px;left:300px;width:520px;'
            f'box-shadow:0 8px 30px #0003"><div class="title">{e(ev["title"])}</div>'
            f'<div class="muted">{e(ev["when"])}</div>{rows}</div></div>')


def sms(s):
    msgs = "".join(f'<div class="bubble them">{e(t)}<div class="t">{e(w)}</div></div>'
                   for t, w in s["msgs"])
    return (_status(s) + f'<div class="bar"><span class="title">{e(s["sender"])}</span></div>'
            f'<div class="muted" style="text-align:center;font-size:12px;margin:8px">'
            f'Text Message · {e(s.get("day", "Today"))}</div>{msgs}')


def sheet(s):
    head = "".join(f"<th>{e(h)}</th>" for h in s["cols"])
    rows = "".join("<tr>" + "".join(f"<td>{e(str(c))}</td>" for c in r) + "</tr>" for r in s["rows"])
    return (f'<div class="titlebar">{e(s["file"])} - Sheets</div><div style="padding:12px">'
            f'<table><tr><th></th>{head}</tr>'
            + rows.replace("<tr>", "<tr><td class='muted'>#</td>")
            + "</table></div>")


def doc(s):
    paras = "".join(f"<p style='margin:12px 0'>{e(p)}</p>" for p in s["paras"])
    return (f'<div class="titlebar">{e(s.get("site", "docs"))} — {e(s["title"])}</div>'
            f'<div style="max-width:760px;margin:0 auto;padding:26px"><div class="title" '
            f'style="font-size:1.8em">{e(s["title"])}</div><div class="muted">{e(s.get("byline", ""))}'
            f'</div>{paras}</div>')


RENDER = {"chat": chat, "email": email, "kv": kv, "terminal": terminal, "code": code,
          "settings": settings, "post": post, "notes": notes, "calendar": calendar, "sms": sms,
          "sheet": sheet, "doc": doc}
