# ⚠️ Disclaimer — RF, safety, status

**SkyLive** · Copyright (c) 2026 Tom Schoen ([@SchoenTom](https://github.com/SchoenTom)) · Licensed [CC BY 4.0](LICENSE)

## Radio / regulatory

Radio transmit power is regulated. The plan of record for this project is **licence-free SRD at 25 mW EIRP** for all development and testing and a **PMSE short-term frequency assignment** (BNetzA, Germany) for event operation. Operating at 1 W under an amateur-radio licence is a legal grey zone in Germany (§5 AFuG / §16 AFuV, plus a hard bandwidth cap) — it is *not* what this project relies on; the full reasoning is in [`build/LEGAL_DE.md`](build/LEGAL_DE.md). **Anyone reproducing this work is responsible for their own regulatory compliance in their own jurisdiction.**

## Safety

This device is designed to be worn on a skydiver's helmet next to life-critical equipment. The documentation includes the safety concept (snag-free shell, screw-clamped captive antenna, tab-locked battery door, strain relief, thermal operating doctrine, SAR assessment and AAD manufacturer sign-off as hard gates before any jump) — **none of it is validated yet**. Do not jump any build of this hardware before the documented ground gates pass, a written AAD manufacturer statement exists, and the drop zone / safety officer has approved it.

## Status

Prototype-stage engineering, shared in full. Calculated values are marked as calculated; nothing carries a "measured" badge yet. The material is provided **"as is", without warranty of any kind**. This is not a validated, certified, or sellable product.
