# SkyLive — Assembly, step by step (the fiddly bits)

*The close-up companion to [`BUILD_GUIDE.md`](BUILD_GUIDE.md). Where the build guide gives you the
system and the wiring map, this file walks the **hand movements** — the ones that go wrong the
first time if nobody warns you. Each step is written as **Do / Why / Watch out (the failure it
produces)**, in the order you actually work.*

*Labels, same discipline as the rest of the repo: sourced numbers carry their origin, **[CALC]** =
calculated, `MEASURE_ME` = you must caliper your own part, **`TBD-ASSET`** = a photo/render or a
still-open, model-dependent number that lands when the final CAD pass closes. **Nothing here
carries a "measured" badge yet** — the reference prototype prints and fits; the numbers below are
spec-locked, not bench-proven. A CAD boolean is not a test.*

> ⚠️ Read [`LEGAL_DE.md`](LEGAL_DE.md) before any transmit. All development is **25 mW SRD**;
> 1 W is the event-only PMSE path. And read the three hardware-killer rules in
> [`BUILD_GUIDE.md` § 6](BUILD_GUIDE.md#6--hardware-killers-never-skip) before you power anything.

---

## Before you start — the two-minute inventory

The four functional parts (VTX, camera, battery, switch), **3× Wago 221-412**, the
**U.FL→SMA flange pigtail**, one antenna (donut omni **or** down patch), the **1.5 mm thermal
pad**, the printed shell + lid + drop-in divider tray + battery door, the small-parts bag
(**M3 brass heat-set inserts, M2 & M3 DIN 912 cap screws**), and the tools:
**soldering iron (for the inserts only — the wiring is solder-free)**, a multimeter, an 8 mm
wrench for the SMA, hot glue/RTV, a caliper.

> Order note: seat the **heat-set inserts first** (they need a hot iron and an empty shell),
> then do all the cold work. Never run the iron near a seated battery or the VTX.

`TBD-ASSET` — layout photo of the full parts spread (renders/steps/00_inventory.png).

---

## Step 1 · Melt the M3 brass inserts into the roof-lid posts

**Do.** The shell prints with **Ø 4.6 mm insert holes** in **Ø 8 mm corner posts** under the roof opening (3 posts — the camera owns the fourth corner),
each with a small **Ø 5.2 × 0.5 mm lead-in chamfer** on top. Set the soldering iron to
**250–270 °C** (rule: print temperature **+10…20 °C** — hot enough to melt PETG, not scorch it).
Sit a brass insert (**Ø 5.0 mm OD × 6.0 mm long**, measured on the reference part) on the chamfer,
put the iron tip **flat into the insert's bore from directly above**, and let *its own weight plus
the lightest push* sink it. Keep the iron **dead vertical**. Stop when the insert sits **~0.3 mm
below flush** (sub-flush, so the lid face seats on plastic, not on brass). Withdraw the iron
straight up; a wet fingertip or a flat cold tool can true the top while the plastic is still soft.

**Why.** A cold-pressed insert splits the boss; a heat-set one melts the plastic into its knurl and
locks in. The **Ø 4.6 hole is a deliberate ~0.4 mm undersize** vs the 5.0 insert — the displaced
melt is what grips the knurl. The **Ø 10 boss** keeps ≥ 50 % of an insert-diameter of wall around
it so it doesn't bulge the outside. Sub-flush by 0.3 keeps the sealing face clean.
(All geometry [CALC] from standard heat-set guidance + the measured insert; **fit is
bench-verified pending** the first real melt.)

**Watch out.**
- **Brass blob / plastic welling up over the rim** → iron too hot or pushed too hard. It's sunk too
  far and the boss face is fouled. Back off temperature, let it cool, pare the blob flush.
- **Insert goes in tilted (skew)** → the iron wasn't vertical, or you pushed off-axis. A tilted
  insert cross-threads the M3 later. Reheat, push it upright against a flat block, re-true.
- **Insert won't sink / plastic barely softens** → iron too cold or hole printed under-size; give it
  temperature, not force — forcing a cold insert cracks the boss.
- **Insert spins in the hole afterwards** → over-heated, the melt reflowed too loose. That boss is
  compromised; the honest fix is to plug and reprint, not to glue.

There are **4× M3 inserts** in the lid corners (the lid opens **only floor 2** — the battery bay
keeps its solid wall and is reached through the door). `TBD-ASSET` — final insert count/positions
confirm with the closing CAD pass; macro photo → renders/steps/01_insert.png.

---

## Step 2 · Fit the antenna coax into its edge clamp (the 2.9 mm principle)

*(Donut-omni variant. Skip to Step 3 if you build the down-patch variant — its patch bolts into the
bottom shell instead; see [`ENGINEERING/antenna_capsule.md` § 5](ENGINEERING/antenna_capsule.md).)*

**Do.** The semi-rigid antenna coax runs into an **open-edge clamp** cast onto the wall: you **lay
the cable into the channel from the side** (never thread it through a closed hole), then close the
mating cap. Fully closed, the clamp leaves a **2.9 mm gap** onto the **Ø 3.1 mm coax** — i.e. a
**−0.2 mm interference**. The cap pulls down with **cap screws into printed cores** (the
strain-relief block on the reference part is **4× M2**, body ~17.9 × 13.05 × 5.8 mm). Snug the
screws evenly, corner to corner, until the cap face meets the block face.

**Why.** −0.2 mm is a **clamp, not a crush**: enough to hold the cable against a pull so the load
lands in the printed wall, not enough to deform the coax and detune the antenna. Laying the cable in
(vs. threading) means the connector never has to pass a closed hole — the whole strain-relief
family in this project works that way. **If your coax measures thicker than Ø 3.1, open the channel
to suit — do not widen the 2.9 clamp gap; keep the −0.2 grip and give the extra to the channel.**

**Watch out.**
- **Coax jacket bulges / oval, or S11 shifts** → over-clamped (channel too tight for *your* cable).
  Relieve the channel, preserve the −0.2 gap.
- **Cable pulls free / slides under load** → cap screws not evenly seated, or the gap ended up
  *over* 2.9 (cap not bottomed). It should not move by hand.
- **Cap won't close square** → a screw core stripped or the cable is pinched proud of the channel;
  re-seat the cable fully before the cap, don't force the cap onto it.

Then form the coax's **single 90° bend (R ≥ 8 mm)** once, by hand on the printed jig, and mate the
**SMA** to the internal jack (8 mm wrench, firm — not gorilla-tight). The fragile **U.FL is touched
exactly once** at the pigtail and never again. `TBD-ASSET` — clamp cross-section render →
renders/steps/02_coax_clamp.png; final block dimensions confirm with the CAD pass.

---

## Step 3 · Seat the VTX against the thermal pad

**Do.** Peel one face of the **1.5 mm silicone thermal pad (≥ 3 W/mK)** and stick it to the
**inside of the case wall** opposite the antenna capsule. Seat the VTX with its **hottest face flat
against the pad**, no air gap, and let the printed shelf/ribs locate it. The VTX is **not** screwed
to the wall — the pad's tack plus the shelf hold it; the wiring dresses last.

**Why.** At 1 W the VTX is the hottest thing in the box (~90 °C in ~2 min in a closed case on the
bench, [CALC]). The pad is a **mandatory** second heat path into the wall — on the ground it only
moves ~0.6 W, but it buys 1–2 minutes in the power-up window and carries ~2.5 W in freefall
([CALC], derivation in [`ENGINEERING/thermal.md`](ENGINEERING/thermal.md)).

**Watch out.**
- **Air gap behind the VTX** → pad not compressed, thermal path is fiction. You should see the pad
  *slightly* squished when seated.
- **Pad on the wrong face** → it must touch the VTX's heat-spreader face, not the connector side.
- **Never bench-power the VTX in the closed case at > 25 mW for more than a minute or two** — it
  will over-temp and RF-cut. That's expected behaviour, not a fault.

`TBD-ASSET` — VTX-seated render → renders/steps/03_vtx_pad.png.

---

## Step 4 · Camera + MIPI

**Do.** Sit the camera in its printed cradle with the **lens looking out through the wall opening**
(outer face essentially flush/snag-free). Route the **20-pin MIPI ribbon** to the VTX and seat the
connector squarely. The camera is retained from **inside** by an **M2 DIN 912 cap screw** in a
counterbore sized so the head fully sinks (**Ø 4.4 × 2.4 mm counterbore** for the Ø 3.8 × 2.0 mm M2
head — the project screw standard).

**Why.** Inverting the *mounting* structure inward (lens still out) keeps the outside clean and the
camera captured; the counterbore keeps the screw head below the surface so nothing snags. The camera
is powered **over the MIPI by the VTX** — there is no separate camera wire.

**Watch out.**
- **MIPI seated at an angle / half-in** → the ribbon is fragile and the contact is finicky; a dark
  or glitchy picture is almost always the MIPI, not the camera. Re-seat gently, straight in.
- **Creasing the ribbon** → don't fold it to make it fit; give it a gentle service loop.
- **Lens proud of the wall** → check the cradle depth; the outer face should sit flush, not stick
  out (the whole point of the inverted mount).

`TBD-ASSET` — cradle + lens-window render → renders/steps/04_camera.png; final counterbore/hole
figures confirm with the CAD pass.

---

## Step 5 · XT30 strain relief — lay in, lock, *then* solder behind

*This is the one place a soldering iron touches the power side, and it happens **after** the cable
is mechanically captured, so the solder joint never carries load.*

**Do, in this exact order:**
1. **Lay** the two battery-lead conductors (**Ø 2.8 mm each**, measured) into their **two separate
   channels** on the strain-relief saddle — red in one, black in the other. Each channel closes to a
   **2.6 mm clear width** (**−0.2 mm** on the 2.8 conductor), separated by a **~1.8 mm web**.
2. **Close the bar** over them: **2× M2 DIN 912 cap screws into printed Ø 1.7 mm cores** (undersize
   on purpose — print shrink lets the screw cut its own thread). Snug evenly until the conductors
   are captured.
3. **Only now** solder the **XT30 behind the clamp** (on the far/door side, +X end), with the
   ≥ 10 mm of iron clearance the block leaves toward the door.

**Why.** Two separate channels stop the conductors wandering (one wide channel lets them cross). The
**−0.2 mm** grip captures each conductor mechanically **before** anything is soldered, so a pull on
the battery cable lands in the printed block and the **XT30 joint sits load-free**. The
**base is printed integral to the body** (stronger than a bolt-on back plate, no mounting screws),
and the saddle builds **up/inward** (never down toward the battery) — the XT30 stows up top, so the
geometry agrees with itself.

**Watch out.**
- **Soldered the XT30 first** → you can no longer lay the conductors into the channels; you'd have
  to feed the whole connector through. Wrong order — the mechanical capture must come first.
- **One conductor jumped its channel / both in one groove** → they'll chafe and can short; each gets
  its own channel, red and black kept apart.
- **Conductor squashed flat under the bar** → over-tightened; −0.2 is a grip, ease off.
- **Iron can't reach / melts the block** → respect the ≥ 10 mm clearance toward the door and keep
  the tip on the terminal, not the plastic.

`TBD-ASSET` — two-channel saddle render + the lay-in/lock/solder sequence →
renders/steps/05_xt30_relief.png; final saddle dimensions confirm with the CAD pass. There are
**two** of these saddles (left + right at the door end).

---

## Step 6 · Power wiring — three Wago 221-412, zero solder

*(Verbatim-critical steps mirror [`BUILD_GUIDE.md` § 4](BUILD_GUIDE.md#4--wiring--completely-solder-free)
— reproduced here so the sequence reads in one place.)*

**Do.** Plug the stock **JST-GH 6-pin harness** into the VTX and take **red (+) and black (GND)**;
cap the unused yellow/white/blue with heat-shrink. Then three **Wago 221-412** lever clamps:

```
Battery XT30 ── pigtail (+) ──[Wago]── switch ──[Wago]── VTX red (+)
                pigtail (−) ──[Wago]──────────────────── VTX black (GND)
```

The **+ line uses two Wagos** (through the switch); the **− line uses one**. Strip to the Wago's
window, flip the lever down, done. Thin strand wobbling in the clamp? **Fold the bare end double** —
no ferrule, no crimper. When wiring is confirmed, put a dab of **RTV/hot glue on each lever** against
vibration.

**Why.** No motors, clean supply → **no capacitor, no solder** on the power path. Levers re-open in
seconds for service. The switch **breaks the battery + line directly** (~1.3 A, [CALC] 850 mAh /
~1.3 A).

**Watch out.**
- **Lever not fully closed** → intermittent power, the worst kind of fault in the air. Every lever
  flat-down, give each wire a gentle tug.
- **Balance (JST-XH) plug wandering toward the VTX** → **charging only**, never toward the VTX.
- **Reverse polarity** → the VTX has **no reverse-polarity protection**. See Step 8 — multimeter
  before first power, no exceptions.

---

## Step 7 · Dress the cables through the fixed shelf

**Do.** The divider shelf is **printed into the body** — there is nothing to install. Route the
battery leads **up through the shelf cut-outs** (two large windows at the ±X ends; the +X one is
the XT30/airflow window), lay each cable **into** its opening — laid in, never threaded through a
closed hole. Park the mated XT30 and the Wago bank in the **left-hand zone** of floor 2 (the open
volume beside the camera module).

**Why.** A printed-in shelf removes one part, one alignment step and two screws versus a drop-in
tray, and the interlayer joint is replaced by solid walls. The cut-outs double as the chimney
airflow path. Derivation: [`ENGINEERING/divider.md`](ENGINEERING/divider.md) *(the tray analysis
there documents the earlier drop-in design — superseded by the printed-in shelf).*

**Watch out.**
- **Cable pinched between battery and shelf** → the battery won't slide fully home; route leads
  into the +X window *before* seating the battery.
- **Wagos drifting over the VTX** → keep them in the left-hand zone; the VTX needs its full
  clearance under the lid.

`TBD-ASSET` — tray drop-in render → renders/steps/06_divider.png.

---

## Step 8 · First power (bench) — the ritual that saves the VTX

**Do, every time, in order:**
1. **Antenna on BEFORE power — always.** SMA mated (or a **50 Ω dummy load**) *before* the battery
   goes in.
2. **Multimeter on the VTX red/black:** red must read **+11–12.6 V** (3S), red = +, black = −.
3. Battery in → the VTX boots in **pit mode (0 mW)**. Set channel and power from the **ground-station
   (BoxPro) menu**, lowest usable power, watch the heat.

**Why.** Powering a VTX **without an antenna reflects the PA's own power back into it and kills it
instantly** — this is the single most common way these die. The **no reverse-polarity protection**
means one swapped Wago at 12 V ends the VTX; the multimeter is a hard gate.

**Watch out.**
- **No orange witness dot in the capsule dome** → the antenna is **not** inside. Dark hole = EMPTY =
  do not power (see [`ENGINEERING/antenna_capsule.md` § 4](ENGINEERING/antenna_capsule.md)).
- **Any heat you can't hold a finger on within ~2 min at > 25 mW in the closed case** → power down;
  that's the thermal envelope, not a surprise.

---

## Step 9 · Close the battery door (the TV-remote move)

**Do.** With the battery in its bay (and its **foam preload** in place so it can't fly free), fit
the door: **slide it in along the bay**, then a **gentle end-tilt (≤ 4°)** until the retaining noses
catch, and press home — you'll feel **two side clicks**. Finally drive the **single M2 DIN 912
screw** to lock it. It works exactly **like a TV-remote battery door**: slide, tip, click, then
the screw is just the safety.

**Why.** The slide-then-tilt lets the noses engage without forcing the door square onto them; the
clicks are the snap features seating; the screw is a positive lock, not the primary retention. The
**foam preload is mandatory** — a loose 80 g pack hits ~590 N on a hard stop, the foam cuts that to
~250 N ([CALC], [`ENGINEERING/divider.md`](ENGINEERING/divider.md)).

**Watch out.**
- **Tilting more than a few degrees / forcing it flat** → you'll shear or miss the noses. Small
  tilt, let them catch, then press.
- **No click, or the door springs back** → a nose isn't engaged or a cable is pinched behind the
  door; back out, clear the cable, retry. Don't drive the screw to pull a mis-seated door closed.
- **Door rattles after the screw** → foam preload missing or too thin; the pack must be captured,
  not free.

`TBD-ASSET` — door slide/tilt/click sequence render → renders/steps/07_door.png; final nose/latch
geometry confirms with the CAD pass.

---

## Step 10 · Final walk-around before the case is trusted

- Every **Wago lever flat-down**, glued; give each wire a tug.
- **Multimeter** polarity re-checked at the VTX.
- **Antenna captured**, orange witness dot visible, SMA snug.
- **Thermal pad** compressed, no air gap.
- **Strain reliefs** (antenna clamp + both XT30 saddles) hold against a firm cable pull — the pull
  lands in the printed block, not on a joint.
- **Battery door** clicked and screwed; **foam preload** present.
- **Roof lid** seated on its rebate (lip dips into the opening, flush on top), 3× M3 snug from above (not crushing the posts); the 12 mm switch pokes through its lid hole.

Then — and only then — go to the empirical protocol: **[`MEASURE.md`](MEASURE.md)** (VNA S11 of the
encapsulated antenna, the thermal A/B test, the caliper list). This assembly is
**bench-verified pending**: the shell prints and the parts fit on the reference prototype, but no
step above has a *measured* badge until you run those tests on your own build.

`TBD-ASSET` — finished-assembly hero + the full step gallery (renders/steps/\*.png) land as the
final CAD/render pass closes.
