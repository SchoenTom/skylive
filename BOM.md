<!-- Part of the SkyDive·Live showcase — see README.md -->

# 🧩 SkyDive·Live — Bill of materials (BOM)

*Component level, concept/prototype state. Vendors & prices deliberately not public.*

## Sender — electronics & RF

| component | spec / role |
|---|---|
| **HDZero Freestyle V2 VTX** | 5.8 GHz, 1 W, MIPI in, U.FL out, 7–25 V, 30×29×14 mm — the heart |
| **HDZero Micro V3 camera** | 19×19×24 mm, MIPI 20-pin FFC — powered by the VTX over MIPI |
| **MIPI cable 80 mm** | 20-pin FFC, 0.5 mm pitch — video + power, camera↔VTX |
| **3S LiPo ~850 mAh** (low-temp) | ~56×30×23 mm, XT30 + JST-XH, rated to −20 °C |
| **3S BMS, 3.0 V cutoff** | cell protection (deliberately 3.0 V instead of 2.55 V) |
| **Patch TBS 5G8 RHCP** | 35×35×6 mm, ~5 dBi · 110° — primary antenna |
| **Slide switch SS-12D00G** | switches only the gate, never the load current |
| **MOSFET AO3401A** | P-channel SOT-23, carries the 1.35 A |
| **ATtiny412 + 10 kΩ NTC** | over-temperature cutoff @ 75 °C (latch-off) |
| **5 V buck/BEC** | feeds ATtiny/fan (3S directly would kill the ATtiny) |
| **Sunon GM0502PFV1** | 25×25×10 mm, ~3.5 CFM — active cooling concept (MK2 duct) |
| **Thermal pad Arctic TP-3** | ~6 W/mK — couples the VTX to the aluminium outer wall (fanless, v5) |
| **SPDT RF switch** | DC–6 GHz — selects patch ↔ dipole (v5 module) |
| **λ/2 dipole 5.8 GHz** | ~26 mm, U.FL — secondary antenna for head-down (v5) |
| **U.FL pigtail RG178** | U.FL → RP-SMA bulkhead |

## Sender — housing & mechanics

| component | role |
|---|---|
| **ASA/PETG printed parts** | body, cover, sled, RF window |
| **Aluminium lower body** (MK4 target) | structure, GoPro mount, heatsink mass, antenna ground plane |
| **M3/M2 brass heat-set inserts** | cover (4× M3), tray (1× M3), VTX (M2) |
| **GoPro M5 thumbscrew** | helmet mount |
| **GORE pressure-equalisation vent** | pressure equalisation without moisture ingress |
| **Pyrogel XT / polyimide** | heat shield, battery ↔ VTX |
| **Dyneema lanyard** | FOD retention, tray → helmet |
| **Conformal coating** | protection against cloud moisture / condensation |

## Ground station

| component | spec / role |
|---|---|
| **HDZero VRX4** | diversity receiver, 4× SMA, HDMI out — the core |
| **TrueRC X²-AIR MkII** (2–3×) | high-gain directional patch, aimed up — main link |
| **Lumenier AXII 2 LR** (1–2×) | omni — close range / dropout catch |
| **ezcap273A** | HDMI → microSD recorder — guaranteed recording |
| **Field monitor 1080p** | daylight-readable live display |
| **Fibre-optic HDMI 50–70 m** | to the public-viewing screen |
| **LiFePO4 ~300 Wh** | autonomous field power |
| **Tripod + antenna mast** | aiming / height |

## Measurement gear (prototype validation)

| device | purpose |
|---|---|
| **LiteVNA-64** (to 6.3 GHz) | patch/dipole S11 @ 5.8 GHz |
| **tinySA Ultra+ (ZS-406)** (to 6 GHz) | spectrum + harmonics + EIRP (the older Ultra tops out ~5.4 GHz — below the band) |
| **Thermal camera / IR** | VTX thermals at 1 W (gate G1-T) |
| **Current clamp** | real current draw |
