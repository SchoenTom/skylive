<!-- Teil des SkyDive·Live Showcase — siehe README.md -->

# 🧩 SkyDive·Live — Stückliste (BOM)

*Komponentenebene, Konzept-/Prototyp-Stand. Bezugsquellen & Preise bewusst nicht öffentlich.*

## Sender — Elektronik & Funk

| Komponente | Spec / Rolle |
|---|---|
| **HDZero Freestyle V2 VTX** | 5,8 GHz, 1 W, MIPI-In, U.FL-Out, 7–25 V, 30×29×14 mm — Herzstück |
| **HDZero Micro V3 Kamera** | 19×19×24 mm, MIPI 20-Pin FFC — wird über MIPI vom VTX gespeist |
| **MIPI-Kabel 80 mm** | 20-Pin FFC, 0,5 mm Raster — Bild + Strom Kamera↔VTX |
| **3S-LiPo ~850 mAh** (Low-Temp) | ~56×30×23 mm, XT30 + JST-XH, −20 °C tauglich |
| **3S-BMS, 3,0-V-Cutoff** | Zellenschutz (bewusst 3,0 V statt 2,55 V) |
| **Patch TBS 5G8 RHCP** | 35×35×6 mm, ~5 dBi · 110° — Hauptantenne (Belly) |
| **Schiebeschalter SS-12D00G** | schaltet nur das Gate, nie den Laststrom |
| **MOSFET AO3401A** | P-Channel SOT-23, trägt 1,35 A |
| **ATtiny412 + NTC 10 kΩ** | Übertemperatur-Cutoff @ 75 °C (Latch-Off) |
| **5-V-Buck/BEC** | versorgt ATtiny/Lüfter (3S direkt würde ATtiny zerstören) |
| **Sunon GM0502PFV1** | 25×25×10 mm, ~3,5 CFM — aktives Kühlkonzept (MK2-Kanal) |
| **Wärmeleitpad Arctic TP-3** | ~6 W/mK — koppelt VTX an Alu-Außenwand (lüfterlos, v5) |
| **SPDT-RF-Switch** | DC–6 GHz — schaltet Patch ↔ Dipol (v5-Modul) |
| **λ/2-Dipol 5,8 GHz** | ~26 mm, U.FL — Zweitantenne Head-down (v5) |
| **U.FL-Pigtail RG178** | U.FL→RP-SMA-Bulkhead |

## Sender — Gehäuse & Mechanik

| Komponente | Rolle |
|---|---|
| **ASA/PETG-Druckteile** | Korpus, Cover, Einschub, RF-Fenster |
| **Alu-Unterkorpus** (MK4-Ziel) | Struktur, GoPro-Mount, Heatsink-Masse, Ground-Plane |
| **Heat-Set-Inserts M3/M2** | Cover (4×M3), Tray (1×M3), VTX (M2) |
| **GoPro-M5-Daumenschraube** | Helm-Montage |
| **GORE-Druckausgleichmembran** | Druckausgleich ohne Feuchteeintritt |
| **Pyrogel XT / Polyimid** | Heatshield Akku ↔ VTX |
| **Dyneema-Lanyard** | FOD-Sicherung Tray → Helm |
| **Conformal Coating** | Schutz gegen Wolkenfeuchte/Kondensat |

## Bodenstation

| Komponente | Spec / Rolle |
|---|---|
| **HDZero VRX4** | Diversity-Empfänger, 4× SMA, HDMI-Out — Kern |
| **TrueRC X²-AIR MkII** (2–3×) | High-Gain-Richt-Patch, nach oben — Hauptlink |
| **Lumenier AXII 2 LR** (1–2×) | Omni — Nahbereich/Abriss-Auffang |
| **ezcap273A** | HDMI→microSD-Recorder — garantierter Mitschnitt |
| **Feldmonitor 1080p** | sonnentaugliches Live-Display |
| **Glasfaser-HDMI 50–70 m** | zum Public-Viewing-Screen |
| **LiFePO4 ~300 Wh** | autonome Feldstromversorgung |
| **Stativ + Antennenmast** | Ausrichtung/Höhe |

## Messtechnik (Prototyp-Validierung)

| Gerät | Zweck |
|---|---|
| **LiteVNA-64** (bis 6,3 GHz) | Patch/Dipol S11 @ 5,8 GHz |
| **tinySA Ultra+ (ZS-406)** (bis 6 GHz) | Spektrum + Oberwellen + EIRP (älterer Ultra endet ~5,4 GHz → unter dem Band) |
| **Wärmebildkamera / IR** | VTX-Thermik bei 1 W (Gate G1-T) |
| **Strommesszange** | reale Stromaufnahme |
