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
