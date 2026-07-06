# SkyLive — Build Guide (solder-free)

> **Wiring doctrine (updated):** the **soldered build is the recommended flight configuration** —
> every lead cut to its actual run length (shorter cables = less weight, less rattle, fewer
> failure points). The Wago 221-412 path below stays as the excellent **zero-solder quick-build**
> for a first assembly and for iterating. Everything else on this page applies to both.


*Condensed English edition of the project's German build document (`BAUANLEITUNG`, 2026-06-29,
specs verified against HDZero documentation). Status: the electronics build below is bought,
specified and wiring-verified on paper; the printed case passes its geometry gates at
**63 × 71 × 85 mm** (side-capsule omni variant; the down-firing patch variant is 63 × 71 × 101 mm).
The STEP/STL files build from [`../cad/`](../cad/). **Nothing here carries a "measured" badge yet —
the first print is a fit prototype, and a handful of values are still datasheet fallbacks.***

> ⚠️ Read [`LEGAL_DE.md`](LEGAL_DE.md) before transmitting anything. In Germany, all testing
> happens at **25 mW** under the licence-free SRD general authorization; 1 W needs a PMSE
> short-term assignment (event) — see the doctrine there.

---

## 1 · The system — two devices

| device | purpose | core |
|---|---|---|
| **Sender** (helmet) | 1 W live video from freefall (up to 4 km) | HDZero **Freestyle V2** VTX + **Nano90** camera · 3S LiPo · standalone — **no flight controller, no BEC** |
| **Ground station** (DZ) | receive + public viewing | HDZero **BoxPro** (4-antenna diversity, Mini-HDMI out) + aimed patch & omnis |

## 2 · Sender parts (all plug/lever — no soldering iron)

- **HDZero Freestyle V2 VTX** — 1 W, input 7–25 V (2–6S), 6–15 W draw, U.FL antenna output, **no reverse-polarity protection**
- **HDZero Nano90 camera** + 20-pin **MIPI cable** (fragile — powered by the VTX over MIPI)
- **Tattu R-Line 3S 850 mAh** (XT30 + JST-XH balance) — smaller 2–3S packs work too, only shorter airtime
- **12 mm latching push-button** (2 A / 12–250 V, pre-wired) — carries the ~1.3 A directly in the + line
- **3× Wago 221-412** lever clamps (0.14–4 mm²) — the entire power wiring
- **U.FL→SMA flange pigtail** (e.g. TBS, 60 mm) — fixed once, protects the fragile U.FL
- **Antennas (5.8 GHz, RHCP):** the captive donut omni (Lumenier AXII 2) or the down patch
  (TBS 5G8) — one at a time, see [`ENGINEERING/antenna_capsule.md`](ENGINEERING/antenna_capsule.md)
- **Thermal pad** 1.5 mm, ≥ 3 W/mK, VTX face → case wall (mandatory — see doctrine, § 7)
- **Printed case** — PETG for fit prototypes, **ASA for the final part, never PLA** (`TBD-CAD-M6`)

Tools/consumables: **multimeter (mandatory — polarity check)**, heat-shrink, RTV/hot glue
(secure the Wago levers + strain relief), zip ties, a 50 Ω SMA dummy load (safe bench testing).

## 3 · Connector facts (verified)

- **VTX harness = JST-GH 1.25 mm, 6-pin.** Pinout:
  **Black = GND · Red = Power (+) · Yellow = RX · White = TX · Blue = SmartAudio** (one pin free).
  Standalone video needs **only Red + Black**. The harness plugs into the VTX — no soldering.
- **Battery: XT30** (battery female → pigtail male). Charging (3S): XT30 **and** JST-XH balance
  both into a balance charger; XT60→XT30 adapter if needed.
- **Antenna rules:** U.FL on the VTX = **~30 mating cycles, fragile** → plug it once into the
  flange pigtail and never touch it again; all swapping happens at the **SMA** (≥ 500 cycles).
  **SMA ≠ RP-SMA** (they thread together but don't connect) — check every plug pair.
  All 5.8 GHz antennas **RHCP on both ends** (mixing polarizations costs the link).

## 4 · Wiring — completely solder-free

```
Battery XT30 ── XT30-female pigtail (+) ──[Wago]── switch ──[Wago]── VTX red (+)
                XT30-female pigtail (−) ──[Wago]──────────────────── VTX black (GND)
                VTX yellow/white/blue → heat-shrink caps (unused)
Camera ── MIPI ──→ VTX          VTX U.FL ── U.FL→SMA flange pigtail ── antenna
```

1. Plug the JST-GH harness into the VTX. Take red + black (bare ends).
2. **Three Wago 221-412:** + line = pigtail(+) ↔ switch ↔ VTX red (2 Wagos);
   − line = pigtail(−) ↔ VTX black (1 Wago). Thin strand wobbly? **Fold the end double** —
   no ferrule, no crimper needed.
3. Connect antenna (U.FL → flange pigtail, once) and camera (MIPI). **Antenna on BEFORE power — always.**
4. Secure the Wago levers with a dab of RTV/hot glue (vibration) + strain relief (§ 5).

> No capacitor needed — there are no motors, the supply is clean. **Zero solder joints.**

## 5 · Strain relief (consumer-safe)

Principle: *pull on the battery cable is absorbed by the case before it reaches any connection.*

1. **Stopper hole (passive):** route the cable so the thin wire passes but the thick spot
   (XT30/heat-shrink bulge) cannot — a pull seats the bulge against the wall. Idiot-proof.
2. **Zip-tie anchor** around the cable jacket through two printed webs.
3. **Service loop** (slack loop inside).
4. **90° anti-kink boot** over the pigtail transition.

(All four are designed into the case CAD — cable channel, stopper step, zip-tie webs. `TBD-CAD-M6`)

## 6 · 🚨 Hardware killers (never skip)

1. **NEVER power the VTX without an antenna or a 50 Ω dummy load** — reflected power kills the PA instantly.
2. **Check polarity with a multimeter before first power** — the Freestyle V2 has **no reverse-polarity
   protection**. VTX red must read +11–12.6 V. Red = +, black = −.
3. **PETG/ASA case + thermal pad VTX→wall** — at 1 W the VTX reaches ~90 °C in ~2 minutes in a
   closed case on the bench. It is the hottest part in the box.
4. **U.FL ≈ 30 mating cycles and fragile** — seat it firmly, secure with a dab of hot glue,
   never unplug it for fun.
5. **The JST-XH balance plug is for charging only** — never toward the VTX.

## 7 · Power & thermal operating doctrine (BINDING — derivation: [`ENGINEERING/thermal.md`](ENGINEERING/thermal.md))

At 1 W RF the VTX dissipates **~13–14 W as heat** — on the ground, in still air, that is
**not passively removable** (no vent geometry changes that; over-temperature = a hard RF cut
by the VTX "until repowered" = picture gone until you cycle the switch). Therefore:

| phase | power | why |
|---|---|---|
| Ground / waiting / climb | **25 mW** (pit mode usually suffices) | continuously coolable (chimney vents) |
| 200 mW on the ground | **max. 10 min** (≈ 5 min at a 35 °C summer DZ) | borderline |
| **Door open / exit call** | **only now 1 W** (set via the ground station) | from exit, ram-air cools with 4–8× reserve |
| After landing | **OFF within 60 s** | hot start + still air = the second worst case (~2–4 min to cut-out, calculated) |

The 1.5 mm thermal pad VTX→side wall is mandatory: on the ground it only moves ~0.6 W, but it
doubles the effective heat capacity (buys 1–2 minutes in the power-up window) and carries
~2.5 W in freefall as a second path.

## 8 · Charging & first start

- **Charging (3S):** balance charger, XT30 **and** JST-XH both connected, ~1C, LiPo 3S mode.
  Never without balance, never on a 1S charger. LiPo bag recommended.
- **First start:** antenna on → battery in → the VTX boots in **pit mode (0 mW)** → set channel
  and power via the **ground-station (BoxPro) menu**. 1 W requires the unlock — mind the licence
  situation ([`LEGAL_DE.md`](LEGAL_DE.md)). Watch the heat; lowest usable power on the ground.

## 9 · Ground station

- **HDZero BoxPro** — 4-way diversity (2 internal patches + 2 external SMA), Mini-HDMI straight
  to the public-viewing TV.
- **TrueRC X²-AIR MK II patch, RHCP, SMA** — the range-maker; aim it at the working sky
  (nominal 13 dBic — honestly budget ~10).
- **Lumenier Double AXII 2 LR** (~4.7 dBic) — horizon omni.
- **TrueRC Matchstick Carbon Long** (~1.9 dBic) — overhead omni.
- Doctrine: **the gain belongs on the ground.** A stronger body antenna buys ~2–3 dB; the aimed
  ground antenna buys 10–14 dB. The tumbling end gets a round radiator; the still, aimable end
  gets the gain and the diversity.

## 10 · What you must measure yourself

Nothing in this project is guessed. Before printing/final assembly, work through
[`MEASURE.md`](MEASURE.md) — caliper dimensions, S11 of the encapsulated antenna, and the
thermal A/B test are all listed there with instructions.
