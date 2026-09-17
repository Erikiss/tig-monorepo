#!/usr/bin/env python3
"""Schematic figures for the report (hand-laid SVG, print medium)."""
from figures import BLUE, ORANGE, AQUA, INK, MUTED, FAINT, GRID, SURFACE, SANS, MONO, esc

NAVY = "#143a5e"
SOFT = "#f3f6f9"
TINT = "#e7f0f9"
RULE = "#d7dee6"


def _box(x, y, w, h, fill, stroke, rx=4, sw=1.2):
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')


def _txt(x, y, s, size=8.2, fill=INK, anchor="start", weight="400", fam=SANS):
    return (f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" font-family="{fam}" '
            f'font-size="{size}" font-weight="{weight}" fill="{fill}">{esc(s)}</text>')


def _arrow(x1, y1, x2, y2, col=FAINT, dash=None, w=1.3):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{col}" '
            f'stroke-width="{w}" marker-end="url(#ah)"{d}/>')


DEFS = (f'<defs><marker id="ah" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="5.5" '
        f'markerHeight="5.5" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="{FAINT}"/></marker>'
        f'<marker id="ahb" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="5.5" '
        f'markerHeight="5.5" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="{BLUE}"/></marker>'
        f'</defs>')


# ══════════════════════════════════════════════════════════════════
# Figure: die feste Trainingsschleife und die drei Einstiegspunkte
# ══════════════════════════════════════════════════════════════════
def fig_loop():
    W, H = 520.0, 300.0
    LX, LW = 8.0, 232.0          # harness column
    RX, RW = 288.0, 224.0        # optimizer column
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.0f} {H:.0f}" role="img" '
         f'aria-label="Trainingsschleife der Challenge und die Einstiegspunkte des Optimierers">',
         f'<rect width="{W:.0f}" height="{H:.0f}" fill="{SURFACE}"/>', DEFS]

    o.append(_txt(LX, 11, "tig-challenges — unveränderlich", 7.6, FAINT, weight="700"))
    o.append(_txt(RX, 11, "dc_steer_v6 — Gestaltungsraum des Innovators", 7.6, BLUE, weight="700"))
    o.append(f'<line x1="{LX}" y1="16" x2="{LX+LW}" y2="16" stroke="{RULE}" stroke-width="1"/>')
    o.append(f'<line x1="{RX}" y1="16" x2="{RX+RW}" y2="16" stroke="{BLUE}" stroke-width="1.4"/>')

    rows = [
        # (y, side, title, sub)
        (28,  "L", "Epoche e: Trainingsdaten mischen", "1.000 Punkte → 8 Mini-Batches à 128"),
        (70,  "R", "optimizer_query_at_params(…)", "optional Ersatzparameter θ′ — hier: None"),
        (112, "L", "Forward + Backward mit θ", "liefert Gradienten g je Parametertensor"),
        (154, "R", "optimizer_step(θ, g, e, train_loss, val_loss)", "liefert Updates Δθ je Tensor"),
        (196, "L", "θ ← θ + Δθ", "Harness wendet an; eingefrorene Schichten werden übersprungen"),
    ]
    BH = 32.0
    for y, side, t, s in rows:
        if side == "L":
            o.append(_box(LX, y, LW, BH, SOFT, RULE))
            o.append(_txt(LX + 9, y + 13, t, 8.2, INK, weight="700"))
            o.append(_txt(LX + 9, y + 24, s, 7.2, MUTED))
        else:
            o.append(_box(RX, y, RW, BH, TINT, BLUE))
            o.append(_txt(RX + 9, y + 13, t, 7.6, NAVY, weight="700", fam=MONO))
            o.append(_txt(RX + 9, y + 24, s, 7.2, MUTED))

    # crossing arrows
    o.append(_arrow(LX + LW + 4, 44, RX - 4, 82, BLUE, w=1.4))
    o.append(_arrow(RX - 4, 98, LX + LW + 4, 122, BLUE, w=1.4))
    o.append(_arrow(LX + LW + 4, 128, RX - 4, 166, BLUE, w=1.4))
    o.append(_arrow(RX - 4, 182, LX + LW + 4, 206, BLUE, w=1.4))

    # per-batch loop bracket
    o.append(f'<path d="M {LX-4:.0f} 32 L {LX-6:.0f} 32 L {LX-6:.0f} 224 L {LX-4:.0f} 224" '
             f'fill="none" stroke="{FAINT}" stroke-width="1"/>')
    o.append(f'<text transform="translate({LX-10:.0f},128) rotate(-90)" text-anchor="middle" '
             f'font-family="{SANS}" font-size="6.8" fill="{FAINT}">je Mini-Batch</text>')

    # end of epoch
    o.append(_box(LX, 240, W - LX - 8, 36, "#eff8f5", AQUA))
    o.append(_txt(LX + 9, 254, "Ende der Epoche: Validierung (200 Punkte) → bestes Modell sichern",
                  8.2, "#0d5f54", weight="700"))
    o.append(_txt(LX + 9, 266, "Early Stopping nach 50 Epochen ohne Verbesserung · höchstens 1.000 Epochen "
                               "· bewertet wird das gesicherte Modell, nicht das letzte", 7.2, MUTED))
    o.append(_txt(LX, 291, "Der Optimierer sieht val_loss — und ist die einzige Stelle, an der der Innovator "
                           "eingreift.", 7.4, FAINT))
    o.append("</svg>")
    return "\n".join(o)


# ══════════════════════════════════════════════════════════════════
# Figure: Dispatch nach num_hidden_layers
# ══════════════════════════════════════════════════════════════════
def fig_dispatch():
    W, H = 520.0, 246.0
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.0f} {H:.0f}" role="img" '
         f'aria-label="Verteilung auf fünf Track-Implementierungen nach Netztiefe">',
         f'<rect width="{W:.0f}" height="{H:.0f}" fill="{SURFACE}"/>', DEFS]

    o.append(_box(8, 96, 104, 44, NAVY, NAVY))
    o.append(_txt(60, 112, "solve_challenge", 7.8, "#ffffff", anchor="middle", weight="700", fam=MONO))
    o.append(_txt(60, 124, "match", 7.4, "#a9c6e2", anchor="middle", fam=MONO))
    o.append(_txt(60, 134, "num_hidden_layers", 6.8, "#a9c6e2", anchor="middle", fam=MONO))

    rows = [
        ("4",  "track_t29", "Dual-Phase Consensus + DC (eigene Kopie)", "DC an", AQUA),
        ("7",  "track_t30", "Dual-Phase Consensus, val-abh. Mischung", "DC aus", FAINT),
        ("10", "track_t26", "Dual-Phase Consensus + Init-Skalierung",  "DC an, Gain 1,2", AQUA),
        ("14", "track_t27", "Prometheus: Adan/AdaBelief + Muon + MARS", "DC an", AQUA),
        ("18", "track_t28", "Prometheus, schlank (kein Muon/MARS)",     "DC an", AQUA),
    ]
    BX, BW, BH, Y0, GAP = 168.0, 344.0, 32.0, 24.0, 10.0
    for i, (n, name, desc, dc, dccol) in enumerate(rows):
        y = Y0 + i * (BH + GAP)
        o.append(_arrow(114, 118, BX - 5, y + BH / 2, FAINT))
        o.append(_box(BX, y, BW, BH, SOFT, RULE))
        # depth chip
        o.append(f'<rect x="{BX+7}" y="{y+8:.1f}" width="30" height="16" rx="8" fill="{NAVY}"/>')
        o.append(_txt(BX + 22, y + 19, f"n={n}", 7.4, "#ffffff", anchor="middle", weight="700"))
        o.append(_txt(BX + 44, y + 14, name, 7.8, NAVY, weight="700", fam=MONO))
        o.append(_txt(BX + 44, y + 25, desc, 7.2, MUTED))
        # DC badge
        bw = 52 if "Gain" not in dc else 68
        o.append(f'<rect x="{BX+BW-bw-6:.1f}" y="{y+9:.1f}" width="{bw}" height="14" rx="3" '
                 f'fill="{"#eff8f5" if dccol==AQUA else "#f0f2f5"}" stroke="{dccol}" stroke-width="1"/>')
        o.append(_txt(BX + BW - bw / 2 - 6, y + 19, dc, 6.6,
                      "#0d5f54" if dccol == AQUA else MUTED, anchor="middle", weight="700"))

    o.append(_txt(8, 236, "Jede andere Tiefe → Fehler. Die Challenge kennt genau diese fünf Tracks, "
                          "deshalb ist die Fallunterscheidung vollständig.", 7.2, FAINT))
    o.append("</svg>")
    return "\n".join(o)


# ══════════════════════════════════════════════════════════════════
# Figure: DC-Puls und paarweise Bewertung
# ══════════════════════════════════════════════════════════════════
def fig_dc():
    W, H = 520.0, 236.0
    EW, EH, EY = 186.0, 32.0, 70.0
    E1X, E2X = 20.0, 258.0
    NSTEP = 8
    sw_full = (EW - 16) / NSTEP

    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.0f} {H:.0f}" role="img" '
         f'aria-label="Zeitlicher Ablauf eines DC-Pulses \u00fcber zwei Epochen">',
         f'<rect width="{W:.0f}" height="{H:.0f}" fill="{SURFACE}"/>', DEFS]

    o.append(_txt(E1X, 13, "Epoche e \u2014 Referenz, kein Puls", 8.0, MUTED, weight="700"))
    o.append(_txt(E2X, 13, "Epoche e+1 \u2014 Puls", 8.0, NAVY, weight="700"))

    # pulse callout, right-aligned above the pulsed epoch
    px = E2X + EW - 8 - sw_full / 2
    o.append(_txt(W - 8, 32, "letzter Schritt der Epoche: +g\u00b7\u03b4 auf die Aktualisierung",
                  7.4, "#8c4a1d", anchor="end", weight="700"))
    o.append(_txt(W - 8, 42, "der letzten trainierbaren BN-Bias \u2014 die Laufstatistik hat den",
                  7.2, MUTED, anchor="end"))
    o.append(_txt(W - 8, 52, "Versatz noch nicht aufgenommen, er kommt am Ausgang an",
                  7.2, MUTED, anchor="end"))
    o.append(f'<line x1="{px:.1f}" y1="56" x2="{px:.1f}" y2="{EY+6:.1f}" stroke="{ORANGE}" '
             f'stroke-width="1.5" marker-end="url(#ah)"/>')

    for x, pulsed in ((E1X, False), (E2X, True)):
        o.append(_box(x, EY, EW, EH, SOFT if not pulsed else TINT, RULE if not pulsed else BLUE))
        for k in range(NSTEP):
            sx = x + 8 + k * sw_full
            last = (k == NSTEP - 1)
            fill = ORANGE if (last and pulsed) else ("#c6d5e4" if not pulsed else "#9fc0e0")
            o.append(f'<rect x="{sx:.1f}" y="{EY+8:.1f}" width="{sw_full-3:.1f}" height="16" '
                     f'rx="2" fill="{fill}"/>')
        o.append(_txt(x + EW / 2, EY + EH + 11, "8 Mini-Batch-Schritte", 7.0, FAINT, anchor="middle"))

    # validation read-outs
    for x, q, col in ((E1X + EW, "L\u2080", FAINT), (E2X + EW, "L\u2081", ORANGE)):
        o.append(f'<circle cx="{x+14:.1f}" cy="{EY+EH/2:.1f}" r="9.5" fill="{SURFACE}" '
                 f'stroke="{col}" stroke-width="1.6"/>')
        o.append(_txt(x + 14, EY + EH / 2 + 3, q, 7.8, col, anchor="middle", weight="700", fam=MONO))
        o.append(_txt(x + 14, EY + EH + 11, "Val.", 6.8, FAINT, anchor="middle"))

    # paired score bracket
    y0 = EY + EH + 20
    o.append(f'<path d="M {E1X+EW+14:.1f} {y0:.1f} L {E1X+EW+14:.1f} {y0+9:.1f} '
             f'L {E2X+EW+14:.1f} {y0+9:.1f} L {E2X+EW+14:.1f} {y0:.1f}" fill="none" '
             f'stroke="{ORANGE}" stroke-width="1.3"/>')
    o.append(_txt(W / 2, y0 + 24, "score(g) = L\u2081 \u2212 L\u2080", 9.0, INK,
                  anchor="middle", weight="700", fam=MONO))
    o.append(_txt(W / 2, y0 + 35, "Gepulste und ungepulste Epochen wechseln sich ab, deshalb f\u00e4llt die "
                                  "Drift zwischen Epochen aus der Differenz heraus.",
                  7.2, MUTED, anchor="middle"))

    # restore
    o.append(_box(8, 176, W - 16, 52, "#fdf6f0", ORANGE))
    o.append(_txt(17, 190, "Erster Schritt der Folgeepoche: \u2212g\u00b7\u03b4 \u2014 der Puls wird "
                           "zur\u00fcckgenommen.", 8.0, "#8c4a1d", weight="700"))
    o.append(_txt(17, 202, "Das Training l\u00e4uft auf der unver\u00e4nderten Bahn weiter. Nur der "
                           "Pr\u00fcfpunkt, an dem der Harness das beste", 7.2, MUTED))
    o.append(_txt(17, 211, "Modell sichert, sieht die Korrektur.", 7.2, MUTED))
    o.append(_txt(17, 223, "Nach der Probephase setzt argmin(score) den besten Gain dauerhaft; \u03b4 wird "
                           "alle 8 Epochen neu bestimmt.", 7.2, MUTED))
    o.append("</svg>")
    return "\n".join(o)


if __name__ == "__main__":
    import pathlib
    d = pathlib.Path(__file__).parent
    (d / "fig_loop.svg").write_text(fig_loop(), encoding="utf-8")
    (d / "fig_dispatch.svg").write_text(fig_dispatch(), encoding="utf-8")
    (d / "fig_dc.svg").write_text(fig_dc(), encoding="utf-8")
    print("wrote fig_loop.svg, fig_dispatch.svg, fig_dc.svg")
