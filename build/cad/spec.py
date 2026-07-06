"""
spec.py — SkyLive Sender: SINGLE SOURCE OF TRUTH (all dimensions in mm).

Every number here is (a) measured from an official manufacturer STEP file,
(b) sourced from a datasheet/vendor page (URL in comment), or (c) explicitly
listed in MEASURE_ME because it is not publicly sourceable and Tom must caliper it.
NOTHING is estimated. CAD, docs, and renders all import from this file → no drift.

Antenna doctrine (CRUCIAL): the donut must radiate DOWN + UP (sky+ground), NOT to the
horizon. The ground station is always below the jumper. So the omni lies HORIZONTAL,
its axis ACROSS the body (left-right) → strong lobes down/up/forward/back, nulls to the
sides. Validated by RF_ANALYSIS_DONUT.md (up/down beats horizontal by ~15-18 dB purely
by aiming) and independently by a national-team camera flyer (films from above → DZ
below/forward → the favorable geometry).
"""

# ─────────────────────────────────────────────────────────────────────────────
# 0 · GLOBAL / ENCLOSURE
# ─────────────────────────────────────────────────────────────────────────────
WALL = 3.0                 # SACROSANCT — never thinned (Tom, repeated). Exceptions below are the only ones.
WALL_BULKHEAD_RECESS = 2.8 # local counterbore so the Würth SMA bulkhead's 2.8 mm max clamp is met
RF_WINDOW_WALL = 1.5       # thin PETG radome only where an antenna radiates through the shell
MATERIAL = "ASA_preferred_PETG_prototype_ok"  # final part ASA (PETG HDT ~68-75 °C vs 60 °C car +
                                              #   90 °C VTX + helmet UV); PETG ok for fit prototypes;
                                              #   never PLA. (THERMAL + PRINT_FACTOR_REGISTER agree.)
TOL = 0.5                  # general clearance around PCBs / parts (gate basis)
# Shrink compensation moved to section 10 (PRINT & FORM): ASA +0.8% isotropic, PETG via coupon.

# Two-story architecture (RE-CONFIRMED by Tom 2026-07-02: "das Innenleben klar auf zwei
#   Stockwerke teilen"). Floor 1 (bottom) = battery. Floor 2 (top) = VTX+camera.
#
# DIVIDER — FINAL DOCTRINE (derivation: DIVIDER_STRUCTURE_SPEC.md, 2026-07-02):
#   The divider is a SEPARATE, FLAT-PRINTED drop-in TRAY resting on printed wall ledges.
#   Why: integral horizontal divider in an upright print puts PETG interlayer strength
#   (18 MPa) exactly in the load direction vs 47 MPa XY for a flat tray — and cables get
#   LAID IN instead of threaded; no connector ever passes a closed hole. The divider is a
#   bulkhead/frame: only its PERIMETER attachment is structural, the center field is
#   expendable (aircraft-frame lightening-hole principle).
DIVIDER_T = 3.0
DIVIDER_AS_TRAY = True           # flat-printed drop-in tray on wall ledges (47 vs 18 MPa in load dir)
DIVIDER_LEDGE = (3.0, 3.0)       # printed ledges ADDED to the wall (wall itself stays 3.0)
DIVIDER_TRAY_CLEAR = 0.3         # slide fit tray<->wall
DIVIDER_EDGE_BAND = 6.0          # continuous solid perimeter band = THE structure; max 3 breaks
DIVIDER_MAX_CUTOUT_PCT = 50      # center field may lose up to 50% area WITH ribs
DIVIDER_MIN_WEB = 4.0            # min residual web between cutouts
DIVIDER_RIB = (2.4, 6.0)         # 2 longitudinal ribs = spine; ribs (not plate) carry battery impact
DIVIDER_RIB_QTY = 2
DIVIDER_SCREWS = 2               # diagonal M3 hold-downs into heat-set bosses
DIVIDER_DESIGN_ACCEL_G = 10      # design factor over sourced 2-6 g opening shock
DIVIDER_DROP_LOAD_N = 250        # 1.5 m handling drop WITH foam preload (beam calc, NOT tested)
BATT_FOAM_PRELOAD = 2.0          # MANDATORY: battery must never fly free inside the bay
# Feedthrough catalog (REPLACES the old too-small FEEDTHROUGH_D=6.5 / SLOT=(4,10) —
#   an XT30 face is 11x6 and never fit through Ø6.5):
FEEDTHROUGH_XT30 = (14.0, 9.0)   # window at the door edge (XT30 face + clearance)
FEEDTHROUGH_JST_XH4 = (14.0, 8.5)
FEEDTHROUGH_JST_GH6 = (10.5, 7.0)  # reserve window (JST eGH.pdf: 8.75 x 5.7 x 4.15)
FEEDTHROUGH_D = 8.0              # Ø for standard rubber grommets (groove width 3.0 = plate t)
FEEDTHROUGH_SLOT = (7.0, 14.0)   # open keyhole grooves: cables drop in from above
FEEDTHROUGH_EDGE_BREAKS_MAX = 3  # max interruptions of the 6 mm edge band
PIGTAIL_CHANNEL = (6.0, 2.5, 2.0)  # RG178 side channel = 2 printed interior ribs; wall untouched
DIVIDER_VENT_AREA_MIN = 750.0    # mm² NET air path through divider (connector windows + grooves
                                 #   COUNT toward this; = 1.5x inlet as cable-blockage reserve,
                                 #   THERMAL_VENT_OPTIMUM.md). Sits close to the 50% cutout budget
                                 #   -> rib doctrine is not optional.
SPARE_ANT_POCKET = None          # honestly computed: 73 mm AXII does not fit (~60 mm field diagonal)
                                 #   -> spare antenna lives in the ground-station box; sender keeps
                                 #   cable slack space only
CORNER_SCREW = "M3_heatset"     # 4 corner screws fasten BOTH the top cover AND the bottom patch shell
CORNER_INSET = 4.0

# ─────────────────────────────────────────────────────────────────────────────
# 1 · VTX — HDZero Freestyle V2  (IMPORT the official STEP, do not remodel)
# ─────────────────────────────────────────────────────────────────────────────
VTX_STEP = "references/HDZero Freestyle V2 VTX.step"   # official hd-zero/hdzero-tooling
VTX_BOARD = (29.2, 30.0, 14.1)   # measured from STEP; datasheet 29x30x14, 22.3 g
VTX_MASS_G = 22.3
VTX_MOUNT_PITCH = (19.6, 19.6)   # 20x20 nominal, holes at +/-9.8
VTX_MOUNT_HOLE_D = 2.41          # M2 clearance
VTX_UFL_EDGE = "-Y"              # U.FL is on the short edge OPPOSITE the camera (Tom confirmed)
VTX_UFL_STUB_LEN = 11.4          # coax stub already in the STEP (bbox Y reaches 41.4)

# ─────────────────────────────────────────────────────────────────────────────
# 2 · CAMERA — HDZero Nano 90  (IMPORT official STEP)
# ─────────────────────────────────────────────────────────────────────────────
CAM_STEP = "references/HDZero_Nano90.stp"              # official; ships in the Freestyle V2 Kit
CAM_FRAME_STEP = "references/HDZero_Nano90_Frame_14to19.stp"  # 19x19 adapter frame (optional; +19.6 tall)
CAM_BODY = (14.0, 18.5, 19.0)    # W x depth(incl lens) x H; H=19.0 Tom gemessen 2026-07-04 (rechteckig 14x19, nicht quadratisch)
CAM_LENS_D = 12.0                # lens barrel Ø (STEP); exact thread NOT published
CAM_LENS_PROTRUDE = 13.3         # front face -> lens tip
CAM_MASS_G = 5.2
CAM_MOUNT = ("INVERTED mount (Tom 2026-07-04): collar protrudes INWARD, exterior flat, 4x M2 flat-head "
             "COUNTERSUNK from outside in the real native Nano90 13.5x17.5 pattern (corner holes).")
CAM_MOUNT_PITCH = 15.5           # DEPRECATED (old outward 2-hole scheme; 15.5 was a knife-edge vs the
                                 # window). Kept only so the paused flat variant still imports. Hochkant
                                 # now uses CAM_MOUNT_PATTERN below.
CAM_MOUNT_PATTERN = (13.5, 17.5) # real native Nano90 front holes (X x Z), verified from the official STEP;
                                 # placed as 4 CORNER holes (±6.75 X, ±8.75 Z) → clears the Ø13.5 window ≥1 mm
CAM_MOUNT_HOLE_D = 2.0           # M2 clearance shaft
CAM_MOUNT_CS_D = 3.8             # M2 flat-head Ø (DIN 965) → 90° countersink on the flat exterior (flush)
CAM_MOUNT_PILOT = 1.7            # M2 self-tap / heat-set pilot in the printed mount bosses
CAM_MOUNT_LENS_OFF = 4.0         # holes sit 4 mm behind the lens face (toward the lens datum)
# ── OFFICIAL Nano-90 mount frame, ALL values MEASURED from HDZero_Nano90_Frame_14to19.stp
#    (bounding box + cylindrical-face survey, build123d import_step). Reproduced as printed
#    housing geometry (the frame becomes part of the −Y side wall). Y = view/lens axis (thin).
CAM_FRAME_OUT = (19.0, 19.6)     # outer footprint W(X) x H(Z)   [bbox X 19.0, Z 19.6]
CAM_FRAME_DEPTH = 7.3            # depth along the lens/view axis (Y)   [bbox Y 7.3]
CAM_FRAME_WINDOW = (14.8, 14.8)  # central through-opening W(X) x H(Z) (lens/board window)
CAM_FRAME_CORNER_R = 2.5         # external corner fillet radius (r=2.5 corner cylinders)
CAM_FRAME_MOUNT_D = 3.0          # corner through-holes Ø3.0 (r=1.5 cyl, axis Y)
CAM_FRAME_MOUNT_X = 8.0          # corner-hole centre offset in X (±8.0)
CAM_FRAME_MOUNT_Z = 8.3          # corner-hole centre offset in Z (±8.3)
CAM_FRAME_SIDE_D = 2.1           # side M2 mount holes Ø2.1 (r=1.05 cyl, axis X, ±X faces)
CAM_FRAME_SIDE_Y = 2.3           # side-hole centre, +Y behind the lens-exit (front) face
# Camera sits at the FRONT; lens through the front wall. VTX U.FL faces the REAR (opposite).
# ── FLUSH recessed camera window (2026-07-04) — REPLACES the proud 19×19.6 mount-frame block
#    (CAM_FRAME_* above, no longer built into the wall; kept only as reference data). The −Y outer
#    wall stays smooth; a clean rounded-rect opening lets the lens (Ø12) see out while the board
#    (14×18) is trapped BEHIND the window shoulder. Design choices derived from the MEASURED lens Ø
#    (12) + a 0.75 mm/side clearance and the MEASURED board 14×18 — no invented part dimensions.
CAM_WINDOW = (13.5, 13.5)        # W(X) x H(Z) through-opening = lens Ø12 + 2×0.75 clearance; the
                                 #   board 14×18 overhangs it (X 0.25 / Z 2.25 shoulder) → cannot exit −Y
CAM_WINDOW_R = 2.5               # window corner radius (soft, ~matches the round lens)
CAM_WINDOW_CHAMFER = 1.2         # 45° exterior rim chamfer — snag-free "weich verrundet" lead-in
# ── REFERENZ-STYLE camera collar ("Wölbung") — GRAFTED 1:1 from Referenz-Prototyp's OWN extracted STEP (2026-07-04).
#    The parametric rebuild below (CAM_BULGE*) is SUPERSEDED: instead of re-modelling the collar we
#    IMPORT Referenz-Prototyp's real extracted bulge solid and boolean-UNION it onto the −Y wall (nothing rebuilt,
#    nothing invented). Measured facts of the STEP (build123d import + solid-classifier survey):
#    wall/attach plane Y=24.9, tip Y=31.4 → 6.5 mm proud; solid footprint 22 (X) × 14 (Z); rounded
#    corner/dome tori R≈4.2; the camera bolts to 4 Ø3 (R1.5) axis-Y frame holes whose centroid =
#    (26.25, 12.5) = the lens axis; aperture open at the wall plane. The Nano90 lens (Ø12) looks out
#    through a 13.5 window cut through the 3.0 wall BEHIND the grafted collar (collar geometry untouched).
CAM_BULGE_STEP = "references/reference_camera_bulge.step"  # Referenz-Prototyp's REAL extracted collar — grafted, not rebuilt
# legacy parametric collar params — kept only as reference data (no longer built into the wall):
CAM_BULGE = (21.5, 22.0)         # W(X) x H(Z) outer collar contour — Referenz-Prototyp 1:1 (height clamped in CAD
                                 #   so the collar stays under the top cover; width+proud+rim exact)
CAM_BULGE_PROUD = 6.4            # OUTWARD protrusion beyond the −Y wall face (Referenz-Prototyp: tip 31.4 − wall 25.0)
CAM_BULGE_R = 4.0                # rounded-rect corner radius (Referenz-Prototyp corner tori Rmaj≈4.0)
CAM_BULGE_RIM = 2.5             # front-rim roll radius = the soft "Wölbung" lip (Referenz-Prototyp rim tori Rmin≈2.0–2.2)
CAM_CRADLE_WALL = 1.6            # printed side-rail thickness that locates the board in X (slide fit)
CAM_CRADLE_LIP = 0.8             # rear snap-lip inward projection (board flexes past on insert → +Y stop)

# ─────────────────────────────────────────────────────────────────────────────
# 3 · BATTERY — Tattu 3S 850 mAh 75C, XT30  (TOM'S DECISION 2026-07-02: "vorerst bleiben
#   wir beim momentanen 850 mAh 3S Modell". Tom OWNS this pack physically.)
#   The interrupted 2026-07-01 edit had swapped in a GNB 350 2S HV — REVERTED: 2S carried a
#   documented brownout risk (7 V floor, abrupt cut) and contradicted the 3S doctrine in
#   every other doc. 3S 850 = generous headroom + whole-session runtime at our ~1.5–2 A.
# ─────────────────────────────────────────────────────────────────────────────
BATT_CELL = (60.0, 30.0, 23.0)   # Tattu 3S 850 — 60 × 30 × 23 mm, 80 g (genstattu.com product page)
BATT_MEASURED = (58.0, 30.0, 22.0)  # Tom GEMESSEN 2026-07-06 — real kleiner als Datenblatt.
                                 #   Envelope/Guides bleiben bewusst auf Datenblatt+Swell (konservativ).
BATT_MASS_G = 80.0               # vendor page; Tom owns the pack — caliper check optional
# M2-Messing-Insert — Tom GEMESSEN 2026-07-06: außen Ø3,2 × L3,0.
# Bohrung −0,4 Untermaß (wie Toms M3-Praxis Ø5→4,6), Tiefe = Insert + 2 Verdrängungsraum (wie 6→8).
INSERT_M2 = (3.2, 3.0)
INSERT_M2_HOLE_D = 2.8; INSERT_M2_HOLE_DEPTH = 5.0; INSERT_M2_CHAMFER = 0.4
BATT_LEADS_LEN = 45.0            # to XT30 (vendor page)
BATT_MAIN_CONN = "XT30"
BATT_BAL_CONN = "JST-XH-4"
# BAY ENVELOPE. 2026-07-04: Tom's directive "minimise size, keep a small buffer" supersedes the
#   earlier generous 40 W. Width tightened 40->34 (cell 30 + ~2/side; leads route UP through the
#   divider feed-throughs to the floor-2 Wagos, NOT sideways — so Y carried no cable buffer). Length
#   65 (cell 60 + 5 for XT30/slack at the door) and height 25 (cell 23 + 2 swell) kept — both justified.
#   NB: tightening W does NOT shrink the case — outer width is VTX+switch-governed (IN_Y_ELEC>IN_Y_BAY).
BATT_BAY_ENVELOPE = (65.0, 34.0, 25.0)   # internal clear volume of Floor 1 (L x W x H)
BATT_SWELL = (1.0, 1.0, 2.0)     # informational; already contained within BATT_BAY_ENVELOPE
# DOOR MECHANISM (Tom's original mechanism, unchanged): door at the CABLE end, battery slides
#   in BODY-FIRST (flat, lying), XT30 + slack live in the envelope's buffer zone at the door.
#   Battery orientation question (upright-load vs flat/side-door) is thereby RESOLVED: flat.
BATT_LAYOUT = "a_door_pocket"    # a = Tom's door mechanism (pocket now inside BATT_BAY_ENVELOPE)

# ─────────────────────────────────────────────────────────────────────────────
# 4 · SWITCH — Gebildet 12 mm latching push-button  (Amazon.de B08L484J7W)
# ─────────────────────────────────────────────────────────────────────────────
SW_HEAD_D = 14.0                 # bezel/cap Ø (listing "9/16in")
SW_PANEL_HOLE = 12.0
SW_THREAD = "M12x0.75"
SW_LEADS_LEN = 120.0             # pre-wired
SW_BUTTON_PROUD = 10.0           # latching button protrudes ~10 (generic 12mm latching drawing)
SW_BEHIND_PANEL = 27.0           # *** MEASURE_ME — datasheet fallback (Multicomp MP004451 ~27.5) ***
SW_LATCH_BODY_D = 12.5           # body Ø behind the barrel (approx from generic drawing)
# Mounts through the COVER, drops into a dedicated vertical clearance bay (its 27mm body
# must not overlap VTX/sled/battery). Breaks the battery + line (carries ~1.3 A).

# ─────────────────────────────────────────────────────────────────────────────
# 5 · SOLDER-FREE JOINS + CONNECTORS
# ─────────────────────────────────────────────────────────────────────────────
WAGO_221_412 = (13.2, 8.6, 18.8)  # W x H x L (WAGO datasheet); 3x used; grey body + 2 orange levers
WAGO_QTY = 3
XT30_MALE = (13.0, 11.0, 6.0)     # + 2 gold pins ~Ø3.5 x 5 proud (vendor-measured)
JST_XH4 = (12.3, 5.7, 7.5)        # official JST eXH.pdf, 2.5 pitch
UFL_PLUG_D = 2.0                  # Hirose U.FL, mated height 2.4, 1.13 coax, ~30 cycles
VTX_HARNESS = "JST-GH 1.25mm 6-pin: Black=GND Red=+ Yellow=RX White=TX Blue=SA (1 free)"
MIPI_LEN = 80.0                   # kit MIPI cable — KORRIGIERT 2026-07-05: real bestellt/geliefert 80 mm [ordering-log]; 120 war stale

# SMA bulkhead (Würth WR-UMRF 636208110200 mechanicals; RP-SMA identical shell)
BULKHEAD_HEX_AF = 8.0
BULKHEAD_NUT_T = 2.0
BULKHEAD_THREAD_OD = 6.35         # 1/4-36 UNS
BULKHEAD_BODY_LEN = 11.4
BULKHEAD_PANEL_HOLE = 6.5
BULKHEAD_MAX_CLAMP = 2.8          # => WALL_BULKHEAD_RECESS
# CONNECTOR GENDERS — resolved 2026-07-02 from Tom's real order log (~/Downloads/
#   agent-skylive-ordering.txt): he ordered BOTH pigtail genders, deliberately:
#   - U.FL->SMA pigtail  -> for the omnis / wall bulkhead (TBS Unify Pro 5G8 SMA pigtail)
#   - U.FL->RP-SMA pigtail -> for the TBS 5G8 patch, which is RP-SMA
#   Shells are mechanically identical (only pin gender differs) -> zero CAD impact.
#   VERIFY_HARDWARE: cross-check connectors on unpacking (RP-SMA vs SMA mix up easily).
CONNECTOR_STD = "SMA"            # omni feed standard (wall bulkhead side)
PATCH_CONN = "RP-SMA"            # TBS 5G8 patch is RP-SMA (order log); uses its own pigtail
PIGTAIL = ("U.FL->SMA flange", "RG178 Ø1.8", 60.0)  # fixed in the wall; swap antenna at SMA
PIGTAIL_PATCH = ("U.FL->RP-SMA", "RG178 Ø1.8", 60.0)  # for Variant B (patch)

# ─────────────────────────────────────────────────────────────────────────────
# 6 · ANTENNAS — doctrine + the three swappable variants
# ─────────────────────────────────────────────────────────────────────────────
DONUT_AXIS = "across_body_horizontal"  # axis left-right => donut radiates DOWN+UP+fwd+back, nulls sides

# PRIMARY VARIANT — CAPTIVE WALL OMNI (TOM'S DECISION 2026-07-02, verbatim intent):
#   "Die Omni soll fest in der Gehäusewand verstaut bzw. befestigt sein; leicht rausschauen
#   ist ok, vielleicht sogar ganz — aber volle Exposition heißt vermutlich zu viel Windlast."
#   This MERGES the former Version A (fully external) and Version A2 (fully internal nose)
#   into one variant: AXII laid horizontal (up/down donut, doctrine above), captured
#   form-fit in a wall pocket/nose, at most slightly proud. Wind-load math + exact capsule
#   geometry: OMNI_CAPTIVE_SPEC.md (params below marked PENDING until that lands).
OMNI = "Lumenier AXII 2"          # n-factory set; Tom owns it
OMNI_TOTAL_LEN = 73.0             # incl RG402 45mm cable
OMNI_HEAD_D = 17.5
OMNI_GAIN_DBIC = 2.2
OMNI_CONN = "SMA"
OMNI_CABLE = "RG402 semi-rigid 45mm"
OMNI_MOUNT = "captured IN the wall, LAID HORIZONTAL (axis across body) -> up/down donut"
# CAPSULE DESIGN — resolved 2026-07-02 (derivation + wind-load math: OMNI_CAPTIVE_SPEC.md):
OMNI_EXPOSURE = "fully_encapsulated"  # static wind load survives belly (SF 1.3-2.8), speed is
                                      #   marginal-to-plastic (SF 0.7-1.5); the real killers are
                                      #   ~630 Hz vortex shedding at the SMA crimp, gusts/burble
                                      #   x1.5-2, line-strike + snag. 1.5 mm radome costs ~0 dB
                                      #   -> a viewing window buys nothing. Puck 100% enclosed.
OMNI_MASS_G = 7.8                # product page
OMNI_CABLE_OD = 3.58             # RG402 datasheet
OMNI_CABLE_MIN_BEND_R = 6.35     # RG402 "repeated" minimum (datasheet)
OMNI_FORM_BEND_R = 8.0           # ONE single 90° formed bend (printed bending jig) — without it
                                 #   the 73 mm AXII fits in no direction; bend doubles as SMA
                                 #   anti-rotation lock
OMNI_CAPSULE_POS = "floor2_sidewall_top_band_opposite_thermal_pad"
                                 # axis across body (doctrine auto-satisfied); >=45 mm off the head
                                 #   centerline (+4-5 dB side-offset relief, RF_ANALYSIS_DONUT);
                                 #   down-lobe clears battery/divider. Rejected: lid zone (+22 mm
                                 #   height), fully interior (down-lobe through LiPo = fatal),
                                 #   front/rear (camera / MOUNT2).
OMNI_WALL_OPENING_D = 19.0
OMNI_CAPSULE_SINK = 10.0         # root sink-in -> nose only ~18 proud, total width ~64
OMNI_CAPSULE_PROUD = 18.0        # CALCULATED — finalize after MEASURE (AXII head length)
OMNI_AIR_GAP = 2.5               # radial element<->PETG gap (rule of thumb; NanoVNA verify is
                                 #   MANDATORY; AXII bandwidth 5.3-6.2 GHz = sourced detune reserve)
OMNI_RADOME_T = RF_WINDOW_WALL   # 1.5 cylindrical 360° ONLY in the element band (donut radiates
                                 #   radially all around); root zone + dome (= pattern null) full 3.0
OMNI_GRIP = "TPU pads at axis ends only (pattern nulls); radial air gap at the lobes"
OMNI_CAP_SCREWS = "2x M3 nylon"  # RF-neutral fasteners at the capsule cap
OMNI_WITNESS_HOLE_D = 2.5        # sight hole on orange TPU tip pad: orange = antenna present
OMNI_TOPOLOGY = "T1_internal_jack"  # AXII SMA mates the pigtail flange jack on an interior rib.
                                 #   T2 (wall bulkhead) is geometrically impossible with a captive
                                 #   puck (45 mm cable + puck would sit fully outside). Swap without
                                 #   soldering, U.FL untouched: lid off -> SMA loose -> cap off.
KEEPOUT_METAL = 13.0             # λ/4 @5.8 GHz metal-free zone around the element band
                                 #   (identical to VENT_ANTENNA_KEEPOUT — same physics)

# Version B — underside patch = the BOTTOM SHELL, which ALSO carries the primary GoPro mount
PATCH = "TBS 5G8 RHCP"
PATCH_PCB = (35.0, 35.0, 3.0)     # 35x35 sourced; thickness *** MEASURE_ME ***
PATCH_MAX_WITH_CONN = 15.0        # Tom: patch + connector <= 15 mm
PATCH_GAIN_DBI = 5.0
PATCH_BEAM_DEG = 110
# Architecture (Tom): MOUNT 1 = the UNDERSIDE of the sender = the patch module + primary GoPro
# interface in ONE. The patch is connected through a HOLE in the underside and then FULLY
# COVERED / concealed by the bottom shell (Schale) — nothing exposed. It radiates straight DOWN
# through the thin PETG shell (+ around it; PETG is RF-transparent). Screws on via the 4 corner
# screws. MOUNT 2 (rear) is a separate, optional chin mount.
PATCH_FACES = "ground"            # patch on the underside radiates down through the covering shell
PATCH_SHELL_CAVITY = 15.0         # Tom (2026-07): the bottom shell is a HOLLOW CAP with ~15 mm internal depth
                                  # housing the FULL patch + SMA connector, ENVELOPING it like a protective
                                  # lens-cap (small RF standoff, NOT touching the patch face); radome =
                                  # RF_WINDOW_WALL only on the outer down-face. (Previous build wrongly used a
                                  # ~2.5 mm sump for just the bare 3 mm PCB — that is the bug he spotted.)

# ─────────────────────────────────────────────────────────────────────────────
# 7 · MOUNTS — GoPro standard (sourced) + chin mount
# ─────────────────────────────────────────────────────────────────────────────
GOPRO_FINGER_T = 3.0             # Tom 2026-07-06 FINAL: „mach die GoPro-Zähne 3 mm" (Fit-Print: 2,8 zu dünn/locker);
                                 # a 3.2 prong is too thick. 2.7 nominal prints ≈2.9 → fits the 3.1 slot
                                 # snug, not jamming. Confirm on the physical mate (→2.8 if it rattles).
GOPRO_GAP = 3.3                  # Tom 2026-07-04: the gap between OUR prongs = the GoPro cavity (3.3) that
                                 # GoPro's own ~3.2 mating prong fills as the counterpart. (was 3.0.)
GOPRO_HOLE_D = 5.0               # caliper 5.09 (NOT 4mm)
GOPRO_2PRONG = (15.0, 15.5, 18.0)   # female/socket footprint (bbox ref; prong LENGTH now GOPRO_PRONG_LEN)
GOPRO_3PRONG = (26.0, 15.0, 18.0)   # male/plug footprint
GOPRO_PIVOT_FROM_BASE = 10.0        # Tom 2026-07-04: pivot-hole centre 9-11 mm above the sender base (->10)
GOPRO_PRONG_LEN = 14.5              # Tom 2026-07-04: GoPro-standard finger length (tip 4.5 mm below the pivot hole)
GOPRO_SCREW = "M5x0.8, 18-20mm"
MOUNT1 = "UNDERSIDE — carries the patch module + primary GoPro interface (Version B, patch down)"
MOUNT2 = "REAR — optional Cookie-G3-style chin mount, FORWARD-facing (sight line)"
CHIN_MOUNT = "Cookie G3 static, terminates in GoPro 2-prong, forward-facing angle"
CHIN_ANGLE_DEG = None            # *** MEASURE_ME *** forward/sight-line; good for normal belly (head cranes back), less for 4-way cam
CHIN_ARM_LEN = None              # *** MEASURE_ME ***
# RF: Tom's G3 chin bar is PLASTIC (RF-transparent, NOT carbon) and the anchored screws lie
# beside the patch = negligible mini-reflectors -> no meaningful RF penalty. (Carbon G3 variants
# would reflect ~50 dB; note that for other users' helmets.) Confirm with VNA anyway.
CHIN_RF = "G3 bar plastic = RF-transparent; anchored screws negligible; VNA-confirm"

# ─────────────────────────────────────────────────────────────────────────────
# 8 · GROUND STATION (for docs/renders, not the sender CAD)
# ─────────────────────────────────────────────────────────────────────────────
GROUND = {
    "rx": "HDZero BoxPro (4-way diversity, Mini-HDMI out)",
    "patch": ("TrueRC X2-AIR MK II", 10, "dBic real/de-rated (nominal 13)", (72, 34, 22)),
    "omni_horizon": ("Lumenier Double AXII 2 LR", 4.7, "dBic", (130, 17.5)),
    "omni_overhead": ("TrueRC Matchstick Carbon Long", 1.9, "dBic", (125, 12.7)),
    "doctrine": "the gain and the diversity live on the ground",
}

# ─────────────────────────────────────────────────────────────────────────────
# 9 · THERMAL / VENTS — passive two-regime design (derivation: THERMAL_VENT_OPTIMUM.md)
#   Honest headline: 1 W on the ground is passively UNSOLVABLE steady-state (~13-14 W heat,
#   chimney Δp ≈ 0.056 Pa vs ram-air ~1500 Pa in freefall). The same slots make 25 mW
#   ground-continuous / 200 mW 10-min-safe (chimney) AND deliver 4-8x the freefall need (ram).
# ─────────────────────────────────────────────────────────────────────────────
VENT_SLOT_W = 2.5                 # snag-free + support-free printable
VENT_SLOT_L = 14.0                # vertical (print Z) -> no bridging
VENT_RIB_W = 3.0                  # web between slots = wall thickness -> wall stays robust
VENT_LOUVER_DEG = 45.0            # louvered down-and-out: dew shield + support-free
VENT_INLET_ZONE = "floor1_bottom_band_sides_and_rear"  # max chimney stack; battery sits in the
                                  #   fresh-air stream; lowest point doubles as dew drainage
VENT_INLET_AREA_MIN = 500.0       # mm² (~15 slots)
VENT_OUTLET_ZONE = "top_band_under_lid_lip_sides_and_rear"  # lid lip = rain shield
VENT_OUTLET_AREA_MIN = 600.0      # ~1.2x inlet: outlet must never throttle (series orifices;
                                  #   warm outlet air ~10% more voluminous)
VENT_STACK_H_MIN = 55.0           # chimney Δp ∝ height
VENT_ANTENNA_KEEPOUT = 13.0       # = KEEPOUT_METAL; vents themselves are RF-transparent (air),
                                  #   only the omni capsule stays opening-free (water/dirt)
VENT_FACADES = 3                  # sides + rear -> windward/leeward gradient in every pose
VENT_NACA = None                  # quantified + rejected: slots already give >=4x need @55 m/s;
                                  #   NACA adds snag/water/print cost for ~2x more recovery
THERMAL_PAD_FACE = "vtx_big_face_to_sidewall_opposite_omni"
THERMAL_PAD_SIZE = (29.2, 30.0)   # full VTX alu face = 876 mm²
THERMAL_PAD_T = 1.5               # bridges TOL 0.5 + print scatter
THERMAL_PAD_K_MIN = 3.0           # W/mK; >6 buys nothing (the 3 mm wall at ~17 K/W is the bottleneck).
                                  #   Ground: only ~0.6 W BUT doubles effective heat capacity
                                  #   (= 1-2 extra minutes in the power-on window); freefall ~2.5 W.
# Operating doctrine (refined; the docs never said "climb = off", they said "on <=10 min before exit"):
OPS_GROUND_POWER = "25mW"         # waiting/climb: pit-mode power
OPS_200MW_GROUND_MAX_MIN = 10     # 200 mW ground limit
OPS_1W_TRIGGER = "door_open"      # full power only at door-open (set via ground station)
OPS_OFF_AFTER_LANDING_S = 60      # hot start + still air = second worst case; VTX overtemp = HARD
                                  #   RF cut ("until armed or repowered") = mission kill, ~2-4 min
                                  #   at 1 W ground from cold (calc, consistent with BAUANLEITUNG)

# ─────────────────────────────────────────────────────────────────────────────
# 10 · PRINT & FORM — GoPro-real final case (derivation: PRINT_FACTOR_REGISTER.md, 85 factors)
#   All radii are DESIGN DECISIONS with the GoPro Hero as form reference (NOT measured GoPro values).
# ─────────────────────────────────────────────────────────────────────────────
GOPRO_REF = (71.8, 50.8, 33.6)    # official Hero-12 size — form reference only
FILLET_CORNER_V = 9.0             # vertical case corners, outside
FILLET_CORNER_V_IN = 6.0          # MANDATORY = outside − WALL, else the corner diagonal silently
                                  #   thins below the sacrosanct 3.0
FILLET_EDGE_H = 3.0               # horizontal edges (top/bottom rims)
FILLET_SEAM = 1.0                 # at the lid seam
FILLET_FINGER_ROOT = 1.5          # GoPro finger root — fights layer-line fracture
LENS_BEZEL_OD = 20.0              # raised GoPro-style lens ring…
LENS_BEZEL_PROUD = 2.0            # …lens tip max +1.5 above the ring = lay-down protection
LOGO_DEBOSS_DEPTH = 0.5
LOGO_STROKE_MIN = 0.8
FUZZY_SKIN = (0.3, 0.4)           # thickness/point distance; NEVER on mating faces or radome
TOL_PRESS = 0.1; TOL_SLIDE = 0.3; TOL_LOOSE = 0.5
TOL_HOLE_V = 0.2                  # vertical-axis holes print undersized -> compensate
TOL_HOLE_H = 0.3                  # horizontal-axis holes additionally get a teardrop
HOLE_SWITCH = 12.3                # M12x0.75: NO printed thread (0.46 mm depth unresolvable with
                                  #   0.4 nozzle) -> through-hole + switch's own nut + star washer
HOLE_LENS = 12.6
HOLE_BULKHEAD = 6.7               # for the flange jack (interior rib, T1 topology)
HOLE_CORNER_M3 = 3.7
LID_LIP = (2.0, 4.0, 0.2)         # lip ON the cover (t, h, clearance) — a groove IN the body
                                  #   would halve the 3.0 wall
INSERT_M3_HOLE_D = 4.0; INSERT_M3_HOLE_DEPTH = 7.0; INSERT_M3_BOSS_D = 9.0; INSERT_M3_CHAMFER = 0.5
PRINT_NOZZLE = 0.4
PRINT_EW = 0.5                    # extrusion width: 6 x 0.5 = exactly 3.0 (at 0.45 the slicer
                                  #   stuffs a gap-fill worm into every wall)
PRINT_PERIMETERS = 6
PRINT_LAYER = 0.2
PRINT_ELEPHANT_CHAMFER = 0.5      # 0.5x45° design chamfer on ALL plate edges + slicer comp 0.2
PRINT_OVERHANG_MAX_DEG = 45
PRINT_BRIDGE_MAX = 8.0
PRINT_SHRINK_ASA = 1.008          # isotropic +0.8% — ASA only; NEVER also scale in the slicer
PRINT_SHRINK_PETG = 1.000         # calibrate via 100 mm coupon
PRINT_CHORD_TOL = 0.02            # STL export chord tolerance
PRINT_ORIENT = {"body": "opening_up", "cover": "outer_face_down",
                "battery_door": "outer_face_down", "bottom_shell": "on_rear_side"}
                                  # bottom_shell on its rear side => layers run ALONG the GoPro
                                  #   fingers (opening shock would snap across-layer fingers)
WEEP_HOLE_D = 1.5                 # condensation drains at the lowest point of both floors + patch cavity
SWITCH_WELL_D = 26.0              # thumb well; latching button sits flush = snag-safe
LIGHTPIPE_D = 3.2                 # VTX status LED — position from the VTX STEP, never guessed

# ─────────────────────────────────────────────────────────────────────────────
# 11 · VERIFICATION GATES (asserted on every CAD build — fail loudly)
# ─────────────────────────────────────────────────────────────────────────────
GATE_MIN_CLEARANCE = 0.5     # min gap between any two interior parts (mm); <0 = interference = FAIL
GATE_WATERTIGHT = True       # every printed part must be a single watertight solid
GATE_WALL_MIN = WALL         # no wall < 3.0 except the listed RF windows + bulkhead recess
GATE_ALLOWED_PROTRUSIONS = ["camera_lens", "switch_button", "omni_capsule", "lens_bezel", "gopro_fingers",
                            "camera_bulge"]  # Referenz-style OUTWARD camera collar (6.4 mm proud, −Y wall)
                             # omni_capsule REPLACES omni_puck + sma_bulkhead (T1: jack moved inside)
GATE_VENT_AREAS = True       # assert VENT_INLET/OUTLET/DIVIDER area minimums are met
GATE_OMNI_CAPSULE_FIT = True # AXII envelope + form bend R8 + air gap inside capsule; cap removable

# ─────────────────────────────────────────────────────────────────────────────
# MEASURE_ME — the ONLY unsourced values; do NOT invent, Tom calipers these
# ─────────────────────────────────────────────────────────────────────────────
MEASURE_ME = {
    "SW_BEHIND_PANEL": "switch total depth behind the panel (fallback 27)",
    "PATCH_thickness_and_overall": "TBS 5G8 bare thickness + overall-with-connector (fallback 3 / <=15)",
    "CHIN_ANGLE_DEG": "Cookie G3 static chin-mount built-in tilt",
    "CHIN_ARM_LEN": "chin-mount arm/standoff length",
    "GOPRO_prong_tip_radius_and_pivot_offset": "from a physical GoPro mount",
    "on_helmet_patch_detune": "VNA S11 on the actual G3 with the carbon bar",
    # added 2026-07-02 by the four design analyses:
    "AXII_head_length": "puck head alone, without cable (fallback 22.5) -> finalizes OMNI_CAPSULE_PROUD",
    "SMA_male_len_and_AF": "AXII SMA male length + wrench flats",
    "PIGTAIL_jack_dims": "U.FL->SMA flange jack: flange size + hole pattern (for the interior rib)",
    "XT30_FEMALE_envelope": "mated XT30 pair envelope (feedthrough window check)",
    "MIPI_cable_width": "kit MIPI flat cable width (nowhere published)",
    "BULKHEAD_flat": "does the flange jack have a D-flat? (anti-rotation feature choice)",
    "VTX_LED_position": "status LED xyz from the VTX STEP (light pipe placement)",
}
# Resolved since the original list: OMNI_cable_OD = 3.58 (RG402 datasheet, section 6).
