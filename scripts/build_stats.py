#!/usr/bin/env python3
"""Writes the cards in assets/stats/ from public GitHub data.

Uses the REST API (set GITHUB_TOKEN for a higher rate limit) and ghchart.rshah.org for daily
contribution counts. Any failed request stops the run before a card is written, so the
last good cards stay in place.
"""
import json
import os
import re
import urllib.parse
import urllib.request
from collections import Counter
from datetime import date, timedelta

from theme import ASSETS, EDGE, FAINT, INK, MANILA, RED, esc, svg, tag

USER = "KiShOrE-2008"
SKIP_REPOS = {USER}
INKS = ["#38bdf8", "#34d399", "#818cf8", "#f43f5e", "#fbbf24", "#94a3b8"]


def fetch(url):
    headers = {"User-Agent": "profile-stats"}
    if url.startswith("https://api.github.com"):
        headers["Accept"] = "application/vnd.github+json"
        if os.environ.get("GITHUB_TOKEN"):
            headers["Authorization"] = f'Bearer {os.environ["GITHUB_TOKEN"]}'
    with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=30) as r:
        return r.read().decode()


def api(path):
    return json.loads(fetch(f"https://api.github.com/{path}"))


def count(path, q):
    return api(f"search/{path}?per_page=1&q={urllib.parse.quote(q, safe=':+')}")["total_count"]


def calendar():
    """Returns {date: contributions} for the last year."""
    raw = fetch(f"https://ghchart.rshah.org/14284B/{USER}")
    days = {}
    for tag_text in re.findall(r"<rect[^>]*data-score[^>]*>", raw):
        score = re.search(r'data-score="(\d+)"', tag_text).group(1)
        day = re.search(r'data-date="([\d-]+)"', tag_text).group(1)
        days[date.fromisoformat(day)] = int(score)
    if len(days) < 300:
        raise RuntimeError(f"Contribution chart looks wrong: only {len(days)} days found")
    return dict(sorted(days.items()))


def streaks(days, today):
    current, longest, run = 0, 0, 0
    for n in days.values():
        run = run + 1 if n else 0
        longest = max(longest, run)
    d = today if days.get(today) else today - timedelta(days=1)
    while days.get(d):
        current, d = current + 1, d - timedelta(days=1)
    return current, longest


def card(title, body, label, w=460, h=280):
    head = f'<text x="62" y="46" class="st" font-size="27">{esc(title)}</text>'
    return svg(w, h, tag(1, 1, w - 2, h - 2) + head + body, label)


def activity(s):
    rows = [("Commits", s["commits"]), ("Pull requests", s["prs"]), ("Merged", s["merged"]),
            ("Public repositories", s["repos"]), ("Stars earned", s["stars"])]
    body = "".join(
        f'<text x="62" y="{90 + i * 36}" font-size="21">{a}</text>'
        f'<path d="M62 {98 + i * 36}H436" stroke="{INK}" stroke-opacity=".3" stroke-dasharray="2 4"/>'
        f'<text x="436" y="{92 + i * 36}" class="st" font-size="27" text-anchor="end">{v}</text>'
        for i, (a, v) in enumerate(rows))
    return card("Activity", body, "; ".join(f"{a}: {v}" for a, v in rows))


def streak(total, current, longest):
    def block(x, n, name, color=INK):
        return (f'<text x="{x}" y="160" class="st" font-size="66" text-anchor="middle" style="fill:{color}">{n}</text>'
                f'<text x="{x}" y="196" font-size="19" text-anchor="middle">{name}</text>')
    body = block(142, total, "12 months") + block(262, current, "day streak", RED) + block(376, longest, "longest")
    body += f'<path d="M202 108V204M322 108V204" stroke="{INK}" stroke-opacity=".35"/>'
    return card("Contributions and streaks", body, f"{total} contributions in the last 12 months; current streak {current} days; longest {longest} days")


def languages(sizes):
    top = sizes.most_common(6)
    total = sum(sizes.values())
    x, bar, legend = 62.0, "", ""
    for i, (name, size) in enumerate(top):
        pct = size / total
        width = 374 * pct
        bar += f'<rect x="{x:.1f}" y="74" width="{max(width, 2):.1f}" height="22" fill="{INKS[i]}"/>'
        x += width
        lx, ly = 62 + (i % 2) * 192, 132 + (i // 2) * 44
        legend += (f'<rect x="{lx}" y="{ly-14}" width="15" height="15" fill="{INKS[i]}"/>'
                   f'<text x="{lx+24}" y="{ly}" font-size="19">{esc(name)}</text>'
                   f'<text x="{lx+24}" y="{ly+20}" font-size="16" opacity=".78">{pct*100:.1f}%</text>')
    label = ", ".join(f"{n} {s/total*100:.1f}%" for n, s in top)
    return card("Languages", bar + legend, label)


def recent(days, today):
    span = [today - timedelta(days=29 - i) for i in range(30)]
    vals = [days.get(d, 0) for d in span]
    top = max(max(vals), 1)
    x0, x1, y0, y1 = 62, 436, 214, 78
    px = lambda i: x0 + (x1 - x0) * i / 29
    py = lambda v: y0 - (y0 - y1) * v / top
    grid = "".join(f'<path d="M{x0} {y}H{x1}" stroke="{INK}" stroke-opacity=".16"/>' for y in range(y1, y0 + 1, 17))
    grid += "".join(f'<path d="M{px(i):.1f} {y1}V{y0}" stroke="{INK}" stroke-opacity=".1"/>' for i in range(0, 30, 3))
    pts = " ".join(f"{px(i):.1f},{py(v):.1f}" for i, v in enumerate(vals))
    peak = vals.index(max(vals))
    body = (grid + f'<polyline points="{pts}" fill="none" stroke="{RED}" stroke-width="2.6" stroke-linejoin="round"/>'
            f'<text x="{x0}" y="238" font-size="16">{span[0]:%d %b}</text>'
            f'<text x="{x1}" y="238" font-size="16" text-anchor="end">{span[-1]:%d %b}</text>'
            f'<text x="249" y="238" font-size="16" text-anchor="middle">peak {max(vals)} on {span[peak]:%d %b}</text>')
    return card("Last 30 days", body, f"Daily contributions from {span[0]} to {span[-1]}, peaking at {max(vals)}")


def heatmap(days, today, total):
    first = min(days)
    start = first - timedelta(days=(first.weekday() + 1) % 7)
    hi = max(max(days.values()), 1)
    cell, pitch, x0, y0 = 13, 16.2, 62, 76
    cells, months, seen = [], [], None
    for d, n in days.items():
        wk = (d - start).days // 7
        dow = (d.weekday() + 1) % 7
        x, y = x0 + wk * pitch, y0 + dow * pitch
        if n:
            level = 0.3 + 0.7 * (min(n, hi) / hi) ** 0.5
            cells.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{cell}" height="{cell}" rx="2" fill="{INK}" fill-opacity="{level:.2f}"/>')
        else:
            cells.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{cell}" height="{cell}" rx="2" fill="none" stroke="{FAINT}"/>')
        if d.month != seen and d.day <= 7 and wk < 52:
            months.append(f'<text x="{x:.1f}" y="{y0-9}" font-size="15">{d:%b}</text>')
            seen = d.month
    head = (f'<text x="62" y="34" class="st" font-size="27">Contribution heatmap</text>'
            f'<text x="944" y="34" font-size="16" text-anchor="end">{total} contributions, refreshed {today:%d %b %Y}</text>')
    return svg(960, 212, tag(1, 1, 958, 210) + head + "".join(months) + "".join(cells),
               f"{total} contributions in the last 12 months")


def main():
    today = date.today()
    days = calendar()
    repos = [r for r in api(f"users/{USER}/repos?per_page=100") if r["name"] not in SKIP_REPOS]
    sizes = Counter()
    for r in repos:
        if not r["fork"]:
            sizes.update(api(f'repos/{USER}/{r["name"]}/languages'))
    stats = {"commits": count("commits", f"author:{USER}"),
             "prs": count("issues", f"author:{USER} type:pr"),
             "merged": count("issues", f"author:{USER} type:pr is:merged"),
             "repos": len(repos) + 1,
             "stars": sum(r["stargazers_count"] for r in repos)}
    total = sum(days.values())
    current, longest = streaks(days, today)
    out = ASSETS / "stats"
    out.mkdir(parents=True, exist_ok=True)
    cards = {"activity": activity(stats), "streak": streak(total, current, longest),
             "languages": languages(sizes), "recent": recent(days, today),
             "heatmap": heatmap(days, today, total)}
    for name, content in cards.items():
        (out / f"{name}.svg").write_text(content)


if __name__ == "__main__":
    main()
