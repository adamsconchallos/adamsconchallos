// Routes map for the Trade Costs policy summary.
// Draws arcs from Puerto Montt to the capital of every 2024 destination of
// Chilean salmon and trout. Data: destinos-2024.json (built by
// scripts/trade_costs_map_data.py). Needs d3 v7 and topojson-client v3.
(function () {
  "use strict";
  var WORLD = "https://cdn.jsdelivr.net/npm/world-atlas@2.0.2/countries-110m.json";
  var COLORS = { sea: "#2a78d6", air: "#eb6834", land: "#1baf7a" };
  var BRAND = "#671130";
  var TEXT = {
    es: { modes: { sea: "barco", air: "avión", land: "camión" }, musd: "millones", share: "del valor",
          main: "principal medio", aria: "Mapa de los destinos del salmón chileno en 2024, con arcos desde Puerto Montt.",
          dec: ",", thou: "." },
    en: { modes: { sea: "sea", air: "air", land: "truck" }, musd: "million", share: "of value",
          main: "main mode", aria: "Map of 2024 destinations of Chilean salmon, with arcs from Puerto Montt.",
          dec: ".", thou: "," }
  };
  // Label placement for the five largest destinations: [dx, dy, text-anchor]
  var LABELS = { "225": [8, -8, "start"], "331": [8, -8, "start"], "220": [9, 4, "start"],
                 "336": [0, 18, "middle"], "562": [0, 28, "middle"] };
  var SVGNS = "http://www.w3.org/2000/svg";

  function fmt(v, t, dec) {
    var s = v.toFixed(dec);
    var parts = s.split(".");
    parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, t.thou);
    return parts.length > 1 ? parts[0] + t.dec + parts[1] : parts[0];
  }

  function el(name, attrs, parent) {
    var n = document.createElementNS(SVGNS, name);
    for (var k in attrs) n.setAttribute(k, attrs[k]);
    if (parent) parent.appendChild(n);
    return n;
  }

  function draw(root, world, data) {
    var t = TEXT[root.dataset.lang] || TEXT.es;
    var W = 960;
    var proj = d3.geoEqualEarth().rotate([100, 0]).fitWidth(W, { type: "Sphere" });
    var path = d3.geoPath(proj);
    var top = proj([-100, 80])[1], bottom = proj([-100, -57])[1];
    var svg = el("svg", { viewBox: "0 " + top + " " + W + " " + (bottom - top), role: "img",
                          "aria-label": t.aria, class: "tc-map-svg" });
    root.appendChild(svg);

    el("path", { d: path({ type: "Sphere" }), class: "tc-ocean" }, svg);
    el("path", { d: path(d3.geoGraticule10()), class: "tc-grat" }, svg);
    var countries = topojson.feature(world, world.objects.countries).features;
    var land = el("g", { class: "tc-land" }, svg);
    countries.forEach(function (f) {
      el("path", { d: path(f), class: f.id === "152" ? "tc-chile" : "tc-country" }, land);
    });

    var o = data.origin, p0 = proj([o.lon, o.lat]);
    var vmax = d3.max(data.destinations, function (d) { return d.musd; });
    var arcs = el("g", { class: "tc-arcs" }, svg);
    data.destinations.slice().sort(function (a, b) { return a.musd - b.musd; }).forEach(function (d) {
      var p1 = proj([d.lon, d.lat]);
      var dx = p1[0] - p0[0], dy = p1[1] - p0[1], dist = Math.hypot(dx, dy) || 1;
      var nx = -dy / dist, ny = dx / dist;
      if (ny > 0) { nx = -nx; ny = -ny; }          // bulge upward
      var k = Math.min(0.25 * dist, 140);
      var cx = (p0[0] + p1[0]) / 2 + nx * k, cy = (p0[1] + p1[1]) / 2 + ny * k;
      var s = Math.sqrt(d.musd / vmax);
      var g = el("g", { class: "tc-dest", tabindex: "0" }, arcs);
      var mainShare = Math.round(100 * d[d.mode]);
      var tip = d[root.dataset.lang === "en" ? "en" : "es"] + " · USD " + fmt(d.musd, t, d.musd < 10 ? 1 : 0) +
                " " + t.musd + " · " + fmt(d.share, t, d.share < 1 ? 2 : 1) + "% " + t.share +
                " · " + t.main + ": " + t.modes[d.mode] + " (" + mainShare + "%)";
      el("title", {}, g).textContent = tip;
      el("path", { d: "M" + p0[0] + "," + p0[1] + "Q" + cx + "," + cy + " " + p1[0] + "," + p1[1],
                   class: "tc-arc", stroke: COLORS[d.mode], "stroke-width": (0.6 + 5.4 * s).toFixed(2),
                   "stroke-opacity": (0.35 + 0.55 * s).toFixed(2), "vector-effect": "non-scaling-stroke" }, g);
      el("path", { d: "M" + p0[0] + "," + p0[1] + "Q" + cx + "," + cy + " " + p1[0] + "," + p1[1],
                   class: "tc-hit", "vector-effect": "non-scaling-stroke" }, g);
      el("circle", { cx: p1[0], cy: p1[1], r: (1.6 + 4 * s).toFixed(2), fill: COLORS[d.mode], class: "tc-dot" }, g);
    });

    el("circle", { cx: p0[0], cy: p0[1], r: 5, fill: BRAND, class: "tc-origin" }, svg);
    var labels = el("g", { class: "tc-labels" }, svg);
    var placed = [];
    var origin = el("text", { "text-anchor": "end", class: "tc-mlabel tc-mlabel-origin" }, labels);
    origin.textContent = o[root.dataset.lang === "en" ? "en" : "es"];
    data.destinations.forEach(function (d) {
      var L = LABELS[d.code];
      if (!L) return;
      var p = proj([d.lon, d.lat]);
      var txt = el("text", { "text-anchor": L[2], class: "tc-mlabel" }, labels);
      txt.textContent = d[root.dataset.lang === "en" ? "en" : "es"] + " " + Math.round(d.share) + "%";
      placed.push([txt, p, L]);
    });
    placed.push([origin, p0, [-9, 5]]);

    // Keep label text near 12px and its offsets constant on screen, whatever the map width.
    function resize() {
      var scale = svg.getBoundingClientRect().width / W || 1;
      labels.setAttribute("font-size", (12 / scale).toFixed(1));
      labels.setAttribute("stroke-width", (3 / scale).toFixed(2));
      placed.forEach(function (q) {
        q[0].setAttribute("x", (q[1][0] + q[2][0] / scale).toFixed(1));
        q[0].setAttribute("y", (q[1][1] + q[2][1] / scale).toFixed(1));
      });
    }
    resize();
    if (window.ResizeObserver) new ResizeObserver(resize).observe(svg);
    root.classList.add("tc-ready");
  }

  function init() {
    var roots = document.querySelectorAll(".tc-map[data-src]");
    if (!roots.length || !window.d3 || !window.topojson) return;
    fetch(WORLD).then(function (r) { return r.json(); }).then(function (world) {
      roots.forEach(function (root) {
        fetch(root.dataset.src).then(function (r) { return r.json(); })
          .then(function (data) { draw(root, world, data); });
      });
    });
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
