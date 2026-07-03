# SkyLive — Legal framework (Germany, 5.8 GHz FPV live stream)

*Condensed English edition of the project's German legal research (`RECHTSRAHMEN`, 2026-07).*

> ⚠️ **This is NOT legal advice.** It is technical project research without legal qualification.
> Labels: **[LAW]** = primary source with citation · **[PRACTICE]** = documented (partly informal)
> regulator practice · **[ASSESSMENT]** = our own reading. Before any operation above 25 mW:
> get written clarification from BNetzA (the German regulator) / DARC. If you rebuild this
> outside Germany, your own jurisdiction's rules apply — check them first.

## 1 · The three ways to operate

| | **(a) SRD general authorization** | **(b) Amateur radio (Class E)** | **(c) PMSE short-term assignment** |
|---|---|---|---|
| Who | anyone, no licence | licence holders only | applicant (event operator) |
| Frequency | 5725–5875 MHz | 5650–5850 MHz (amateur is **secondary**) | assigned by BNetzA (5.8 GHz can be requested, not guaranteed) |
| Power | **25 mW EIRP**, no exceptions | 5 W PEP (since 06/2024) | set in the assignment; > 25 mW possible, 1 W not guaranteed |
| Public-viewing demo | unproblematic | **critical** — see § 2 | unproblematic; explicitly meant for sport events |
| Procedure / cost | none / € 0 | exam + call sign | apply ≥ 15 working days ahead, from ~€ 30 |
| Verdict | **legal today — the standard path for ALL tests** | **fragile** (four open points) | **the robust path for the event demo** |

Sources [LAW]: BNetzA Vfg 91/2025 (SRD) · AFuV Annex 1 as amended 2024 (BGBl. 2024 I Nr. 175) ·
§ 55 TKG + BNetzA short-term-assignment practice.

## 2 · Why 1 W under an amateur licence stays LOCKED (the honest part)

1. **Purpose**: is an FPV video feed amateur radio at all? A documented (informal) BNetzA reply
   from 2013 read model-flight video links narrowly. Our case differs (ATV-like, no control
   link), but the narrow reading exists. [PRACTICE]
2. **"For third parties" / broadcast-like**: § 5 AFuG forbids message transfer for third
   parties; § 16(9) AFuV forbids broadcast-like programming. A live feed onto a public DZ
   screen is one-way entertainment for an unspecified audience — a realistic reading says:
   not permitted. No ruling, no official statement on this exact case. [LAW + ASSESSMENT]
3. **Encryption/obscuring clause § 16(8) AFuV (2024 wording)**: recoverability with generally
   available equipment is the yardstick — any store-bought HDZero receiver recovers the
   picture, and there is no intent to obscure. Probably defused for HDZero; officially
   unresolved. [LAW + ASSESSMENT]
4. **Bandwidth — the hard, often-missed blocker**: AFuV Annex 1, usage rule 9 caps occupied
   bandwidth at **10 MHz, or 20 MHz for television transmissions**. HDZero occupies **27 MHz**
   in standard mode and **17 MHz** in narrow mode (540p60). **Standard HDZero exceeds even the
   20 MHz TV cap** — only narrow mode could fit, and only if the feed counts as television. [LAW]

**[ASSESSMENT]** Power is covered (1 W ≤ 5 W PEP) — but points 1–2 question whether the
transmission is amateur radio at all, and point 4 blocks the standard HDZero mode technically.
Class E is an option after written clarification, not a foundation.

## 3 · The project's operating doctrine

| phase | path | configuration |
|---|---|---|
| **All testing** (bench, range, jump trials) | SRD general authorization | VTX locked to **25 mW**, 5725–5875 MHz. Legal immediately, no application. Key question to answer empirically: does 25 mW + aimed ground antenna close 4 km line-of-sight? |
| **Event demo** | **PMSE short-term assignment** | apply to BNetzA ≥ 15 working days before the event: place/date, 5.8 GHz video link, TX power, antenna characteristics, duration. From ~€ 30. |
| **1 W amateur operation** | **locked until clarified** | only after written BNetzA/DARC answers on purpose/third-parties/broadcast **and** a bandwidth solution (narrow mode 17 MHz or a cleared reading of rule 9). |

## 4 · SAR and harmonics (any path above 25 mW)

- **SAR — 1 W next to a head:** the sender sits on the helmet, centimetres from the skull.
  Reference: ICNIRP/EU limit 2 W/kg (local, 10 g average). At 25 mW uncritical [ASSESSMENT];
  at 1 W the antenna-to-head distance is the decisive quantity. The side/bottom antenna
  placement (radiating away from the head) helps but **replaces no assessment** — a SAR
  evaluation is a hard gate before real 1 W operation or giving the device to anyone else.
  No measurement exists — not overclaimed.
- **Harmonics @ 1 W:** required suppression ≥ 50 dBc → each harmonic ≤ −20 dBm absolute [LAW:
  AFuV Annex 1 B; Vfg 33/2007]. 2nd harmonic = 11.6 GHz, 3rd = 17.4 GHz → proof needs an
  ≥ 18 GHz analyzer (a tinySA Ultra tops out at 6 GHz). Practical path: band-pass filter in
  line → fundamental checked locally → harmonics spot-checked in a properly equipped lab.

## 5 · Disclaimer

Anyone reproducing this work is responsible for their own regulatory compliance. This project
publishes its legal homework so you can do yours — it does not do it for you.
