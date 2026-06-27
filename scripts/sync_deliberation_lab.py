# -*- coding: utf-8 -*-
"""Sync deliberation_lab audit exports into the Quarto website section."""
from __future__ import annotations

import re

FULL_NAME_MAP = {
    "Nora Varela": "Amélie Maturana",
    "Ian Mercado": "Humberto Parra",
    "Tomas Echeverria": "Nicanor Bolaño",
    "Faye Lin": "Roberto Nothomb",
    "Sima Rao": "Oleo Cebaroa",
}
FIRST_NAME_MAP = {
    "Nora": "Amélie", "Ian": "Humberto", "Tomas": "Nicanor",
    "Faye": "Roberto", "Sima": "Oleo",
}
LAST_NAME_MAP = {
    "Varela": "Maturana", "Mercado": "Parra", "Echeverria": "Bolaño",
    "Lin": "Nothomb", "Rao": "Cebaroa",
}


def _apply(mapping: dict[str, str], text: str) -> str:
    for old, new in mapping.items():
        text = re.sub(r"\b" + re.escape(old) + r"\b", new, text)
    return text


def rename(text: str) -> str:
    text = _apply(FULL_NAME_MAP, text)
    text = _apply(FIRST_NAME_MAP, text)
    text = _apply(LAST_NAME_MAP, text)
    return text


LANGS = {
    "en": {
        "base": "/projects/deliberation-lab",
        "switch": ("Español", "/projects/deliberation-lab/es/index.html"),
        "tabs": [
            ("about", "About", "index.html"),
            ("statements", "Statements", "statements/index.html"),
            ("conversations", "Conversations", "conversations.html"),
            ("reflections", "Reflections", "reflections.html"),
            ("profiles", "Profiles", "profiles.html"),
        ],
        "titles": {"conversations": "Conversations", "reflections": "Reflections",
                   "profiles": "Profiles", "statement": "Joint statement"},
    },
    "es": {
        "base": "/projects/deliberation-lab/es",
        "switch": ("English", "/projects/deliberation-lab/index.html"),
        "tabs": [
            ("about", "Inicio", "index.html"),
            ("statements", "Declaraciones", "statements/index.html"),
            ("conversations", "Conversaciones", "conversations.html"),
            ("reflections", "Reflexiones", "reflections.html"),
            ("profiles", "Perfiles", "profiles.html"),
        ],
        "titles": {"conversations": "Conversaciones", "reflections": "Reflexiones",
                   "profiles": "Perfiles", "statement": "Declaración conjunta"},
    },
}


def nav_bar(active_id: str, lang: str) -> str:
    cfg = LANGS[lang]
    items = []
    for tid, label, href in cfg["tabs"]:
        cls = "nav-link active" if tid == active_id else "nav-link"
        items.append(
            f'<li class="nav-item"><a class="{cls}" href="{cfg["base"]}/{href}">{label}</a></li>'
        )
    sw_label, sw_href = cfg["switch"]
    items.append(
        f'<li class="nav-item" style="margin-left:auto;"><a class="nav-link" href="{sw_href}">{sw_label}</a></li>'
    )
    return '<ul class="nav nav-pills" style="margin-bottom:1.5rem;">' + "".join(items) + "</ul>\n\n"


def front_matter(title: str, date: str | None = None) -> str:
    lines = ["---", f'title: "{title}"']
    if date:
        lines.append(f'date: "{date}"')
    lines += ["---", "", ""]
    return "\n".join(lines)


def strip_h1_and_intro(md: str) -> str:
    idx = md.find("\n## ")
    if idx == -1:
        return md.strip() + "\n"
    return md[idx + 1:].strip() + "\n"


def build_page(title: str, active_id: str, lang: str, body: str,
               date: str | None = None, banner: str | None = None) -> str:
    parts = [front_matter(title, date), nav_bar(active_id, lang)]
    if banner:
        parts.append("::: {.callout-note}\n" + banner + "\n:::\n\n")
    parts.append(body)
    return "".join(parts)


def parse_joint_statements(md: str) -> list[dict]:
    blocks = re.split(r"(?=^## joint_\d+)", md, flags=re.M)
    stmts = []
    for b in blocks:
        m = re.match(r"## (joint_\d+)", b)
        if not m:
            continue
        pub = re.search(r"Published at:\s*(\S+)", b)
        stmts.append({
            "id": m.group(1),
            "published_at": pub.group(1) if pub else None,
            "body": b.strip(),
        })
    return stmts


def statement_slug(stmt: dict) -> str:
    date = (stmt["published_at"] or "0000-00-00")[:10]
    num = stmt["id"].replace("joint_", "")
    return f"{date}-joint-{num}"


_REGENDER_SUBS = [
    (r"\bShe\b", "He"), (r"\bshe\b", "he"),
    (r"\bHerself\b", "Himself"), (r"\bherself\b", "himself"),
    (r"\bHer\b", "His"), (r"\bher\b", "his"),
]


def regender(text: str) -> str:
    for pat, rep in _REGENDER_SUBS:
        text = re.sub(pat, rep, text)
    return text


def regender_phenomenologist(profiles_md: str) -> str:
    parts = re.split(r"(?=^## )", profiles_md, flags=re.M)
    out = []
    for p in parts:
        if p.startswith("## Roberto Nothomb"):
            p = regender(p)
        out.append(p)
    return "".join(out)


def wrap_tabset(body: str) -> str:
    return "::: {.panel-tabset}\n\n" + body.strip() + "\n\n:::\n"


def style_conversation(md: str) -> str:
    blocks = re.split(r"(?=^## turn_)", md, flags=re.M)
    out = []
    for b in blocks:
        m = re.match(r"## turn_\d+ \| Round (\d+) \| (.+)", b)
        if not m:
            continue
        round_no = m.group(1)
        speaker = m.group(2).strip()
        role_m = re.search(r"^- Role:\s*(.+)$", b, flags=re.M)
        role = role_m.group(1).strip() if role_m else ""
        body = re.sub(r"^## turn_.*\n", "", b, count=1, flags=re.M)
        body = re.sub(r"^- Role:.*\n", "", body, count=1, flags=re.M)
        body = re.sub(r"^- Created at:.*\n", "", body, count=1, flags=re.M)
        body = body.strip()
        if role == "joint_statement" or speaker.lower() == "public":
            out.append(f'::: {{.callout-note title="Joint statement · Round {round_no}"}}\n{body}\n:::\n')
        else:
            out.append(f"### {speaker} · Round {round_no}\n\n*{role}*\n\n{body}\n\n---\n")
    return "\n".join(out) + "\n"


import argparse
from pathlib import Path


def _read(p: Path) -> str:
    return Path(p).read_text(encoding="utf-8")


def _write(p: Path, text: str) -> None:
    p = Path(p)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


def sync(from_dir, out_dir, lang: str = "en", banner: str | None = None) -> None:
    from_dir = Path(from_dir)
    out_dir = Path(out_dir)
    t = LANGS[lang]["titles"]

    _write(out_dir / "conversations.qmd",
           build_page(t["conversations"], "conversations", lang,
                      style_conversation(rename(_read(from_dir / "public_deliberations.md"))),
                      banner=banner))

    _write(out_dir / "reflections.qmd",
           build_page(t["reflections"], "reflections", lang,
                      wrap_tabset(strip_h1_and_intro(rename(_read(from_dir / "private_reflections.md")))),
                      banner=banner))

    _write(out_dir / "profiles.qmd",
           build_page(t["profiles"], "profiles", lang,
                      wrap_tabset(strip_h1_and_intro(regender_phenomenologist(rename(_read(from_dir / "agent_profiles.md"))))),
                      banner=banner))

    joint = rename(_read(from_dir / "joint_statements.md"))
    for stmt in parse_joint_statements(joint):
        dest = out_dir / "statements" / statement_slug(stmt) / "index.qmd"
        if dest.exists():
            continue
        date = (stmt["published_at"] or "")[:10] or None
        title = f'{t["statement"]} — {date}' if date else t["statement"]
        _write(dest, build_page(title, "statements", lang, stmt["body"] + "\n",
                                date=date, banner=banner))


def main(argv=None) -> None:
    ap = argparse.ArgumentParser(description="Sync deliberation_lab exports into the website.")
    ap.add_argument("--from", dest="from_dir", type=Path,
                    default=Path("../deliberation_lab/exports/clean_joint_real"))
    ap.add_argument("--out", dest="out_dir", type=Path,
                    default=Path("projects/deliberation-lab"))
    ap.add_argument("--lang", choices=["en", "es"], default="en")
    ap.add_argument("--banner", default=None)
    args = ap.parse_args(argv)
    sync(args.from_dir, args.out_dir, lang=args.lang, banner=args.banner)
    print(f"synced [{args.lang}] {args.from_dir} -> {args.out_dir}")


if __name__ == "__main__":
    main()
