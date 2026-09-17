# dc_steer_v6 — Anwendungsreport

Eine unabhängige technische Einschätzung des TIG-Algorithmus
[`dc_steer_v6`](../../tig-algorithms/src/neuralnet_optimizer/dc_steer_v6) für die
Challenge `neuralnet_optimizer`: was er tut, wie er sich in The Innovation Game
einfügt, wo seine Stärken und Schwächen liegen und wie er sich weiterentwickeln
ließe.

**→ [`dc_steer_v6_anwendungsreport.pdf`](dc_steer_v6_anwendungsreport.pdf)** (30 Seiten, deutsch)

## Inhalt

| Abschnitt | Thema |
|---|---|
| 1 | Management-Summary |
| 2 | Kontext: TIG, die Challenge, und was tatsächlich gemessen wird |
| 3 | Aufbau: Verteilung nach Netztiefe, gemeinsamer Kern, Herkunft |
| 4 | Die fünf Track-Implementierungen |
| 5 | DC-Steering — der eigentliche Beitrag |
| 6 | Bewertung: Stärken, Befunde, Zustand der Codebasis |
| 7 | Dreizehn Vorschläge zur Weiterentwicklung |
| 8 | Übertragbarkeit über TIG hinaus |
| A | Anhang: Dateien, Vorgabewerte, Lizenzen, Methodik |

## Grundlage und Grenzen

Der Bericht beruht ausschließlich auf einer Quelltextanalyse dieses Repositorys.
**Es wurden keine eigenen Trainingsläufe durchgeführt** — die Challenge braucht eine
CUDA-fähige GPU. Aussagen über Struktur, Rechenwege und erreichbare Codepfade sind
am Quelltext belegt und mit Datei und Zeile referenziert; alle Zahlen zu gemessenen
Quality-Gewinnen stammen aus Kommentaren im Algorithmus und sind als Angabe des
Autors gekennzeichnet. Abschnitt A.4 des PDF führt diese Abgrenzung im Einzelnen aus.

Zeilennummern beziehen sich auf den Stand von `main` am 17. September 2026.

## Neu erzeugen

Der Bericht wird aus HTML über Chromium (DevTools-Protokoll) gesetzt. Benötigt werden
Python 3.11+, die Pakete `websockets` und `pypdf` sowie ein Chromium-Binary.

```bash
cd reports/dc_steer_v6/src
pip install websockets pypdf
export CHROME=/pfad/zu/chromium          # von html2pdf.py gelesen
python3 figures.py && python3 figures2.py   # SVG-Abbildungen erzeugen
python3 build.py ../dc_steer_v6_anwendungsreport.pdf
```

| Datei | Zweck |
|---|---|
| `cover.html`, `body.html` | Inhalt |
| `style.css` | Druck-Stylesheet (A4) |
| `figures.py` | Datengrafiken (Codeumfang, Quality-Nomogramm) |
| `figures2.py` | Schemazeichnungen (Trainingsschleife, Verteilung, DC-Puls) |
| `hyphenate.py` | Kuratierte Trennstellen — Chromium hat hier kein Wörterbuch |
| `checkhyph.py` | Meldet lange Wörter ohne Trennstelle |
| `html2pdf.py` | Rendert HTML über CDP, mit Kopfzeile und Seitenzahlen |
| `build.py` | Setzt Deckblatt und Textteil zusammen |

## Lizenz

Dieser Bericht ist eine eigenständige Analyse und keine Veröffentlichung der
TIG Foundation. Der besprochene Algorithmus steht unter den TIG-Lizenzen; siehe
[`docs/licenses`](../../docs/licenses) und Abschnitt A.3 des Berichts.
