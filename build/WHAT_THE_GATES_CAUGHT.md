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

## The door boss that would have blocked the battery — **caught by a question**

The battery door was held by an M2 screw driven into an interior boss — a 7 × 7 mm block
reaching from the rear wall into the battery bay. It passed every *existing* gate, because no
gate ever placed the **battery's nominal envelope** against it: the 60 mm pack plus 1 mm of
swell ends at X 28.5, and the boss began at X 26.5 — **up to 2 mm of guaranteed interference**,
invisible in renders, waiting for the first real battery. The catch came from asking the
audit question out loud ("does the pack even fit past that thread?") and then encoding it:
the boss is gone, the door now closes with a flat top tab screwed into the wall + shelf ledge
(zero interior claim), and a new `[akku-frei]` gate asserts the ex-boss zone intersects
**0.00 mm³** of body on every rebuild — so this class of bug can't come back quietly.

> Lesson: a gate only protects what it measures. Every envelope that shares space with a
> printed feature needs its own nominal-collision assert — "nobody complained yet" is not one.

---

## The flange that grazed the antenna cable — **0.025 mm³, caught on the gate's first run**

When the optional cable-side T-piece got its ready-made U-notch (Ø 3.2, horizontal, at seat
height, open toward the stem's bottom edge), a new gate was written alongside it: lay a nominal
Ø 3.1 coax in the round seat and assert the mounted T-piece intersects it by **zero**. The very
first run failed — **0.025 mm³**. The notch cleared the stem fine, but the cable's top edge
(Z 25.55) reached 0.05 mm past the flange's underside (Z 25.5), a graze no render would ever
show. The relief now runs the full depth of the part, flange included; the doctrine stays
clean — the 2.9 mm wall slot does all the clamping, the T-piece never touches the cable — and
the assert runs on every rebuild of both senders.

> Lesson: write the gate *with* the feature, not after it. This one paid for itself before
> the geometry was an hour old.

---

## Why this matters

None of these were visible in a render. All of them would have cost a print, an evening, and a
little trust in the design. The point of gate-driven CAD isn't that the code is clever — it's
that **the model refuses to lie to you**. When this repo says the parts fit, that claim has been
executed, not eyeballed.

*(And where the gates can't reach — insert melt strength, snap cycles, RF detuning — the docs say
`MEASURE_ME` and mean it. A CAD boolean is not a test.)*
