"""Report long German words in the body that carry no soft hyphen.

Justified German text without a hyphenation dictionary develops rivers around
long compounds. This lists the candidates so they can be added to the curated
dictionary in hyphenate.py.
"""
import re, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from hyphenate import hyphenate, SHY

SKIP = re.compile(r"(<pre\b.*?</pre>|<code\b.*?</code>|<style\b.*?</style>"
                  r'|<span class="ref">.*?</span>|<[^>]+>)', re.S)
WORD = re.compile(r"[A-Za-zÄÖÜäöüß­]{15,}")

html = hyphenate(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"))
text = SKIP.sub(" ", html)
missing = {}
for w in WORD.findall(text):
    if SHY in w:
        continue
    missing[w] = missing.get(w, 0) + 1
if missing:
    print(f"{len(missing)} lange Wörter ohne Trennstelle:")
    for w, n in sorted(missing.items(), key=lambda kv: (-kv[1], kv[0])):
        print(f"  {n:>3}x  {w}")
else:
    print("alle langen Wörter haben Trennstellen")
