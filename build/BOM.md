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
| M2 DIN 912 cap screws: 4× M2×8 (antenna T-pieces) + 1× M2×6 (door tab) + 4× M2×8 (XT30 latches) + 2× M2 (camera) | ~4 | all cap-head (project standard) |
| M2 brass heat-set insert, Ø3.2 × 3.0 (measured) | ~1 | door-tab thread — the most-cycled screw (every battery swap) gets brass, not self-tapped PETG; T-pieces/latches stay on Ø1.7 printed cores (low-cycle) |
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

## 6 · Alternatives (with dims)

*Every part below is a real, buyable component with a verifiable published dimension (or an
honest "dims unpublished" where the maker only ships CAD). "Fits as-is" means it drops into the
current case concept; "fits with note X" means it works but changes something you must account
for. Wall thickness is never traded for volume — see the wall-thickness doctrine.*

### 6.1 · VTX alternatives (core: Freestyle V2 = 29.2 × 30 × 14.1 mm, U.FL, 20×20 M2)

| part | L×W×H | interface | fit |
|---|---|---|---|
| **HDZero Freestyle V1** (30×30) — the backup unit on hand | 40 × 42 × 10 mm, 28 g | U.FL, **30×30 M3** mount | **fits with rework**: larger footprint (40×42 vs 29.2×30) but thinner (10 vs 14.1) → needs a **wider, shallower VTX bay** and a 30×30 M3 boss pattern instead of 20×20 M2. Same 1 W class, same U.FL-once rule. |
| **HDZero Race V3** | 28 × 32 × 5 mm, 5.5 g | U.FL, 20×20 M2 mount | **fits with note**: smaller and far thinner than the V2 (frees bay depth), 20×20 M2 boss pattern matches. **But max 200 mW, not 1 W** (4–12 V input, no 6S) → this is a link-budget downgrade, not a like-for-like swap — only for a short-range/low-power build. |

### 6.2 · Camera alternatives (core: Nano90 = 14 × 18.5 × 19 mm, MIPI 20-pin)

| part | L×W×H | interface | fit |
|---|---|---|---|
| **HDZero Nano V3** | 14 × 16 × 14 mm, 2.2 g | MIPI 20-pin | **fits as-is** — nano-class body, essentially interchangeable with the Nano90 in the same clamp; Starlight low-light sensor is a bonus. |
| **HDZero Micro V2** | 19 × 19 × 21 mm, 8.5 g | MIPI, 19×19 mount | **requires camera-bay rework** — the 19 mm square micro body does **not** fit the ~15 mm nano clamp; you would re-cut the camera bay for a 19×19 front mount. |

### 6.3 · Battery alternatives — **rule: ≤ 60 × 30 × 23 mm fits the bay; a shorter pack = more XT30 room**

Core: Tattu R-Line 3S 850 = 60 × 30 × 23 mm, XT30. All 3S / XT30. Long-type "pencil" packs
(≈ 72–74 mm) **exceed the 60 mm bay length** — do not force them.

| part | L×W×H | interface | fit |
|---|---|---|---|
| **Tattu R-Line 3S 450** (compact) | 45 × 24 × 21 mm | XT30 + JST-XH | **fits as-is** — 15 mm shorter than the 850 → generous XT30 slack; shortest airtime. |
| **GNB/Gaoneng 3S 550** (standard) | 58 × 31 × 17 mm | XT30 + JST-XH | **fits with note**: length/height fine, width **31 mm is ~1 mm over the 30 mm bay** → snug; rely on the mandatory foam preload, don't over-compress. |
| **CNHL Pizza 3S 600** | 74 × 12 × 24 mm | XT30 | **does not fit as-is** — 74 mm length exceeds the 60 mm bay by 14 mm; listed only to illustrate the rule (long-type packs are out). |

### 6.4 · Antenna alternatives (RHCP omni; core: Lumenier AXII 2 = Ø17.5 × 73 mm, SMA)

The captive-antenna coax clamp leaves a **~2.9 mm gap** — that grips the thin coax *cable*, not a
molded antenna head. Any SMA omni below swaps at the **SMA joint** exactly like the AXII 2; only
the coax that runs to the clamp matters for the gap.

| part | Ø × L | interface | fit |
|---|---|---|---|
| **Foxeer Lollipop 4 Plus** | head Ø15 × ~60 mm, 7.3 g, 2.6 dBic | SMA (RHCP) | **fits with note**: swaps at SMA like the AXII 2; the **Ø15 molded head will not pass the 2.9 mm coax clamp** — clamp the thin coax/SMA base, never the head. Shorter than the AXII 2. |
| **TrueRC Singularity 5.8 SMA** | head Ø11.8 × 8.2 mm, overall ~120 mm (length varies), 1.9 dBic stubby option | SMA (RHCP) | **fits as-is** — smallest CP head on the market; its thin flexible coax (~Ø1.1) actually suits the 2.9 mm clamp. Lower gain than the AXII 2 — a size/gain trade. |

### 6.5 · Switch alternatives (core: 12 mm latching, 2 A)

| part | dims | interface | fit |
|---|---|---|---|
| **12 mm anti-vandal latching** (Langir / APIELE / RJS class) | Ø12 mm thread, **12.2 mm panel cutout**, body ~28.7 mm long (excl. terminals), panel 1–11 mm | pre-wired or solder-tag | **fits as-is** — identical 12 mm dimensional family, same panel cutout. ⚠ **Verify current rating ≥ 2 A**: many 12 mm latching switches are rated only 1–2 A, and momentary-only variants exist — the + line carries ~1.3 A continuous, so a sub-2 A or momentary part is unsafe/wrong. |

### 6.6 · Heat-set insert alternatives (core: our bosses = Ø4.6 × 8 mm holes for a Ø5 × 6 insert)

| part | OD × length | recommended hole | fit |
|---|---|---|---|
| **ruthex RX-M3×5.7** | length 5.7 mm; OD not published on the product page (CAD download only) — M3×5.7 class is smaller than our Ø5 | Ø4.0 mm (per maker) | **fits with rework** — drill the bosses to the **maker's hole (Ø4.0)**, not our Ø4.6; an oversized hole lets the insert spin. |
| **CNC Kitchen M3×5.7** | length 5.7 mm; OD per maker CAD (M3-standard) | Ø4.0–4.2 mm (per maker) | **fits with rework** — same story: match the boss hole to CNC Kitchen's 4.0–4.2 mm spec, not our Ø4.6. Blind hole ≈ 1 mm deeper than the insert. |

**Rule:** a different insert = a different pilot hole. Always drill to the *insert maker's* spec,
not to our Ø4.6 (which is sized for the Ø5 × 6 insert).

### 6.7 · Wago alternative (core: 221-412, 2-conductor lever nut)

| part | L×W×H | conductors | fit |
|---|---|---|---|
| **Wago 221-2411** (inline splice) | 35.5 × 8.1 × 8.9 mm, 0.2–4 mm² | 2, **feed-through** (in one end, out the other) | **no direct 1:1 substitute** — different topology. The 221-2411 is a *straight inline* joiner (slim, wires enter opposite ends), handy where the + line runs end-to-end; the 221-412 is the general junction block. Keep the 221-412 for the main +/− joins; use the 2411 only for a clean inline splice. |

### Sources (§6)

- [HDZero Freestyle V1 VTX — docs](https://docs.hd-zero.com/freestyle-v1) · [Freestyle 30×30 listing (40×42×10, 28 g, 30×30 M3)](https://www.racedayquads.com/products/hdzero-freestyle-30x30-25-1000mw-digital-hd-vtx-u-fl)
- [HDZero Race V3 VTX — docs (28×32×5, 5.5 g, 25–200 mW, 20×20)](https://docs.hd-zero.com/race-v3) · [Race V3 review — Oscar Liang](https://oscarliang.com/hdzero-race-v3-vtx/)
- [HDZero Nano V3 camera — docs (14×16×14, 2.2 g)](https://docs.hd-zero.com/camera-nano-v3)
- [HDZero Micro V2 camera (19×19×21, 8.5 g, 19×19 mount)](https://www.getfpv.com/runcam-hdzero-micro-camera-v2.html)
- [Tattu R-Line 3S 450 (compact) — genstattu](https://genstattu.com/tattu-450mah-11-1v-75c-3s1p-lipo-battery-pack-with-xt30-plug.html) · [GNB 3S 550 standard (58×31×17)](https://pyrodrone.com/products/gaoneng-gnb-111v-550mah-80-160c-3s-lipo-battery-jst-xt30) · [CNHL Pizza 3S 600 (74×12×24)](https://chinahobbyline.com/products/cnhl-pizza-series-600mah-11-1v-3s-120c-lipo-battery-with-xt30)
- [Foxeer Lollipop 4 Plus (2.6 dBic, SMA)](https://www.foxeer.com/foxeer-lollipop-4-plus-high-quality-5-8g-2-6dbi-fpv-omni-lds-antenna-g-374) · [TrueRC Singularity 5.8 SMA (head Ø11.8×8.2)](https://truerc.com/71964-singularity-58-sma)
- [12 mm anti-vandal latching switch — dimensional family](https://www.langir.com/l12-anti-vandal-switch/) · [12 mm switch panel/thread data — APIELE](https://www.apiele.com/collections/12mm-latching)
- [ruthex RX-M3×5.7 insert (length 5.7 mm, CAD only)](https://www.ruthex.de/en/products/ruthex-gewindeeinsatz-m3-100-stuck-rx-m3x5-7-messing-gewindebuchsen) · [CNC Kitchen M3×5.7 + hole guide](https://www.cnckitchen.com/blog/tipps-amp-tricks-fr-gewindeeinstze-im-3d-druck-3awey)
- [Wago 221-2411 inline splice (35.5×8.1×8.9)](https://www.wago.com/global/installation-terminal-blocks-and-connectors/inline-splicing-connector-with-levers/p/221-2411)

## Order-log reality notes (kept, because they will bite you too)

- The **VTX kit** was in stock at n-Factory when ordered; two other shops 404'd the same week.
- Buy the **patch in the connector variant that matches your pigtail** — the order log caught
  an RP-SMA/SMA mismatch at checkout.
- **HDZero receivers churn**: BoxPro was sold out at one shop; a used HDZero goggle/VRX from the
  classifieds is the cheapest first picture. Analog goggles **cannot** receive HDZero at all.
- Sender hardware total (without receiver): **~€ 410–450** as ordered.
