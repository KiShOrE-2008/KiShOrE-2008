#!/usr/bin/env python3
"""Writes README.md, assets/hero.svg, assets/chain.svg and chain.json from the resume data below.

Edit ENTRIES (or the other lists) and run:  python3 scripts/build_resume.py
"""
import base64
import hashlib
import json

from theme import ASSETS, EDGE, INK, KRAFT, MANILA, PAPER, RED, ROOT, esc, svg, tag

GITHUB = "KiShOrE-2008"
GENESIS = "0" * 64

ENTRIES = [
    {"kind": "education", "when": "Sep 2025 – Aug 2029", "short": "Sep 2025",
     "title": "B.Tech Information Technology", "tag_title": "B.Tech IT",
     "org": "Chennai Institute of Technology", "tag_org": "Chennai Inst. of Technology",
     "notes": ["CGPA 7.4/10"]},
    {"kind": "experience", "when": "Jan 2026 – Mar 2026", "short": "Jan 2026",
     "title": "Ethical Hacking Intern", "tag_title": "Ethical Hacking Intern",
     "org": "EduSkills Academy (AICTE Virtual Internship), remote", "tag_org": "EduSkills Academy",
     "notes": ["Performed basic vulnerability assessment and web application penetration testing using Kali Linux and security testing tools.",
               "Studied social engineering, malware analysis, network security and common web application vulnerabilities.",
               "Completed a 10-week program and a cybersecurity capstone project."]},
    {"kind": "experience", "when": "Jun 2026", "short": "Jun 2026",
     "title": "Cyber Security Intern", "tag_title": "Cyber Security Intern",
     "org": "Amroha Police Cyber Security Internship Program (APCSIP-2026), Moradabad", "tag_org": "Amroha Police APCSIP-2026",
     "notes": ["Studied OSINT, digital and mobile forensics, Android malware, threat intelligence, MITRE ATT&CK and cyber law in sessions led by law-enforcement and industry experts.",
               "Gained exposure to forensic tools including FTK, Oxygen Forensics, Magnet Axiom and Belkasoft.",
               "Examined cybercrime cases involving UPI fraud, mule accounts and SIM-swap attacks."]},
    {"kind": "project", "when": "Jul 2026 – Sep 2026", "short": "Jul 2026", "repo": "Netscope",
     "title": "NetScope: network discovery and monitoring", "tag_title": "NetScope",
     "org": "Java 21, Spring Boot, PostgreSQL, React, WebSockets, Docker", "tag_org": "Network monitoring platform",
     "notes": ["Built a monitoring platform with ICMP and TCP subnet discovery, Nmap scanning, SNMP metrics, automated alerts and live WebSocket updates.",
               "Discovered 22 devices on a /24 test network, with 20 online and 12 reporting SNMP data.",
               "Containerized the application with Docker and tested REST APIs with JUnit and Mockito."]},
    {"kind": "project", "when": "Aug 2026", "short": "Aug 2026", "repo": "Tracex",
     "title": "Tracex: digital forensics workspace (hackathon, team of 3)", "tag_title": "Tracex",
     "org": "React, TypeScript, Leaflet", "tag_org": "Digital forensics workspace",
     "notes": ["Built a prototype that links suspects, phone numbers, accounts and locations using entity graphs, geospatial mapping and timelines.",
               "Added SHA-256 evidence hashing and a hash-chained audit log to support chain of custody."]},
    {"kind": "project", "when": "Sep 2026 – Oct 2026", "short": "Sep 2026", "repo": "iDAM",
     "title": "iDAM: parking marketplace (web and Android)", "tag_title": "iDAM",
     "org": "React, TypeScript, Capacitor, Supabase, PostgreSQL, Razorpay", "tag_org": "Parking marketplace",
     "notes": ["Built a two-sided parking marketplace with map search, time-slot booking, online payments and QR passes, shipped as a website and an Android app from one React codebase.",
               "Secured bookings, payments and payouts with row-level security and server-side functions, giving clients no write access to those tables.",
               "Implemented owner payouts through Razorpay Route, held for 24 hours after each booking ends."]},
]

SKILLS = [
    ("Languages", "Python, Java, JavaScript, TypeScript, C, C++"),
    ("Frontend", "HTML5, CSS3, React.js, Tailwind CSS, Vite, GSAP"),
    ("Backend", "Java Spring Boot, Node.js, Express.js, FastAPI, Flask, REST APIs, WebSockets"),
    ("Databases", "PostgreSQL, MongoDB, MySQL, Supabase"),
    ("Cybersecurity", "Application security, authentication and authorization, JWT, password hashing, CSRF protection, role-based access control, security auditing, Wireshark, Burp Suite"),
    ("Networking", "TCP/IP, network discovery, SNMP, Nmap, network monitoring, DNS diagnostics, network telemetry"),
    ("Mobile", "Android development with Capacitor, QR code integration, third-party API integration"),
    ("DevOps and tools", "Git, GitHub, Docker, Docker Compose, Linux, Maven, Vercel, VS Code"),
]

CERTS = [
    "Python Essentials 1 and 2, Cisco Networking Academy (2025, 2026)",
    "Introduction to Cybersecurity, Cisco (Dec 2025)",
    "Cybersecurity Job Simulation, Forage and Mastercard (May 2026)",
    "Python (Basic), HackerRank (Feb 2026)",
    "Cybersecurity Career Starter, Hack & Fix (Jan 2026)",
]

ACHIEVEMENTS = [
    "Solved 255 LeetCode problems with a contest rating of 1551 across 27 contests.",
    "Ranked Top 20 in the CyberStrike’26 CTF and Top 60 in the Into The Void CTF.",
]


def canonical(e):
    return "\n".join([e["when"], e["title"], e["org"], *e["notes"]])


def seal(entries):
    prev, chain = GENESIS, []
    for e in entries:
        text = canonical(e)
        digest = hashlib.sha256(f"{prev}\n{text}".encode()).hexdigest()
        chain.append({"text": text, "prev": prev, "hash": digest})
        prev = digest
    return chain


def hero():
    photo = base64.b64encode((ROOT / "scripts" / "photo.jpg").read_bytes()).decode()
    rows = [("Based in", "Chennai, Tamil Nadu, India"),
            ("Studying", "B.Tech IT, Chennai Institute of Technology"),
            ("Builds", "Full-stack apps, network monitors, security tools")]
    typed = "".join(
        f'<text x="72" y="{258 + i * 31}" font-size="18.5" opacity=".72">{a}</text>'
        f'<text x="176" y="{258 + i * 31}" font-size="18.5">{esc(b)}</text>'
        f'<path d="M172 {265 + i * 31}H660" stroke="{INK}" stroke-opacity=".3" stroke-dasharray="2 4"/>'
        for i, (a, b) in enumerate(rows))
    body = f"""
<path d="M18 62q0-10 10-10h14l14-38q3-8 12-8h262q9 0 12 8l14 38h586q10 0 10 10v346q0 10-10 10H28q-10 0-10-10Z" fill="{EDGE}"/>
<text x="74" y="40" class="st" font-size="23">File no. KV-2008</text>
<rect x="18" y="60" width="924" height="358" rx="10" fill="{MANILA}" filter="url(#grain)"/>
<g transform="rotate(-.5 480 240)">
<rect x="44" y="82" width="872" height="316" fill="#00000022" transform="translate(3 4)"/>
<rect x="44" y="82" width="872" height="316" fill="{PAPER}" filter="url(#grain)"/>
<text x="70" y="136" font-size="19" opacity=".72">Examiner of record</text>
<text x="68" y="222" class="st" font-size="88" letter-spacing="1">KISHORE K V</text>
{typed}
</g>
<g transform="rotate(3 800 210)">
<rect x="700" y="52" width="208" height="266" fill="#00000030" transform="translate(4 5)"/>
<rect x="700" y="52" width="208" height="266" fill="#FFFDF6"/>
<image x="712" y="64" width="184" height="236" preserveAspectRatio="xMidYMin slice" href="data:image/jpeg;base64,{photo}"/>
</g>
<path d="M758 92V30a13 13 0 0 1 26 0v74a8 8 0 0 1-16 0V40" fill="none" stroke="#68717F" stroke-width="3.5" stroke-linecap="round"/>
<g transform="translate(590 364) rotate(-3) scale(.86)"><g class="stamp">
<rect x="-188" y="-29" width="376" height="58" rx="5" fill="none" stroke="{RED}" stroke-width="4"/>
<rect x="-182" y="-23" width="364" height="46" rx="3" fill="none" stroke="{RED}" stroke-width="1.5"/>
<text class="st" y="11" font-size="31" text-anchor="middle" letter-spacing="1" style="fill:{RED}">OPEN TO INTERNSHIPS</text>
</g></g>"""
    css = """.stamp{transform-box:fill-box;transform-origin:center;opacity:.9;animation:thump .32s cubic-bezier(.3,1.4,.6,1) .5s backwards}
@keyframes thump{from{opacity:0;transform:scale(1.7)}}
@media (prefers-reduced-motion:reduce){.stamp{animation:none}}"""
    label = ("Case-file style header for Kishore K V, B.Tech IT student in Chennai, with a clipped photo "
             "and a red stamp reading open to internships.")
    return svg(960, 424, body, label, css)


def chain_svg(chain):
    tw, th, gap = 280, 176, 34
    xs = [24, 24 + tw + gap, 24 + 2 * (tw + gap)]
    pos = [(xs[0], 66), (xs[1], 66), (xs[2], 66), (xs[2], 276), (xs[1], 276), (xs[0], 276)]
    out = [f'<rect width="960" height="478" rx="10" fill="{KRAFT}" filter="url(#grain)"/>',
           f'<text x="26" y="44" class="st" font-size="27" style="fill:{PAPER}">Chain of custody</text>',
           f'<text x="934" y="43" font-size="17" text-anchor="end" style="fill:{PAPER}">Each entry seals the hash of the one before it</text>']

    def link(cx, cy, vertical=False):
        r = 90 if vertical else 0
        return (f'<g transform="translate({cx} {cy}) rotate({r})" fill="none" stroke-width="4">'
                f'<rect x="-17" y="-7" width="21" height="14" rx="7" stroke="{INK}"/>'
                f'<rect x="-4" y="-7" width="21" height="14" rx="7" stroke="{RED}"/></g>')

    for i, ((x, y), e, c) in enumerate(zip(pos, ENTRIES, chain)):
        t = x + 50
        out.append(tag(x, y, tw, th))
        out.append(f'<text x="{t}" y="{y+30}" font-size="16">Entry {i+1}, {esc(e["short"])}</text>'
                   f'<text x="{t}" y="{y+66}" class="st" font-size="{25 if len(e["tag_title"])<19 else 19.5}">{esc(e["tag_title"])}</text>'
                   f'<text x="{t}" y="{y+92}" font-size="{15 if len(e["tag_org"])<24 else 13.5}">{esc(e["tag_org"])}</text>'
                   f'<path d="M{t} {y+106}H{x+tw-14}" stroke="{INK}" stroke-opacity=".35" stroke-dasharray="2 4"/>'
                   f'<text x="{t}" y="{y+130}" font-size="16" opacity=".78">prev {c["prev"][:12]}</text>'
                   f'<text x="{t}" y="{y+154}" font-size="16" style="fill:{RED}">hash {c["hash"][:12]}</text>')
    for i in range(5):
        (ax, ay), (bx, by) = pos[i], pos[i + 1]
        if ay == by:
            out.append(link((max(ax, bx) + min(ax, bx) + tw) / 2, ay + th / 2))
        else:
            out.append(link(ax + tw / 2, ay + th + (by - ay - th) / 2, True))

    label = "Six career entries from " + ENTRIES[0]["short"] + " to " + ENTRIES[-1]["short"] + " linked as a SHA-256 hash chain."
    return svg(960, 478, "".join(out), label)


def badge(text, logo, url, color="14284B"):
    return (f'<a href="{url}"><img alt="{text}" '
            f'src="https://img.shields.io/badge/{text.replace(" ", "_")}-{color}?style=for-the-badge&logo={logo}&logoColor=E6C884"/></a>')


def entry_md(i, e, c):
    title = f'[{e["title"]}](https://github.com/{GITHUB}/{e["repo"]})' if e.get("repo") else e["title"]
    lines = [f"### {title}", "", f'{e["org"]}  ', f'{e["when"]}  ',
             f'<sub>Chain entry {i}, hash <code>{c["hash"][:12]}</code></sub>', ""]
    lines += [f"- {n}" for n in e["notes"]] + [""]
    return lines


def readme(chain):
    numbered = list(zip(range(1, len(ENTRIES) + 1), ENTRIES, chain))
    md = [
        f'<p align="center"><img src="assets/hero.svg" width="100%" alt="Kishore K V: B.Tech IT student in Chennai, building full-stack apps, network monitors and security tools. Open to internships."/></p>',
        "",
        '<p align="center">',
        badge("Portfolio", "vercel", "https://kishore-kv-portfolio.vercel.app"),
        badge("LinkedIn", "linkedin", "https://linkedin.com/in/kishore-k-v-090491349"),
        badge("Email", "gmail", "mailto:kv.kishorevijay@gmail.com"),
        "</p>",
        "",
        "B.Tech Information Technology student building full-stack web and Android applications, network monitoring tools and security software. "
        "I work with Java, Spring Boot, React, TypeScript, Python, PostgreSQL and Docker, and I have completed two cybersecurity internships. "
        "I'm looking for software development, networking or cybersecurity internships.",
        "",
        "## Career, as a hash chain",
        "",
        '<img src="assets/chain.svg" width="100%" alt="Six career entries linked as a SHA-256 hash chain, from B.Tech IT in September 2025 to iDAM in September 2026."/>',
        "",
        "Tracex keeps its audit log tamper-evident by hashing each record together with the one before it, so I did the same with this resume. "
        "Change one word in any entry and every later hash stops matching. "
        "Run `python3 scripts/verify_chain.py` to check it yourself.",
        "",
        "## GitHub stats",
        "",
        "<table>",
        "<tr>",
        '<td width="50%"><img src="assets/stats/activity.svg" width="100%" alt="GitHub activity totals"/></td>',
        '<td width="50%"><img src="assets/stats/streak.svg" width="100%" alt="Contribution streaks"/></td>',
        "</tr>",
        "<tr>",
        '<td width="50%"><img src="assets/stats/languages.svg" width="100%" alt="Most used languages"/></td>',
        '<td width="50%"><img src="assets/stats/recent.svg" width="100%" alt="Daily contributions over the last 30 days"/></td>',
        "</tr>",
        "</table>",
        "",
        '<img src="assets/stats/heatmap.svg" width="100%" alt="Contribution heatmap for the last year"/>',
        "",
        "## Experience",
        "",
    ]
    for i, e, c in numbered:
        if e["kind"] == "experience":
            md += entry_md(i, e, c)
    md += ["## Projects", ""]
    for i, e, c in reversed(numbered):
        if e["kind"] == "project":
            md += entry_md(i, e, c)
    md += ["## Education", ""]
    for i, e, c in numbered:
        if e["kind"] == "education":
            md += [f'**{e["org"]}**  ', f'{e["title"]}, {e["when"]}, {e["notes"][0]}  ',
                   f'<sub>Chain entry {i}, hash <code>{c["hash"][:12]}</code></sub>', ""]
    md += ["## Skills", "", "| | |", "|---|---|"]
    md += [f"| **{a}** | {b} |" for a, b in SKILLS]
    md += ["", "## Certifications", ""] + [f"- {c}" for c in CERTS]
    md += ["", "## Achievements", ""] + [f"- {a}" for a in ACHIEVEMENTS] + [""]
    return "\n".join(md)


def main():
    chain = seal(ENTRIES)
    ASSETS.mkdir(exist_ok=True)
    (ASSETS / "hero.svg").write_text(hero())
    (ASSETS / "chain.svg").write_text(chain_svg(chain))
    (ROOT / "chain.json").write_text(json.dumps(chain, indent=2, ensure_ascii=False) + "\n")
    # Legacy generator commented out to preserve the redesigned README.md:
    # (ROOT / "README.md").write_text(readme(chain))


if __name__ == "__main__":
    main()
