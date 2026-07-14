# RF link analysis — helmet sender, donut orientation

*Condensed from the project's full analysis (`RF_ANALYSIS_DONUT`, model v1.0, 2026-07-01).*

> **THIS IS A CALCULATION / LINK-BUDGET MODEL, NOT A MEASURED TEST.** Every number comes from
> textbook formulas and literature ranges — no jump, no spectrum analyzer, no measured pattern.
> It says *where to look*, it proves nothing. The verification list is at the bottom.

> **Link model v1.0 note.** The RX gains below reflect the **interim store-bought ground
> station** (aimed patch + omnis). The current ground-station doctrine is several fixed beams
> of self-printed helix antennas (estimators span 10.7–13.9 dBic — measurement decides); a
> helix-based link model follows **after measurement D1**, rather than silently editing these
> numbers.

**Companion tool:** [`linkbudget_donut.html`](linkbudget_donut.html) — an interactive,
self-contained explorer (open it in any browser, no install). Play with altitude, drift,
pose and orientation and watch the margin.

## 1 · System parameters (sourced / given)

TX **+30 dBm** (1 W, HDZero Freestyle V2) · 5.8 GHz · TX cabling **−1.5 dB** · TX antenna
AXII 2 RHCP omni, **+2.2 dBic peak** · RX main: aimed patch used at an **honest +10 dBic**
(nominal 13) · RX diversity omnis +4.7 / +1.9 dBic (4-way receiver) · RX cable −1 dB ·
lock threshold **−90 dBm** (HDZero degrades gracefully a few dB below).
FSPL (Friis): **119.8 dB at 4 km**.

## 2 · The key correction to intuition

An omni's peak gain is **fixed** at +2.2 dBic no matter how you orient it. Turning the antenna
does not add power — it only re-points where the peak and the null go. Laying the puck
horizontal (axis pointing through the case wall) doesn't "transmit more downward"; it **aims** the same donut
at the ground station instead of wasting it on a horizontal ring. In freefall over the DZ the
ground station sits at down-angles of 63–83° — deep in the down hemisphere — so:

| altitude (500 m drift) | up/down donut advantage over an upright antenna |
|---|---|
| 4 km | **+17.9 dB** |
| 3 km | +17.5 dB |
| 2 km | +13.9 dB |
| 1 km | +7.3 dB |

**Do not stand the antenna vertical.** (The upright case even had its null-axis placed at the
least favourable azimuth — the delta above is conservative.)

## 3 · Body shadow (the honest crux)

Radio does not pass a human well. On-body literature at 5.8 GHz: torso deep-shadow −10…−18 dB,
head −6…−12 dB, with diffraction relief at body edges. A side-mounted element ~3–5 cm off the
head centreline buys a few dB back. Used values (side-mount): **head-down −1 dB · back-fly
−7 dB · belly −10 dB · sit −12 dB.** Body shadow is body geometry — identical for both antenna
orientations, and the **single biggest uncertainty in the whole model**.

## 4 · Margins at 4 km (dB above −90 dBm, up/down donut, honest RX gain)

| pose | 4 km | 3 km | 2 km | 1 km |
|---|---|---|---|---|
| **Head-down** | **+8.8 ✓** | +11.2 ✓ | +14.3 ✓ | +18.6 ✓ |
| **Back-fly** | +2.8 ⚠ | +5.2 ⚠ | +8.3 ✓ | +12.6 ✓ |
| **Belly** | **−0.2 ✗** | +2.2 ⚠ | +5.3 ⚠ | +9.6 ✓ |
| **Sit** | −2.2 ✗ | +0.2 ⚠ | +3.3 ⚠ | +7.6 ✓ |

What closes the thin cells: the patch's nominal gain if it delivers (+3 dB everywhere) ·
4-way ground diversity catching pose transitions · **descent** (2–3 dB per km, within seconds) ·
HDZero's usable picture a few dB below lock. What must be proven: the sit/high-altitude corner.

## 5 · Assumptions & their direction of error

FSPL only (no multipath — ground reflections near the DZ swing ±several dB) · shadow values are
literature midpoints, not this helmet · ideal-dipole toroid floored at −18 dB (the real CP
pattern is rounder — narrows the delta, doesn't flip the sign) · RX patch assumed aimed
(a lost aim costs up to 10 dB instantly — the omnis are the backstop) · RHCP↔RHCP matched.

## 6 · Verify before trusting (in order)

1. **VNA S11 of the antenna with its coax in the printed clamp** (instrument must cover 5.8 GHz).
2. **Bench range test** (antenna on a pole, walk the RX out) — isolates FSPL+antennas from body shadow.
3. **A real jump with a logging ground station**: RSSI vs altitude/pose vs these cells — one
   belly pass from 4 km validates or kills the −10 dB shadow assumption.
4. **Diversity switching in situ** on pose transitions.

*No superlatives. The result is: up/down is clearly the right orientation for a below-you
ground station; head-down and descending belly close comfortably; the head-up/high-altitude
corners are the ones to prove with a real jump.*
