# What the gates caught

*Every part in this repo was built by parametric CAD code with **assertion gates** — boolean
collision checks, wall-thickness sweeps, screwdriver-path probes — that run on every rebuild and
**refuse to export** if anything intersects. This file is the honest logbook of what those gates
caught before a single gram of filament was wasted. Most hardware repos show you the result.
This one shows you the saves.*

---

## The lid that could never be screwed — **687 mm³**

The first lid design anchored its four M3 insert bosses on the long side wall, reaching 10.5 mm
into the interior. A neutral audit placed the *nominal* VTX envelope (29.2 × 30 × 18.6 mm) against
every interior feature — and found the bosses buried **687 mm³ deep inside the radio**. Not a
tolerance issue: with the VTX needing 30 of the 33.5 mm interior width, *any* boss deeper than
1.75 mm on that wall collides, always. The fix wasn't a smaller boss — it was moving the lid to
the **roof**, where three corner posts live in space no component ever claims.

> Lesson: check envelopes against *nominal* positions, never against the already-carved body.
> A gate that "passes" because the conflict was carved away is a lie with green text.

## The door that could not swing — **a geometric proof**

The battery door was designed to hinge in like a TV-remote lid. The swing simulation (door rotated
about its nose line in 2° steps, intersected with the body) showed **60–180 mm³ of collision at
every angle past 1°** — and stayed above 60 mm³ even with the *entire top half of the door
deleted*. The culprit: the R6 interior corner fillet, which curves the cavity wall into the path
of the door's tongue flanks. That's not a bug to patch; it's a proof that a flush four-sided plug
door cannot rotate into a filleted cavity. The door now **slides in straight and tips ≤ 4°** at
the end to hook its noses (0.00 / 0.07 mm³ at 2°/4° — measured, gated) — which is exactly how a
real TV-remote door seats, so nothing of value was lost. The full sweep is still logged on every
build, honestly, above the assert that checks what is actually achievable.

## The vent that opened into the camera — **24.65 mm³**

When the camera moved fully outboard against the front wall (so its left screw could pass through
the *outside* of the case — one countersink, zero internal structure), the upper front vents
suddenly opened straight into the camera's back. The collision gate flagged 24.65 mm³ on the next
build. The vents weren't nudged — they were **deleted**, because the honest reading was that the
zone is simply occupied now. The lower vents (battery floor) stayed.

## The strain-relief boss that swallowed an insert hole — **a blocked drill**

The antenna strain-relief's threaded boss and a lid corner post both wanted the same patch of the
front wall. The gate that failed wasn't a collision check — it was a **0.4 mm air-cube probe**
placed inside the insert bore, asserting the hole is actually open. It found solid brass-to-be:
the strain relief's boss had quietly filled the corner post's drilling. Two constants moved
(the strain relief slid to wall-center, its boss shortened 0.5 mm clear of the camera), and the
probe breathed again.

## The screw path with a burr in it — **2.5 mm³**

A Ø3 mm virtual screwdriver, driven down each lid screw axis, clipped 2.5 mm³ of rebate-shoulder
material hanging over the corner posts. Invisible in any render; a real obstruction for a real
hex key. The posts now carry a Ø4 clearance bore through the shoulder — which the M3 shaft needed
anyway.

---

## Why this matters

None of these were visible in a render. All of them would have cost a print, an evening, and a
little trust in the design. The point of gate-driven CAD isn't that the code is clever — it's
that **the model refuses to lie to you**. When this repo says the parts fit, that claim has been
executed, not eyeballed.

*(And where the gates can't reach — insert melt strength, snap cycles, RF detuning — the docs say
`MEASURE_ME` and mean it. A CAD boolean is not a test.)*
