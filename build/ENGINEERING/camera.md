# The camera — a Nano90 cradled behind a flush lens window

*Engineering note for the sender's camera integration. Labels: sourced (manufacturer / STEP
file), **[CALC]** = geometric model, `MEASURE_ME` = must be calipered on the real part.
**A watertight CAD boolean is not an empirical fit test** — a printed coupon check of the lens
window and cradle is mandatory before the retention is believed. Geometry lands in the case
CAD: see [`../cad/README.md`](../cad/README.md).*

## 1 · The part

**HDZero Nano90** (official STEP, calipered against it): board **14 × 18 × 18.5 mm**, lens
barrel **Ø12 mm protruding ~13.3 mm** from the board face. It is powered and read out over a
single **20-pin MIPI ribbon** from the Freestyle V2 VTX — there is **no separate camera power
and no BEC**. The ribbon is fragile and short; it wants the camera close to the VTX and its
service loop protected, not stretched.

The camera carries a **native side-wall mount: 2 × M2, Ø2.0 mm clearance, 14 mm apart**
(STEP-measured). We deliberately do **not** use it — see § 3.

## 2 · The lens window (flush, snag-safe)

The lens looks out through the long front wall. The opening is a **13.5 × 13.5 mm rounded
square, corner R2.5**, cut through the 3.0 mm wall so the Ø12 barrel clears with ~0.75 mm all
round [CALC]. Two rules drive the detail:

- **Recessed, never proud.** The window face sits **0.5 mm inside** the outer wall, with a
  **1.2 mm × 45° chamfer** breaking every edge. Nothing protrudes into the airstream or a
  riser's path — the whole sender's job is to not snag on a helmet, a canopy line, or a jump
  partner. A protruding lens bezel is exactly the line-catch we design out.
- **No radome over the glass.** The window is left open. (For reference: a thin PETG cover
  would cost only **≈0.15 dB** optically-negligible — but this is *video*, not RF, and an
  extra optical surface fogs and scratches, so the lens stays exposed and the barrel itself
  seals the hole.)

## 3 · Retention — why a cradle, not screws

The obvious move is the camera's own 2 × M2 side holes. On this wall it does not survive the
geometry: threading M2 bosses beside a 13.5 mm window in a 3.0 mm wall leaves a **rail only
~2.1 mm thick that would break through into the window** [CALC]. Driving screws there buys a
weaker wall, not a stronger mount.

So the camera is **cradled**, captured on all six sides by printed structure instead of
fasteners:

- **−Y (forward):** the window shoulder. The 18 mm board cannot pass the 13.5 mm window — it
  seats against the shoulder, positively locating the lens.
- **±X (sides):** two printed rails hug the board width.
- **+Y (rear):** two **0.3 mm snap lips** — a light catch, enough to hold the board back
  against the shoulder during handling, not a structural load path.
- **±Z (top/bottom):** the closed lid above and the VTX body below trap it once assembled.

Net: zero fasteners at the camera, no thin threaded rail, and the board is fully constrained
the moment the lid closes. Honest limit — this is a **fit-prototype retention**. For a final
build the snap lips or a retention lip may want tuning, or a dab of RTV on the board edge;
that is a `MEASURE_ME` on the printed part, not a CAD claim.

## 4 · Placement (and what still needs measuring)

- Camera on the **long front wall**, lens on the optical axis, VTX directly behind so the MIPI
  ribbon stays short and its service loop sits in the divider window.
- `MEASURE_ME`: real board thickness tolerance and the lens-barrel seat depth — these set the
  shoulder recess and the snap-lip reach. The 13.3 mm protrusion is from the STEP; confirm on
  the physical camera before locking the wall stack-up.
- `MEASURE_ME`: MIPI ribbon free length and minimum bend radius — drives how far the camera
  can sit from the VTX without stressing the connector.
