"""Build the HTML/CSS figures for the Trade Costs policy summary (ES and EN).

Run from the repository root:
    python scripts/trade_costs_figures.py

Writes include files (_fig-*.md) and figs.css into
research/articles/ceballos-2026-trade-costs/.

Every number comes from the text of the published article
(Ceballos-Concha et al., 2026, Aquaculture Economics & Management 30(2): 348-380):
- TILES: export value USD 5.97 billion in 2024, fourfold real increase over 2002 (p. 352);
  exports to Brazil by road up nearly 22-fold since 2002, USD 904 million in 2024 (p. 356);
  combined US and Japan value share 85.5% in 2002 and 57.1% in 2024 (p. 353).
- ROUTES: product-form and transport shares for the US, Japan, and Brazil (p. 355, Figure 4).
- TIMELINE: ISA 2007-2010 (pp. 351, 354), Russian embargo 2014 (pp. 353-354),
  COVID-19 2020-2021 (p. 354).
- MAP: destinos-2024.json, Chilean customs data for 2024 aggregated by
  scripts/trade_costs_map_data.py. Drawn in the browser by mapa.js.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from size_premia_figures import CSS as BASE_CSS, num, wrap  # noqa: E402

OUT = Path(__file__).resolve().parent.parent / "research" / "articles" / "ceballos-2026-trade-costs"

ROUTES = [  # market, [(label key, share)], [(label key, share)]
    ("usa", [("fresh_fillet", 81.5)], [("air", 75.7)]),
    ("jpn", [("frozen_whole", 67.7), ("frozen_fillet", 32.0)], [("sea", 99.9)]),
    ("bra", [("fresh_whole", 89.2)], [("land", 98.4)]),
]

T = {
    "es": {
        "tiles_title": "Figura 2. El salmón chileno en tres cifras",
        "tiles": [
            ("4×", "creció el valor exportado entre 2002 y 2024, en términos reales. "
                   "En 2024 llegó a USD 5.970 millones."),
            ("22×", "creció la exportación por camión a Brasil desde 2002. "
                    "En 2024 llegó a USD 904 millones."),
            ("85,5% → 57,1%", "cayó la participación conjunta de Estados Unidos y Japón "
                              "en el valor exportado entre 2002 y 2024."),
        ],
        "tiles_src": "Fuente: Ceballos-Concha et al. (2026), con datos de aduanas de Chile.",
        "routes_title": "Figura 3. Tres mercados, tres rutas",
        "routes_sub": "Qué producto compra cada mercado y cómo llega. Porcentajes del valor exportado típico "
                      "del período 2002–2024.",
        "routes_src": "Fuente: Ceballos-Concha et al. (2026), figura 4, calculada con valores medianos del período. "
                      "Por eso difiere de las cifras de 2024 del mapa.",
        "markets": {"usa": "Estados Unidos", "jpn": "Japón", "bra": "Brasil"},
        "product": "Producto", "transport": "Transporte",
        "labels": {"fresh_fillet": "Filete fresco", "frozen_whole": "Congelado entero",
                   "frozen_fillet": "Filete congelado", "fresh_whole": "Fresco entero",
                   "air": "Por avión", "sea": "Por barco", "land": "Por camión"},
        "routes_cols": ["Mercado", "Dimensión", "Categoría", "Participación"],
        "tl_title": "Figura 4. Ante las crisis, Chile reasignó sus exportaciones",
        "tl_sub": "Principales crisis del período y cómo respondieron los exportadores.",
        "tl_src": "Fuente: Ceballos-Concha et al. (2026).",
        "timeline": [
            ("2007–2010", "Virus ISA",
             "La producción de salmón Atlántico cae cerca de 80%. Los peces se cosechan más pequeños.",
             "El salmón fresco entero se va a Brasil en camión. Brasil pasa a ser el tercer mercado."),
            ("2014", "Embargo ruso",
             "Rusia cierra su mercado a los productos del mar de Noruega y otros países occidentales.",
             "Chile envía salmón congelado por barco. Rusia llega a 9,2% del valor exportado."),
            ("2020–2021", "Pandemia de COVID-19",
             "Hay problemas de operación, ausentismo y caídas de ventas.",
             "El orden de los principales mercados no cambia."),
        ],
        "shock": "Crisis", "response": "Respuesta",
        "see_data": "Ver los datos",
    },
    "en": {
        "tiles_title": "Figure 2. Chilean salmon in three numbers",
        "tiles": [
            ("4×", "real growth in export value between 2002 and 2024. "
                   "In 2024 it reached USD 5.97 billion."),
            ("22×", "growth in exports by truck to Brazil since 2002. "
                    "In 2024 they reached USD 904 million."),
            ("85.5% → 57.1%", "decline in the combined share of the United States and Japan "
                              "in export value between 2002 and 2024."),
        ],
        "tiles_src": "Source: Ceballos-Concha et al. (2026), based on Chilean customs data.",
        "routes_title": "Figure 3. Three markets, three routes",
        "routes_sub": "What each market buys and how it gets there. Shares of typical export value "
                      "over 2002–2024.",
        "routes_src": "Source: Ceballos-Concha et al. (2026), Figure 4, based on median values for the period. "
                      "This is why it differs from the 2024 figures in the map.",
        "markets": {"usa": "United States", "jpn": "Japan", "bra": "Brazil"},
        "product": "Product", "transport": "Transport",
        "labels": {"fresh_fillet": "Fresh fillet", "frozen_whole": "Frozen whole",
                   "frozen_fillet": "Frozen fillet", "fresh_whole": "Fresh whole",
                   "air": "By air", "sea": "By sea", "land": "By truck"},
        "routes_cols": ["Market", "Dimension", "Category", "Share"],
        "tl_title": "Figure 4. In each crisis, Chile reallocated its exports",
        "tl_sub": "Main crises of the period and how exporters responded.",
        "tl_src": "Source: Ceballos-Concha et al. (2026).",
        "timeline": [
            ("2007–2010", "ISA virus",
             "Atlantic salmon production falls by nearly 80%. Fish are harvested smaller.",
             "Fresh whole salmon goes to Brazil by truck. Brazil becomes the third-largest market."),
            ("2014", "Russian embargo",
             "Russia closes its market to seafood from Norway and other Western countries.",
             "Chile ships frozen salmon by sea. Russia reaches 9.2% of export value."),
            ("2020–2021", "COVID-19 pandemic",
             "Firms face operational disruptions, absenteeism, and lower sales.",
             "The ranking of the main markets does not change."),
        ],
        "shock": "Crisis", "response": "Response",
        "see_data": "Show the data",
    },
}


def fig_tiles(lang):
    t = T[lang]
    tiles = "".join(f"<div class=\"tc-tile\"><p class=\"tc-hero\">{v}</p><p class=\"tc-label\">{d}</p></div>"
                    for v, d in t["tiles"])
    return wrap(f"<figure class=\"sp-fig\"><figcaption><p class=\"sp-title\">{t['tiles_title']}</p></figcaption>"
                f"<div class=\"tc-tiles\">{tiles}</div><p class=\"sp-src\">{t['tiles_src']}</p></figure>")


def meter(label, share, lang):
    tip = f"{label}: {num(share, lang)}%"
    return (f"<div class=\"tc-meter\" tabindex=\"0\" title=\"{tip}\" aria-label=\"{tip}\">"
            f"<div class=\"tc-mhead\"><span>{label}</span><span class=\"tc-mval\">{num(share, lang)}%</span></div>"
            f"<span class=\"tc-track\"><span class=\"tc-fill\" style=\"width:{share:.1f}%\"></span></span></div>")


def fig_routes(lang):
    t = T[lang]; cards = []; rows = []
    for mkt, prods, modes in ROUTES:
        name = t["markets"][mkt]
        body = (f"<p class=\"tc-dim\">{t['product']}</p>"
                + "".join(meter(t["labels"][k], s, lang) for k, s in prods)
                + f"<p class=\"tc-dim\">{t['transport']}</p>"
                + "".join(meter(t["labels"][k], s, lang) for k, s in modes))
        cards.append(f"<div class=\"tc-card\"><p class=\"sp-ptitle\">{name}</p>{body}</div>")
        rows += [[name, t["product"], t["labels"][k], num(s, lang) + "%"] for k, s in prods]
        rows += [[name, t["transport"], t["labels"][k], num(s, lang) + "%"] for k, s in modes]
    head = "".join(f"<th scope=\"col\">{c}</th>" for c in t["routes_cols"])
    body = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    table = (f"<details class=\"sp-data\"><summary>{t['see_data']}</summary>"
             f"<table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></details>")
    return wrap(f"<figure class=\"sp-fig\"><figcaption><p class=\"sp-title\">{t['routes_title']}</p>"
                f"<p class=\"sp-sub\">{t['routes_sub']}</p></figcaption>"
                f"<div class=\"tc-cards\">{''.join(cards)}</div>"
                f"<p class=\"sp-src\">{t['routes_src']}</p>{table}</figure>")


def fig_timeline(lang):
    t = T[lang]
    items = "".join(
        f"<li class=\"tc-event\"><p class=\"tc-year\">{y}</p><div class=\"tc-body\"><p class=\"tc-name\">{n}</p>"
        f"<p class=\"tc-line\"><span class=\"tc-tag\">{t['shock']}</span><span>{s}</span></p>"
        f"<p class=\"tc-line\"><span class=\"tc-tag tc-resp\">{t['response']}</span><span>{r}</span></p></div></li>"
        for y, n, s, r in t["timeline"])
    return wrap(f"<figure class=\"sp-fig\"><figcaption><p class=\"sp-title\">{t['tl_title']}</p>"
                f"<p class=\"sp-sub\">{t['tl_sub']}</p></figcaption>"
                f"<ol class=\"tc-timeline\">{items}</ol><p class=\"sp-src\">{t['tl_src']}</p></figure>")


MAP_T = {
    "es": {
        "title": "Figura 1. Desde Puerto Montt a 81 países",
        "sub": "Destinos del salmón y la trucha de Chile en 2024. El grosor de cada línea indica el valor "
               "exportado y su color, el principal medio de transporte.",
        "modes": {"sea": "Barco", "air": "Avión", "land": "Camión"},
        "src": "Fuente: elaboración propia con datos de Aduanas de Chile, 2024. Salmón y trucha, valor FOB. "
               "Las líneas unen Puerto Montt con la capital de cada destino. No representan rutas reales de transporte.",
        "cols": ["País", "Millones de USD", "% del valor", "Principal medio"],
        "noscript": "El mapa necesita JavaScript. Los datos están en la tabla.",
        "see_data": "Ver los 81 destinos",
    },
    "en": {
        "title": "Figure 1. From Puerto Montt to 81 countries",
        "sub": "Destinations of Chilean salmon and trout in 2024. Line width shows export value and "
               "color shows the main transport mode.",
        "modes": {"sea": "Sea", "air": "Air", "land": "Truck"},
        "src": "Source: own elaboration with Chilean customs data, 2024. Salmon and trout, FOB value. "
               "Lines connect Puerto Montt with the capital of each destination. They do not represent actual shipping routes.",
        "cols": ["Country", "Million USD", "% of value", "Main mode"],
        "noscript": "The map needs JavaScript. The data are in the table.",
        "see_data": "Show all 81 destinations",
    },
}
MODE_CLASS = {"sea": "tc-k-sea", "air": "tc-k-air", "land": "tc-k-land"}


def fig_map(lang):
    t = MAP_T[lang]
    data = json.loads((OUT / "destinos-2024.json").read_text(encoding="utf-8"))
    legend = "<ul class=\"sp-legend\">" + "".join(
        f"<li><span class=\"tc-kline {MODE_CLASS[m]}\"></span>{t['modes'][m]}</li>" for m in ("sea", "air", "land")) + "</ul>"
    rows = "".join(
        f"<tr><td>{d[lang]}</td><td>{num(d['musd'], lang, 1)}</td><td>{num(d['share'], lang, 2)}%</td>"
        f"<td>{t['modes'][d['mode']]} ({round(100 * d[d['mode']])}%)</td></tr>" for d in data["destinations"])
    head = "".join(f"<th scope=\"col\">{c}</th>" for c in t["cols"])
    table = (f"<details class=\"sp-data\"><summary>{t['see_data']}</summary><div class=\"tc-scroll\">"
             f"<table><thead><tr>{head}</tr></thead><tbody>{rows}</tbody></table></div></details>")
    scripts = ("<script src=\"https://cdn.jsdelivr.net/npm/d3@7.9.0/dist/d3.min.js\"></script>"
               "<script src=\"https://cdn.jsdelivr.net/npm/topojson-client@3.1.0/dist/topojson-client.min.js\"></script>"
               "<script src=\"mapa.js\"></script>")
    return wrap(f"<figure class=\"sp-fig\"><figcaption><p class=\"sp-title\">{t['title']}</p>"
                f"<p class=\"sp-sub\">{t['sub']}</p></figcaption>{legend}"
                f"<div class=\"tc-map\" data-src=\"destinos-2024.json\" data-lang=\"{lang}\">"
                f"<noscript><p class=\"sp-sub\">{t['noscript']}</p></noscript></div>"
                f"<p class=\"sp-src\">{t['src']}</p>{table}{scripts}</figure>")


EXTRA_CSS = """
/* Trade Costs summary: stat tiles, route meters, timeline */
.tc-tiles { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 1rem; }
.tc-tile { border-top: 3px solid var(--sp-hi); padding-top: .5rem; }
.tc-hero { font-size: 1.75rem; font-weight: 600; line-height: 1.1; margin: 0 0 .35rem; color: var(--sp-ink); }
.tc-label { margin: 0; color: var(--sp-ink-2); font-size: .85rem; }
.tc-cards { display: grid; grid-template-columns: repeat(auto-fit, minmax(190px, 1fr)); gap: 1rem 1.5rem; }
.tc-dim { margin: .5rem 0 .2rem; font-size: .75rem; text-transform: uppercase; letter-spacing: .04em;
  color: var(--sp-muted); }
.tc-meter { margin-bottom: .45rem; outline-offset: 2px; }
.tc-mhead { display: flex; justify-content: space-between; gap: .5rem; font-size: .85rem; color: var(--sp-ink-2); }
.tc-mval { color: var(--sp-ink); font-variant-numeric: tabular-nums; }
.tc-track { display: block; height: 8px; border-radius: 4px; background: var(--sp-track); overflow: hidden; }
.tc-fill { display: block; height: 100%; border-radius: 4px; background: var(--sp-hi); }
.tc-timeline { list-style: none; margin: 0; padding: 0; }
.tc-event { display: grid; grid-template-columns: 6.5em 1fr; gap: 1rem; padding: .6rem 0;
  border-top: 1px solid var(--sp-grid); }
.tc-year { margin: 0; font-weight: 600; font-variant-numeric: tabular-nums; color: var(--sp-ink); }
.tc-body p { margin: 0 0 .3rem; font-size: .88rem; color: var(--sp-ink-2); }
.tc-body .tc-name { font-weight: 600; color: var(--sp-ink); font-size: .95rem; }
.tc-line { display: grid; grid-template-columns: 7.5em 1fr; gap: .5rem; align-items: baseline; }
.tc-tag { font-size: .7rem; text-transform: uppercase;
  letter-spacing: .04em; color: var(--sp-muted); }
.tc-tag.tc-resp { color: var(--sp-ink); font-weight: 600; }
/* routes map */
.tc-map { position: relative; }
.tc-map:not(.tc-ready) { min-height: 180px; background: #eef2f6; border-radius: 4px; }
.tc-map-svg { display: block; width: 100%; height: auto; }
.tc-ocean { fill: #eef2f6; }
.tc-grat { fill: none; stroke: #dde4ea; stroke-width: .5; }
.tc-country { fill: #dedcd5; stroke: #ffffff; stroke-width: .4; }
.tc-chile { fill: #671130; stroke: #ffffff; stroke-width: .4; }
.tc-arc { fill: none; stroke-linecap: round; }
.tc-hit { fill: none; stroke: transparent; stroke-width: 10px; }
.tc-dot { stroke: #ffffff; stroke-width: .8; }
.tc-dest { outline: none; }
.tc-dest:hover .tc-arc, .tc-dest:focus .tc-arc { stroke-opacity: 1; }
.tc-origin { stroke: #ffffff; stroke-width: 2; }
.tc-mlabel { fill: #0b0b0b; stroke: #ffffff; paint-order: stroke; stroke-linejoin: round; font-weight: 500; }
.tc-mlabel-origin { fill: #671130; font-weight: 600; }
.tc-kline { display: inline-block; width: 18px; height: 3px; border-radius: 2px; }
.tc-k-sea { background: #2a78d6; } .tc-k-air { background: #eb6834; } .tc-k-land { background: #1baf7a; }
.tc-scroll { max-height: 320px; overflow: auto; }
@media (max-width: 480px) { .tc-event { grid-template-columns: 1fr; gap: .2rem; } .tc-line { display: block; } .tc-tag { display: block; } }
"""


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "figs.css").write_text(BASE_CSS + EXTRA_CSS, encoding="utf-8")
    for lang in ("es", "en"):
        (OUT / f"_fig-mapa-{lang}.md").write_text(fig_map(lang), encoding="utf-8")
        (OUT / f"_fig-cifras-{lang}.md").write_text(fig_tiles(lang), encoding="utf-8")
        (OUT / f"_fig-rutas-{lang}.md").write_text(fig_routes(lang), encoding="utf-8")
        (OUT / f"_fig-crisis-{lang}.md").write_text(fig_timeline(lang), encoding="utf-8")
    print("wrote figures to", OUT)


if __name__ == "__main__":
    main()
