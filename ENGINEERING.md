<!-- Teil des SkyDive·Live Showcase — siehe README.md -->

# 📐 SkyDive·Live — Die Zahlen

*Das hier ist der Grund, warum das Projekt kein Bastel-Glücksspiel ist: jeder kritische Pfad ist **durchgerechnet und mit Reserve ausgelegt**. Sauber getrennt: was Formel/Herstellerspec ist — und was noch durch Messung (Gates G1–G3) zu bestätigen ist.*

---

## 1 · Funkstrecke — Link-Budget

**Basis:** 5 800 MHz · **+30 dBm (1 W)** TX · TX-Patch +5 dBi · RX-Boden-Patch +13 dBic · Kabel/Filter −3 dB · Schwelle für stabiles Bild −90 dBm (konservativ; HDZero-VRX-Spec −105 dBm).

**Freiraumdämpfung @ 4 000 m, 5,8 GHz:** `FSPL = 20·log(4000) + 20·log(5,8e9) − 147,55 =` **119,8 dB**

| Lage | Empfangspegel | Schwelle | **Reserve** | |
|---|---|---|---|---|
| **Bauch (Belly)**, Patch ↓ | −76,8 dBm | −90 dBm | **+13,2 dB** | 🟢 |
| Head-down, Patch ↑ | −103,8 dBm | −90 dBm | −13,8 dB | 🔴 |
| Head-down **+ Sekundär-Dipol** | −88,0 dBm | −90 dBm | **+2,0 dB** | 🟡 |

**Warum Head-down abreißt:** Patch-Rückkeule −12 dB + Körperabschattung −15 dB + Polarisation −2 dB = **−29 dB**. **Lösung (im Design, nicht im Backlog):** Dual-Antenne (Patch unten + λ/2-Dipol oben) **plus** Diversity-Empfang am Boden — dort liegt die eigentliche Robustheit (mehrere Boden-Antennen, Empfänger wählt das stärkste Signal; gleicher Ansatz wie Fastrax/Vislink).

**Oberwellen-Compliance:** AFuV verlangt ≥ 50 dBc; HDZero-PA liefert nur 30–45 dBc → **LPF ist Pflicht** (Mini-Circuits LFCW-6000+, −1,6 dB). Nachweis braucht ≥ 18-GHz-Analyzer (Gate G1-R, offen).

---

## 2 · Thermik — der eigentliche Knackpunkt, gelöst durch den Fahrtwind

**Verlustleistung:** bei 1 W RF zieht der VTX **~14 W** (HDZero-Spec 6–15 W) → **Q ≈ 13–14 W Wärme** (1 W geht als HF raus).

**Benötigter Wärmewiderstand:** `R_th = ΔT_limit / Q = 25 K / 14 W =` **1,79 K/W**

| Regime | Bedingung | ΔT | Case-Temp | Ziel ΔT<25 K? |
|---|---|---|---|---|
| Boden, Lüfter an | Q=13 W | ~55–80 K | 80–105 °C | grenzwertig |
| Boden, Alu passiv | Q≤10 W | ~25 K | ~50 °C | ✅ |
| **Freifall, v=50 m/s, Alu** | Q=14 W | **~6 K** | ~−9 °C (4 000 m) | **✅ deutlich** |

**Der entscheidende Hebel:** Im Freifall steht das Alu-Gehäuse im **~200 km/h Fahrtwind** → erzwungene Konvektion `h ≈ 90 W/m²K`, `R_th = 1/(90·0,026 m²) =` **0,43 K/W** → `ΔT = 14·0,43 =` **6 K**. Die thermische Masse (C ≈ 170 J/K) puffert die 60 s Freifall mühelos — **Doktrin: VTX erst ≤ 10 min vor dem Absprung einschalten, er startet kalt.**

**Hardware-Schutz** (ATtiny + NTC, Schaltung verifiziert): Lüfter an 45 °C · OSD-Warnung 65 °C · **VTX-Cutoff 75 °C** (5 K Reserve unter ~80 °C Limit) · Wiedereinschalten 55 °C.

---

## 3 · Regulatorik

| Kriterium | Wert |
|---|---|
| Band | 5 650–5 850 MHz (6-cm-Amateurfunk) |
| Lizenz | **Klasse E** (BNetzA-Duldung) |
| Max. Leistung Klasse E | **5 W PEP** → 1 W liegt komfortabel darunter |
| Oberwellen | ≥ 50 dBc / ≤ −20 dBm (AFuV Anlage 1) → LPF |
| Fallback | SRD lizenzfrei 5 725–5 875 MHz @ 25 mW EIRP |

*Offener Rechts-Vorbehalt: Publikumsanzeige (§5 AFuG / §16 AFuV) ist Grauzone — Klärung mit DARC/BNetzA geplant.*

---

## 4 · Energie & Gewicht

| Parameter | Wert | Grundlage |
|---|---|---|
| Akku | 3S LiPo 850 mAh (Low-Temp) | BOM |
| Stromaufnahme | **1,26 A @ 11,1 V** | 14 W / 11,1 V |
| Laufzeit (theoretisch) | **~40 min** | 850 mAh / 1 260 mA |
| Laufzeit (80 % DoD) | **~32 min** | dimensioniert |
| Einsatzdoktrin | ≤ 10 min aktiv vor Exit | Thermik |
| **Masse Sender (MK3)** | **~200–250 g** | dimensioniert |

---

## 5 · Verifizierungsstatus — ehrlich getrennt

| Wert | Art | Status |
|---|---|---|
| FSPL 119,8 dB | Formel | ✅ verifiziert |
| Link-Reserve +13,2 dB (Belly) | aus Herstellerspecs berechnet | ⏳ Feldmessung (G2) |
| Q = 13–14 W | externer Messwert + Spec | ⏳ Messung am VTX (G1-T) |
| Freifall ΔT 6 K | Flachplatten-Konvektion | ⏳ Flugtest (G3) |
| Laufzeit ~32 min | Kapazitätsrechnung | ⏳ Pack-Messung |
| S11 < −10 dB Patch | Theorie/Spec | ⏳ VNA (G1-R) |
| Cutoff @ 75 °C | dimensioniert + Code | ⏳ HW-Zyklustest |

> **Die Haltung:** Erst rechnen, mit Reserve auslegen, dann bauen und messen. Die Margen (+13 dB Funk, +19 K Thermik im Freifall) sind so dimensioniert, dass die offenen Messungen den Entwurf **bestätigen** sollten — der nächste Schritt ist der gebaute Prototyp, kein weiteres Dokument.
