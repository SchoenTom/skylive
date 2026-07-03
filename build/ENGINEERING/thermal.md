# Thermal design — passive cooling & vent optimum

*Condensed English edition of the project's German derivation (`THERMAL_VENT_OPTIMUM`,
2026-07-02). Labels: **[SOURCE]** = manufacturer/datasheet with URL in the original ·
**[CALC]** = our own engineering calculation, formulas and assumptions disclosed —
**calculated, NOT measured**. Every [CALC] number stands or falls with the measurement
plan in [`../MEASURE.md`](../MEASURE.md).*

Binding constraints: purely **passive** (no fan, no extra electronics — 4 parts, solder-free),
**3.0 mm wall sacrosanct** (vents are cutouts, never thinned wall), upright two-storey layout
(floor 1 = battery, floor 2 = VTX + camera), omni captured in the side wall.

## 1 · The honest headline numbers

- At 1 W RF the Freestyle V2 draws ~14 W → **~13 W becomes heat** (design value; worst 14 W).
  [SOURCE: manufacturer docs + independent review — "~14 W at 1 W/R1", "consumes up to 15 W"]
- **No passive vent design on earth holds 1 W on the ground in still air.** Chimney draft
  delivers tenths of a pascal; ram-air delivers hundreds — a factor of ~10 000. HDZero itself
  says: on the bench, use a fan or low power. [SOURCE + CALC]
- Therefore the design is **two-regime**: (a) chimney vents that make 25 mW continuous and
  200 mW 10-minute-safe on the ground, and (b) the same vents as a flow-through path in
  freefall, where ~500 mm² of slots delivers **4–8× the need**. [CALC]

## 2 · Load cases [all CALC]

| case | mechanism | result |
|---|---|---|
| Ground, still air, 25–35 °C | chimney draft (Δp ≈ 0.06 Pa) + shell convection/radiation | ~4.5–6.5 W removable → **25 mW: holds · 200 mW: ≤ 10 min (≤ 5 min at 35 °C) · 1 W: impossible steady-state** |
| Climb (last ≤ 10 min powered) | same as ground, cooler air | fine at 25 mW; set 1 W only at door-open |
| **Freefall 55–75 m/s** | ram-air through-flow, ΔCp ≈ 0.3 conservative → ~9 L/s through 500 mm² | **≈ 46 W capacity vs 14 W worst need** — even with 50 % blockage 2–4× surplus. The fall is the heatsink |
| Canopy 10–15 m/s | same path, weaker | ~12 W at ΔT 5 K — 1 W holds with reserve |
| **After landing** | hot start + still air + 1 W | protective RF cut in ~1–2 min → **doctrine: OFF within 60 s** |

The VTX's own protection is a **hard RF shutdown** until repowered [SOURCE] — for a live
stream that's a mission kill, so the doctrine limits are *broadcast-guarantee* limits.

## 3 · Architecture (zones, not final coordinates)

```
   OUTLET →  slot band under the lid lip (sides + rear; front is the camera's)
             ┌──────────────────────┐
             │ floor 2: VTX+camera  │  ← 13 W source · thermal pad → wall OPPOSITE the omni
             ├── divider tray ──────┤  ← free openings ≥ 750 mm² (riser channel)
             │ floor 1: battery     │  ← battery sits in the COOL intake stream
   INTAKE →  └──────────────────────┘  ← lowest wall band, sides + rear (floor stays free: mount)
```

- **Chimney through the battery floor: yes.** Intake at the bottom raises the stack height
  (+30–65 % draft), the battery sits in fresh intake air (heat rises away from it), and the
  bottom slots double as condensation drainage.
- **Three facades**: poses change the airflow direction in freefall — vents on sides + rear
  guarantee a windward/leeward pair in every pose, with no moving parts.

## 4 · Slot geometry (one shape solves print, snag and rain)

**Vertical louver slots, 2.5 × 14 mm, tilted 45° downward-outward through the 3.0 mm wall.**

- 2.5 mm: no line-snag catch (flush, no undercut), finger/foreign-body safe, prints without support.
- Vertical + 45° louver: no bridging, self-supporting overhang, and no straight water path in
  (drops can't travel upward). The wall stays 3.0 mm everywhere — a slot is a cutout, not a thin spot.
- Areas: intake ≥ 500 mm² (~15 slots), outlet ≥ 600 mm² (~18 slots, ≈ 1.2× intake — outlet air is
  warmer/bulkier and must never throttle the ram path), divider net free area ≥ 750 mm².
- **A NACA duct was evaluated and rejected** [CALC]: plain slots already give ≥ 4× freefall
  surplus; a NACA inlet would only add margin nobody needs and costs snag safety, printability
  and water-tightness.

## 5 · The thermal pad — honest about what it does

1.5 mm silicone pad, ≥ 3 W/mK, full VTX face (29.2 × 30 mm) to the side wall opposite the omni.
Honest series-resistance math [CALC]: the PETG wall is the bottleneck — on the ground the pad
moves only **~0.6 W of 13 W**. It is still mandatory, because it (1) roughly **doubles the
effective heat capacity** in the power-up window (buys 1–2 min before cut-out), (2) carries
~2.5 W in freefall as a second path, (3) is a set project rule.

**Material:** the pad contact zone can exceed 70 °C in a fault → **ASA preferred for the final
part** (Tg ≈ 100 °C vs PETG ≈ 70–80 °C); PETG is fine for fit prototypes; **never PLA**.

## 6 · Operating doctrine (the design's fifth component)

25 mW on the ground (unlimited) · 200 mW ≤ 10 min · **1 W only at door-open/exit call**
(~2 min before exit: the VTX starts the jump 30–40 K below the cut-out zone and ram-air takes
over at exit) · **OFF ≤ 60 s after landing** · at a 35 °C DZ keep it in the shade / print bright.

*Nothing in this document is measured. The architecture decisions (chimney bottom→top, louver
slots, three facades, no NACA) are robust for any heat load between 5 and 15 W; the numeric
margins await the multimeter + thermometer protocol in [`../MEASURE.md`](../MEASURE.md).*
