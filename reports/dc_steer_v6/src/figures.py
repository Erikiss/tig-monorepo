#!/usr/bin/env python3
"""Generate the report's data figures as inline SVG.

Print medium: no hover layer, no dark mode. Categorical hues are slots 1-3 of the
validated default palette (#2a78d6 blue, #eb6834 orange, #1baf7a aqua); the aqua
slot carries a contrast WARN on a white surface, so every mark is direct-labelled.
"""

BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"
INK, MUTED, FAINT = "#16202b", "#5d6b7c", "#8794a4"
GRID, SURFACE = "#e8edf2", "#ffffff"
SANS = "DejaVu Sans, Liberation Sans, sans-serif"
MONO = "DejaVu Sans Mono, monospace"


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# ══════════════════════════════════════════════════════════════════════
# Figure: Codeumfang je Track (stacked horizontal bar, 2 series)
# ══════════════════════════════════════════════════════════════════════
def fig_loc():
    rows = [
        ("T29", "n=4",  935, 391),
        ("T30", "n=7",  1288, 494),
        ("T26", "n=10", 557, 491),
        ("T27", "n=14", 630, 642),
        ("T28", "n=18", 387, 380),
        ("gemeinsam", "helpers + mod", 999, 0),
    ]
    W, ROW_H, GAP = 520.0, 20.0, 9.0
    L, R, TOP = 96.0, 54.0, 30.0
    plot_w = W - L - R
    vmax = 1800.0
    H = TOP + len(rows) * (ROW_H + GAP) + 26

    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.0f} {H:.0f}" '
         f'role="img" aria-label="Codeumfang je Track in Zeilen">',
         f'<rect width="{W:.0f}" height="{H:.0f}" fill="{SURFACE}"/>']

    # legend (2 series -> legend always present)
    o.append(f'<g font-family="{SANS}" font-size="8.5">')
    o.append(f'<rect x="{L}" y="10" width="9" height="9" rx="2" fill="{BLUE}"/>'
             f'<text x="{L+13}" y="18" fill="{MUTED}">Rust</text>')
    o.append(f'<rect x="{L+52}" y="10" width="9" height="9" rx="2" fill="{ORANGE}"/>'
             f'<text x="{L+65}" y="18" fill="{MUTED}">CUDA</text>')
    o.append(f'<text x="{W-R}" y="18" text-anchor="end" fill="{FAINT}">Zeilen Quelltext</text>')
    o.append("</g>")

    # recessive gridlines
    for gv in (500, 1000, 1500):
        gx = L + plot_w * gv / vmax
        o.append(f'<line x1="{gx:.1f}" y1="{TOP-4:.0f}" x2="{gx:.1f}" y2="{H-22:.0f}" '
                 f'stroke="{GRID}" stroke-width="1"/>')
        o.append(f'<text x="{gx:.1f}" y="{H-10:.0f}" text-anchor="middle" '
                 f'font-family="{SANS}" font-size="7.5" fill="{FAINT}">{gv}</text>')

    y = TOP
    for name, sub, rs, cu in rows:
        w_rs = plot_w * rs / vmax
        w_cu = plot_w * cu / vmax
        o.append(f'<text x="{L-9}" y="{y+10.5:.1f}" text-anchor="end" font-family="{MONO}" '
                 f'font-size="8.5" fill="{INK}">{esc(name)}</text>')
        o.append(f'<text x="{L-9}" y="{y+19:.1f}" text-anchor="end" font-family="{SANS}" '
                 f'font-size="6.8" fill="{FAINT}">{esc(sub)}</text>')
        # 4px rounded data-end, anchored at the baseline; 2px surface gap between fills
        o.append(f'<rect x="{L:.1f}" y="{y:.1f}" width="{w_rs:.1f}" height="{ROW_H}" '
                 f'rx="2.5" fill="{BLUE}"/>')
        if cu:
            o.append(f'<rect x="{L+w_rs+2:.1f}" y="{y:.1f}" width="{max(w_cu-2,1):.1f}" '
                     f'height="{ROW_H}" rx="2.5" fill="{ORANGE}"/>')
        if w_rs > 34:
            o.append(f'<text x="{L+w_rs-6:.1f}" y="{y+13.5:.1f}" text-anchor="end" '
                     f'font-family="{SANS}" font-size="8" font-weight="700" fill="#ffffff">{rs}</text>')
        if cu and w_cu > 30:
            o.append(f'<text x="{L+w_rs+w_cu-6:.1f}" y="{y+13.5:.1f}" text-anchor="end" '
                     f'font-family="{SANS}" font-size="8" font-weight="700" fill="#ffffff">{cu}</text>')
        o.append(f'<text x="{L+w_rs+w_cu+7:.1f}" y="{y+13.5:.1f}" font-family="{SANS}" '
                 f'font-size="8" fill="{MUTED}">{rs+cu}</text>')
        y += ROW_H + GAP

    o.append("</svg>")
    return "\n".join(o)


# ══════════════════════════════════════════════════════════════════════
# Figure: Quality-Nomogramm -- Test-MSE <-> Quality (eine Größe, zwei Skalen)
# ══════════════════════════════════════════════════════════════════════
def fig_quality():
    EPS2 = 0.32          # eps*^2 = (4 / N_test) * sum over N*D elements ~ 8 * sigma^2
    FLOOR = 0.04         # sigma^2, irreduzibel
    LMAX = 0.36
    W, H = 520.0, 190.0
    L, R = 58.0, 26.0
    BAR_Y, BAR_H = 104.0, 26.0
    plot_w = W - L - R

    def x(loss):
        return L + plot_w * loss / LMAX

    def loss_of_q_k(qk):        # qk = Quality in Tausend
        return EPS2 * (1.0 - qk / 1000.0)

    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.0f} {H:.0f}" '
         f'role="img" aria-label="Zusammenhang von Test-MSE und Quality">',
         f'<rect width="{W:.0f}" height="{H:.0f}" fill="{SURFACE}"/>',
         '<defs><pattern id="hatch" width="5" height="5" patternTransform="rotate(45)" '
         'patternUnits="userSpaceOnUse">'
         '<rect width="5" height="5" fill="#eef1f4"/>'
         '<line x1="0" y1="0" x2="0" y2="5" stroke="#c4cedb" stroke-width="1.6"/>'
         '</pattern>'
         '<linearGradient id="ach" x1="0" x2="1">'
         '<stop offset="0" stop-color="#1c5cab"/><stop offset="1" stop-color="#cde2fb"/>'
         '</linearGradient></defs>']

    # ── Quality scale (top) ───────────────────────────────────────────
    o.append(f'<text x="{L}" y="13" font-family="{SANS}" font-size="7.6" fill="{FAINT}">'
             f'Quality Q (in Tausend)</text>')
    for qk in (875, 750, 500, 250, 0):
        xx = x(loss_of_q_k(qk))
        o.append(f'<line x1="{xx:.1f}" y1="24" x2="{xx:.1f}" y2="30" stroke="{FAINT}" stroke-width="1"/>')
        o.append(f'<text x="{xx:.1f}" y="21" text-anchor="middle" font-family="{SANS}" '
                 f'font-size="7.5" fill="{MUTED}">{qk}</text>')
    o.append(f'<line x1="{x(loss_of_q_k(875)):.1f}" y1="30" x2="{x(loss_of_q_k(0)):.1f}" y2="30" '
             f'stroke="{GRID}" stroke-width="1"/>')

    # ── Marker labels (between the two scales) ────────────────────────
    labels = (
        (FLOOR, AQUA, "Rauschboden \u03c3\u00b2 = 0,04",
         "Q = 875.000 \u2014 selbst ein perfektes Modell", "kommt nicht darunter", "start"),
        (EPS2, ORANGE, "Schwelle \u03b5*\u00b2 = 0,32",
         "Q = 0 \u2014 Annahmegrenze", "", "end"),
    )
    for loss, col, t1, t2, t3, anchor in labels:
        xx = x(loss)
        tx = xx + 8 if anchor == "start" else xx - 8
        o.append(f'<line x1="{xx:.1f}" y1="46" x2="{xx:.1f}" y2="{BAR_Y+BAR_H:.0f}" '
                 f'stroke="{col}" stroke-width="1.6" stroke-dasharray="3 2.5"/>')
        o.append(f'<circle cx="{xx:.1f}" cy="46" r="3.4" fill="{col}" stroke="{SURFACE}" stroke-width="2"/>')
        o.append(f'<text x="{tx:.1f}" y="{"56" if anchor=="start" else "56"}" text-anchor="{anchor}" '
                 f'font-family="{SANS}" font-size="8.6" font-weight="700" fill="{INK}">{t1}</text>')
        o.append(f'<text x="{tx:.1f}" y="66" text-anchor="{anchor}" font-family="{SANS}" '
                 f'font-size="7.6" fill="{MUTED}">{t2}</text>')
        if t3:
            o.append(f'<text x="{tx:.1f}" y="75.5" text-anchor="{anchor}" font-family="{SANS}" '
                     f'font-size="7.6" fill="{MUTED}">{t3}</text>')

    # ── The scale bar ─────────────────────────────────────────────────
    o.append(f'<rect x="{x(0):.1f}" y="{BAR_Y}" width="{x(FLOOR)-x(0):.1f}" height="{BAR_H}" '
             f'fill="url(#hatch)"/>')
    o.append(f'<rect x="{x(FLOOR)+2:.1f}" y="{BAR_Y}" width="{x(EPS2)-x(FLOOR)-2:.1f}" '
             f'height="{BAR_H}" fill="url(#ach)"/>')
    o.append(f'<rect x="{x(EPS2)+2:.1f}" y="{BAR_Y}" width="{x(LMAX)-x(EPS2)-2:.1f}" '
             f'height="{BAR_H}" fill="#f4f6f8" stroke="{GRID}" stroke-width="1"/>')
    o.append(f'<text x="{x(0.055):.1f}" y="{BAR_Y-4:.0f}" font-family="{SANS}" font-size="7" '
             f'font-weight="700" fill="#1c5cab">\u2190 besser</text>')
    o.append(f'<text x="{x(LMAX)-4:.1f}" y="{BAR_Y+BAR_H/2+3:.1f}" text-anchor="end" '
             f'font-family="{SANS}" font-size="7" fill="{FAINT}">abgelehnt</text>')

    # ── Loss scale (bottom) ───────────────────────────────────────────
    for lv in (0.0, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35):
        xx = x(lv)
        o.append(f'<line x1="{xx:.1f}" y1="{BAR_Y+BAR_H+1:.0f}" x2="{xx:.1f}" '
                 f'y2="{BAR_Y+BAR_H+5:.0f}" stroke="{FAINT}" stroke-width="1"/>')
        o.append(f'<text x="{xx:.1f}" y="{BAR_Y+BAR_H+15:.0f}" text-anchor="middle" '
                 f'font-family="{SANS}" font-size="7.5" fill="{MUTED}">'
                 f'{("%.2f" % lv).replace(".", ",")}</text>')
    o.append(f'<text x="{L}" y="{H-7:.0f}" font-family="{SANS}" font-size="7.6" fill="{FAINT}">'
             f'mittlerer quadratischer Testfehler je Ausgabeelement</text>')
    o.append(f'<text x="{W-R:.0f}" y="{H-7:.0f}" text-anchor="end" font-family="{MONO}" '
             f'font-size="7.3" fill="{FAINT}">dQ/dL = \u22123,125\u00b710\u2076</text>')
    o.append("</svg>")
    return "\n".join(o)


if __name__ == "__main__":
    import pathlib, sys
    d = pathlib.Path(__file__).parent
    (d / "fig_loc.svg").write_text(fig_loc(), encoding="utf-8")
    (d / "fig_quality.svg").write_text(fig_quality(), encoding="utf-8")
    print("wrote fig_loc.svg, fig_quality.svg")
