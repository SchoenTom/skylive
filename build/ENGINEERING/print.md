# Print & form factor — the factor register

*Condensed English edition of the project's German register (`PRINT_FACTOR_REGISTER`,
2026-07-02): every decision that turns CAD into a part that survives a helmet at 200 km/h.
Labels in the original: measured / datasheet / FDM practice / design decision / **coupon**
(= must be calibrated by test print before the full case). Case files: `TBD-CAD-M6`.*

## 1 · Form (GoPro aesthetics without lying about it)

- Form model: GoPro Hero proportions (official 71.8 × 50.8 × 33.6 mm as *reference only*);
  all radii are design decisions, not measured GoPro values.
- Vertical corner radii R 9 outside — **inner radius MUST be R 6 (= R9 − wall)**, otherwise the
  corner wall silently thins to ~0.5 mm exactly where the case hits concrete.
- Lid seam as a deliberate shadow gap (0.8–1 mm chamfer both sides) — a 0.1 mm print offset
  reads as design, not defect; no snag lip.
- Raised conical bezel ring around the lens; camera set so the lens tip stands ≤ 1.5 mm above
  the ring (the lens protrudes 13.3 mm from the camera front — measured from the official STEP).
- Fuzzy skin 0.3/0.4 only on side walls — **never** on mating faces (eats ~0.3 mm/side of
  tolerance) and never on the 1.5 mm RF radome (undefined wall in the RF path).
- Logo debossed 0.5 mm (raised text = snag + elephant-foot mush).

## 2 · Orientation — the one that saves the sender

- **body**: opening up, upright — cavity, bosses and ledges all print support-free; horizontal
  wall holes as teardrops.
- **cover / battery door**: outer face on the plate.
- **bottom_shell — THE critical part**: printed **lying on its rear face so the GoPro fingers
  lie FLAT** → layers run along the finger length and opening-shock bending loads the strong
  in-plane direction, not the 18 MPa interlayer bond. Ignore this and **the fingers shear along
  the layers and the sender leaves the helmet at altitude** — the #1 killer in the register.
  Plus: R 1.5 fillet at every finger root, finger zone 100 % infill, M5 steel screw carries the
  clamp (never plastic edges), seam never placed on a finger.

## 3 · Tolerances that actually print (0.4 mm nozzle, calibrated)

| joint | value | why |
|---|---|---|
| press fit (one-time joints only) | 0.0–0.1 mm | PETG creeps — never press-fit anything you reopen |
| sliding fit (door guide) | 0.3 mm | |
| never-jams (cable windows) | 0.5 mm | |
| printed holes | **+0.2 vertical axis · +0.3 horizontal axis + teardrop** | FDM holes print 0.1–0.5 mm undersize |
| switch hole M12×0.75 | **Ø 12.3 through-hole + the switch's own nut** — printed fine threads are a lie (0.46 mm thread depth ≈ one extrusion) | |
| M3 heat-set (Ruthex class) | hole Ø 4.0 × 7.0 deep, boss Ø 9, 0.5 chamfer, ≥ 3 perimeters | manufacturer install spec + insert-study practice |
| lid fit | **inner lip ON THE COVER** (2 × 4 mm, 0.2 clearance/side) — a groove in the body wall would halve the sacrosanct 3.0 mm | |
| wall slicing | **6 perimeters × 0.5 mm = exactly 3.0** — no gap-fill sliver inside the wall | |
| shrink | ASA **+0.8 % isotropic** in the export script (never additionally in the slicer); PETG starts at 1.000 and is calibrated by a 100 mm coupon | |
| stack-up gate | for every joint: nominal gap − (shrink bias + 2×0.15 spread + hole undersize) ≥ 0 — scripted check | |

## 4 · Robustness & environment

- **Material: ASA for the final part** (Tg ≈ 100 °C, UV-stable — a helmet spends whole seasons
  in the sun and 60 °C cars; PETG's HDT ~68–75 °C is too close). PETG for fit prototypes.
  Never PLA. ASA warps: enclosure, brim 6 mm, draft shield, ~105 °C bed.
- No screw ever threads directly into printed plastic (inserts or nuts only).
- Condensation philosophy: **drainage instead of sealing** — Ø 1.5–2 mm weep holes at the
  lowest point of both floors and of the patch cavity (never through the radome).
- The 1.5 mm radome prints as **3 solid perimeters** — no infill sandwich in the RF path.
- Everything inside is form-locked or foam-preloaded — nothing may rattle at 200 km/h.
- Usability at the exit: thumb well Ø 26 around the flush latching button (glove-operable,
  no snag), captive battery door with a ≥ 12 mm thumb tab, light pipe for the VTX status LED
  (position read from the official STEP, not guessed).

## 5 · Coupons before the full case (print these first)

Insert-boss field + pull-out test · switch-panel hole ladder Ø 12.1/12.3/12.5 · door-fit ladder
0.2–0.5 · **GoPro finger pair in the chosen orientation + break test against an upright-printed
control** · bulkhead hole + counterbore + nut test · 100 mm shrink ruler XYZ per material ·
bezel + lens bore against the camera · 1.5 mm radome plate (thickness + opacity check).
Print order: coupons → bottom_shell (riskiest) → body → cover/door. Doors and bottom shells
are wear parts: print two.
