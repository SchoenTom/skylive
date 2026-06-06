# CAD — source files for SolidWorks & slicers

Both builds, **exactly as constellated in this repo**. Every part is watertight and a single solid (B-rep), generated from the parametric `build123d` sources.

## For SolidWorks → open the `.step` files
SolidWorks imports **STEP (AP242)** natively as **editable solid bodies** (not mesh) — this is the right hand-off.
- Individual parts → [`v5_dual_antenna/step/`](v5_dual_antenna/step) · [`mk2_foundation/step/`](mk2_foundation/step)
- Whole build, pre-positioned → `*/step/<build>_ASSEMBLY.step`

> A native **`.SLDPRT`** can only be written by SolidWorks itself (proprietary format). STEP is the universal solid-exchange standard and opens as real, editable solids — so it's the correct, lossless way to hand the geometry over. Your colleague can feature-recognize it in SolidWorks if he wants a feature tree.

## For printing → `stl/` and `3mf/`
Load into any slicer. **ASA**, **+0.8 % isotropic shrink**, 3.0 mm walls, print open-top-up. (Heat-sets: M2/M3 brass, no self-tappers.)

## What's in each build

### `v5_dual_antenna/` — Gen 2 · "never lose the image" (7 parts)
`body` · `cover` · `electronics_sled` · `antenna_module_top` (λ/2 dipole + RF switch) · `antenna_shell_side` (−X end-cap, patch, alu = ground-plane) · `battery_tray` · `battery_door`

### `mk2_foundation/` — Gen 1 · the foundation (3 parts)
`body` · `cover` · `battery_tray`

**Assembly order:** see [`../BUILD.md`](../BUILD.md). Sources: `mk3_v11_flat_v5.py`, `mk2.py` (parametric build123d).
