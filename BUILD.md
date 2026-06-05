<!-- Teil des SkyDive·Live Showcase — siehe README.md -->

# 🔧 SkyDive·Live — Schritt-für-Schritt-Bauanleitung (Sender)

*Stand: CAD-Verifikation abgeschlossen (9/9 ✓, 2026-06-01) — Geometrie watertight & kollisionsfrei. Der erste Kalibrierdruck und die Passungstests A–F sind der geplante nächste Schritt.*

---

## 1. 3D-Druck des Gehäuses

### 1.1 Druckteile

| Datei (`housing_out_mk2/`) | Bounding Box | Volumen | Orientierung |
|---|---|---|---|
| `mk2_body.stl` | 78 × 63 × 69 mm | 59,7 cm³ | offener Top nach oben, auf den GoPro-Fingern |
| `mk2_cover.stl` | 78 × 56 × 3 mm | 12,8 cm³ | flach, Außenseite unten |
| `mk2_tray.stl` | 34 × 30 × 50 mm | 11,0 cm³ | flach, Türplatte unten |

### 1.2 Druckeinstellungen (PETG, Iteration 1)

| Parameter | Wert | | Parameter | Wert |
|---|---|---|---|---|
| Düse | 0,4 mm | | Düsentemp | ~240 °C |
| Schichthöhe | 0,2 mm | | Betttemp | ~80 °C |
| Perimeter | 4 | | Lüfter | 30–50 % (1. Schicht 0 %) |
| Infill | 30–40 % Gyroid | | Speed | 40–50 mm/s · Brim 5 mm |

**Support:** Touching-Buildplate unter Boden + Linsen-Nase (Baum-Support). Standoffs, Hitzewand, Lokatoren drucken senkrecht ohne Stütze. **Warum PETG:** schlagfest, leicht druckbar, ausreichend wärmebeständig (PETG-CF/ASA werden für MK3 evaluiert).

### 1.3 Nacharbeit

1. Support entfernen (Boden + Linsen-Nase).
2. **Radom-Fläche** (Bodenmitte, 1,2 mm) leicht planschleifen — die 1,2 mm müssen erhalten bleiben (HF-transparent bei 5,8 GHz).
3. **5× M3-Heat-Set-Inserts** einschmelzen (~200 °C): 4× Cover-Bosse, 1× Tray-Riegel.
4. Bohrungen/Schlitze entgraten.

> Plane einen **Kalibrierdruck** ein (PETG schrumpft/quillt 0,1–0,3 mm). Finalen Satz erst drucken, wenn Tests A–F sitzen.

---

## 2. Bauteile vorbereiten

| Bauteil | Maß | Vorbereitung |
|---|---|---|
| HDZero Freestyle V2 VTX | 29 × 30 × 14 mm | Stock-Heatsink bleibt drauf |
| HDZero Micro V3 Kamera | 19 × 19 × 24 mm | M12-Linse + Fokus, Anti-Fog |
| MIPI-Kabel | 80 mm, 20-Pin FFC | ESD-Erdband |
| 3S-LiPo + BMS | 24 × 14 × 46 mm | BMS 3,0-V-Cutoff, JST-XH-4P |
| Patch-Antenne | 35 × 35 × 3 mm | 13 × 6 mm Hinterkante ausschneiden → NanoVNA: S11 < −10 dB @ 5,8 GHz |
| Sunon-Lüfter | 25 × 25 × 10 mm | Leichtgängigkeit prüfen |
| AO3401 MOSFET | SOT-23-3 | auf Lochraster, 10 kΩ Pull-up |

---

## 3. Montagereihenfolge (zwingend — spätere Teile sonst unerreichbar)

1. **Patch-Antenne** in die Bodenwanne (`Pos 9,6,−26`), U.FL einrasten + Heißkleber, Pigtail durch Ø-4,4-Kanal nach oben. *Zuerst, weil der VTX-Stack später den Zugang versperrt.*
2. **VTX flach** auf die 2 hinteren M2-Standoffs (M2×5, self-tapping). Heatsink + Wärmeleitpad. *Flach, weil 29 & 30 mm Board-Maße nur über die 14-mm-Dicke in Z passen (DD-001).*
3. **Schalter** SS-12D00G in den +X-Schlitz, **MOSFET-Platine** daneben heißkleben.
4. **Kamera** Push-Fit in 4 Lokator-Rippen, Linse durch Ø-14-Nase. *Schneller Feldtausch, vibrationsfest ohne Schraube.*
5. **Cover**: Schaumpad auf Lüfter (klemmt VTX-Stack), 2× M2 Lüfter, 4× M3 Cover.

---

## 4. Verkabelung & Strom

1. **MIPI** Kamera↔VTX (ESD, Slack über die Hitzewand, Heißkleber an beiden Steckern).
2. **U.FL-Pigtail** Patch→VTX einrasten + Heißkleber.
3. **Power** 2× 60 mm AWG-26 V+/V− → AO3401 (Drain), Sternpunkt-Masse.
4. **Schalter** 50 mm AWG-28 Common→Akku-Knoten, Gate→MOSFET (10 kΩ Pull-up).
5. **Lüfter** 2× 80 mm AWG-26.
6. **Conformal Coating** auf alle Lötstellen (Gehäuse ist belüftet, nicht versiegelt — Coating schützt gegen Wolkenfeuchte).
7. **Akku-Tray** von −X einschieben, Pogo-Pins ~1,5 mm Mid-Stroke, captive M3-Rändelschraube, **Dyneema-Sicherungsleine** zum Helm.

> ⚠️ LiPo **ausschließlich extern** am Balance-Lader laden — nie eingebaut.

---

## 5. Verifikation — Passungstest A–F (nächster Schritt nach dem Kalibrierdruck)

| Test | Prüft | Soll |
|---|---|---|
| **A** Maßhaltigkeit | Außenhülle / Wand / Radom / Hitzewand | 78×56×57 mm · 3,0 mm · 1,2 mm · 2,0 mm |
| **B** Cover & Schrauben | 4× M3-Heat-Set bündig, kein Spalt, GORE-Loch frei | — |
| **C** Akku-Tray *(kritischster Test)* | 5× rein/raus ohne Klemmen, Riegel klickt, 3 Pogo-Pins ~1,5 mm, Verpolschutz | — |
| **D** VTX/Kamera/Antenne | VTX flach auf 4 Säulen, Kamera fest in Rippen, **Kamera-Lüfter-Spalt > 2 mm** (MK1-Engpass, in MK2 +6 mm gelöst), Patch-NanoVNA | — |
| **E** Kühlung/Schalter/Mount | NACA-Einlass + 3 Auslässe frei, Schalter versenkt, GoPro-Ø-5-Bohrung, Kabelwege | — |
| **F** Gesamtmontage | alles ohne Würgen, Tray → LED grün → Bild auf Monitor, Gewicht + Schwerpunkt | — |

**Freigaberegel:** Erst wenn **A–F** bestehen, wird der finale Satz gedruckt — bei Fehlschlag nur das betroffene Teil korrigieren.

---

*Abgenommen im CAD: 3× watertight, 0 Kollisionen, Wandstärke min 0,95 mm, Bauteilmaße gegen reale Werte. Offen (nächster Schritt): Passungstests, Thermik-Messung am VTX, Flugtest.*
