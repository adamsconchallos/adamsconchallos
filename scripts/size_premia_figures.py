"""Build the HTML/CSS figures for the Size Premia policy summary (ES and EN).

Run from the repository root:
    python scripts/size_premia_figures.py

Writes include files (_fig-*.md) and figs.css into
research/articles/ceballos-2026-size-premia/.

Data provenance (Straume and Ceballos-Concha, accepted manuscript v1, Nov 2026):
- VALUE: Table 1, export value in million USD by size category, 2012-2025.
- PREMIA: Table 2, baseline model, log-price coefficients and standard errors.
  Percent premia follow equation (2) of the paper, 100*(exp(b)-1), with 95%
  intervals 100*(exp(b -/+ 1.96*se)-1).
- MARKETS: Figure 4, destination shares of export value by size (fresh whole
  salmon). Read from the vector geometry of the figure's EMF file. The implied
  destination totals reproduce Table 5 (Brazil 7404, USA 2239, China 1341,
  Argentina 409 million USD) to within 1 million USD.
"""
from math import exp
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "research" / "articles" / "ceballos-2026-size-premia"

# ---------------------------------------------------------------- data
VALUE = {
    "whole": [("2-3", 592), ("3-4", 910), ("4-5", 2448), ("5-6", 3050), ("6-7", 2645), ("7+", 2334)],
    "fillet": [("0.5-1.0", 2026), ("1.0-1.5", 12214), ("1.5-2.0", 11902), ("2.0+", 3565)],
}
HIGHLIGHT = {"whole": {"4-5", "5-6", "6-7"}, "fillet": {"1.0-1.5", "1.5-2.0"}}

PREMIA = {  # (size, coefficient, standard error); None marks the reference size
    "whole": [("2-3", -0.013, 0.004), ("3-4", -0.002, 0.004), ("4-5", 0.003, 0.002),
              ("5-6", None, None), ("6-7", 0.015, 0.003), ("7+", 0.016, 0.003)],
    "fillet": [("0.5-1.0", -0.073, 0.003), ("1.0-1.5", None, None),
               ("1.5-2.0", 0.025, 0.002), ("2.0+", 0.010, 0.002)],
}

MARKET_ORDER = ["Brazil", "USA", "China", "Argentina", "Other"]
MARKETS = {  # percent of each size's export value, fresh whole salmon
    "2-3": [54.76, 12.10, 9.10, 13.69, 10.35],
    "3-4": [76.18, 16.50, 0.60, 3.53, 3.19],
    "4-5": [73.00, 13.93, 1.19, 6.16, 5.72],
    "5-6": [55.81, 21.18, 13.26, 2.84, 6.92],
    "6-7": [49.05, 23.16, 23.05, 1.30, 3.44],
    "7+": [68.57, 17.94, 10.19, 1.02, 2.29],
}
MARKET_CLASS = ["m-bra", "m-usa", "m-chn", "m-arg", "m-oth"]

# ---------------------------------------------------------------- text
T = {
    "es": {
        "whole": "Salmón entero", "fillet": "Filetes",
        "markets": {"Brazil": "Brasil", "USA": "Estados Unidos", "China": "China",
                    "Argentina": "Argentina", "Other": "Otros"},
        "fig1_title": "Figura 1. El valor exportado se concentra en los tamaños intermedios",
        "fig1_sub": "Participación de cada tamaño en el valor exportado de salmón fresco, 2012–2025. "
                    "En azul, los tamaños intermedios.",
        "fig1_src": "Fuente: Straume y Ceballos-Concha (en prensa), tabla 1, con datos de aduanas de Chile.",
        "fig1_cols": ["Producto", "Tamaño", "Millones de USD", "Participación"],
        "of_value": "del valor",
        "musd": "millones de USD",
        "fig2_title": "Figura 2. En los filetes, el tamaño pesa más en el precio",
        "fig2_sub": "Diferencia de precio respecto del tamaño de referencia, en %. "
                    "Las líneas muestran el intervalo de confianza de 95%.",
        "fig2_src": "Fuente: Straume y Ceballos-Concha (en prensa), tabla 2. Compara envíos de la misma "
                    "empresa, al mismo destino y en el mismo mes.",
        "fig2_cols": ["Producto", "Tamaño", "Diferencia de precio", "Intervalo de 95%"],
        "premium": "Premio", "discount": "Descuento", "ns": "Diferencia no significativa",
        "ref": "Tamaño de referencia", "ref_short": "referencia",
        "fig3_title": "Figura 3. Cada mercado compra tamaños distintos",
        "fig3_sub": "Participación de cada destino en el valor exportado de salmón entero fresco, "
                    "por tamaño, 2012–2025.",
        "fig3_src": "Fuente: elaboración propia a partir de la figura 4 de Straume y Ceballos-Concha (en prensa).",
        "fig3_cols": ["Tamaño", "Brasil", "Estados Unidos", "China", "Argentina", "Otros"],
        "see_data": "Ver los datos",
        "size": "Tamaño",
    },
    "en": {
        "whole": "Whole salmon", "fillet": "Fillets",
        "markets": {"Brazil": "Brazil", "USA": "United States", "China": "China",
                    "Argentina": "Argentina", "Other": "Other"},
        "fig1_title": "Figure 1. Export value is concentrated in intermediate sizes",
        "fig1_sub": "Share of each size in the export value of fresh salmon, 2012–2025. "
                    "Intermediate sizes in blue.",
        "fig1_src": "Source: Straume and Ceballos-Concha (forthcoming), Table 1, based on Chilean customs data.",
        "fig1_cols": ["Product", "Size", "Million USD", "Share"],
        "of_value": "of value",
        "musd": "million USD",
        "fig2_title": "Figure 2. For fillets, size matters more for the price",
        "fig2_sub": "Price difference relative to the reference size, in %. "
                    "Lines show the 95% confidence interval.",
        "fig2_src": "Source: Straume and Ceballos-Concha (forthcoming), Table 2. Compares shipments by the "
                    "same exporter, to the same destination, in the same month.",
        "fig2_cols": ["Product", "Size", "Price difference", "95% interval"],
        "premium": "Premium", "discount": "Discount", "ns": "Not statistically significant",
        "ref": "Reference size", "ref_short": "reference",
        "fig3_title": "Figure 3. Each market buys different sizes",
        "fig3_sub": "Share of each destination in the export value of fresh whole salmon, "
                    "by size, 2012–2025.",
        "fig3_src": "Source: own elaboration based on Figure 4 in Straume and Ceballos-Concha (forthcoming).",
        "fig3_cols": ["Size", "Brazil", "United States", "China", "Argentina", "Other"],
        "see_data": "Show the data",
        "size": "Size",
    },
}


# ---------------------------------------------------------------- helpers
def num(v, lang, dec=1):
    s = f"{v:,.{dec}f}"
    if lang == "es":
        s = s.replace(",", "_").replace(".", ",").replace("_", ".")
    return s


def signed(v, lang, dec=1):
    s = num(abs(v), lang, dec)
    return ("+" if v > 0 else "−" if v < 0 else "") + s + "%"


def size_label(code, lang):
    s = code.replace("-", "–") + " kg"
    return s.replace(".", ",") if lang == "es" else s


def half_up(v):
    return int(v + 0.5)


def wrap(html):
    return "```{=html}\n" + html.strip() + "\n```\n"


def details(lang, cols, rows):
    head = "".join(f"<th scope=\"col\">{c}</th>" for c in cols)
    body = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return (f"<details class=\"sp-data\"><summary>{T[lang]['see_data']}</summary>"
            f"<table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></details>")


# ---------------------------------------------------------------- figure 1
def fig_value(lang):
    t = T[lang]; scale = 55.0; panels = []; rows_tbl = []
    for prod in ("whole", "fillet"):
        total = sum(v for _, v in VALUE[prod])
        rows = []
        for code, v in VALUE[prod]:
            share = 100 * v / total; lab = size_label(code, lang)
            hi = " sp-hi" if code in HIGHLIGHT[prod] else ""
            tip = f"{t[prod]}, {lab}: {num(share, lang)}% {t['of_value']} ({num(v, lang, 0)} {t['musd']})"
            rows.append(
                f"<div class=\"sp-row\" tabindex=\"0\" title=\"{tip}\" aria-label=\"{tip}\">"
                f"<span class=\"sp-lab\">{lab}</span>"
                f"<span class=\"sp-track\"><span class=\"sp-bar{hi}\" style=\"width:{share / scale * 100:.2f}%\"></span>"
                f"<span class=\"sp-val\">{num(share, lang)}%</span></span></div>")
            rows_tbl.append([t[prod], lab, num(v, lang, 0), num(share, lang) + "%"])
        panels.append(f"<div class=\"sp-panel\"><p class=\"sp-ptitle\">{t[prod]}</p>{''.join(rows)}</div>")
    return wrap(
        f"<figure class=\"sp-fig\"><figcaption><p class=\"sp-title\">{t['fig1_title']}</p>"
        f"<p class=\"sp-sub\">{t['fig1_sub']}</p></figcaption>"
        f"<div class=\"sp-panels\">{''.join(panels)}</div>"
        f"<p class=\"sp-src\">{t['fig1_src']}</p>{details(lang, t['fig1_cols'], rows_tbl)}</figure>")


# ---------------------------------------------------------------- figure 2
LO, HI = -8.0, 3.0
TICKS = [-8, -6, -4, -2, 0, 2]


def xpos(v):
    return (v - LO) / (HI - LO) * 100


def fig_premia(lang):
    t = T[lang]; panels = []; rows_tbl = []
    grid = "".join(f"<span class=\"sp-grid{' sp-zero' if k == 0 else ''}\" style=\"left:{xpos(k):.2f}%\"></span>"
                   for k in TICKS)
    axis = "".join(f"<span class=\"sp-tick\" style=\"left:{xpos(k):.2f}%\">{signed(k, lang, 0) if k else '0'}</span>"
                   for k in TICKS)
    for prod in ("whole", "fillet"):
        rows = []
        for code, b, se in PREMIA[prod]:
            lab = size_label(code, lang)
            if b is None:
                tip = f"{t[prod]}, {lab}: {t['ref']}"
                mark = (f"<span class=\"sp-ring\" style=\"left:{xpos(0):.2f}%\"></span>"
                        f"<span class=\"sp-dlab\" style=\"left:{xpos(0):.2f}%\">{t['ref_short']}</span>")
                rows_tbl.append([t[prod], lab, t["ref"], "–"])
            else:
                p = 100 * (exp(b) - 1); lo = 100 * (exp(b - 1.96 * se) - 1); hi = 100 * (exp(b + 1.96 * se) - 1)
                cls = "sp-ns" if lo < 0 < hi else ("sp-pos" if p > 0 else "sp-neg")
                ci = f"{signed(lo, lang)} {'a' if lang == 'es' else 'to'} {signed(hi, lang)}"
                tip = f"{t[prod]}, {lab}: {signed(p, lang)} ({ci})"
                x = xpos(p); align = "sp-al" if x < 12 else ("sp-ar" if x > 88 else "")
                mark = (f"<span class=\"sp-ci {cls}\" style=\"left:{xpos(lo):.2f}%;width:{xpos(hi) - xpos(lo):.2f}%\"></span>"
                        f"<span class=\"sp-dot {cls}\" style=\"left:{x:.2f}%\"></span>"
                        f"<span class=\"sp-dlab {align}\" style=\"left:{x:.2f}%\">{signed(p, lang)}</span>")
                rows_tbl.append([t[prod], lab, signed(p, lang), ci])
            rows.append(
                f"<div class=\"sp-drow\" tabindex=\"0\" title=\"{tip}\" aria-label=\"{tip}\">"
                f"<span class=\"sp-lab\">{lab}</span><span class=\"sp-plot\">{grid}{mark}</span></div>")
        rows.append(f"<div class=\"sp-drow sp-axis\" aria-hidden=\"true\"><span class=\"sp-lab\"></span>"
                    f"<span class=\"sp-plot\">{axis}</span></div>")
        panels.append(f"<div class=\"sp-panel sp-full\"><p class=\"sp-ptitle\">{t[prod]}</p>{''.join(rows)}</div>")
    legend = (f"<ul class=\"sp-legend\"><li><span class=\"sp-key sp-pos\"></span>{t['premium']}</li>"
              f"<li><span class=\"sp-key sp-neg\"></span>{t['discount']}</li>"
              f"<li><span class=\"sp-key sp-ns\"></span>{t['ns']}</li>"
              f"<li><span class=\"sp-key sp-keyring\"></span>{t['ref']}</li></ul>")
    return wrap(
        f"<figure class=\"sp-fig\"><figcaption><p class=\"sp-title\">{t['fig2_title']}</p>"
        f"<p class=\"sp-sub\">{t['fig2_sub']}</p></figcaption>{legend}"
        f"<div class=\"sp-panels\">{''.join(panels)}</div>"
        f"<p class=\"sp-src\">{t['fig2_src']}</p>{details(lang, t['fig2_cols'], rows_tbl)}</figure>")


# ---------------------------------------------------------------- figure 3
def fig_markets(lang):
    t = T[lang]; rows = []; rows_tbl = []
    names = [t["markets"][m] for m in MARKET_ORDER]
    for code, shares in MARKETS.items():
        lab = size_label(code, lang); segs = []
        for name, cls, s in zip(names, MARKET_CLASS, shares):
            tip = f"{lab}, {name}: {num(s, lang)}%"
            inner = f"{half_up(s)}%" if s >= 12 else ""
            segs.append(f"<span class=\"sp-seg {cls}\" style=\"flex:{s:.2f} 1 0\" tabindex=\"0\" "
                        f"title=\"{tip}\" aria-label=\"{tip}\">{inner}</span>")
        rows.append(f"<div class=\"sp-srow\"><span class=\"sp-lab\">{lab}</span>"
                    f"<span class=\"sp-stack\">{''.join(segs)}</span></div>")
        rows_tbl.append([lab] + [num(s, lang) + "%" for s in shares])
    legend = "<ul class=\"sp-legend\">" + "".join(
        f"<li><span class=\"sp-key sp-sq {cls}\"></span>{n}</li>" for n, cls in zip(names, MARKET_CLASS)) + "</ul>"
    return wrap(
        f"<figure class=\"sp-fig\"><figcaption><p class=\"sp-title\">{t['fig3_title']}</p>"
        f"<p class=\"sp-sub\">{t['fig3_sub']}</p></figcaption>{legend}"
        f"<div class=\"sp-stacks\">{''.join(rows)}</div>"
        f"<p class=\"sp-src\">{t['fig3_src']}</p>{details(lang, t['fig3_cols'], rows_tbl)}</figure>")


CSS = """/* Figures for the Size Premia policy summary. Generated by scripts/size_premia_figures.py */
.sp-fig {
  --sp-surface: #ffffff;
  --sp-ink: #0b0b0b; --sp-ink-2: #52514e; --sp-muted: #898781;
  --sp-grid: #e1e0d9; --sp-base: #c3c2b7; --sp-track: #f3f2ee;
  --sp-hi: #2a78d6; --sp-lo: #c3c2b7;
  --sp-pos: #2a78d6; --sp-neg: #e34948; --sp-ns: #898781;
  --sp-bra: #2a78d6; --sp-usa: #eb6834; --sp-chn: #1baf7a; --sp-arg: #eda100; --sp-oth: #c3c2b7;
  margin: 2rem 0; color: var(--sp-ink); font-size: 0.9rem; max-width: 100%; min-width: 0;
}
.sp-fig figcaption { margin-bottom: .75rem; color: var(--sp-ink); font-size: inherit; text-align: left; }
.sp-title { font-weight: 600; margin: 0 0 .2rem; font-size: 1rem; color: var(--sp-ink); }
.sp-sub, .sp-src { color: var(--sp-ink-2); margin: 0; font-size: .85rem; }
.sp-src { margin-top: .75rem; }
.sp-panels { display: flex; flex-wrap: wrap; gap: 1rem 2rem; }
.sp-panel { flex: 1 1 260px; min-width: 0; }
.sp-panel.sp-full { flex-basis: 100%; }
.sp-ptitle { font-weight: 600; margin: 0 0 .35rem; font-size: .9rem; }
.sp-lab { color: var(--sp-ink-2); font-variant-numeric: tabular-nums; white-space: nowrap; }
/* figure 1: bars */
.sp-row { display: grid; grid-template-columns: 6.2em 1fr; align-items: center; height: 30px; outline-offset: 2px; }
.sp-track { position: relative; display: flex; align-items: center; height: 100%; }
.sp-bar { display: block; height: 18px; background: var(--sp-lo); border-radius: 0 4px 4px 0; }
.sp-bar.sp-hi { background: var(--sp-hi); }
.sp-val { margin-left: .4em; font-variant-numeric: tabular-nums; color: var(--sp-ink); }
.sp-row:hover .sp-bar, .sp-row:focus .sp-bar { filter: brightness(1.12); }
/* figure 2: dots and intervals */
.sp-drow { display: grid; grid-template-columns: 6.2em 1fr; align-items: stretch; height: 40px; }
.sp-drow.sp-axis { height: 22px; }
.sp-drow .sp-lab { align-self: end; padding-bottom: 3px; }
.sp-plot { position: relative; margin: 0 .6em; }
.sp-grid { position: absolute; top: 0; bottom: 0; width: 1px; background: var(--sp-grid); }
.sp-grid.sp-zero { background: var(--sp-muted); }
.sp-ci { position: absolute; top: 27px; height: 2px; border-radius: 1px; }
.sp-dot, .sp-ring { position: absolute; top: 28px; width: 10px; height: 10px; border-radius: 50%;
  transform: translate(-50%, -50%); box-shadow: 0 0 0 2px var(--sp-surface); }
.sp-ring { background: var(--sp-surface); border: 2px solid var(--sp-muted); box-shadow: none; }
.sp-ci.sp-pos, .sp-dot.sp-pos { background: var(--sp-pos); }
.sp-ci.sp-neg, .sp-dot.sp-neg { background: var(--sp-neg); }
.sp-ci.sp-ns, .sp-dot.sp-ns { background: var(--sp-ns); }
.sp-dlab { position: absolute; top: 2px; transform: translateX(-50%); font-size: .8rem; white-space: nowrap;
  font-variant-numeric: tabular-nums; color: var(--sp-ink); background: var(--sp-surface); padding: 0 2px; }
.sp-dlab.sp-al { transform: translateX(-6px); }
.sp-dlab.sp-ar { transform: translateX(calc(-100% + 6px)); }
.sp-tick { position: absolute; top: 2px; transform: translateX(-50%); font-size: .75rem; color: var(--sp-muted);
  font-variant-numeric: tabular-nums; }
.sp-drow:hover .sp-dot, .sp-drow:focus .sp-dot { width: 12px; height: 12px; }
/* figure 3: stacked bars */
.sp-stacks { display: flex; flex-direction: column; gap: 8px; }
.sp-srow { display: grid; grid-template-columns: 4.2em 1fr; align-items: center; }
.sp-stack { display: flex; gap: 2px; height: 28px; }
.sp-seg { min-width: 0; display: flex; align-items: center; padding-left: 5px; font-size: .75rem;
  font-variant-numeric: tabular-nums; color: #ffffff; white-space: nowrap; overflow: visible; }
.sp-seg:first-child { border-radius: 4px 0 0 4px; }
.sp-seg:last-child { border-radius: 0 4px 4px 0; }
.sp-seg:hover, .sp-seg:focus { filter: brightness(1.12); }
.m-bra { background: var(--sp-bra); } .m-usa { background: var(--sp-usa); }
.m-chn { background: var(--sp-chn); } .m-arg { background: var(--sp-arg); color: #0b0b0b; }
.m-oth { background: var(--sp-oth); color: #0b0b0b; }
/* legend and data table */
.sp-legend { list-style: none; padding: 0; margin: 0 0 .75rem; display: flex; flex-wrap: wrap; gap: .25rem 1rem;
  color: var(--sp-ink-2); font-size: .85rem; }
.sp-legend li { display: flex; align-items: center; gap: .4em; }
.sp-key { display: inline-block; width: 10px; height: 10px; border-radius: 50%; }
.sp-key.sp-pos { background: var(--sp-pos); } .sp-key.sp-neg { background: var(--sp-neg); }
.sp-key.sp-ns { background: var(--sp-ns); }
.sp-key.sp-keyring { border: 2px solid var(--sp-muted); background: var(--sp-surface); }
.sp-key.sp-sq { border-radius: 2px; width: 12px; height: 12px; }
.sp-data { margin-top: .5rem; font-size: .85rem; max-width: 100%; overflow-x: auto; }
.sp-data summary { cursor: pointer; color: var(--sp-ink-2); }
.sp-data table { margin-top: .5rem; border-collapse: collapse; font-variant-numeric: tabular-nums; }
.sp-data th, .sp-data td { padding: .2rem .75rem .2rem 0; text-align: left; border-bottom: 1px solid var(--sp-grid); }
"""


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "figs.css").write_text(CSS, encoding="utf-8")
    for lang in ("es", "en"):
        (OUT / f"_fig-valor-{lang}.md").write_text(fig_value(lang), encoding="utf-8")
        (OUT / f"_fig-premios-{lang}.md").write_text(fig_premia(lang), encoding="utf-8")
        (OUT / f"_fig-mercados-{lang}.md").write_text(fig_markets(lang), encoding="utf-8")
    print("wrote figures to", OUT)


if __name__ == "__main__":
    main()
