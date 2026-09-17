#!/usr/bin/env python3
"""Build the report PDF: cover (no running head) + body (running head + page numbers)."""
import asyncio, os, re, sys, pathlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from html2pdf import render
from hyphenate import hyphenate
from pypdf import PdfWriter, PdfReader

D = pathlib.Path(__file__).parent
OUT = sys.argv[1] if len(sys.argv) > 1 else str(D / "dc_steer_v6_anwendungsreport.pdf")


FIG = re.compile(r"<!--FIG:([a-z_0-9]+)-->")


def prep(name):
    """Inline the figures, soft-hyphenate long German compounds, then stage."""
    src = (D / name).read_text(encoding="utf-8")
    src = FIG.sub(lambda m: (D / (m.group(1) + ".svg")).read_text(encoding="utf-8"), src)
    dst = D / ("_h_" + name)
    dst.write_text(hyphenate(src), encoding="utf-8")
    return str(dst)


async def main():
    await render(prep("cover.html"), str(D / "_cover.pdf"), headers=False)
    await render(prep("body.html"), str(D / "_body.pdf"), headers=True)
    w = PdfWriter()
    for f in ("_cover.pdf", "_body.pdf"):
        for page in PdfReader(str(D / f)).pages:
            w.add_page(page)
    w.add_metadata({
        "/Title": "dc_steer_v6 - Anwendungsreport",
        "/Subject": "Analyse und Weiterentwicklungspotenzial des TIG-Optimizers dc_steer_v6",
        "/Keywords": "TIG, neuralnet_optimizer, dc_steer_v6, CUDA, Optimierer, Deep Learning",
        "/Creator": "Claude Code",
    })
    with open(OUT, "wb") as fh:
        w.write(fh)
    n = len(PdfReader(OUT).pages)
    print(f"wrote {OUT} -- {n} pages, {os.path.getsize(OUT)} bytes")


asyncio.run(main())
