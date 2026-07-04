# Verification & Quality — how we make a printable part *trustworthy*

Most "3D-printable" hardware repos hand you an STL and hope. This one treats the gap between
a CAD model and a part that actually works as the real engineering problem. Here is the honest
principle first, then the method.

> **No CAD check can promise "100 % error-free." A gate is a boolean test on a digital model —
> it is not a physical test.** What a good process delivers instead: it catches each *class* of
> error at its own layer, so the chance of an uncaught defect becomes vanishingly small **and**
> whatever slips through shows up *cheaply* (a 5 g coupon) rather than *expensively* (a ruined
> full print). That is why the full print is the **last** step, never the first.

## Defense in depth — seven layers

**1 · Prevention — errors that never happen.**
A single source of truth (`cad/spec.py`) holds every dimension; each is either measured from an
official manufacturer STEP, sourced from a datasheet (URL in a comment), or explicitly flagged as
"must be calipered." No magic numbers live in the model. Everything is parametric, so changing one
number updates the model *and* its checks consistently — no drift between docs, model and renders.

**2 · Automated geometry gates — every build, fail loud.**
Each build asserts: watertight single solids, pairwise interference ≥ clearance, minimum wall,
internal bay envelope, vent open-areas, antenna-capsule fit, switch-head clearance, connector
feed-throughs. **The load-bearing rule:** a gate checks against the *nominal, as-designed* feature
positions — **never against the post-boolean body**. A gate that "passes" only because the conflict
was carved out of the shell is banned; it would hide exactly the structural defect it should catch.
(We learned this the hard way: an early interference gate silently passed while a switch overlapped
a load-bearing screw boss, because the boss had been cut away to make room. Now the check runs on
the intended geometry.)

**3 · Cross-checks & redundancy.**
Key quantities are measured two independent ways — boolean volume vs. summed volume, exported-STL
bounding box vs. the model's own dimensions — so a silent export or transform error can't hide.
Orthographic drawings and shaded renders get a human eye on every geometry change.

**4 · Independent adversarial verification.**
A second, fresh reviewer with its *own* watertight and collision checker re-derives every pairing
and does not trust the builder's gates. Disagreement is the point.

**5 · The CAD → print bridge — where most real defects are born.**
Before printing we read the **slicer's actual toolpaths**, not the CAD: walls the slicer silently
drops, gap-fill worms, overhangs beyond the support-free limit, seam placement, bridges. Walls are
kept to an integer multiple of the extrusion width so no gap-fill lands inside a wall. A worst-case
tolerance stack-up is computed per joint (shrink bias + spread + hole under-size): does it still fit?
Shrinkage compensation, elephant-foot chamfers and per-part print orientation (so the layer lines
never run along the main load direction) are all fixed here.

**6 · Physical coupons — the only real proof before the full print.**
Small test prints of every critical fit — heat-set boss, switch hole, battery door, camera/GoPro
mount, antenna capsule, divider ledge — are printed and tested with the *actual hardware*. Structural
claims (e.g. "the divider survives a 1.5 m drop") are validated with a coupon drop test, not left as
a beam calculation. The antenna capsule gets a NanoVNA S11 sweep, because the real RF risk of
encapsulation is detuning, not the (calculated, negligible) ~0.15 dB of dielectric loss.

**7 · Measurement & release discipline.**
The handful of values that can't be sourced are calipered and pinned into `spec.py` before anything
is called "final." Until then it is explicitly a *fit prototype* — and it is labelled as one. A
release checklist (below) must be fully green.

## Release checklist

- [ ] All gates pass, checked against **nominal** geometry (no masking by subtraction)
- [ ] Exported-STL bounding box equals the model's dimensions (cross-check clean)
- [ ] Independent verification with no open blocker
- [ ] Slicer preview clean — no dropped walls, no gap-fill worms, support planned
- [ ] Worst-case tolerance stack-up > 0 at every joint
- [ ] Every critical fit passed as a physical coupon (incl. drop test + NanoVNA)
- [ ] All "must-caliper" values measured and pinned into `spec.py`
- [ ] Material is ASA (final) / PETG (prototype), never PLA
- [ ] Honestly labelled: the first print is a fit prototype

*As long as one box is open, it is a prototype — and it is called one.*
