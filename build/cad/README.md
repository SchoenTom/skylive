# SkyLive CAD — parametric, gated, honest

> **Status: the v2 case builds and passes all geometry gates** (both antenna variants:
> WALL = side-capsule omni **63 × 71 × 85 mm**, PATCH = down-firing patch **63 × 71 × 101 mm**;
> watertight, 3 mm wall, zero interference — independently re-verified). What's still open
> before a *final* print: a few hand-measured values replace their datasheet fallbacks, and
> the first print is a fit prototype (fit coupons first). Read, run, tweak.

## The files

| file | role |
|---|---|
| **`spec.py`** | **Single source of truth for every dimension** (~185 parameters). Each value is (a) measured from an official manufacturer STEP, (b) sourced from a datasheet/vendor page (URL in the comment), or (c) listed in `MEASURE_ME` with a documented fallback. Nothing is estimated. CAD, docs and renders all import from here — no drift. |
| **`skylive_sender_v2.py`** | Builds the upright two-storey case (body, cover, battery door, divider tray, bottom shell) in variants **A** (captive side omni), **A2** (legacy internal omni position) and **B** (down patch in the bottom shell). Runs hard gates: every part watertight, pairwise clearance ≥ 0.5 mm, only whitelisted protrusions through walls, dimension asserts against `spec.py`, divider cutout ≤ 50 %. Exports STEP/STL/GLB + hidden-line SVGs. |
| **`render_glb.py`** | Blender headless render rig (Cycles CPU): auto-framing, studio light, PBR materials inferred from the per-part colors. |

## How to build

```bash
python -m venv .venv && source .venv/bin/activate
pip install build123d==0.10.*        # tested with build123d 0.10 on Python 3.13
python skylive_sender_v2.py all      # or: A | A2 | B
# outputs → ../skylive_out/ (created next to the script's parent tree)
```

**You also need the two official manufacturer STEP files** (not redistributed here — fetch
them from the manufacturer's published CAD):

```
references/HDZero Freestyle V2 VTX.step
references/HDZero_Nano90.stp
```

placed relative to the path in `spec.VTX_STEP` / `spec.CAM_STEP` (adjust those two lines to
your layout if needed). The script imports the real VTX and camera solids and positions the
case around them — that is the point: the electronics are real geometry, not gray boxes.

Renders (optional, Blender ≥ 4.x):

```bash
blender --background --factory-startup --python render_glb.py -- \
    ../skylive_out/skylive_A_ASSEMBLY.glb out_renders skylive_A iso,front,side
```

## Design rules baked into the scripts

- **Wall 3.0 mm — sacrosanct.** The only exceptions: the bulkhead counterbore (2.8) and the
  1.5 mm RF radome windows. Ledges, ribs and channels are *additive* — the wall is never grooved.
- **Gates fail loudly.** A build that isn't watertight, collides, or drifts from `spec.py`
  raises an assert instead of silently exporting garbage.
- **`MEASURE_ME` over guessing.** If a vendor doesn't publish a dimension, the parameter
  carries a documented fallback and a caliper instruction (see [`../MEASURE.md`](../MEASURE.md)) —
  it is never quietly invented.
- Print doctrine (orientation, tolerances, shrink, coupons): [`../ENGINEERING/print.md`](../ENGINEERING/print.md).
