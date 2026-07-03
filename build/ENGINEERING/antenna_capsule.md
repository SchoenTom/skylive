# The antenna capsule — a donut omni captured in the wall

*Condensed English edition of the project's German spec (`OMNI_CAPTIVE_SPEC`, 2026-07-02).
Labels: sourced (manufacturer/datasheet), **[CALC]** = calculated model, `MEASURE_ME` = must be
calipered. **Nothing here is an empirical RF test — VNA verification of the built capsule is
mandatory before any RF value is believed.** Geometry lands in the case CAD: `TBD-CAD-M6`.*

## 1 · The part and the doctrine

**Lumenier AXII 2, RHCP, SMA** (manufacturer page): 2.2 dBic max, SWR ≤ 1.5, **bandwidth
5.3–6.2 GHz** (the 900 MHz reserve that makes encapsulation viable), 73 × 17.5 mm, 7.8 g,
45 mm semi-rigid RG402 cable that is *meant* to be formed once ("90 degrees or more").

**Orientation doctrine:** the puck lies with its axis **across the body (horizontal)** → the
donut pattern fires **down + up**, nulls point out to the sides. The ground station is below
you; laying the antenna re-aims the fixed +2.2 dBic peak at it instead of at the horizon —
worth **~15–18 dB at 4 km over standing it upright** ([CALC], see [`../rf/README.md`](../rf/README.md)).
Better aiming, not more power.

## 2 · Why fully captured (the wind-load math, honestly)

Free-standing like on a quad (puck + 45 mm cable in the wind) [all CALC]:

- Belly, 55 m/s: ~0.9 N on the puck → ~25 MPa bending at the cable root — **survives** (the
  static worry is quantitatively unfounded).
- Head-down/speed, 75 m/s: ~47 MPa vs annealed copper yield 33–70 MPa — **borderline to
  plastic**, and the *real* killers are dynamic: vortex shedding at ~630 Hz fatiguing the SMA
  crimp, riser slap at deployment (not seriously calculable, certainly ≫ 2 N), and snag safety.
- A half-exposed "window" buys nothing: 1.5 mm PETG is RF-transparent, so exposing the puck
  saves ~0 dB and adds a line-catch surface.

**→ 100 % encapsulated, 0 mm free.** Wind load goes into the printed wall structure
(< 0.1 MPa); the cable sees nothing; there is no snag feature and no way to rip the antenna off.

## 3 · The capsule ("nose") design

- Side wall of floor 2, **opposite the thermal-pad wall**, top band: the element ends up
  ≥ ~45 mm off the head centreline — exactly the side-mount offset the RF model credits with
  +4…+5 dB of body-edge relief. Down-lobe clears wall, divider and battery.
- Ø 19 wall opening (puck 17.5 + clearance — an opening, not a thinned wall) + printed cap:
  root zone 3.0 mm, **element band 1.5 mm radome, cylindrical 360°** (the donut radiates
  radially all round), solid 3.0 dome on the pattern-null axis. 2× M3 (nylon preferred) into
  heat-sets.
- The puck is touched only at its two **axis ends** (TPU tip pad + TPU root ring) — the axis is
  the pattern null, so contact there detunes least ("grip at the nulls, air at the lobes" —
  rule of thumb, VNA decides). Preloaded, nothing rattles.
- **Radial air gap 2.5 mm** puck↔radome. Honest label: design decision/rule of thumb, no sourced
  limit exists; the classical λ/10 rule would say 5.2 mm. Defensible because of the antenna's
  900 MHz bandwidth and because its own polycarbonate radome already sits directly on the
  element. **Mandatory verification: VNA S11 of the antenna inside the finished capsule**
  (5.65/5.8/5.95 GHz markers, SWR ≤ 2 in band; instrument must reach 5.8 GHz).
- Cable route: **exactly one 90° bend, R 8 mm** (datasheet minimum 6.35 repeated), formed once
  on a printed jig, ending at an internal SMA jack on a printed rib. The wall-bulkhead topology
  was evaluated and **rejected**: with a captured puck it is geometrically impossible (the whole
  73 mm chain would stand proud) and an external joint is just a lever/corrosion point.
- Swap procedure: open lid → undo SMA (8 mm wrench) → unscrew cap (2× M3) → pull the antenna
  **outward** through its Ø 19 opening. No soldering, the U.FL is never touched.
- Metal keep-out ≥ 13 mm (λ/4 rule of thumb) around the element zone — same value the vent
  layout respects.

## 4 · "Never transmit without an antenna" — solved structurally

1. The antenna is form-locked in the capsule — it cannot vibrate loose, be forgotten, or be
   pulled off; the 90° bend + TPU clamping block the only loosening motion.
2. **Witness hole Ø 2.5 in the dome centre** (on the pattern null — RF-irrelevant): the TPU tip
   pad behind it is **signal orange**. Orange dot = antenna inside; dark hole = EMPTY.
3. Checklist line stays: "Orange dot visible? Only then power."
4. Deliberately **not** built: electronic antenna detection — extra electronics contradict the
   four-part doctrine, and the VTX documents no VSWR protection to rely on.

## 5 · Version B — the down patch (unchanged variant)

The TBS 5G8 patch (RHCP, **RP-SMA** on this project's unit — match your pigtail!) lives in the
**bottom shell**: a 15 mm hollow cap with a 1.5 mm radome floor, radiating down through it,
with its own weep hole at the cavity edge. Best for belly flying with the DZ below/ahead;
swings off-target in head-down — that's the donut's case.

## 6 · Open verifications (honest list)

Caliper: puck head length, SMA body, cable OD (`MEASURE_ME`) → final sink/protrusion numbers.
VNA S11 in the capsule · ground-level RSSI walk-around capsule vs free antenna (expected loss
~0–2 dB, **unmeasured**) · glove pull test + 1.5 m drop of the printed nose · steel-vs-nylon
cap screws A/B on the VNA if steel is used.
