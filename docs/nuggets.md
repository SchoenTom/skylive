# SkyLive — five numbers that carry the design

*Five engineering "nuggets" — one number each, a few sentences each. The kind of small, exact
figure that a whole design quietly hangs on. Sourced where sourced, **[CALC]** where modelled,
honest either way. Card texts for the show layer; the derivations live in [`../build/`](../build/).
These five render as number cards in the Pages site (docs/index.html).*

---

### R 1.55
**The nose that matches the cable exactly.**
The antenna cable drops all the way down into a round seat with clearance — insertion never fights
the print. Then the T-piece's stem lands on it: a convex nose of radius 1.55 mm, precisely the
cable's own radius, so it cradles instead of cutting. Two vertical M2 screws pull that nose 0.4 mm
onto the cable — the screws are the clamp, measured 1:1 off a working reference build. A yank on
the antenna loads the printed wall and the bolted nose, never the connector.

---

### −0.2 mm
**The squeeze standard (where squeezing is right).**
The battery-lead saddles are under-sized by a tiny, deliberate amount: 0.2 mm less than the wire
they hold. It's the line between gripping and crushing. The antenna clamp deliberately does NOT use
it — coax hates being squeezed by tolerances (it detunes), so there the seat has clearance and two
screws deliver a controlled, serviceable clamping force instead. Same goal, two honest mechanisms.

---

### 90°
**The turn that dodges the null.**
The omni doesn't stand upright like on an FPV quad — its coax runs horizontally through the case
wall and the bell sits directly against it, axis pointing straight through the wall. An upright
omni's donut pattern has nulls straight up and down: in head-up or head-down freefall that aims a
blind spot exactly at the receiver. Laid sideways, the donut fires down, up and all around — signal
toward the ground in every jump attitude. And the strain relief becomes trivially simple: the cable
never turns, so the T-clamp just drops onto it and screws shut.

---

### 14 ms
**Glass-to-glass latency.**
From the lens in freefall to the picture on the ground TV is about 14 milliseconds — faster than a
blink, faster than you can perceive as delay (manufacturer figure). It's not the internet and it's
not a stream; it's a private digital radio link with nothing in the middle to buffer. The jump you
watch on the screen *is* the jump happening in the sky, in the present tense.

---

### 4 parts
**No flight controller. No BEC. One printed body.**
The entire transmitter is four things — a radio, a camera, a battery, and an antenna — inside one
printed body. Every FPV builder expects a flight controller, a voltage regulator, a rat's nest of
wiring; there is none of it here. The few joints that remain are soldered once, properly, for
flight — every joint earns its place. The restraint *is* the engineering: fewer parts, fewer
failure points.
