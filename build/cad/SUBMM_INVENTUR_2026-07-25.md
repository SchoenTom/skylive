# Sub-mm-Inventur — Zwischengröße (`mid_sender.py`), 2026-07-25

Ingenieur-Leitlinie: „Alles unter 1 mm muss größer oder stabiler — zu filigran für den Drucker."
Regel dieser Inventur: **Wände/Stege** < 1 mm sind Kandidaten. **Spalte/Toleranzen/Quetschmaße**
sind ABSICHTLICH klein und tabu — sie zu vergrößern zerstört Passung oder Klemmung.
Backstop auf Mesh-Ebene: das Printability-Gate v2 failt bei jedem Export hart auf
flächige Dünnwand-Plateaus < 0,8 mm (aktuell: 6/6 PASS).

## Heute durch die Fixes BESEITIGT (waren die echten Sünder)

| Feature | war | Status |
|---|---|---|
| Tür-Finger t=1,2 quer zur Schicht + 90°-Haken 1,0 | brach beim Absupporten | **F3: ersatzlos entfernt** |
| XT30-M2-Kern-TRÄGER = freier 6,6er-Finger | „Löcher praktisch nicht vorhanden" | **F2: Kerne in Vollmaterial-Brücke** — Korrektur (Review): im Rinnen-Tiefenband (oberste 1,3) schneidet der Kern wie in v1 beidseitig 0,15 in die Rinnenflanken; darunter voll ummantelt. Der eigentliche Fix ist der massive Träger. |
| XT30-Finger-Sättel 6,6 breit, frei zu Mitte+Rand | Support-fragil | **F2: durchgehende Brücke** |
| Kamera-Flanke nur an Schichtnaht der Wand | riss beim Absupporten | **F1: Fuß auf Shelf** |
| Omni-Kappen-Piloten Ø1,7 horizontal in 3er-Wand | Seitenhalterung | **F4: ersatzlos entfernt** |

## Bleibt — mit Begründung (Toms Entscheidung, Zeile für Zeile)

| # | Feature | Maß | Klasse | Empfehlung |
|---|---|---|---|---|
| 1 | Vent-Lamellen-Steg (senkrecht, 45°-Projektion) | **0,72** (VENT_W 1,4 · Pitch 3,0) | bewusstes Feinfeature | **Lassen** — am 850er-Druck bewiesen (druckt als 1–2-Perimeter-Band). Falls Tom mehr Fleisch will: Pitch 3,0→3,4 ⇒ Steg 1,0, Kosten: ~12 % weniger Luftquerschnitt. |
| 2 | ZE-Insert-Restwand nach außen | ~1,5–1,6 | grenzwertig, dokumentiert | Lassen (Druckhinweis „vorsichtig einschmelzen" im README existiert). |
| 3 | Tür-Pilot M2 selbstschneidend | Ø1,6 Kern | Funktionsmaß | Lassen (Schraube braucht Biss). |
| 4 | XT30-M2-Kerne | Ø1,7 Kern | Funktionsmaß | Lassen — seit F2 voll ummantelt. |
| 5 | GoPro-Zinken-Wurzel-Fillet | R0,8 | Feinfeature | Lassen (Tom: „Zinken sind perfekt"; mehr Radius erst nach Fit-Messung, TOM_PENDING #5). |
| 6 | XT30-Brücken-Rinnenboden (Nachtrag Review) | **0,7** (Brücke 2,0 − Rinne 1,3) | tragende Bogen-Geometrie unter Klemmlast | Beobachten am Fit-Print; Bogen (kein Plateau) → Printability-Gate grün. Bei Bruch: XT30_SAD_Z-Band um 0,5 höher ziehen. |

## Tabu-Liste (klein = Absicht, NIE „aufdicken")

| Maß | Wert | Funktion |
|---|---|---|
| TOL_SLIDE | 0,3/Seite | Tür-Gleitspiel — größer = Klappern, kleiner = klemmt |
| Kabel-Quetsch | 0,2 (Licht 2,6 auf Ader 2,8) | DIE Klemmwirkung der Zugentlastung |
| AZE_CLR | 0,1/Seite | T-Stück-Passung |
| Diverse 0,1/0,2/0,3-Offsets | — | Montage-/Schwenkluft, Blind-Schultern |

*Konstanten-Ebene vollständig geprüft; Mesh-Ebene übernimmt das Gate (hart < 0,8). CAD ≠ Drucktest.*
