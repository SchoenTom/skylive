# SkyLive CAD — parametric, gated, honest

> **Status: the V3 family builds and passes all geometry gates** — three sizes, one
> architecture, upright two-storey shells: **850** 71 × 40 × 56 mm (flight unit) ·
> **mid** 69 × 38 × 48 mm · **Mini 300** 59.5 × 39.5 × 48 mm. Watertight, 3 mm wall,
> printability gate on every export. Still open before a part is *trusted*: the physical
> tests — a CAD boolean is not a test. Read, run, tweak.

## The files

| file | role |
|---|---|
| **`spec.py`** | **Single source of truth for every dimension** (~185 parameters). Each value is (a) measured from an official manufacturer STEP, (b) sourced from a datasheet/vendor page (URL in the comment), or (c) listed in `MEASURE_ME` with a documented fallback. Nothing is estimated. CAD, docs and renders all import from here — no drift. |
| **`v3_min.py`** | Builds the **850 flight unit**: one-piece two-storey body (battery downstairs, radio + camera upstairs — the divider shelf is printed in), tab-locked battery door on a brass-insert screw, roof lid on 3 corner inserts, 2× XT30 clamp bar, 2× strain-relief T-piece. Camera bulge inverted 1:1 from a measured reference print. Hard gates on every rebuild. |
| **`mid_sender.py`** | The **mid sender** — the same architecture around the smaller Tattu 300 3S HV pack (measured 45 × 17.5 × 15.3). |
| **`mini_300.py`** | The **Mini 300** — smallest port of the same architecture; no power switch (floor 2 has no room for one — power = plug the battery). |
| **`printability_gate.py`** | Mesh-level print gate run before every STL export: knife-edge / vanishing-wall detection (FAIL), overhang clusters, enclosed voids, sliver triangles — the failure class a solid-level boolean gate cannot see. |
| **`skylive_sender_v2.py`** | **Legacy** — the earlier V2 case (side-capsule omni and down-patch studies, 63 × 71 footprint). Kept because its derivations are referenced from [`../ENGINEERING/`](../ENGINEERING/); superseded by the V3 family above. |
| **`render_glb.py`** | Blender headless render rig (Cycles CPU): auto-framing, studio light, PBR materials inferred from the per-part colors. |

## How to build

```bash
python -m venv .venv && source .venv/bin/activate
pip install build123d==0.10.*        # tested with build123d 0.10 on Python 3.13
python v3_min.py          # 850 flight unit
python mid_sender.py      # mid sender
python mini_300.py        # Mini 300
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
