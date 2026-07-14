# SkyLive — What YOU must measure (nothing is guessed)

*Condensed English edition of the project's German measurement protocol
(`MESSPROTOKOLL_SENDER`, 2026-07-03). The project rule: **no dimension is ever estimated.**
Every number is calipered, confirmed against the real part, or taken from a datasheet with the
source noted. Open values stay open until measured — they are never silently filled in.*

If you rebuild this project, the same discipline applies to you: your parts (pigtail batch,
switch clone, patch revision) may differ from ours. The CAD (`cad/spec.py`) marks every
unsourceable dimension as `MEASURE_ME` with a documented fallback — measure, replace, rebuild.

## A · Blocks the final print file (10 minutes with a caliper)

| # | dimension | how to measure | CAD fallback (documented, not trusted) |
|---|---|---|---|
| A1 | **Switch: total depth behind the panel plane** (barrel + body + lugs + cable exit) | hold it through a hole / over a table edge, panel seat → deepest point | 27.0 mm |
| A2 | **Omni (AXII 2) head/puck length alone** (without cable, cable root → tip) | lay it along the caliper | 22.5 mm |
| A3 | **Omni SMA plug**: length + wrench flat size | — | — |
| A4 | **Flange pigtail jack (U.FL→SMA)**: flange W×H, hole spacing, hole Ø | the sheet-metal end of the pigtail | — |
| A5 | **XT30 MATED** (plug + socket connected): total envelope L×W×H | measure the mated pair | window 14 × 9 mm |
| A6 | **MIPI ribbon width** (the kit cable VTX↔camera) | flat | **published nowhere** — must be measured |
| A7 | **TBS 5G8 patch**: PCB thickness + total height incl. connector | — | 3 / ≤ 15 mm |

## B · Important, not print-blocking

- Does the flange pigtail have a **flat (D-shape) on the thread**? → decides D-hole vs
  tooth-washer anti-rotation in the CAD.
- **VTX status LED position** on the board (which edge, mm from corner) — read from the official
  STEP if possible, for the light-pipe bore.
- **Battery pack recheck** (L×W×H hard, cable length to XT30) against the manufacturer's
  60 × 30 × 23 mm — trust, then verify.
- GoPro-mount finger tip radius + pivot offset from a real mount (mount fine-tuning).

## C · Empirical — after printing / with instruments (in order)

1. **VNA S11 of the omni with its coax in the printed clamp** — mandatory before believing any
   RF number (markers 5.65 / 5.8 / 5.95 GHz, target SWR ≤ 2 in band).
   ⚠ The instrument must actually cover 5.8 GHz — a NanoVNA-H does not.
2. **On-helmet detuning** (VNA S11 with the antenna mounted on the real helmet; the patch version of this test belongs to the legacy study).
3. **Thermal A/B test**: 200 mW on the ground, vents open vs taped shut; log U×I with a
   multimeter per power step (always with an antenna attached!). This is the experiment that
   calibrates the whole thermal model.
4. **1.5 m drop test** of the printed-in divider shelf (coupon) with an 80 g battery dummy — the beam
   calculation is not a test.
5. **Fit coupons BEFORE the full-case print** (insert boss, switch hole, door fit, GoPro
   fingers) — plan in [`ENGINEERING/print.md`](ENGINEERING/print.md).

## What happens with the numbers

A1–A7 flow directly into `cad/spec.py` (the fallbacks there are flagged `MEASURE_ME`) →
one rebuild run regenerates all parts, and the build gates (watertightness, interference ≥ 0.5 mm,
wall ≥ 3.0 mm, dimension asserts) check them automatically. No dimension lives in the model
that isn't measured, confirmed, or sourced.
