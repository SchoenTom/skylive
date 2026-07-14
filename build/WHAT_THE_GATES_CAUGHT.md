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

## The strain relief we read backwards — **overturned by a neutral review**

For days this design carried a confident claim: the antenna coax is held by a **2.9 mm
press-fit slot** ("−0.2 mm interference, the slot grips the jacket") and the T-piece is merely
a lid. It sounded right, it gate-checked green — and it was a misreading of the reference
build. When the builder pushed back ("the cable should go all the way down and be *fully*
clamped — pressed by the two screws"), the claim was handed to a **neutral reviewing agent**
with photographs and the reference STEP files, with instructions to explain the mechanism from
scratch. The measurements said the opposite of the claim: the reference seat is **Ø 3.2 with
clearance** on a Ø 3.1 cable, and the T-piece's stem ends in a **convex nose of R 1.55 —
exactly the cable radius**. The slot guides; the seat supports; **the two vertical M2 screws
create the clamping force** by pulling the nose 0.4 mm onto the cable.

Both senders were rebuilt to the real mechanism, and the old gate ("T-piece must never touch
the cable") was replaced by its inverse: a **clamp gate** that lays a nominal Ø 3.1 coax in the
seat and asserts the seated T-piece interferes with it by a *defined* amount — 1.15 mm³, the
0.4 mm press — on every rebuild.

> Lesson: a gate can only defend the design intent you encoded. If the intent itself is a
> misreading, green gates just make the mistake reproducible. When the person holding the
> physical part says "that's not how this works" — measure again, from scratch, without your
> own assumptions in the prompt.

---

## The counterbore that swallowed the screw head — **caught by looking at the part**

The roof lid is 3.0 mm thick. Its three M3 counterbores were speced at Ø 6.1 × **3.4 deep** —
head height 3.0 plus 0.4 to sit sub-flush. Nobody ever held that 3.4 against the 3.0 the lid
actually has: the counterbore went **clean through**, turning each screw hole into a Ø 6.1
through-bore. The Ø 5.5 cap head would have dropped straight through the lid and clamped
nothing — a lid held by friction and hope. Every existing gate passed, because every existing
gate checked shape validity and collisions, not *function*. The catch came from looking at the
printed-parts preview and asking the obvious question: "does that head actually bear on
anything?"

The final fix came from the reference build's own lid: its STEP file measures **4.5 mm thick**
with a **Ø 6.5 × 3.4 counterbore** — a 1.1 mm floor, head sunk 0.4 sub-flush. This lid gets
there with **local Ø 10 × 1.5 pads on its underside** (4.5 mm exactly where the screws live,
3.0 everywhere else), the bosses shortened to make room, and the screws moved 1 mm diagonally
inboard so the sunken head sits entirely inside the rebate's corner radius — each constraint
found and enforced by the rebuilt `[deckel-kopf]` gate (floor bears, head is sub-flush, head
touches no body material).

> Lesson: the drawing convention ("head height + 0.4") is not a design check. Every
> counterbore depth needs to be asserted against the *local* thickness it lives in.

---

## The tab a neighbor spotted — **15 mm²**

The battery door closes with a classic proud tab: a flat tongue over the wall, one M2 into a
brass insert. Every gate was green — form closure 0.000 mm³, zero overhang past the tab, swing
sweep clean. Then, at the lab's slicing station, someone leaned over from the next PC and said
the joint between the door and that tab *"looks weak."* He was right, and measurably so: the
tab bonded to the door's outer face over a strip of just **10 × 1.5 mm — 15 mm²** — and the
tab doubles as the grip, so that little patch gets **peel-loaded** every time someone levers
the open door by it. Peel on a small printed bond line is the classic crack starter, and no
gate had ever *measured* the bond, because the intent "tab attaches here" was encoded as a
boolean union, not as an area worth asserting.

The fix cost nothing anywhere else: the tab grew from 10 to 12 mm wide (+20 % at the critical
parting-line section) and its bonding apron was extended from 1.5 to 6 mm down the door face —
**72 mm² of lap joint instead of 15 of peel line** (54 mm² on the mini, whose door louvers sit
higher). The body, lid, latches and strain-relief tees are byte-identical to before; only the
door reprints.

> Lesson: gates only defend what you thought to measure — and a fresh pair of eyes is a gate
> you can't write. This project is open source on purpose; critique from the next desk over
> is part of the toolchain. (Whether the joint *holds* is still a pull test, not a boolean.)

---

## The review that upgraded the gate itself — and found three real bugs

A colleague printed the sender, opened the STEPs in SolidWorks, and sent back two videos of
findings. Chasing them taught the toolchain more than any single fix:

- **"Infinitely thin edges everywhere the radius runs out"** — the mesh gate confirmed
  sub-0.1 mm readings all over the body… and then section renders showed every one of them is
  a *tangency cusp* where a fillet feathers into a plane. The printed part in hand proves the
  slicer just merges them. The naive gate was crying wolf.
- So the gate learned to *classify*, not just measure: a thin cluster is only a FAIL if it is
  **a surface, not a curve** (PCA width) **and a plateau, not a ramp** (thickness IQR).
  Calibration anchors: a synthetic 0.4 mm membrane must FAIL, an acute wedge must PASS,
  the louver blades (0.72 mm by design, printed successfully) must WARN — not block.
- The upgraded gate immediately caught **three real design bugs** the old one was blind to:
  a 0.5 mm counterbore floor in the flush strain-relief tee (now 1.0 mm), an XT30 clamp bar
  that was sub-millimetre over its cable grooves in *every* size (now 1.7 mm of floor), and
  groove positions on the mid-size body that had never been rescaled after the case got
  narrower — one groove was quietly eating 0.8 mm into the wall.
- The one part that actually **broke** in the field — a GoPro fork finger — already had its
  root fillet. The real culprit is layer orientation on a one-piece body: the fingers print
  vertically, layers across the load. A bigger radius is measured-fit-gated; until then the
  doctrine is a brim and no prying.

> Lesson: a printability gate is a hypothesis about what "unprintable" means. A real print,
> a real break, and a skeptical reviewer are the experiments that falsify it. Version 2 of
> the gate now ships in `build/cad/printability_gate.py` and runs as a hard export gate in
> all three model scripts.

---

## Why this matters

None of these were visible in a render. All of them would have cost a print, an evening, and a
little trust in the design. The point of gate-driven CAD isn't that the code is clever — it's
that **the model refuses to lie to you**. When this repo says the parts fit, that claim has been
executed, not eyeballed.

*(And where the gates can't reach — insert melt strength, snap cycles, RF detuning — the docs say
`MEASURE_ME` and mean it. A CAD boolean is not a test.)*
