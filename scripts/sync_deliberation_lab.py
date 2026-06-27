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
