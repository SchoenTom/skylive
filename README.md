<div align="center">

<img src="renders/hero.png" alt="SkyDive·Live — a 1-watt HDZero live-stream transmitter for skydiving, lens facing the viewer, on a dark telemetry-HUD background" width="100%">

### Real-time video from freefall — the jumper's POV, live on the screen at the drop zone.

[![status](https://img.shields.io/badge/status-prototype-orange?style=for-the-badge)](#status--roadmap)
[![license](https://img.shields.io/badge/license-CC--BY--4.0-3b82f6?style=for-the-badge)](LICENSE)
[![CAD](https://img.shields.io/badge/CAD-build123d%20%2F%20Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](#reproduce-the-cad)
[![live 3D](https://img.shields.io/badge/live-interactive%203D-22d3ee?style=for-the-badge&logo=googlechrome&logoColor=white)](https://schoentom.github.io/skydive-live/)
[![pitch deck](https://img.shields.io/badge/pitch%20deck-open-ff4081?style=for-the-badge)](decks/pitch_EN.html)

**[▶ Spin it in 3D](https://schoentom.github.io/skydive-live/)** · **[Pitch deck](decks/pitch_EN.html)** · **[The numbers](ENGINEERING.md)** · **[Build it](BUILD.md)**

</div>

---

## What if the whole drop zone could watch — live?

Today, the ground sees only **a dot in the sky**. Spectators, the waiting area, your own team — they follow the jump with the naked eye, and the footage only arrives *after* landing. The moment itself stays invisible.

**SkyDive·Live** puts the jump on the screen **as it happens**. A helmet-mounted transmitter the size of an action cam sends a digital HDZero picture from ~4 km up to a receiver at the landing zone — straight onto the big TV in the waiting area. Its own radio link, no internet, ~14 ms latency. Not a recording. **The present tense.**

```
Camera (MIPI) → 1 W VTX → U.FL → antenna(s) → ~4 km of air → ground antenna array → diversity RX → HDMI → monitor / public-viewing TV
```

| | the jumper sees | the ground sees |
|---|---|---|
| **before** | everything | a dot |
| **with SkyDive·Live** | everything | **everything — live, on the big screen** |

---

## Two generations. One idea.

Hundreds of iterations distilled into **two purpose-built designs** — a proven foundation, and a leap that solves the one moment that breaks every single-antenna link.

<div align="center">
<img src="renders/two_generations.png" alt="Two generations side by side: Gen 1 MK2 (the foundation) and Gen 2 v5 (never lose the image)" width="100%">
</div>

### ① Gen 1 — MK2 · *The Foundation*

The complete printed system, and the proof the concept holds together. **Self-thinking cooling**: a sensor reads the chip temperature and the fan runs *only when it's hot* — in freefall the 200 km/h ram-air does the work; on the ground it runs on until everything is cool. GoPro form factor, tool-free battery swap, real off-the-shelf RF parts.

### ② Gen 2 — v5 · *Never lose the image*

**A body is a shadow.** Belly-down, the antenna points cleanly at the ground. Go **head-down** and the jumper's own body slides between transmitter and ground — a single antenna tears off, right at the most spectacular moment. So Gen 2 carries **two**: a patch that looks down, a dipole up top, and an RF switch that picks the better one in real time. Both sit **flush** in the shell — screwed in, no stuck-on bump, no snag risk.

> 🛰️ **Feel it yourself** — the interactive [dual-antenna demo](https://schoentom.github.io/skydive-live/): rotate the jumper head-down, watch the single antenna drop to *"NO SIGNAL"*, then switch on the second and watch the link hold.

---

## Inside the sender

<div align="center">
<img src="renders/sender_internals.png" alt="Cutaway of the sender showing camera, VTX, heat-wall and battery, lens facing the viewer" width="62%">
</div>

Every block has its place — justified thermally and by RF. **Colour = component identity**, the same key used throughout the pitch deck:

| | part | what it does | real off-the-shelf part |
|---|---|---|---|
| 🟠 **Camera** | the eye | HD wide-angle skydive POV; lens flush through the front wall — nothing protrudes to snag | HDZero Micro V3 |
| 🟦 **VTX** | the radio heart | turns the picture into a 1 W signal, ~14 ms, reaches 4 km with margin | HDZero Freestyle V2 |
| 🟩 **Antenna** | the link | patch radiates down to the DZ; RHCP for clean reception (Gen 2 adds the up-facing dipole) | TBS 5G8 RHCP patch |
| 🟦 **Battery** | the energy | 3S LiPo in a protected, tool-free swap tray; externally charged | 3S LiPo + BMS |

---

## The numbers that matter → [`ENGINEERING.md`](ENGINEERING.md)

This is not a hobby gamble. Every critical path is calculated, and **honestly split into *calculated* vs *to-be-measured*.**

| | value | |
|---|---|---|
| 📡 **Transmit power** | +30 dBm (1 W) — well under the 5 W Class-E limit | compliant |
| 📡 **Free-space loss @ 4 km** | 119.8 dB (5.8 GHz, Friis) | ✅ derived |
| 📡 **Link margin @ 4 km** | **+9 dB** (worst-case omni TX, unfavourable attitude) | calculated |
| 📡 **Zero-margin range** | ≈ 11.6 km — so 4 km is deliberately conservative | calculated |
| 🌡 **Thermals in freefall** | ΔT **≈ 6 K** — ram-air convection carries the VTX heat | calculated |
| 🔋 **Runtime** | ~40 min theoretical / ~32 min practical | dimensioned |
| ⚖️ **Sender mass** | ~200–250 g | dimensioned |

> **The hard case (head-down)** is identified *and solved*: the body-shadow penalty → dual antenna at the sender **plus** diversity at the ground. The real proof comes with the first jump — **no overclaiming.**

---

## Build it yourself → [`BUILD.md`](BUILD.md)

<div align="center">
<img src="renders/exploded.png" alt="Exploded view of the sender" width="46%">
<img src="renders/assembly.gif" alt="Assembly animation of the sender" width="46%">
</div>

**① 3D-print** (verified watertight STLs) → **② prep components** → **③ assembly stack** (antenna → VTX flat → camera → cover) → **④ wiring & power** (MOSFET fan control, conformal coating) → **⑤ fit tests A–F**. Full step-by-step in [`BUILD.md`](BUILD.md).

---

## The other half — the ground station

<div align="center">
<img src="renders/groundstation.png" alt="Ground-station receiver: monitor, sun-hood, antenna mast" width="30%">
</div>

A monitor on a tripod catches the signal over **two antennas** (omni + directional patch) and always shows the stronger one — true **diversity**, the same approach professional systems use. Daylight-readable with a sun-hood; an external recorder grabs an instant-playback copy; HDMI runs the same picture onto the big public-viewing TV. **Two safeguards against the same dropout — the picture gets through.**

---

## Reproduce the CAD

Everything is parametric and scriptable:

- 🧊 **Interactive 3D** — [spin the model in your browser](https://schoentom.github.io/skydive-live/) (assembled ↔ exploded). Source GLBs: [`models/`](models/).
- 🛠 **Stack** — `build123d` (parametric CAD in Python) · custom build/verify pipeline · RF link-budget · thermal (convection / flat-plate) · regulatory (AFuV / Class E) · DFM for FDM printing.
- 📋 **[`BOM.md`](BOM.md)** — full bill of materials (sender, ground station, measurement gear).
- 🎞 **Pitch decks** — [EN](decks/pitch_EN.html) · [DE](decks/pitch_DE.html) (self-contained, with 3D viewer).

---

## Status & roadmap

Ambitious engineering project **in development** — not a finished product, not a closed validation.

- ✅ **Done:** CAD (watertight, 0 collisions, fastening verified), electrical compatibility on paper, every budget calculated, both generations designed and collision-checked.
- 🔜 **Next:** first print → VTX thermal measurement → S11 (antenna) measurement → test jump.
- 🎯 **Target:** first official tests, **summer 2026.**

---

## Honest note

A solo-built, prototype-stage project shared in full. Renders are from the project's own CAD; calculated values are marked as such and separated from what still has to be measured. Transmit power is regulated — operation here is framed around an amateur-radio **Class E** licence (with PMSE short-term assignment for the championship demo). Questions and collaboration welcome.

<sub>License: <a href="LICENSE">CC-BY-4.0</a> · Renders &amp; 3D: own CAD (build123d) · Made by <a href="https://github.com/SchoenTom">@SchoenTom</a></sub>
