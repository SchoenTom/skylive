# SkyLive — five numbers that carry the design

*Five engineering "nuggets" — one number each, three sentences each. The kind of small, exact
figure that a whole design quietly hangs on. Sourced where sourced, **[CALC]** where modelled,
honest either way. Card texts for the show layer; the derivations live in [`../build/`](../build/).*

`TBD-ASSET` — these five render as number cards in the Pages site (docs/index.html) and the README
strip; visual treatment lands with the final design pass.

---

### 2.9 mm
**The clamp gap that grips without crushing.**
When the antenna's strain-relief cap closes all the way, it doesn't touch the wall — it leaves
exactly 2.9 mm around a 3.1 mm coax. That last fraction of a millimetre is the whole trick: enough
to hold the cable against a hard pull, not enough to deform it and detune the antenna. A pull on the
lead lands in the printed block; the connector never feels it.

---

### −0.2 mm
**The squeeze standard.**
Every clamp in this build is under-sized by the same tiny, deliberate amount: 0.2 mm less than the
thing it holds. It's the line between *gripping* and *crushing* — 0.2 too little and the cable
slips, 0.2 too much and you flatten a conductor or pinch a coax. One number, reused at the antenna
clamp and both battery-lead saddles, so every strain relief behaves the same way.

---

### 0.15 dB
**The radome that costs almost nothing.**
The omni antenna is sealed completely inside a 1.5 mm printed wall — and at 5.8 GHz that wall costs
about 0.15 dB, roughly 3 % of the signal ([CALC]). It's a slab about one-twentieth of a wavelength
thick, so its two surface reflections nearly cancel and the wave passes as if the plastic weren't
there. For that near-nothing you delete wind load, fatigue and snag risk entirely — the real risk
left is *detuning*, which is why a VNA check is mandatory, not optional.

---

### 14 ms
**Glass-to-glass latency.**
From the lens in freefall to the picture on the ground TV is about 14 milliseconds — faster than a
blink, faster than you can perceive as delay (manufacturer figure). It's not the internet and it's
not a stream; it's a private digital radio link with nothing in the middle to buffer. The jump you
watch on the screen *is* the jump happening in the sky, in the present tense.

---

### 4 parts
**No flight controller. No BEC. No solder on the sender.**
The entire transmitter is four things — a radio, a camera, a battery, and a button — joined with
three lever clamps and not one soldering-iron joint on the power side. Every FPV builder expects a
flight controller, a voltage regulator, a rat's nest of solder; there is none of it here. The
restraint *is* the engineering: fewer parts, fewer failure points, re-openable in seconds.
