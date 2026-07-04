# SkyLive — Bill of Materials

*Prices as of 2026-07, EU/DE vendors, from the project's real order log (German original:
`BESTELLLISTE_SENDER_FINAL`). Stock and prices rotate daily in FPV shops — verify on the day
you click. Items marked “—” were already owned or not in the logged order.*

## 1 · Sender — the four functional parts

| # | part | exact product | ≈ € | note |
|---|---|---|---|---|
| ① | VTX + camera + MIPI | **HDZero Freestyle V2 VTX Kit** (incl. Nano90 camera, MIPI cable, stock antenna) | 179.95 | cheaper than buying VTX (118.95) + camera separately |
| ② | Battery | **Tattu R-Line 3S 850 mAh, XT30** | 14.99 | ×3 bought for bench rotation; cold-rated packs only for the real jump |
| ③ | Switch | **12 mm latching push-button, pre-wired** (2 A / 12–250 V) | ~5 | Amazon-class part; voltage/current-safe for 3S @ ~1.3 A |
| ④ | Power joins | **3× Wago 221-412** lever clamps | ~3 | the entire power wiring — zero solder joints |

## 2 · Antenna path (one SMA joint inside — U.FL touched exactly once)

| part | role | ≈ € | note |
|---|---|---|---|
| **TBS SMA pigtail, U.FL → SMA flange, 60 mm** | the fixed inner joint that protects the VTX U.FL (~30 cycles) | 5.99 | ×4 bought (spares — treat as consumable) |
| **Lumenier AXII 2, RHCP, SMA** | **Version A — the donut omni**, fully encapsulated in the side-wall capsule | — | 73 × 17.5 mm, 7.8 g, 2.2 dBic, 5.3–6.2 GHz (manufacturer page) |
| **TBS 5G8 patch, RHCP** | **Version B — the down patch** in the bottom shell | 11.90–14.90 | ⚠ exists in SMA and RP-SMA variants — the project's patch is **RP-SMA**; match your pigtail, SMA ≠ RP-SMA |
| SMA↔RP-SMA adapter kit | catch-all for any connector mix | ~6 | Amazon kit |

### Antenna test kit (bought deliberately — the shoot-out is part of the project's honesty)

| part | ≈ € | why |
|---|---|---|
| TrueRC OCP 5.8 omni, RHCP, SMA (×2) | 15.99 ea. | omni comparison candidate |
| Foxeer Micro Lollipop, RHCP, U.FL | 18.90 | budget omni comparison |
| TrueRC Matchstick Carbon Long, RHCP, U.FL | 29.90 | premium omni comparison |
| Linear λ/2 dipole, U.FL | 1.85 | **only** to demonstrate the −3 dB polarization penalty vs a true RHCP omni — not a fitted part |

## 3 · Case & assembly consumables

| part | ≈ € | note |
|---|---|---|
| PETG (prototypes) / **ASA (final)** filament | ~25/kg | never PLA — it softens too low; case files `TBD-CAD-M6` |
| Silicone thermal pad, 1.5 mm, ≥ 3 W/mK | ~8 | VTX face → wall, mandatory |
| M3 heat-set inserts (Ruthex RX-M3x5.7 class) + M3 screws | ~10 | 2× nylon M3 preferred at the antenna capsule |
| TPU filament (capsule tip pad + root ring, orange) | ~15 | the orange tip pad doubles as the antenna witness indicator |
| Heat-shrink, RTV/hot glue, zip ties | ~5 | Wago securing + strain relief |
| Soft foam padding, ~2 mm (EVA/PE) | ~3 | **mandatory** battery preload — the pack must never fly free in the bay (a loose 80 g pack hits ~590 N on a hard stop; the foam cuts that to ~250 N) |
| 50 Ω SMA dummy load | ~8 | safe bench power-up without an antenna |

## 4 · Ground station

| part | role | ≈ € |
|---|---|---|
| **HDZero BoxPro** | 4-way diversity RX, Mini-HDMI out to the TV | ~360–420 |
| **TrueRC X²-AIR MK II patch, RHCP, SMA** | aimed range-maker (nominal 13 dBic, budget ~10) | ~60 |
| **Lumenier Double AXII 2 LR, RHCP, SMA** | horizon omni (~4.7 dBic) | ~30 |
| **TrueRC Matchstick Carbon Long, RHCP, SMA** | overhead omni (~1.9 dBic) | 29.90 |
| HDMI cable + public-viewing TV/monitor | the whole point | — |

## 5 · Tools & measurement (staged — bench first)

| item | ≈ € | stage |
|---|---|---|
| **Multimeter** | ~25 | now — polarity check is a hard gate before first power |
| Balance charger 3S (+ XT60→XT30 adapter) | ~40 | now |
| K-type probe thermometer or IR thermometer | 10–20 | thermal A/B test (see [`MEASURE.md`](MEASURE.md)) |
| VNA covering 5.8 GHz (LiteVNA class — a NanoVNA-H does **not** reach the band) | ~120 | before trusting any antenna/capsule RF claim |

## Order-log reality notes (kept, because they will bite you too)

- The **VTX kit** was in stock at n-Factory when ordered; two other shops 404'd the same week.
- Buy the **patch in the connector variant that matches your pigtail** — the order log caught
  an RP-SMA/SMA mismatch at checkout.
- **HDZero receivers churn**: BoxPro was sold out at one shop; a used HDZero goggle/VRX from the
  classifieds is the cheapest first picture. Analog goggles **cannot** receive HDZero at all.
- Sender hardware total (without receiver): **~€ 410–450** as ordered.
