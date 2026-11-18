"""Aggregate 2024 Chilean salmon and trout exports by destination for the routes map.

Needs the customs database of the chile_seafood_trade project (not in this repo)
and the duckdb Python package:
    python scripts/trade_costs_map_data.py <path/to/chilean_exports_hs03.duckdb>

Writes research/articles/ceballos-2026-trade-costs/destinos-2024.json with one
row per destination country: FOB value (million USD), share of total, value
shares by transport mode, and the coordinates of the destination's capital,
which is where each arc ends. Only country aggregates are written.

Transport codes (Servicio Nacional de Aduanas): 1 sea, 4 air, 7 road.
Check: the 2024 total (USD 5,959.6 million) is within 0.2% of the USD 5.97
billion reported in Ceballos-Concha et al. (2026), and the air and road shares
(30.0% and 19.9%) match the shares reported there.
"""
import json
import sys
from pathlib import Path

ORIGIN = {"es": "Puerto Montt", "en": "Puerto Montt", "lat": -41.4693, "lon": -72.9424}

# Aduana country code -> (Spanish name, English name, capital latitude, capital longitude)
CAPITALS = {
    "225": ("Estados Unidos", "United States", 38.9072, -77.0369),
    "331": ("Japón", "Japan", 35.6762, 139.6503),
    "220": ("Brasil", "Brazil", -15.7939, -47.8828),
    "336": ("China", "China", 39.9042, 116.4074),
    "562": ("Rusia", "Russia", 55.7558, 37.6173),
    "216": ("México", "Mexico", 19.4326, -99.1332),
    "306": ("Israel", "Israel", 31.7683, 35.2137),
    "325": ("Vietnam", "Vietnam", 21.0278, 105.8342),
    "319": ("Tailandia", "Thailand", 13.7563, 100.5018),
    "226": ("Canadá", "Canada", 45.4215, -75.6972),
    "330": ("Taiwán", "Taiwan", 25.0330, 121.5654),
    "202": ("Colombia", "Colombia", 4.7110, -74.0721),
    "333": ("Corea del Sur", "South Korea", 37.5665, 126.9780),
    "517": ("España", "Spain", 40.4168, -3.7038),
    "335": ("Filipinas", "Philippines", 14.5995, 120.9842),
    "224": ("Argentina", "Argentina", -34.6037, -58.3816),
    "332": ("Singapur", "Singapore", 1.3521, 103.8198),
    "563": ("Alemania", "Germany", 52.5200, 13.4050),
    "329": ("Malasia", "Malaysia", 3.1390, 101.6869),
    "528": ("Polonia", "Poland", 52.2297, 21.0122),
    "505": ("Francia", "France", 48.8566, 2.3522),
    "210": ("Panamá", "Panama", 8.9824, -79.5199),
    "551": ("Kazajistán", "Kazakhstan", 51.1694, 71.4491),
    "206": ("República Dominicana", "Dominican Republic", 18.4861, -69.9312),
    "328": ("Indonesia", "Indonesia", -6.2088, 106.8456),
    "211": ("Costa Rica", "Costa Rica", 9.9281, -84.0907),
    "507": ("Dinamarca", "Denmark", 55.6761, 12.5683),
    "223": ("Uruguay", "Uruguay", -34.9011, -56.1645),
    "554": ("Lituania", "Lithuania", 54.6872, 25.2797),
    "514": ("Bélgica", "Belgium", 50.8503, 4.3517),
    "218": ("Ecuador", "Ecuador", -0.1807, -78.4678),
    "251": ("Puerto Rico", "Puerto Rico", 18.4655, -66.1057),
    "342": ("Hong Kong", "Hong Kong", 22.3193, 114.1694),
    "341": ("Emiratos Árabes Unidos", "United Arab Emirates", 24.4539, 54.3773),
    "219": ("Perú", "Peru", -12.0464, -77.0428),
    "542": ("Bielorrusia", "Belarus", 53.9006, 27.5590),
    "504": ("Italia", "Italy", 41.9028, 12.4964),
    "201": ("Venezuela", "Venezuela", 10.4806, -66.9036),
    "550": ("Georgia", "Georgia", 41.7151, 44.8271),
    "510": ("Reino Unido", "United Kingdom", 51.5074, -0.1278),
    "222": ("Paraguay", "Paraguay", -25.2637, -57.5759),
    "205": ("Jamaica", "Jamaica", 17.9714, -76.7920),
    "541": ("Azerbaiyán", "Azerbaijan", 40.4093, 49.8671),
    "501": ("Portugal", "Portugal", 38.7223, -9.1393),
    "520": ("Grecia", "Greece", 37.9838, 23.7275),
    "305": ("Chipre", "Cyprus", 35.1856, 33.3823),
    "124": ("Egipto", "Egypt", 30.0444, 31.2357),
    "519": ("Rumania", "Romania", 44.4268, 26.1025),
    "544": ("República Checa", "Czech Republic", 50.0755, 14.4378),
    "213": ("El Salvador", "El Salvador", 13.6929, -89.2182),
    "515": ("Países Bajos", "Netherlands", 52.3676, 4.9041),
    "559": ("Ucrania", "Ukraine", 50.4501, 30.5234),
    "203": ("Trinidad y Tobago", "Trinidad and Tobago", 10.6549, -61.5019),
    "553": ("Letonia", "Latvia", 56.9496, 24.1052),
    "540": ("Armenia", "Armenia", 40.1792, 44.4991),
    "552": ("Kirguistán", "Kyrgyzstan", 42.8746, 74.5698),
    "344": ("Brunéi", "Brunei", 4.9031, 114.9398),
    "215": ("Guatemala", "Guatemala", 14.6349, -90.5069),
    "326": ("Myanmar", "Myanmar", 19.7633, 96.0785),
    "999": ("Curazao", "Curaçao", 12.1091, -68.9316),
    "506": ("Irlanda", "Ireland", 53.3498, -6.2603),
    "301": ("Jordania", "Jordan", 31.9454, 35.9284),
    "311": ("Líbano", "Lebanon", 33.8938, 35.5018),
    "555": ("Macedonia del Norte", "North Macedonia", 41.9981, 21.4254),
    "317": ("India", "India", 28.6139, 77.2090),
    "556": ("Moldavia", "Moldova", 47.0105, 28.8638),
    "233": ("Santa Lucía", "Saint Lucia", 14.0101, -60.9875),
    "243": ("Aruba", "Aruba", 12.5092, -70.0086),
    "107": ("Costa de Marfil", "Côte d'Ivoire", 6.8276, -5.2893),
    "247": ("Antillas Neerlandesas", "Netherlands Antilles", 12.1091, -68.9316),
    "530": ("Hungría", "Hungary", 47.4979, 19.0402),
    "221": ("Bolivia", "Bolivia", -19.0196, -65.2619),
    "314": ("Sri Lanka", "Sri Lanka", 6.9022, 79.9089),
    "212": ("Nicaragua", "Nicaragua", 12.1150, -86.2362),
    "209": ("Cuba", "Cuba", 23.1136, -82.3666),
    "527": ("Bulgaria", "Bulgaria", 42.6977, 23.3219),
    "111": ("Nigeria", "Nigeria", 9.0765, 7.3986),
    "315": ("Camboya", "Cambodia", 11.5564, 104.9282),
    "302": ("Arabia Saudita", "Saudi Arabia", 24.7136, 46.6753),
    "217": ("Guyana", "Guyana", 6.8013, -58.1551),
    "406": ("Australia", "Australia", -35.2809, 149.1300),
}

QUERY = """
SELECT PAISDESTINO, SUM(FOBUS) / 1e6 AS musd,
  SUM(CASE WHEN VIATRANSPORTE = '1' THEN FOBUS ELSE 0 END) / SUM(FOBUS) AS sea,
  SUM(CASE WHEN VIATRANSPORTE = '4' THEN FOBUS ELSE 0 END) / SUM(FOBUS) AS air,
  SUM(CASE WHEN VIATRANSPORTE = '7' THEN FOBUS ELSE 0 END) / SUM(FOBUS) AS land
FROM expo WHERE year = 2024 AND salmon_category IS NOT NULL
GROUP BY PAISDESTINO ORDER BY musd DESC
"""


def main(db):
    import duckdb
    con = duckdb.connect(db, read_only=True)
    rows = con.execute(QUERY).fetchall()
    total = sum(r[1] for r in rows)
    missing = [r[0] for r in rows if r[0] not in CAPITALS]
    if missing:
        sys.exit(f"Missing capital coordinates for Aduana codes: {missing}")
    dest = []
    for code, musd, sea, air, land in rows:
        es, en, lat, lon = CAPITALS[code]
        modes = {"sea": sea, "air": air, "land": land}
        dest.append({"code": code, "es": es, "en": en, "lat": lat, "lon": lon,
                     "musd": round(musd, 2), "share": round(100 * musd / total, 2),
                     "mode": max(modes, key=modes.get),
                     "sea": round(sea, 3), "air": round(air, 3), "land": round(land, 3)})
    out = Path(__file__).resolve().parent.parent / "research" / "articles" / "ceballos-2026-trade-costs" / "destinos-2024.json"
    out.write_text(json.dumps({"year": 2024, "total_musd": round(total, 1), "origin": ORIGIN,
                               "destinations": dest}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(dest)} destinations, total USD {total:,.1f} million -> {out}")


if __name__ == "__main__":
    main(sys.argv[1])
