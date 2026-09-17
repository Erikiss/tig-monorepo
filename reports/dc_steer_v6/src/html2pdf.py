#!/usr/bin/env python3
"""Render a local HTML file to PDF via Chromium's DevTools Protocol.

Unlike `chrome --print-to-pdf`, CDP's Page.printToPDF accepts header/footer
templates, so the output gets real running headers and page numbers.
"""
import asyncio, base64, json, os, subprocess, sys, time, urllib.request

CHROME = os.environ.get("CHROME", "/opt/pw-browsers/chromium-1194/chrome-linux/chrome")
PORT = 9333

HEADER = """
<div style="font-family:'Liberation Sans',sans-serif;font-size:7.5pt;color:#8a94a6;
            width:100%;padding:0 16mm;display:flex;justify-content:space-between;">
  <span>dc_steer_v6 &middot; Anwendungsreport</span>
  <span>TIG &middot; neuralnet_optimizer</span>
</div>
"""

FOOTER = """
<div style="font-family:'Liberation Sans',sans-serif;font-size:7.5pt;color:#8a94a6;
            width:100%;padding:0 16mm;display:flex;justify-content:space-between;">
  <span></span>
  <span><span class="pageNumber"></span> / <span class="totalPages"></span></span>
</div>
"""


async def render(html_path, pdf_path, headers=True):
    import websockets

    proc = subprocess.Popen(
        [CHROME, "--headless", "--disable-gpu", "--no-sandbox", "--hide-scrollbars",
         "--disable-dev-shm-usage", f"--remote-debugging-port={PORT}",
         "--font-render-hinting=none", "about:blank"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    try:
        ws_url = None
        for _ in range(120):
            try:
                with urllib.request.urlopen(f"http://127.0.0.1:{PORT}/json/version", timeout=1) as r:
                    ws_url = json.load(r)["webSocketDebuggerUrl"]
                break
            except Exception:
                time.sleep(0.25)
        if not ws_url:
            raise RuntimeError("Chromium DevTools endpoint did not come up")

        async with websockets.connect(ws_url, max_size=256 * 1024 * 1024) as ws:
            i = 0

            async def cmd(method, params=None, sid=None):
                nonlocal i
                i += 1
                msg = {"id": i, "method": method, "params": params or {}}
                if sid:
                    msg["sessionId"] = sid
                await ws.send(json.dumps(msg))
                while True:
                    res = json.loads(await ws.recv())
                    if res.get("id") == i:
                        if "error" in res:
                            raise RuntimeError(f"{method}: {res['error']}")
                        return res.get("result", {})

            tgt = await cmd("Target.createTarget", {"url": "about:blank"})
            sid = (await cmd("Target.attachToTarget",
                             {"targetId": tgt["targetId"], "flatten": True}))["sessionId"]
            await cmd("Page.enable", {}, sid)
            await cmd("Page.navigate", {"url": "file://" + os.path.abspath(html_path)}, sid)

            # Wait for load + webfont/layout settle.
            deadline = time.time() + 45
            loaded = False
            while time.time() < deadline and not loaded:
                try:
                    ev = json.loads(await asyncio.wait_for(ws.recv(), timeout=5))
                    if ev.get("method") == "Page.loadEventFired":
                        loaded = True
                except asyncio.TimeoutError:
                    break
            await asyncio.sleep(1.0)

            out = await cmd("Page.printToPDF", {
                "printBackground": True,
                "preferCSSPageSize": False,
                "paperWidth": 8.268, "paperHeight": 11.693,
                "displayHeaderFooter": headers,
                "headerTemplate": HEADER,
                "footerTemplate": FOOTER,
                "marginTop": 0.79, "marginBottom": 0.71,
                "marginLeft": 0.669, "marginRight": 0.669,
                "generateTaggedPDF": True,
            }, sid)
            with open(pdf_path, "wb") as fh:
                fh.write(base64.b64decode(out["data"]))
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            proc.kill()


if __name__ == "__main__":
    asyncio.run(render(sys.argv[1], sys.argv[2], headers="--no-headers" not in sys.argv))
    print(f"wrote {sys.argv[2]} ({os.path.getsize(sys.argv[2])} bytes)")
