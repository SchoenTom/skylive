# Structure — the divider tray (floor between battery and radio)

*Condensed English edition of the project's German derivation (`DIVIDER_STRUCTURE_SPEC`,
2026-07-02). Everything here is **beam/strip estimation — no FEM, no physical test**; the
1.5 m drop test in [`../MEASURE.md`](../MEASURE.md) is the gate. Sourced values (opening-shock
literature, printed-PETG datasheet, connector datasheets) are cited in the original.*

## 1 · What the divider actually carries

- **Parachute opening shock:** literature puts sport ram-air openings at ~2–5 g, hard openings
  4–6 g (median peaks 4.0–5.1 g in a measured study) → design value **10 g quasi-static**
  (≈ 2× reserve). The 80 g battery then pushes ~8 N — **downward into the bottom shell**, not
  into the divider. Opening shock is negligible for the divider.
- **The sizing case is a 1.5–2 m handling drop onto concrete, case upside down:** the battery
  slams into the divider. With a rigid stop that's ~750 g (~590 N — unacceptable); with **≥ 5 mm
  of foam preload/stopping distance** it drops to ~300 g → **design load 250 N**, both directions.
  **Rule: the battery must NEVER fly free** — foam preload between battery and divider is mandatory.
- **Helmet-mount loads never pass through the divider.** They run GoPro fingers → bottom shell →
  4 corner screws → the four 3 mm walls as a closed tube. The divider is a **bulkhead/frame**:
  only its perimeter attachment is structural (like aircraft frames with big lightening holes) —
  the centre field is expendable.

## 2 · The material truth that drives everything

Printed PETG (manufacturer TDS): tensile **47 MPa in-plane (XY)** but **interlayer adhesion only
18 ± 4 MPa** — 38 %. Whether the divider survives is decided by **print orientation first**,
cutout geometry second.

An integral horizontal divider in an upright-printed case would (1) print as an unsupported
bridge over the whole battery bay, (2) put plate bending exactly onto the weak interlayer
direction, (3) make stiffening ribs unprintable overhangs.

**→ The divider is a SEPARATE, FLAT-PRINTED DROP-IN TRAY:** bending runs in the strong XY plane,
ribs print as vertical walls, all windows/slots are support-free, and cables get **laid in
instead of threaded** — no connector ever passes a closed hole. It rests on 3 × 3 mm ledges
printed onto the walls (additive — the sacrosanct 3.0 mm wall is never grooved), is keyed
around the corner posts, and is held down by 2 diagonal M3 screws.

## 3 · Cutout doctrine (how much you may remove)

- **Perimeter band 6 mm: always solid** — it *is* the bulkhead function.
  Max. 3 defined feed-through breaks, each ≤ 14 mm, locally doubled.
- **Boss/corner zones stay** (Ø ≥ 12 mm solid around every screw/locating point).
- **Centre field: up to 50 % may be cut out**, if remaining webs are ≥ 4 mm (≥ 4 closed slicer
  perimeter loops), webs are triangulated or tied to the ribs, and the **two longitudinal ribs
  (2.4 × 6 mm, on top)** are present. With ribs, the 250 N drop load carries with a safety
  factor ≈ 1.7 in the strong direction — without ribs the plate is marginal-to-failing. [estimate]

## 4 · Feed-through catalogue (all support-free, all sized from datasheets or measured parts)

| what crosses | opening | why this size |
|---|---|---|
| Battery lead with **XT30** | window **14 × 9 mm** or open edge slot | mated XT30 face ≈ 11 × 6 measured + clearance; the old Ø 6.5 hole fit **no** connector — confirmed bug |
| Balance **JST-XH-4** | window 14 × 8.5 mm | 12.3 × 7.5 datasheet + clearance |
| **U.FL→SMA pigtail** (Ø 1.8) | 3 × 3 mm edge notch | aligns with the wall channel |
| Switch leads | round Ø 8.0 mm | standard grommet size; grommet groove = the 3 mm panel |
| MIPI ribbon | **crosses nothing** — camera and VTX both live upstairs | width is published nowhere → `MEASURE_ME` if ever needed |

Edges of all openings rounded r ≥ 1.5 both sides (cable protection without a grommet);
every slot gets a printed zip-tie anchor next to it (strain relief).

## 5 · What was honestly deleted

A spare-antenna pocket in the divider was **calculated and rejected**: the 73 mm omni doesn't
fit any diagonal of the tray field (~60 mm). Pre-bending the spare's semi-rigid cable to force
it in would damage the spare. The spare antenna travels in the ground-station box instead.
