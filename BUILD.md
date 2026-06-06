<!-- Part of the SkyDive·Live showcase — see README.md -->

# 🔧 Build SkyDive·Live — two builds, pick yours

There are **two ways to build the sender.** They share the same idea — the jumper's POV, live to the drop zone — but they're tuned for different flying. Pick the one that fits you, then follow its step‑by‑step plan below.

> *Status: CAD verified (watertight, 0 collisions, fastening checked). The first calibration print and the fit tests are the planned next step — calculated vs. to‑be‑measured is called out honestly.*

## Which build?

| | **Gen 1 · MK2 — The Foundation** | **Gen 2 · v5 — Never lose the image** |
|---|---|---|
| **Its strength** | **Simplest, most robust, proven.** Fewest parts, forgiving material — the best first build and proof‑of‑concept. | **Holds the link in any orientation.** Dual antenna (patch + dipole + RF switch) keeps the picture even head‑first; flush, compact, all‑day swap. |
| **Best for** | belly‑fly, learning, a dependable first unit | freefly / competition (sit, head‑down, back), media |
| **Printed parts** | 3 (body, cover, tray) | 7 (body, cover, sled, antenna module, antenna shell, tray, door) |
| **Material** | PETG (impact‑tough, easy) | ASA (heat‑stable) · +0.8 % shrink |
| **Antenna** | single down‑facing patch | patch (down) **+** λ/2 dipole (up), switched |
| **Envelope** | 78 × 63 × 69 mm | 57 × 38 × 51 mm (−66 % volume) |
| **Difficulty** | ⭐ easier | ⭐⭐ more involved |

STLs for both are on the **[v1.0 release](../../releases/tag/v1.0)**. Full bill of materials: **[`BOM.md`](BOM.md)**.

---

# Build A — Gen 1 · MK2 *"The Foundation"*

> **Why this one:** the fewest parts, printed in forgiving PETG. It's the dependable first build — get the whole live loop working end‑to‑end before you commit to the compact freefly version.

### A1 · Print (3 parts, PETG)
| File (`Gen1_MK2_STL`) | Bounding box | Orientation |
|---|---|---|
| `MK2_body.stl` | 78 × 63 × 69 mm | open‑top up, on the GoPro fingers |
| `MK2_cover.stl` | 78 × 56 × 3 mm | flat, outside down |
| `MK2_tray.stl` | 34 × 30 × 50 mm | flat, door plate down |

**Settings:** 0.4 mm nozzle · 0.2 mm layers · 4 perimeters · 30–40 % gyroid infill · ~240 °C / bed ~80 °C · brim 5 mm. **Support** only under the floor + lens nose (tree). **Why PETG:** impact‑tough, easy to print, warm enough for Iteration 1.

**Post‑print:** remove support → lightly face the **radome area** (floor centre, keep the 1.2 mm — it's RF‑transparent at 5.8 GHz) → melt in **5× M3 heat‑set inserts** (4× cover bosses, 1× tray latch) at ~200 °C → deburr. *Do a calibration print first; print the final set only once tests A–F pass.*

### A2 · Prepare components
HDZero Freestyle V2 VTX (keep the stock heatsink) · HDZero Micro V3 camera (M12 lens + anti‑fog) · 80 mm MIPI FFC · 3S LiPo + BMS · TBS 5G8 patch (trim rear edge → S11 < −10 dB @ 5.8 GHz) · 25 mm Sunon fan · AO3401 MOSFET on protoboard (10 kΩ pull‑up).

### A3 · Assemble — in this order (later parts are otherwise unreachable)
1. **Patch antenna** into the floor well, click in U.FL + hot‑glue, route the pigtail up. *First — the VTX stack blocks access later.*
2. **VTX flat** on the two rear M2 standoffs + heatsink/thermal pad. *Flat because the 29 & 30 mm board only fits via its 14 mm thickness in Z.*
3. **Switch** into the +X slot; hot‑glue the **MOSFET board** beside it.
4. **Camera** push‑fit into the 4 locator ribs, lens through the Ø14 nose. *Tool‑free field swap.*
5. **Cover**: foam pad on the fan (preloads the VTX stack), 2× M2 fan, 4× M3 cover.

### A4 · Wire & power
MIPI camera↔VTX (ESD, slack over the heat‑wall) → U.FL patch→VTX → power V+/V− through the AO3401 (star ground) → switch to gate (10 kΩ pull‑up) → fan → **conformal‑coat every joint** (vented, not sealed) → slide the **battery tray** in from −X, captive M3 thumbscrew + Dyneema tether. **⚠️ Charge the LiPo externally only.**

### A5 · Fit tests A–F (next step after the calibration print)
**A** dimensions · **B** cover + 4× M3 flush, GORE hole clear · **C** tray 5× in/out without binding, latch clicks, polarity guard *(most critical)* · **D** VTX flat, camera firm, **camera‑fan gap > 2 mm**, patch S11 · **E** NACA inlet + outlets clear, switch recessed, GoPro Ø5, cable runs · **F** full assembly, tray → green LED → picture on the monitor, weight + CG.
**Release rule:** print the final set only when A–F pass; on a fail, fix only the affected part.

---

# Build B — Gen 2 · v5 *"Never lose the image"*

> **Why this one:** a body is a shadow — go head‑first and your own body blocks a single antenna. v5 carries **two** (a patch looking down, a dipole up top) and an **RF switch** that picks the better one live. Flush, compact, tool‑free battery swap. This is the freefly / competition build.

### B1 · Print (7 parts, ASA)
| File (`Gen2_v5_STL`) | Role | Print note |
|---|---|---|
| `…_body.stl` | main shell · integral heat‑wall · side door · flat GoPro mount | open‑top up · tree‑support under the 2 GoPro fingers |
| `…_cover.stl` | top lid · GORE vent · 4× M3 | flat, no support |
| `…_sled.stl` | carries VTX + camera | no support |
| `…_module.stl` | antenna module (dipole + RF switch) | minimal |
| `…_antshell.stl` | −X side end‑cap · flush RF window, holds the patch (alu body = ground‑plane) | minimal |
| `…_tray.stl` | 3S LiPo, slide‑in | no support |
| `…_door.stl` | side, tool‑free battery door | minimal (hinge) |

**Settings:** ASA · **+0.8 % isotropic shrink** · 0.2 mm layers · perimeters that fully fill the **3.0 mm wall** · enclosure + heated bed + mouse‑ears (ASA warps otherwise). Never PLA (softens < 55 °C). **Heat‑sets:** M2 (VTX, pilot Ø3.2) + M3 (cover, antenna, sled‑lock) — no self‑tappers.

### B2 · Prepare components
Same VTX + Micro V3 + 3S LiPo as MK2, **plus** the dual‑antenna kit: TBS 5G8 patch (down), a λ/2 **dipole** (up), an **SPDT RF switch** on one U.FL output, a U.FL→RP‑SMA bulkhead pigtail, a **Pyrogel/Polyimide** heat‑shield strip, and a slide switch (SS‑12D00).

### B3 · Assemble — the seven steps
1. **Heat‑sets** into the body bosses (cover M3, sled‑lock).
2. **Patch** into the **−X side antenna end‑cap** (flush RF window; the aluminium body is its ground‑plane).
3. Load the **battery tray**, slide it into the bottom bay through the side door.
4. **VTX + camera** onto the **sled**; drop it into the body above the heat‑wall (Pyrogel + 4 mm air gap below); **wire through the heat‑wall feed‑through** (battery → electronics).
5. **Dipole + RF switch** into the **antenna module** (top).
6. **Cover** on — 4× M3.
7. Close the **battery door** (tool‑free).

### B4 · Wire & power
MIPI camera↔VTX · patch + dipole → **SPDT RF switch → one switched U.FL** into the VTX (no second TX chain, no extra current) · power through the slide switch/MOSFET, star ground · conformal‑coat · GORE vent in the cover · battery pigtail through the heat‑wall feed‑through. **⚠️ Charge LiPos externally; swap a fresh tray between jumps** (thermal + condensation, not capacity).

### B5 · Fit tests
Same A–F discipline as MK2, **plus**: dipole/RF‑switch continuity, the **flush** antenna module seats with no proud edges, and the **antenna in‑flight position** (the #1 open risk this build addresses) — verify on the test jump.

---

## Shared notes

- **Bill of materials:** [`BOM.md`](BOM.md) (sender, ground station, measurement gear).
- **Fasteners:** brass heat‑sets (M2/M3), an M5×0.8 GoPro thumbscrew, Loctite 243 (never high‑strength on M2).
- **Safety / RF:** LiPo charged externally only; conformal coating against cloud moisture; transmit power is regulated — operate under an amateur‑radio Class‑E licence (PMSE short‑term for the championship demo). See [`LICENSE`](LICENSE).
- **Honest status:** CAD done (watertight, 0 collisions, fastening). Open next: first print, VTX thermal measurement, S11 antenna measurement, test jump. Calculated values are marked as such — no overclaiming.
