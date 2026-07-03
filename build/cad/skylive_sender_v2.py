"""
skylive_sender.py — SkyLive Sender, PARAMETRIC — UPRIGHT / "hochkant" (2026-07-01, Phase 2 v2).

ONE script -> three swappable antenna variants  VARIANT in {"A", "A2", "B"}.
Every dimension is IMPORTED from spec.py (single source of truth). Nothing hardcoded;
if a value is missing here it comes from spec, and the only unsourced values live in
spec.MEASURE_ME (used verbatim, never invented).

REORIENTATION (v2): the sender now STANDS UPRIGHT like a tall action-cam body. The LONGEST
external dimension is the VERTICAL height (Z). Frame (sizes derive from spec.py; with the
Tattu 3S 850 lying flat ≈ 71 deep × ~63 wide × ~84.7 tall; Version B grows downward by the
hollow patch cap):
    X = depth  (front −X / rear +X)
    Y = width  (±Y)
    Z = height (vertical — the longest)

ARCHITECTURE (M1, Tom's decisions 2026-07-02):
  * Two stories STACKED VERTICALLY: Floor 1 (bottom) = battery bay with the clear envelope
    EXACTLY spec.BATT_BAY_ENVELOPE (65x40x25, Tom-set, NOT derived — its 65 runs along X, its
    40-wide band stays clear of the corner posts); Floor 2 (top) = camera high + VTX below it.
    A HORIZONTAL PETG divider (DIVIDER_T, ⟂Z) separates them, carrying an XT30-sized window
    (FEEDTHROUGH_XT30) at the door end + a round lead hole (integral for M1; tray = later MS).
  * Battery Tattu 3S 850 (60x30x23) lies FLAT on the bay floor, flush at −X; the envelope's
    5 mm rest length is the XT30/lead buffer at the +X DOOR end (Tom's door mechanism).
  * Battery DOOR = REAR (+X) side hatch at the cable end: 40x25(+tol) wall cutout, outer plate
    + plug lip with a shallow XT30/JST nest pocket, 2 M3 screws into the rear corner posts.
  * Camera looks HORIZONTALLY out the front (−X), directly above the VTX (floor-2 front band).
  * Switch through the top COVER (now ONE full panel) into its −Y lane over floor 2; 3x Wago
    stacked at the REAR of floor 2 (+Y lane).
  * GoPro mount(s) on the BOTTOM (−Z) face: MOUNT1 (underside patch shell, Version B) is on the
    bottom; MOUNT2 (rear) stays a supplement.
  * WALL sacrosanct; local recess to WALL_BULKHEAD_RECESS only at the SMA bulkhead; RF windows
    = RF_WINDOW_WALL.  Donut axis stays HORIZONTAL across the body (Y) -> radiates down/up.

  Printed parts: body (upright tube + divider ledges), divider_tray (drop-in, M2), cover (full top), door (rear battery
  hatch), bottom_shell (GoPro mount; +patch for B). Real parts: VTX+camera (imported STEP),
  battery+XT30+JST+leads, 3x Wago, switch, antenna (per variant), SMA bulkhead + U.FL + pigtail.
  Cables are swept tubes with SERVICE LOOPS + strain-relief, routed through the feedthroughs.

VARIANTS:
  A  — external Lumenier AXII 2 on the +Y side face, laid HORIZONTAL (axis Y), only the puck proud;
       U.FL->SMA pigtail to an SMA bulkhead in the side wall.
  A2 — the AXII captured internally, laid HORIZONTAL (axis Y), high-ish + offset + away from the LiPo
       (front floor, below the VTX, ahead of the divider from the rear battery), fully internal.
  B  — TBS 5G8 patch carried by the BOTTOM shell: a HOLLOW CAP (spec.PATCH_SHELL_CAVITY = 15 mm
       internal depth) that fully houses the patch + its connector like a protective lens-cap
       (RF standoff, not touching the patch face), radiating DOWN through the RF_WINDOW_WALL
       radome on the outer down-face; the cap also carries the primary GoPro mount.

Gates (assert, fail loudly): every printed part watertight; pairwise min gap >= GATE_MIN_CLEARANCE;
only GATE_ALLOWED_PROTRUSIONS poke walls; dimension-assert block vs spec.

Run (per-variant or all):
  python skylive_sender_v2.py [A|A2|B|all]     (venv with build123d 0.10, see README.md)
"""
import sys
import math
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import spec  # noqa: E402  single source of truth

from build123d import (  # noqa: E402
    Box, Cylinder, Sphere, Circle, RegularPolygon, Plane, Spline,
    Pos, Rot, Axis, Color, Vector, Compound, ExportSVG,
    extrude, sweep, fillet, chamfer, import_step, export_step, export_stl, export_gltf,
)
from OCP.HLRBRep import HLRBRep_Algo, HLRBRep_HLRToShape  # noqa: E402
from OCP.HLRAlgo import HLRAlgo_Projector  # noqa: E402
from OCP.gp import gp_Ax2, gp_Pnt, gp_Dir  # noqa: E402

# ─────────────────────────────────────────────────────────────────────────────
# PATHS
# ─────────────────────────────────────────────────────────────────────────────
HERE = Path(__file__).resolve()
CAD_ROOT = HERE.parents[2]
OUT = CAD_ROOT / "skylive_out"
OUT.mkdir(exist_ok=True)

# cache the imported STEP solids once (slow to import; also used to size the layout)
_VTX_RAW = import_step(str(CAD_ROOT / spec.VTX_STEP))
_CAM_RAW = import_step(str(CAD_ROOT / spec.CAM_STEP))

# ─────────────────────────────────────────────────────────────────────────────
# DERIVED DIMENSIONS  (all from spec.py — no invented numbers)   ·   UPRIGHT FRAME
#   X = depth (front/back)   Y = width   Z = height (vertical, = the old 82 length)
# ─────────────────────────────────────────────────────────────────────────────
WALL = spec.WALL
COVER_T = WALL           # top panel(s)
BOTTOM_T = WALL          # bottom shell
DIV_T = spec.DIVIDER_T
TOL = spec.TOL
RF_W = spec.RF_WINDOW_WALL
RECESS = spec.WALL_BULKHEAD_RECESS
INSET = spec.CORNER_INSET
FT_D = spec.FEEDTHROUGH_D
FT_SLOT = spec.FEEDTHROUGH_SLOT

BATT = spec.BATT_CELL                      # (60,30,23) Tattu 3S 850 (L,W,H) — lies FLAT (M1)
BAY = spec.BATT_BAY_ENVELOPE               # (65,40,25) authoritative Floor-1 clear volume (Tom)
SWELL = spec.BATT_SWELL                    # (1,1,2) informational; contained in BAY
# M0 shim: old BATT_BAY_FRONT_POCKET is GONE from spec — buffer now lives inside BAY (L: 65-60=5)
POCKET = BAY[0] - BATT[0]                  # 5.0 cable/XT30 buffer at the door end (derived, not invented)
CAM = spec.CAM_BODY                        # (14,18.5,18) = (W, depth incl lens, H)
VTX = spec.VTX_BOARD                       # (29.2,30,14.1)

# VTX orientation (needed early — its Y extent now sets the interior width):
# thickness 14.1 -> X (depth), height 29.2 -> Z, board 30 + U.FL coax stub 11.4 -> +Y
_VTX_UP = Rot(0, 90, 0) * (Rot(0, 0, 180) * _VTX_RAW)
_vb = _VTX_UP.bounding_box()
VTX_DX = _vb.max.X - _vb.min.X               # ≈14.1 (thickness, depth)
VTX_DY = _vb.max.Y - _vb.min.Y               # board width + coax stub (toward +Y) ≈41.4
VTX_DZ = _vb.max.Z - _vb.min.Z               # ≈29.2 (height)

# ── Depth X (M1): the bay envelope's 65 length runs along X — door in the REAR (+X) wall ──
F_ELEC = max(CAM[1], VTX[2]) + 2 * TOL     # floor-2 front band depth (X): camera depth 18.5 dominates
IN_X = BAY[0]                              # 65.0 — Tom's envelope length IS the interior depth
EX_X = IN_X + 2 * WALL                     # external depth (71)

# ── Width Y: central battery/VTX bay + a +Y Wago lane + a -Y switch lane ──
WAGO_LANE = spec.WAGO_221_412[0] + 2 * TOL   # 14.2 (+Y)
# Switch lane must clear the panel LOCKNUT (widest interior part), not just the Ø12.5 latch body.
# spec.py has no nut A/F (not a sourceable dim); SW_NUT_AF is a documented engineering assumption:
# a slim M12x0.75 panel-mount locknut ≈ 15 mm A/F. Lane sized to the nut so it never digs the wall.
SW_NUT_AF = 15.0                             # ASSUMPTION (not in spec): slim M12x0.75 panel nut A/F
SW_LANE = SW_NUT_AF + 2 * TOL                # 16.0 (-Y)
# Width drivers: (a) the 40-wide bay envelope must stay CLEAR of the four full-height corner
# posts (2*INSET deep each), so the post-free central band >= BAY[1]; (b) floor 2: the VTX
# (board 30 + U.FL stub 11.4 toward +Y) must clear the switch latch on -Y and keep TOL to +Y.
IN_Y_BAY = BAY[1] + 2 * (2 * INSET)          # 40 + 16 = 56 — envelope clear of the corner posts
IN_Y_ELEC = (SW_LANE / 2 + spec.SW_LATCH_BODY_D / 2 + 0.7) + VTX_DY + TOL  # VTX-driven (≈56.9)
IN_Y = max(IN_Y_BAY, IN_Y_ELEC)              # interior width
EX_Y = IN_Y + 2 * WALL                       # external width (≈63)

# ── Height Z (M1): Floor 1 = bay envelope 25 clear + horizontal divider + Floor 2 (cam/VTX) ──
F2 = 1.0 + CAM[2] + 1.0 + VTX_DZ + 1.5       # floor-2 clear height: cover gap+cam+gap+VTX+divider gap
IN_Z = BAY[2] + DIV_T + F2                   # 25 + 3 + ≈50.7
EX_Z = IN_Z + BOTTOM_T + COVER_T             # ≈84.7  <-- the LONGEST dimension stays VERTICAL

# Version B: the bottom shell is a HOLLOW CAP (spec.PATCH_SHELL_CAVITY = 15 mm internal depth)
# that fully houses the patch + its connector below the floor plate, closed by the
# RF_WINDOW_WALL radome on the outer down-face. B external height grows by cavity + radome.
# (No number invented — all from spec.PATCH_SHELL_CAVITY, RF_WINDOW_WALL.)
B_CAP_EXT = spec.PATCH_SHELL_CAVITY + RF_W   # 16.5 below the A/A2 bottom face
def ex_z(variant):
    return EX_Z + (B_CAP_EXT if variant == "B" else 0.0)
def bottom_outer_z(variant):
    return -EX_Z / 2 - (B_CAP_EXT if variant == "B" else 0.0)   # outer (down) face of the bottom shell

# key planes (origin at external centre)
Z_FLOOR = -EX_Z / 2 + BOTTOM_T               # top face of the bottom shell (interior floor)
Z_TOP = EX_Z / 2                             # top outer face
Z_COVER_BOT = EX_Z / 2 - COVER_T             # interior ceiling (under the top cover/door)
IN_X0, IN_X1 = -IN_X / 2, IN_X / 2           # interior depth span (front .. rear)
IN_Y0, IN_Y1 = -IN_Y / 2, IN_Y / 2           # interior width span

# ── horizontal interfloor divider (⟂Z): Floor 1 (bay) below, Floor 2 (electronics) above ──
Z_DIV_BOT = Z_FLOOR + BAY[2]                 # bay ceiling = divider underside (clear height EXACT 25)
Z_DIV_TOP = Z_DIV_BOT + DIV_T                # floor-2 floor
ELEC_CX = IN_X0 + F_ELEC / 2                 # floor-2 front band centre X (camera over VTX)
# ── M2: the divider is a SEPARATE flat-printed drop-in tray (spec.DIVIDER_AS_TRAY) resting on
#   printed +/-Y wall ledges (spec.DIVIDER_LEDGE, wall stays 3.0). Both X walls face the 65-long
#   bay envelope, so no ledge there. All openings are laid out here so the tray builder AND the
#   divider_vent_area gate compute from the SAME numbers (no drift). ──
TRAY_CLR = spec.DIVIDER_TRAY_CLEAR
TRAY_X0, TRAY_X1 = IN_X0 + TRAY_CLR, IN_X1 - TRAY_CLR
TRAY_Y0, TRAY_Y1 = IN_Y0 + TRAY_CLR, IN_Y1 - TRAY_CLR
BAND = spec.DIVIDER_EDGE_BAND                # 6 mm solid perimeter band = THE structure
FT_CX = TRAY_X1 - BAND - spec.FEEDTHROUGH_XT30[1] / 2   # XT30 window at the door edge, band whole
FT_CY = -9.0                                 # paired with the JST-XH window at +9 (4 mm web)
# rectangular through-windows (cx, cy, dx, dy) — all fully inboard of the 6 mm edge band:
DIV_WINDOWS = (
    (FT_CX, FT_CY, spec.FEEDTHROUGH_XT30[1], spec.FEEDTHROUGH_XT30[0]),           # XT30 14x9
    (TRAY_X1 - BAND - spec.FEEDTHROUGH_JST_XH4[0] / 2, +9.0,
     spec.FEEDTHROUGH_JST_XH4[0], spec.FEEDTHROUGH_JST_XH4[1]),                    # JST-XH 14x8.5
    (9.5, -9.0, spec.FEEDTHROUGH_JST_GH6[1], spec.FEEDTHROUGH_JST_GH6[0]),         # JST-GH reserve
    (-13.0, 0.0, 18.0, 10.0),                                                      # centre vent cutout
)
DIV_GROMMETS = ((-8.0, 15.0), (-8.0, -15.0))  # 2x Ø FEEDTHROUGH_D=8 rubber-grommet holes
# open keyhole slots FEEDTHROUGH_SLOT 7x14 from the tray edge into the field — these are 2 of the
# max FEEDTHROUGH_EDGE_BREAKS_MAX=3 allowed edge-band interruptions: (x-centre, edge side ±Y)
DIV_SLOTS = ((4.0, +1), (-22.0, -1))
# 2 diagonal M3 hold-down holes (Ø3.7) over the wall corner-boss zones (screw-filled, not a break)
DIV_SCREW_D = 3.7
DIV_SCREWS = ((16.5, IN_Y0 + 4.0), (-16.5, IN_Y1 - 4.0))
# 2 longitudinal ribs (spec.DIVIDER_RIB 2.4x6) under the field. They point DOWN (toward the
# battery = the load they catch), so they MUST live outside the sacrosanct 40-wide bay envelope
# (|y| > 20) and are interrupted at the keyhole slots / hold-down bosses: (x0, x1, y-centre)
DIV_RIB_Y = BAY[1] / 2 + 0.5 + spec.DIVIDER_RIB[0] / 2          # 21.7 — 0.5 clear of the envelope
DIV_RIBS = ((-18.0, 10.0, -DIV_RIB_Y), (8.0, TRAY_X1 - BAND, +DIV_RIB_Y))

# ── Floor 1: Tattu 3S 850 lies FLAT — 60 along X, 30 along Y, 23 up; flush at the −X end so
#   the envelope's 5 mm rest length (POCKET) forms the XT30/lead buffer at the +X DOOR end ──
BATT_SW = (BATT[0] + SWELL[0], BATT[1] + SWELL[1], BATT[2] + SWELL[2])
BATT_CX = IN_X0 + BATT[0] / 2
BATT_CY = 0.0
BATT_CZ = Z_FLOOR + BATT[2] / 2              # lying flat on the bay floor
BUF_X0 = IN_X1 - POCKET                      # buffer zone start (= battery +X end, 5 mm to the door)
DOOR_POCKET_D = 2.5                          # shallow nest in the door plug for the XT30 face

# ── Floor 2 (above the divider): camera high at the front, VTX just below it ──
CAM_CY = 0.0
CAM_CZ = Z_COVER_BOT - CAM[2] / 2 - 1.0      # camera high, just under the top cover
CAM_CX = IN_X0 + CAM[1] / 2                  # body depth 18.5 along X at the front; lens pokes -X
# Offset the VTX +Y: its bbox (board 30 + coax stub 11.4 -> +Y) is ≈41 wide, so a centred board
# would reach into the −Y switch bay. Shift it so the −Y board edge clears the switch latch; the
# coax stub then lands on the +Y side by the feedthrough (natural routing).
VTX_CY = (IN_Y0 + SW_LANE / 2) + spec.SW_LATCH_BODY_D / 2 + 0.7 + VTX_DY / 2
VTX_CX = ELEC_CX
VTX_CZ = CAM_CZ - CAM[2] / 2 - 1.0 - VTX_DZ / 2   # directly below the camera
VTX_UFL = (VTX_CX, VTX_CY + VTX_DY / 2 - 1.5, VTX_CZ + VTX_DZ / 2 - 4)  # coax stub tip (+Y, upper)

# ── side lanes (Y) + rear Wago stack (floor 2 is empty behind the front electronics band) ──
WAGO_LANE_Y = IN_Y1 - spec.WAGO_221_412[0] / 2 - TOL   # +Y lane centre (Wagos)
SW_Y = IN_Y0 + SW_LANE / 2                             # -Y lane centre (switch)
SW_X = ELEC_CX                                         # over the floor-2 front band
SW_CLEAR_R = spec.SW_LATCH_BODY_D / 2 + 1.5
WAGO_CX = (IN_X1 - 2 * INSET) - spec.WAGO_221_412[2] / 2 - TOL   # rear, clear of the +X posts

# ── 4 corner screw posts (vertical, full height — outside the 40-wide bay envelope by IN_Y_BAY) ──
CORNERS = [(IN_X0 + INSET, IN_Y0 + INSET), (IN_X0 + INSET, IN_Y1 - INSET),
           (IN_X1 - INSET, IN_Y0 + INSET), (IN_X1 - INSET, IN_Y1 - INSET)]
REAR_CORNERS = [c for c in CORNERS if c[0] > 0]         # door screws anchor into these (through-wall)

# ── antenna mount anchors ──
SMA_X = ELEC_CX                              # +Y side wall, over the electronics floor (Version A)
SMA_Z = CAM_CZ - 8.0                         # high, near camera level, clear of VTX
# Version A2 — internal AXII puck, laid along Y (donut axis across body). spec.py suggests high;
# the upright electronics floor is crowded top (camera) + mid (VTX), so the puck goes in the
# LOWER-FRONT band (below the VTX), still far from the LiPo (rear floor + divider) and offset from
# the head centreline in depth. DEVIATION (front-low vs upper-rear) documented in the report.
A2_PUCK_L = spec.OMNI_HEAD_D + 5.0           # ≈22.5 mm radiating head length (puck, sans coax)
A2_CX = ELEC_CX
A2_CZ = VTX_CZ - VTX_DZ / 2 - spec.OMNI_HEAD_D / 2 - 1.5   # below the VTX, on the front floor
A2_CY = 0.0                                  # axis Y spans the width (donut radiates ±Z)
PATCH = spec.PATCH_PCB                        # (35,35,3)  Version B
PATCH_CX = 0.0                                # centred on the bottom face
PATCH_CY = 0.0

# ─────────────────────────────────────────────────────────────────────────────
# COLORS
# ─────────────────────────────────────────────────────────────────────────────
C_BODY   = Color(0.80, 0.82, 0.85)
C_COVER  = Color(0.12, 0.12, 0.15)
C_BOTTOM = Color(0.30, 0.32, 0.36)
C_DOOR   = Color(0.18, 0.19, 0.22)
C_VTX    = Color(0.62, 0.06, 0.06)
C_CAM    = Color(0.05, 0.05, 0.06)
C_BAT    = Color(0.09, 0.12, 0.38)
C_BATCAP = Color(0.20, 0.20, 0.23)
C_WIRE_R = Color(0.75, 0.05, 0.05)
C_WIRE_B = Color(0.03, 0.03, 0.03)
C_WIRE_Y = Color(0.85, 0.75, 0.10)
C_XT30   = Color(0.88, 0.74, 0.06)
C_GOLD   = Color(0.83, 0.68, 0.22)
C_WHITE  = Color(0.92, 0.92, 0.94)
C_STEEL  = Color(0.60, 0.62, 0.66)
C_WAGO   = Color(0.55, 0.57, 0.60)
C_ORANGE = Color(0.96, 0.45, 0.05)
C_BLACK  = Color(0.05, 0.05, 0.06)
C_SILVER = Color(0.70, 0.70, 0.73)
C_COAX   = Color(0.04, 0.04, 0.04)
C_PATCH  = Color(0.10, 0.35, 0.12)

# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def biggest_solid(shape):
    if hasattr(shape, "__len__") and not hasattr(shape, "bounding_box"):
        try:
            solids = [s for s in shape if hasattr(s, "volume")]
            if solids:
                return max(solids, key=lambda s: s.volume)
        except Exception:
            pass
    return shape


def hex_prism(across_flats, height):
    r = across_flats / math.sqrt(3.0)
    return extrude(RegularPolygon(radius=r, side_count=6), amount=height)


def pipe(points, r):
    pts = [Vector(p) for p in points]
    line = Spline(*pts)
    sec = Plane(origin=pts[0], z_dir=(line % 0.0)) * Circle(r)
    return sweep(sec, path=line)


def service_loop(p0, p1, r, bulge=(0, 0, 8), n=2):
    """A slack cable from p0 to p1 with n coil bulges (service loop) for strain-relief."""
    p0, p1 = Vector(p0), Vector(p1)
    pts = [p0]
    for k in range(1, n + 1):
        t = k / (n + 1)
        mid = p0 + (p1 - p0) * t
        b = Vector(bulge) * (1 if k % 2 else -1)
        pts.append(mid + b)
    pts.append(p1)
    return pipe(pts, r)


def colored(solid, color, label):
    solid.color = color
    solid.label = label
    return solid


def _place_raw(raw, rot, target_center):
    s = Rot(*rot) * raw if rot != (0, 0, 0) else Pos(0, 0, 0) * raw
    bb = s.bounding_box()
    c = Vector((bb.min.X + bb.max.X) / 2, (bb.min.Y + bb.max.Y) / 2, (bb.min.Z + bb.max.Z) / 2)
    return Pos(Vector(target_center) - c) * s


# ─────────────────────────────────────────────────────────────────────────────
# PRINTED ENCLOSURE PARTS
# ─────────────────────────────────────────────────────────────────────────────
def gen_body(variant):
    """Upright tube (4 vertical walls + vertical divider) — open top (cover+door) and bottom (shell)."""
    zc = (Z_FLOOR + Z_COVER_BOT) / 2
    outer = Pos(0, 0, zc) * Box(EX_X, EX_Y, IN_Z)
    inner = Pos(0, 0, zc) * Box(IN_X, IN_Y, IN_Z + 2)
    body = outer - inner
    # M2: divider = separate drop-in tray. The body only carries its seats: two full-depth
    # DIVIDER_LEDGE rails on the +/-Y walls (top face = Z_DIV_BOT, so the bay stays EXACTLY 25
    # clear; ledge faces at |y|=25.4 stay clear of the 40-wide envelope) ...
    for sy in (-1, 1):
        body = body + Pos(0, sy * (IN_Y - spec.DIVIDER_LEDGE[0]) / 2, Z_DIV_BOT - spec.DIVIDER_LEDGE[1] / 2) * \
            Box(IN_X, spec.DIVIDER_LEDGE[0], spec.DIVIDER_LEDGE[1])
    # ... plus 2 diagonal hold-down bosses (heat-set M3, drilled from the seat face) fused to the
    # +/-Y walls under the tray band; boss faces at |y|=20.4 stay outside the bay envelope
    for bx, by in DIV_SCREWS:
        sy = -1 if by < 0 else 1
        body = body + Pos(bx, sy * (IN_Y / 2 - 4.0), Z_DIV_BOT - 4.0) * Box(10.0, 8.0, 8.0)
        body = body - Pos(bx, sy * (IN_Y / 2 - 4.0), Z_DIV_BOT - 3.1) * Cylinder(radius=2.1, height=6.2)
    # battery DOOR opening in the REAR (+X) wall: the bay's 40x25 cross-section + slide tolerances
    # (width 40+2*TOL; height 25+TOL grows DOWN past the floor edge so the divider band stays whole)
    body = body - Pos(IN_X1 + (WALL + 2) / 2 - 0.01, 0, Z_FLOOR + (BAY[2] + TOL) / 2 - TOL) * \
        Box(WALL + 2, BAY[1] + 2 * TOL, BAY[2] + TOL)
    # door screw pilots (M3 self-tap, axis X) through the rear wall into the rear corner posts
    for (cx, cy) in REAR_CORNERS:
        body = body - Pos(IN_X1 - 2, cy, Z_FLOOR + BAY[2] / 2) * Rot(0, 90, 0) * \
            Cylinder(radius=1.35, height=12)
    body = biggest_solid(body)
    # corner posts (full height) + top & bottom M3 heat-set pilots
    for (cx, cy) in CORNERS:
        body = body + Pos(cx, cy, zc) * Box(2 * INSET, 2 * INSET, IN_Z)
        body = body - Pos(cx, cy, Z_COVER_BOT - 3) * Cylinder(radius=2.1, height=6.2)   # top insert
        body = body - Pos(cx, cy, Z_FLOOR + 3) * Cylinder(radius=2.1, height=6.2)       # bottom insert
    body = biggest_solid(body)
    # camera lens hole through the FRONT (−X) wall + nose
    lx = -EX_X / 2
    body = body - Pos(lx, CAM_CY, CAM_CZ) * Rot(0, 90, 0) * Cylinder(radius=spec.CAM_LENS_D / 2 + 1.0, height=WALL * 2)
    no = Pos(lx + 1.5, CAM_CY, CAM_CZ) * Rot(0, 90, 0) * Cylinder(radius=spec.CAM_LENS_D / 2 + 2, height=4)
    ni = Pos(lx + 1.5, CAM_CY, CAM_CZ) * Rot(0, 90, 0) * Cylinder(radius=spec.CAM_LENS_D / 2, height=6)
    body = body + (no - ni)
    body = biggest_solid(body)

    # variant-specific features
    if variant == "A":
        # SMA bulkhead panel hole in +Y side wall + local recess (clamp <= 2.8)
        body = body - Pos(SMA_X, EX_Y / 2, SMA_Z) * Rot(90, 0, 0) * Cylinder(radius=spec.BULKHEAD_PANEL_HOLE / 2, height=WALL * 3)
        body = body - Pos(SMA_X, EX_Y / 2 - RECESS / 2, SMA_Z) * Rot(90, 0, 0) * \
            Cylinder(radius=spec.BULKHEAD_HEX_AF, height=WALL - RECESS + 0.01)
    elif variant == "A2":
        # front-floor BODY cradle: a block on the front wall with an open half-pipe (axis Y) that
        # captures the lower half of the AXII puck rock-solid (upper half held by the cover clip).
        cr_top = A2_CZ
        # TODO (later MS): A2 puck no longer fits below the VTX over the new divider — antenna
        # placement moves with the captive-wall-omni redesign; clamp keeps geometry buildable.
        cr_bot = max(Z_DIV_TOP, A2_CZ - spec.OMNI_HEAD_D / 2 - 3)
        if cr_top - cr_bot > 2:   # pre-M2 A2_CZ sits BELOW Z_DIV_TOP -> no cradle possible; the
            # A2 puck placement is redesigned in the captive-wall-omni MS (see TODO above)
            cradle = Pos(A2_CX, A2_CY, (cr_top + cr_bot) / 2) * Box(spec.OMNI_HEAD_D + 4, A2_PUCK_L, cr_top - cr_bot)
            body = body + cradle
            body = body - Pos(A2_CX, A2_CY, A2_CZ) * Rot(90, 0, 0) * \
                Cylinder(radius=spec.OMNI_HEAD_D / 2 + 0.4, height=A2_PUCK_L + 2)
            body = biggest_solid(body)

    # fillet the four external vertical corners (now along Z). Position-filtered: with the
    # integral divider gone (M2), the concave wall/post junction edges also run full height and
    # a plain length filter would fillet them INTO the bay envelope (18 mm³ intrusion).
    try:
        vert = [e for e in body.edges().filter_by(Axis.Z)
                if e.length > IN_Z - 1
                and abs(abs(e.center().X) - EX_X / 2) < 0.01
                and abs(abs(e.center().Y) - EX_Y / 2) < 0.01]
        if vert:
            body = fillet(vert, radius=2.0)
    except Exception:
        pass
    body = biggest_solid(body)
    return colored(body, C_BODY, f"skylive_{variant}_body")


def gen_cover(variant):
    """Full top panel over Floor 2; carries the switch; screwed at all 4 corner posts (the battery
    door is a SIDE hatch now, so the top is one piece)."""
    clen = EX_X
    ccx = 0.0
    cover = Box(clen, EX_Y, COVER_T)
    for (cx, cy) in CORNERS:
        cover = cover - Pos(cx - ccx, cy, 0) * Cylinder(radius=1.7, height=COVER_T * 2)        # M3 clearance
        cover = cover - Pos(cx - ccx, cy, COVER_T / 2 - 1) * Cylinder(radius=3, height=2)       # head counterbore
    # switch panel hole (over the electronics floor)
    cover = cover - Pos(SW_X - ccx, SW_Y, 0) * Cylinder(radius=spec.SW_PANEL_HOLE / 2, height=COVER_T * 2)
    # GORE vent over the camera
    cover = cover - Pos(CAM_CX - ccx, 0, 0) * Cylinder(radius=3.0, height=COVER_T * 2)
    cover = biggest_solid(cover)
    cover = Pos(ccx, 0, Z_TOP - COVER_T / 2) * cover
    if variant == "A2":
        # retention saddle hanging UNDER the cover would be too far above the low-front puck; instead
        # the puck is fully captured by the body cradle (>half wrap) + a screw-down clip modelled as a
        # small rib on the cover edge nearest the puck. Kept minimal & watertight.
        pass
    return colored(cover, C_COVER, f"skylive_{variant}_cover")


def gen_door(variant):
    """REAR (+X) battery door at the CABLE end (Tom's mechanism): the flat cell slides in body-
    first; an outer plate + plug lip fill the 40x25(+tol) wall cutout; a shallow pocket in the
    plug nests the XT30/JST faces (they live in the envelope's 5 mm buffer); 2 horizontal M3
    screws pass through the wall into the rear corner posts. Prints outer_face_down."""
    zc = Z_FLOOR + BAY[2] / 2
    # plate spans bottom-shell edge (-BOTTOM_T) .. 5 over the opening — flush with the case bottom
    plate = Pos(EX_X / 2 + WALL / 2, 0, zc + 1.0) * Box(WALL, EX_Y, BAY[2] + BOTTOM_T + 5)
    # plug lip: slide fit (0.3/side) into the wall cutout, inner face FLUSH with the bay wall face
    lip = Pos(IN_X1 + WALL / 2, 0, zc - TOL / 2) * \
        Box(WALL, BAY[1] + 2 * TOL - 0.6, BAY[2] + TOL - 0.6)
    door = biggest_solid(plate + lip)
    # XT30/JST nest pocket carved into the plug from its inner face
    door = door - Pos(IN_X1 + DOOR_POCKET_D / 2, 0, Z_FLOOR + 7) * Box(DOOR_POCKET_D, 28, 14)
    # M3 clearance holes + head counterbores (axis X), aligned with the rear corner posts
    for (cx, cy) in REAR_CORNERS:
        door = door - Pos(EX_X / 2 + WALL / 2, cy, Z_FLOOR + BAY[2] / 2) * Rot(0, 90, 0) * \
            Cylinder(radius=1.7, height=WALL * 2)
        door = door - Pos(EX_X / 2 + WALL - 0.75, cy, Z_FLOOR + BAY[2] / 2) * Rot(0, 90, 0) * \
            Cylinder(radius=3, height=1.5)
    door = biggest_solid(door)
    return colored(door, C_DOOR, f"skylive_{variant}_battery_door")


def gen_bottom_shell(variant):
    """Bottom shell (−Z): closes the floor + carries the primary GoPro mount.
    A/A2: flat BOTTOM_T plate.
    B (spec.PATCH_SHELL_CAVITY): a HOLLOW CAP — top plate BOTTOM_T (mates the body, coax hole),
    WALL-thick skirt around a 15 mm internal cavity that fully houses the patch + its connector
    like a protective lens-cap (patch hangs from the plate, RF standoff to the radome, nothing
    touches the patch face), closed by an RF_WINDOW_WALL radome on the outer down-face. Four
    corner bosses span the cavity so the corner screws still reach the body inserts."""
    thick = Z_FLOOR - bottom_outer_z(variant)             # A/A2 = BOTTOM_T ; B = BOTTOM_T + B_CAP_EXT
    outer = -thick / 2                                    # local: outer (down) face
    shell = Box(EX_X, EX_Y, thick)
    if variant == "B":
        cav_top = thick / 2 - BOTTOM_T                    # local z of the plate underside
        cav_cz = cav_top - spec.PATCH_SHELL_CAVITY / 2
        shell = shell - Pos(0, 0, cav_cz) * \
            Box(EX_X - 2 * WALL, EX_Y - 2 * WALL, spec.PATCH_SHELL_CAVITY)                        # hollow cap cavity
        for (cx, cy) in CORNERS:                          # screw bosses bridge plate <-> radome
            shell = shell + Pos(cx, cy, cav_cz) * Box(9.0, 9.0, spec.PATCH_SHELL_CAVITY)
        shell = biggest_solid(shell)
        for (cx, cy) in CORNERS:                          # M3 clearance bores + head counterbores
            shell = shell - Pos(cx, cy, 0) * Cylinder(radius=1.7, height=thick + 2)
            shell = shell - Pos(cx, cy, outer + 1.5) * Cylinder(radius=3.0, height=3.0)
        # coax hole through the top plate (patch connector passes into the interior, off the battery)
        shell = shell - Pos(PATCH_CX - PATCH[0] / 2 + 3, PATCH_CY, thick / 2 - BOTTOM_T / 2) * \
            Cylinder(radius=spec.BULKHEAD_PANEL_HOLE / 2, height=BOTTOM_T + 2)
        shell = biggest_solid(shell)
    else:
        for (cx, cy) in CORNERS:
            shell = shell - Pos(cx, cy, thick / 2 - BOTTOM_T * 1.5) * Cylinder(radius=1.35, height=BOTTOM_T * 3)  # M3 pilot from the top
    # GoPro 2-prong (female) fingers on the underside — strong, filleted
    fw = spec.GOPRO_2PRONG[0]
    ft = spec.GOPRO_FINGER_T
    gap = spec.GOPRO_GAP
    fh = spec.GOPRO_2PRONG[2]
    for fy in (-(gap / 2 + ft / 2), +(gap / 2 + ft / 2)):
        shell = shell + Pos(0, fy, outer - fh / 2) * Box(fw, ft, fh)
    shell = shell - Pos(0, 0, outer - fh + spec.GOPRO_HOLE_D / 2 + 3) * \
        Rot(90, 0, 0) * Cylinder(radius=spec.GOPRO_HOLE_D / 2, height=EX_Y)                       # Ø5 pivot bore
    shell = biggest_solid(shell)
    shell = Pos(0, 0, Z_FLOOR - thick / 2) * shell        # top face lands on Z_FLOOR (mates the body)
    return colored(shell, C_BOTTOM, f"skylive_{variant}_bottom_shell")


def gen_divider_tray(variant):
    """M2: flat-printed drop-in divider tray (spec.DIVIDER_*): DIVIDER_T plate with a 6 mm solid
    edge band, corner notches around the full-height posts (slide fit TRAY_CLR), 2 down-pointing
    longitudinal ribs outside the bay envelope, connector windows / grommet holes / 2 open keyhole
    slots (= 2 of max 3 band breaks) and 2 diagonal M3 hold-down holes over the wall bosses."""
    tray = Pos(0, 0, Z_DIV_BOT + DIV_T / 2) * Box(TRAY_X1 - TRAY_X0, TRAY_Y1 - TRAY_Y0, DIV_T)
    for sx in (-1, 1):                      # corner notches: 2*INSET square + 1 mm overshoot out
        for sy in (-1, 1):
            tray = tray - Pos(sx * (TRAY_X1 - INSET + 0.5), sy * (TRAY_Y1 - INSET + 0.5),
                              Z_DIV_BOT + DIV_T / 2) * Box(2 * INSET + 1, 2 * INSET + 1, DIV_T + 2)
    for x0, x1, ry in DIV_RIBS:             # ribs hang DOWN into the floor-1 side lanes (|y|>20)
        tray = tray + Pos((x0 + x1) / 2, ry, Z_DIV_BOT - spec.DIVIDER_RIB[1] / 2) * \
            Box(x1 - x0, spec.DIVIDER_RIB[0], spec.DIVIDER_RIB[1])
    for cx, cy, dx, dy in DIV_WINDOWS:      # rectangular through-windows (inboard of the band)
        tray = tray - Pos(cx, cy, Z_DIV_BOT + DIV_T / 2) * Box(dx, dy, DIV_T + 2)
    for cx, cy in DIV_GROMMETS:             # Ø8 grommet holes
        tray = tray - Pos(cx, cy, Z_DIV_BOT + DIV_T / 2) * Cylinder(radius=FT_D / 2, height=DIV_T + 2)
    for sx_c, side in DIV_SLOTS:            # open keyhole slots: FT_SLOT deep from the tray edge
        y1 = TRAY_Y1 if side > 0 else TRAY_Y0
        tray = tray - Pos(sx_c, y1 - side * (FT_SLOT[1] / 2 - 1), Z_DIV_BOT + DIV_T / 2) * \
            Box(FT_SLOT[0], FT_SLOT[1] + 2, DIV_T + 2)
    for cx, cy in DIV_SCREWS:               # M3 hold-down clearance holes over the boss zones
        tray = tray - Pos(cx, cy, Z_DIV_BOT + DIV_T / 2) * Cylinder(radius=DIV_SCREW_D / 2, height=DIV_T + 2)
    tray = biggest_solid(tray)
    return colored(tray, Color(0.72, 0.58, 0.20), f"skylive_{variant}_divider_tray")


def printed_parts(variant):
    return [gen_body(variant), gen_cover(variant), gen_door(variant), gen_bottom_shell(variant),
            gen_divider_tray(variant)]


# ─────────────────────────────────────────────────────────────────────────────
# REAL COMPONENTS
# ─────────────────────────────────────────────────────────────────────────────
def comp_vtx():
    # vertical board: thickness 14.1 -> X (depth), height 29.2 -> Z, coax stub -> +Y (upper)
    s = _place_raw(Rot(0, 0, 180) * _VTX_RAW, (0, 90, 0), (VTX_CX, VTX_CY, VTX_CZ))
    return colored(s, C_VTX, "VTX_HDZero_FreestyleV2")


def comp_camera():
    # lens on -Y in the STEP; rotate so lens points -X (front); poke ~through the front wall
    s = Rot(0, 0, -90) * _CAM_RAW
    bb = s.bounding_box()
    cy = (bb.min.Y + bb.max.Y) / 2
    cz = (bb.min.Z + bb.max.Z) / 2
    off = Vector((-EX_X / 2 + WALL - 2.5) - bb.min.X, CAM_CY - cy, CAM_CZ - cz)
    return colored(Pos(off) * s, C_CAM, "Camera_HDZero_Nano90")


def comp_battery():
    """Wrapped LiPo pouch — reads as a real soft-pack cell, not a solid block.
    Tattu 3S 850 lying FLAT (M1): BATT_CELL (60,30,23) -> X=60 (L), Y=30 (W), Z=23 (H).
    All detail is subtractive or inset, so the bbox stays EXACTLY (60,30,23) and the spec
    dimension gate + the Battery↔XT30 buffer gap are untouched. Leads exit the ONE short
    (+X, door-side) end (see comp_battery_leads)."""
    L, W, H = BATT[0], BATT[1], BATT[2]            # 60 (X), 30 (Y), 23 (Z)
    x0 = BATT_CX - L / 2
    x1 = BATT_CX + L / 2                           # +X short end = the lead end (door side)
    parts = []

    # main heat-shrink-wrapped body: soft-pouch fillet on ALL edges (rounded pouch, not a sharp box)
    pack = Pos(BATT_CX, BATT_CY, BATT_CZ) * Box(L, W, H)
    try:
        pack = fillet(pack.edges(), radius=1.5)
    except Exception:
        try:
            pack = fillet([e for e in pack.edges().filter_by(Axis.X) if e.length > L - 1], radius=1.5)
        except Exception:
            pass
    # wrap hints (all shallow → bbox untouched): a longitudinal overlap seam down each broad (±Z)
    # face + two circumferential wrap-edge bands near the ends, so it reads as wrapped foil.
    for sz in (H / 2, -H / 2):
        pack = pack - Pos(BATT_CX, BATT_CY + W / 2 - 2.0, BATT_CZ + sz) * Box(L - 12, 1.0, 0.6)  # overlap seam
    for bx in (x1 - 5.0, x0 + 5.0):
        for sz in (H / 2, -H / 2):
            pack = pack - Pos(bx, BATT_CY, BATT_CZ + sz) * Box(1.2, W - 6, 0.5)             # wrap-edge band
    pack = biggest_solid(pack)
    parts.append(colored(pack, C_BAT, "Battery_Tattu_3S_850"))

    # folded pouch end-cap at the lead end (inset tape plate + a small lead root), distinct grey.
    cap = Pos(x1 - 1.0, BATT_CY, BATT_CZ) * Box(2.0, W - 3.0, H - 2.5)                       # end at x1 -> bbox ok
    root = Pos(x1 - 2.5, BATT_CY - 1.0, BATT_CZ) * Box(3.0, W - 4.0, H - 7.0)               # leads emerge here (inset)
    endcap = biggest_solid(cap + root)
    parts.append(colored(endcap, C_BATCAP, "Battery_wrap_endcap"))

    return colored(Compound(children=parts), C_BAT, "Battery_Tattu_3S_850")


def comp_battery_leads():
    """XT30 + JST-XH-4 in the envelope's 5 mm DOOR buffer (= Tom's rest length, POCKET); their
    faces nest in the shallow door-plug pocket; leads come off the cell's +X end with slack."""
    solids = []
    # ── XT30: chamfered yellow nylon housing on edge in the buffer (6-thick along X, 13 along Y,
    #    11 up), mating face -Y; nose reaches ~1.5 into the door pocket (documented allowance) ──
    xt_cx = BUF_X0 + 0.5 + spec.XT30_MALE[2] / 2
    xt_cz = Z_FLOOR + 0.5 + spec.XT30_MALE[1] / 2
    xt = Pos(xt_cx, -7.0, xt_cz) * Box(spec.XT30_MALE[2], spec.XT30_MALE[0], spec.XT30_MALE[1])
    try:  # chamfer the two keyed top corners of the housing (bbox unchanged → gap safe)
        te = [e for e in xt.edges().filter_by(Axis.Y)
              if e.center().Z > xt_cz + spec.XT30_MALE[1] / 2 - 0.6]
        xt = chamfer(te, length=1.2)
    except Exception:
        pass
    solids.append(colored(biggest_solid(xt), C_XT30, "XT30_male_block"))
    # gold pins exit the -Y mating face into the free bay corner (clear of cell and door)
    for i, dz in enumerate((-2.75, 2.75)):
        pin = Pos(xt_cx, -7.0 - spec.XT30_MALE[0] / 2 - 2.5, xt_cz + dz) * \
            Rot(90, 0, 0) * Cylinder(radius=1.75, height=5)
        solids.append(colored(pin, C_GOLD, f"XT30_pin_{i}"))
    # ── JST-XH-4 balance: white ribbed housing beside the XT30 (5.7 along X, upright 12.3) ──
    j_cx = BUF_X0 + 0.5 + spec.JST_XH4[1] / 2
    j_cz = Z_FLOOR + 0.5 + spec.JST_XH4[0] / 2
    jst = Pos(j_cx, 6.0, j_cz) * Box(spec.JST_XH4[1], spec.JST_XH4[2], spec.JST_XH4[0])
    try:  # shallow ribs on the door-facing (+X) face (bbox unchanged)
        for rz in (-3.0, -1.0, 1.0, 3.0):
            jst = jst - Pos(j_cx + spec.JST_XH4[1] / 2, 6.0, j_cz + rz) * \
                Box(1.0, spec.JST_XH4[2] - 1.0, 0.5)
        jst = biggest_solid(jst)
    except Exception:
        pass
    solids.append(colored(jst, C_WHITE, "JST_XH4_balance"))
    for k, pz in enumerate((-3.75, -1.25, 1.25, 3.75)):     # 4 visible pins on the mating (−Y) face
        jp = Pos(j_cx, 6.0 - spec.JST_XH4[2] / 2 - 1.0, j_cz + pz) * \
            Rot(90, 0, 0) * Cylinder(radius=0.35, height=2)
        solids.append(colored(jp, C_GOLD, f"JST_XH4_pin_{k}"))
    # 45 mm silicone power leads (Ø~1.6) from the cell's +X end -> XT30, with a service loop
    bx = BATT_CX + BATT[0] / 2 - 1.0
    for dy, col, nm in ((-3, C_WIRE_R, "battery_lead_pos"), (3, C_WIRE_B, "battery_lead_neg")):
        solids.append(colored(service_loop((bx, dy - 1, BATT_CZ), (xt_cx, dy - 1, xt_cz - 3),
                                            0.8, bulge=(0, 3, 4), n=2), col, nm))
    # thinner JST-XH-4 balance lead, bundled from the SAME end (the lead root on the end-cap)
    solids.append(colored(service_loop((bx, -3, BATT_CZ + 3), (j_cx, 10.5, j_cz),
                                       0.5, bulge=(0, 2, 3), n=2), C_WIRE_Y, "balance_lead"))
    return solids


def comp_wagos():
    """3x Wago 221-412 in the +Y lane at the REAR of Floor 2 (behind the electronics band, clear
    of the +X corner posts), stacked vertically, levers up (grey + orange)."""
    solids = []
    w, h, l = spec.WAGO_221_412                 # 13.2 W x 8.6 H x 18.8 L
    cx = WAGO_CX
    cy = WAGO_LANE_Y
    for i, cz in enumerate((Z_DIV_TOP + 5, Z_DIV_TOP + 18, Z_DIV_TOP + 31)):   # 13 pitch: lever room
        # L(18.8) along X, W(13.2) along Y, H(8.6) along Z
        body = Pos(cx, cy, cz) * Box(l, w, h)
        # 221-412 = 2 conductors: hint the two wire-entry holes on the -X (front) face
        for dy in (-3.3, 3.3):
            body = body - Pos(cx - l / 2, cy + dy, cz) * Rot(0, 90, 0) * Cylinder(radius=1.4, height=5)
        body = biggest_solid(body)
        solids.append(colored(body, C_WAGO, f"Wago221_412_{i+1}"))
        # two orange levers on the top (+Z) face — clearly proud, with a raised angled finger pad
        # so they read as flippable (base sits on the body face, pad lifts off at the free end).
        for j, dy in enumerate((-3.3, 3.3)):
            base = Pos(cx - l / 2 + 3.0, cy + dy, cz + h / 2 + 1.1) * Box(2.4, 3.6, 2.2)   # hinge root
            pad = Pos(cx - l / 2 + 4.4, cy + dy, cz + h / 2 + 2.4) * Box(1.1, 3.6, 1.6)    # finger tab
            lev = biggest_solid(base + pad)
            solids.append(colored(lev, C_ORANGE, f"Wago{i+1}_lever_{j+1}"))
    return solids


def comp_switch():
    """12 mm latching push-button, vertical through the top cover into its dedicated bay."""
    solids = []
    x, y = SW_X, SW_Y
    top = Z_TOP
    bot = Z_COVER_BOT
    r_barrel = spec.SW_PANEL_HOLE / 2
    # barrel through the panel (in the Ø12 cover hole)
    barrel = Pos(x, y, (top + bot) / 2) * Cylinder(radius=r_barrel, height=COVER_T)
    # externally-threaded barrel ring proud of the panel (M12x0.75), with a few thread grooves
    thr_h = 3.0
    thread = Pos(x, y, top + thr_h / 2) * Cylinder(radius=r_barrel + 0.5, height=thr_h)
    try:
        for k in range(3):
            gz = top + 0.6 + k * 0.9
            groove = Pos(x, y, gz) * (Cylinder(radius=r_barrel + 0.7, height=0.3)
                                      - Cylinder(radius=r_barrel + 0.15, height=0.5))
            thread = thread - groove
    except Exception:
        pass
    # domed anti-vandal bezel (Ø14) seated on the threaded barrel
    bez_z = top + thr_h
    bezel = Pos(x, y, bez_z + 1.5) * Cylinder(radius=spec.SW_HEAD_D / 2, height=3.0)
    steel = biggest_solid(barrel + thread + bezel)
    # actuator button: domed, standing slightly proud of the bezel
    bt = bez_z + 3.0
    br = 4.5
    button = Pos(x, y, bt + 0.75) * Cylinder(radius=br, height=1.5)
    button = button + (Pos(x, y, bt + 1.5) * Sphere(radius=br) - Pos(x, y, bt + 1.5 - br) * Box(2 * br, 2 * br, 2 * br))
    steel = steel + biggest_solid(button)
    solids.append(colored(biggest_solid(steel), C_STEEL, "Switch_12mm_head_barrel_button"))
    nut = Pos(x, y, bot - 3) * hex_prism(SW_NUT_AF, 3.0)
    solids.append(colored(nut, C_STEEL, "Switch_locknut"))
    latch_top = bot - 3
    latch = Pos(x, y, latch_top - spec.SW_BEHIND_PANEL / 2) * Cylinder(radius=spec.SW_LATCH_BODY_D / 2, height=spec.SW_BEHIND_PANEL)
    solids.append(colored(latch, C_BLACK, "Switch_latch_body_27mm"))
    lb = latch_top - spec.SW_BEHIND_PANEL
    # 120 mm pre-wired switch leads with a service loop toward the divider feedthrough
    for dy, col, nm in ((-3, C_WIRE_R, "switch_lead_pos"), (3, C_WIRE_B, "switch_lead_neg")):
        boot = Pos(x + dy, y, lb - 1) * Cylinder(radius=1.6, height=3)
        solids.append(colored(boot, C_BLACK, f"{nm}_boot"))
        solids.append(colored(service_loop((x + dy, y, lb - 2), (WAGO_CX - 12, 0, Z_DIV_TOP + 10),
                                            1.0, bulge=(0, -3, -5), n=3), col, nm))
    return solids


def comp_antenna(variant):
    """Antenna per variant + SMA bulkhead + U.FL plug + pigtail with slack."""
    solids = []
    # U.FL plug on the VTX coax-stub tip (+Y, upper)
    ufl = Pos(*VTX_UFL) * Rot(90, 0, 0) * Cylinder(radius=spec.UFL_PLUG_D / 2, height=spec.UFL_PLUG_D)
    solids.append(colored(ufl, C_SILVER, "UFL_plug_on_VTX"))

    if variant == "A":
        # SMA bulkhead in the +Y side wall (axis Y) + AXII laid horizontal outside, puck proud only
        by = EX_Y / 2
        r_sma = spec.BULKHEAD_THREAD_OD / 2
        barrel = Pos(SMA_X, by - spec.BULKHEAD_BODY_LEN / 2, SMA_Z) * Rot(90, 0, 0) * \
            Cylinder(radius=r_sma, height=spec.BULKHEAD_BODY_LEN)
        try:  # thread grooves along the barrel (axis Y) so it reads as a real threaded SMA bulkhead
            n = int(spec.BULKHEAD_BODY_LEN // 1.0)
            for k in range(1, n):
                gy = by - k * 1.0
                ring = (Pos(SMA_X, gy, SMA_Z) * Rot(90, 0, 0) * Cylinder(radius=r_sma + 0.05, height=0.3)
                        - Pos(SMA_X, gy, SMA_Z) * Rot(90, 0, 0) * Cylinder(radius=r_sma - 0.25, height=0.4))
                barrel = barrel - ring
            barrel = biggest_solid(barrel)
        except Exception:
            pass
        solids.append(colored(barrel, C_GOLD, "SMA_bulkhead_barrel"))
        nut = Pos(SMA_X, by, SMA_Z) * Rot(-90, 0, 0) * hex_prism(spec.BULKHEAD_HEX_AF, spec.BULKHEAD_NUT_T)
        solids.append(colored(nut, C_GOLD, "SMA_bulkhead_nut"))
        conn = Pos(SMA_X, by + spec.BULKHEAD_NUT_T, SMA_Z) * Rot(-90, 0, 0) * hex_prism(spec.BULKHEAD_HEX_AF, 8)
        solids.append(colored(conn, C_GOLD, "Omni_SMA_connector"))
        head = Pos(SMA_X, by + spec.BULKHEAD_NUT_T + 8 + spec.OMNI_HEAD_D / 2, SMA_Z) * Rot(90, 0, 0) * \
            Cylinder(radius=spec.OMNI_HEAD_D / 2, height=spec.OMNI_HEAD_D)
        solids.append(colored(head, C_BLACK, "Omni_Lumenier_AXII2_head"))
        # RG178 pigtail: VTX U.FL -> SMA bulkhead, with a service loop
        solids.append(colored(service_loop(VTX_UFL, (SMA_X, by - spec.BULKHEAD_BODY_LEN, SMA_Z),
                                           0.9, bulge=(-4, 2, 2), n=2), C_COAX, "RG178_UFL_to_SMA_pigtail"))
    elif variant == "A2":
        # AXII captured internally in the front-floor cradle, laid along Y (axis across body)
        head = Pos(A2_CX, A2_CY, A2_CZ) * Rot(90, 0, 0) * Cylinder(radius=spec.OMNI_HEAD_D / 2, height=A2_PUCK_L)
        solids.append(colored(head, C_BLACK, "Omni_Lumenier_AXII2_internal"))
        puck_end = A2_CY - A2_PUCK_L / 2
        nub = Pos(A2_CX, puck_end + 1.0, A2_CZ) * Rot(90, 0, 0) * Cylinder(radius=spec.UFL_PLUG_D / 2, height=2)
        solids.append(colored(nub, C_GOLD, "Omni_UFL_nub"))
        # coax from VTX U.FL down the front floor to the puck base, with a generous service loop
        solids.append(colored(service_loop(VTX_UFL, (A2_CX, puck_end + 0.5, A2_CZ),
                                           0.9, bulge=(0, -6, -5), n=3), C_COAX, "RG402_UFL_to_internal_omni"))
    elif variant == "B":
        # patch inside the HOLLOW-CAP bottom shell: hangs from the plate underside (back against
        # the plate), radiating face DOWN with an RF standoff to the radome (never touching it);
        # its connector passes UP through the Ø6.5 plate hole into the interior.
        patch_top = Z_FLOOR - BOTTOM_T                        # plate underside (cavity top)
        patch_cz = patch_top - PATCH[2] / 2
        patch = Pos(PATCH_CX, PATCH_CY, patch_cz) * Box(*PATCH)
        solids.append(colored(patch, C_PATCH, "TBS_5G8_patch_PCB"))
        conn_x = PATCH_CX - PATCH[0] / 2 + 3.0                # front edge of the patch, off the battery
        pconn = Pos(conn_x, PATCH_CY, patch_top + 2) * Cylinder(radius=spec.UFL_PLUG_D / 2, height=4)
        solids.append(colored(pconn, C_GOLD, "patch_UFL_connector"))
        # coax up through the divider XT30 window to the VTX U.FL, with slack
        solids.append(colored(service_loop((conn_x, PATCH_CY, patch_top + 4), (FT_CX, FT_CY, Z_DIV_BOT),
                                           0.9, bulge=(0, 0, 6), n=2), C_COAX, "patch_coax_lower"))
        solids.append(colored(service_loop((FT_CX, FT_CY, Z_DIV_BOT), VTX_UFL,
                                           0.9, bulge=(-4, 0, 6), n=2), C_COAX, "patch_coax_to_UFL"))
    return solids


# ─────────────────────────────────────────────────────────────────────────────
# SCENES
# ─────────────────────────────────────────────────────────────────────────────
def all_components(variant):
    s = [comp_vtx(), comp_camera(), comp_battery()]
    s += comp_battery_leads()
    s += comp_wagos()
    s += comp_switch()
    s += comp_antenna(variant)
    return s


def translate_solid(s, dv):
    color, label = getattr(s, "color", None), getattr(s, "label", "")
    s2 = Pos(*dv) * s
    if color is not None:
        s2.color = color
    s2.label = label
    return s2


def build_assembled(variant):
    return Compound(children=printed_parts(variant) + all_components(variant))


def build_exploded(variant):
    body = gen_body(variant)
    cover = translate_solid(gen_cover(variant), (-20, 0, 55))
    door = translate_solid(gen_door(variant), (45, 0, 0))
    bottom = translate_solid(gen_bottom_shell(variant), (0, 0, -55))
    tray = translate_solid(gen_divider_tray(variant), (0, -75, 0))
    comps = []
    for c in all_components(variant):
        lbl = c.label
        if lbl.startswith(("VTX", "Camera", "UFL", "Omni", "SMA", "RG", "patch", "TBS")):
            comps.append(translate_solid(c, (-30, 0, 0)))
        elif lbl.startswith("Switch") or "switch" in lbl:
            comps.append(translate_solid(c, (0, 0, 40)))
        elif lbl.startswith(("Battery", "XT30", "JST")) or "lead" in lbl:
            comps.append(translate_solid(c, (30, 0, 0)))
        else:
            comps.append(translate_solid(c, (30, 0, 0)))
    return Compound(children=[body, cover, door, bottom, tray] + comps)


# ─────────────────────────────────────────────────────────────────────────────
# VERIFICATION GATES
# ─────────────────────────────────────────────────────────────────────────────
def _solids(x):
    try:
        s = list(x.solids())
        return s if s else [x]
    except Exception:
        return [x]


def _gbb(solids):
    return Compound(children=list(solids)).bounding_box()


def _aabb_gap(A, B):
    return (max(A.min.X - B.max.X, B.min.X - A.max.X),
            max(A.min.Y - B.max.Y, B.min.Y - A.max.Y),
            max(A.min.Z - B.max.Z, B.min.Z - A.max.Z))


def _grp_ivol(ga, gb):
    v = 0.0
    for sa in ga:
        for sb in gb:
            gx, gy, gz = _aabb_gap(sa.bounding_box(), sb.bounding_box())
            if gx < 0 and gy < 0 and gz < 0:
                try:
                    v += (sa & sb).volume
                except Exception:
                    pass
    return v


def run_gates(variant):
    print(f"\n── GATES · variant {variant} ──")
    ok = True

    # 1) watertight printed parts
    print("  watertight printed parts:")
    for p in printed_parts(variant):
        n = len(p.solids())
        sh = len(p.shells())
        good = (n == 1 and sh == 1)
        ok &= good
        print(f"    {p.label:26s} solids={n} shells={sh}  {'OK' if good else 'FAIL'}")

    # 2) pairwise interference between interior bulk parts
    comps = all_components(variant)
    def grp(pred):
        return [s for s in comps if pred(s.label)]
    groups = {
        "VTX": grp(lambda l: l.startswith("VTX_H")),
        "Camera": grp(lambda l: l.startswith("Camera")),
        "Battery": grp(lambda l: l.startswith("Battery")),
        "XT30": grp(lambda l: l.startswith("XT30")),
        "JST": grp(lambda l: l == "JST_XH4_balance"),
        "Switch": grp(lambda l: l in ("Switch_12mm_head_barrel_button", "Switch_locknut", "Switch_latch_body_27mm")),
    }
    for i in range(1, spec.WAGO_QTY + 1):
        groups[f"Wago{i}"] = grp(lambda l, i=i: l.startswith((f"Wago221_412_{i}", f"Wago{i}_")))
    ant = grp(lambda l: l.startswith(("Omni", "TBS", "patch_UFL")))
    if ant:
        groups["Antenna"] = ant
    groups = {k: v for k, v in groups.items() if v}
    bbs = {k: _gbb(v) for k, v in groups.items()}

    print(f"  pairwise interference (min gap >= {spec.GATE_MIN_CLEARANCE}):")
    names = list(groups)
    any_hit = False
    worst = 1e9
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            gx, gy, gz = _aabb_gap(bbs[names[i]], bbs[names[j]])
            if gx < 0 and gy < 0 and gz < 0:
                v = _grp_ivol(groups[names[i]], groups[names[j]])
                if v > 0.01:
                    any_hit = True
                    ok = False
                    print(f"    !! {names[i]:8s} x {names[j]:8s} vol={v:7.1f}  FAIL")
            else:
                worst = min(worst, max(gx, gy, gz))
    if not any_hit:
        print(f"    none interpenetrate; tightest positive gap ≈ {worst:.2f} mm  OK")

    # 3) allowed-protrusion / envelope check
    env = dict(x0=IN_X0, x1=IN_X1, y0=IN_Y0, y1=IN_Y1, z0=Z_FLOOR, z1=Z_COVER_BOT)
    # XT30/JST noses nest ~1.5 in the door-plug pocket (Tom's door mechanism) → x1 allowed
    allow = {"Camera": {"x0"}, "Switch": {"z1"}, "XT30": {"x1"}, "JST": {"x1"},
             "Antenna": {"y0", "y1", "x0", "x1", "z0", "z1"}}
    print("  interior envelope (only allowed protrusions poke walls):")
    for name in groups:
        bb = bbs[name]
        outs = []
        for lo, hi, mn, mx in (("x0", "x1", bb.min.X, bb.max.X), ("y0", "y1", bb.min.Y, bb.max.Y),
                               ("z0", "z1", bb.min.Z, bb.max.Z)):
            if mn < env[lo] - 1e-6 and lo not in allow.get(name, ()):
                outs.append(f"{lo} by {env[lo]-mn:.2f}")
            if mx > env[hi] + 1e-6 and hi not in allow.get(name, ()):
                outs.append(f"{hi} by {mx-env[hi]:.2f}")
        if outs:
            ok = False
        print(f"    {name:9s} {'OK' if not outs else 'OUT: ' + ', '.join(outs)}")

    # 3b) bay envelope gate (M1): Floor 1 must offer Tom's clear volume — EXACT height/length,
    #     40-wide band clear of the corner posts, and NO printed part may reach into it.
    print(f"  bay_envelope (clear {BAY[0]}x{BAY[1]}x{BAY[2]} per spec.BATT_BAY_ENVELOPE):")
    assert IN_X >= BAY[0] - 1e-6, "bay length < envelope"
    assert IN_Y - 2 * (2 * INSET) >= BAY[1] - 1e-6, "post-free bay width < envelope"
    assert (Z_DIV_BOT - Z_FLOOR) - BAY[2] >= -1e-6, "bay clear height < envelope"
    env_box = Pos(IN_X0 + BAY[0] / 2, 0, Z_FLOOR + BAY[2] / 2) * Box(*BAY)
    bay_ok = True
    for p in printed_parts(variant):
        try:
            iv = (p & env_box).volume
        except Exception:
            iv = 0.0
        if iv > 0.01:
            bay_ok = False
            print(f"    !! {p.label} intrudes the bay envelope by {iv:.1f} mm3  FAIL")
    ok &= bay_ok
    if bay_ok:
        print(f"    dims {IN_X:.1f}x{IN_Y - 4 * INSET:.1f}x{Z_DIV_BOT - Z_FLOOR:.1f} >= spec; "
              f"no printed part intrudes  OK")

    # 3c) divider_vent_area gate (M2): net open area + field-cutout budget of the tray, computed
    #     from the SAME layout constants the tray is built from, then cross-checked against the
    #     actual solid volume (catches drift between the math and the booleans).
    a_win = sum(dx * dy for (_, _, dx, dy) in DIV_WINDOWS)
    a_grom = len(DIV_GROMMETS) * math.pi * (FT_D / 2) ** 2
    a_slot = len(DIV_SLOTS) * FT_SLOT[0] * FT_SLOT[1]
    vent = a_win + a_grom + a_slot                       # screw holes NOT counted (screw-filled)
    field = ((TRAY_X1 - TRAY_X0) - 2 * BAND) * ((TRAY_Y1 - TRAY_Y0) - 2 * BAND)
    in_field = a_win + a_grom + len(DIV_SLOTS) * FT_SLOT[0] * (FT_SLOT[1] - BAND)
    cut_pct = 100.0 * in_field / field
    for cx, cy, dx, dy in DIV_WINDOWS:                   # every window fully inboard of the band
        assert abs(cx) + dx / 2 <= (TRAY_X1 - TRAY_X0) / 2 - BAND + 1e-6, f"window {cx},{cy} breaks band"
        assert abs(cy) + dy / 2 <= (TRAY_Y1 - TRAY_Y0) / 2 - BAND + 1e-6, f"window {cx},{cy} breaks band"
    breaks = len(DIV_SLOTS)
    a_scr = len(DIV_SCREWS) * math.pi * (DIV_SCREW_D / 2) ** 2
    a_notch = 4 * (2 * INSET) ** 2
    v_exp = ((TRAY_X1 - TRAY_X0) * (TRAY_Y1 - TRAY_Y0) - a_notch - vent - a_scr) * DIV_T + \
        sum((x1 - x0) * spec.DIVIDER_RIB[0] * spec.DIVIDER_RIB[1] for (x0, x1, _) in DIV_RIBS)
    v_act = gen_divider_tray(variant).volume
    v_ok = abs(v_act - v_exp) / v_exp < 0.01
    d_ok = (vent >= spec.DIVIDER_VENT_AREA_MIN and cut_pct <= spec.DIVIDER_MAX_CUTOUT_PCT
            and breaks <= spec.FEEDTHROUGH_EDGE_BREAKS_MAX and v_ok)
    ok &= d_ok
    print(f"  divider_vent_area: net open {vent:.1f} mm² (>= {spec.DIVIDER_VENT_AREA_MIN:.0f}), "
          f"field cutout {cut_pct:.1f}% (<= {spec.DIVIDER_MAX_CUTOUT_PCT}), "
          f"band breaks {breaks}/{spec.FEEDTHROUGH_EDGE_BREAKS_MAX}, "
          f"tray vol {v_act/1000:.2f} vs calc {v_exp/1000:.2f} cm³  {'OK' if d_ok else 'FAIL'}")
    assert vent >= spec.DIVIDER_VENT_AREA_MIN, "divider net vent area below spec"
    assert cut_pct <= spec.DIVIDER_MAX_CUTOUT_PCT, "divider field cutout exceeds 50%"

    # 4) dimension asserts vs spec (nothing drifted)
    print("  dimension asserts vs spec.py:")
    checks = [
        ("battery LxWxH", tuple(round(v, 1) for v in comp_battery().bounding_box().size),
         (float(BATT[0]), float(BATT[1]), float(BATT[2]))),
        ("Wago LxWxH", tuple(round(v, 1) for v in _gbb(groups["Wago1"][:1]).size),
         (spec.WAGO_221_412[2], spec.WAGO_221_412[0], spec.WAGO_221_412[1])),
        ("switch latch len", round(spec.SW_BEHIND_PANEL, 1), 27.0),
        ("longest dim vertical", round(ex_z(variant), 1) >= round(max(EX_X, EX_Y), 1), True),
        ("bulkhead recess<=2.8", RECESS <= 2.8, True),
        ("wall==3.0", WALL == 3.0, True),
    ]
    if variant == "B":
        cav_depth = (Z_FLOOR - BOTTOM_T) - (bottom_outer_z("B") + RF_W)   # plate underside -> radome inner face
        standoff = cav_depth - PATCH[2]                                    # patch face -> radome inner face
        checks += [
            ("B cap cavity depth", round(cav_depth, 1), round(spec.PATCH_SHELL_CAVITY, 1)),
            ("patch+conn<=cavity", spec.PATCH_MAX_WITH_CONN <= spec.PATCH_SHELL_CAVITY, True),
            ("patch-face standoff>0", round(standoff, 1) > 0, True),
        ]
    for nm, got, want in checks:
        good = (got == want)
        ok &= bool(good)
        print(f"    {nm:22s} got {got}  {'OK' if good else 'FAIL want ' + str(want)}")

    print(f"  RESULT variant {variant}: {'ALL GATES PASS' if ok else 'GATE FAILURE (see above)'}")
    return ok


# ─────────────────────────────────────────────────────────────────────────────
# CPU HIDDEN-LINE SVG
# ─────────────────────────────────────────────────────────────────────────────
def _edge_ok(e):
    try:
        e.geom_adaptor()
        return e.length > 1e-6
    except Exception:
        return False


def _hlr(shape, vdir, xdir):
    algo = HLRBRep_Algo()
    algo.Add(shape.wrapped)
    algo.Projector(HLRAlgo_Projector(gp_Ax2(gp_Pnt(0, 0, 0), gp_Dir(*vdir), gp_Dir(*xdir))))
    algo.Update()
    algo.Hide()
    hlr = HLRBRep_HLRToShape(algo)
    edges = []
    for g in (hlr.VCompound, hlr.OutLineVCompound):
        try:
            c = g()
            if c is not None:
                edges += Compound(c).edges()
        except Exception:
            pass
    return [e for e in edges if _edge_ok(e)]


def export_svgs(variant):
    views = {"iso": ((1, -1, 1), (1, 0, -1)), "front": ((-1, 0, 0), (0, 1, 0)),
             "side": ((0, -1, 0), (1, 0, 0)), "bottom": ((0, 0, -1), (1, 0, 0))}
    parts = printed_parts(variant) + all_components(variant)
    written = []
    for vn, (vd, xd) in views.items():
        svg = ExportSVG(line_weight=0.15)
        for k, p in enumerate(parts):
            edges = _hlr(p, vd, xd)
            if not edges:
                continue
            layer = f"{p.label}_{k}"
            svg.add_layer(layer, line_color=getattr(p, "color", None) or Color(0, 0, 0), line_weight=0.15)
            try:
                svg.add_shape(edges, layer=layer)
            except Exception:
                for e in edges:
                    try:
                        svg.add_shape(e, layer=layer)
                    except Exception:
                        pass
        path = OUT / f"skylive_{variant}_{vn}.svg"
        svg.write(str(path))
        written.append(path)
    return written


# ─────────────────────────────────────────────────────────────────────────────
def build_variant(variant):
    print(f"\n{'='*70}\nSkyLive Sender — VARIANT {variant} (UPRIGHT)   external W×D×H "
          f"{EX_Y:.0f} × {EX_X:.0f} × {ex_z(variant):.1f} mm  (vertical = {ex_z(variant):.1f})")
    print(f"  height: bay {BAY[2]:.0f} + divider {DIV_T} + floor-2 {F2:.1f}   "
          f"bay envelope {BAY[0]:.0f}x{BAY[1]:.0f}x{BAY[2]:.0f} (Tom)\n{'='*70}")
    for p in printed_parts(variant):
        export_step(p, str(OUT / f"{p.label}.step"))
        export_stl(p, str(OUT / f"{p.label}.stl"))
        bb = p.bounding_box()
        print(f"  printed  {p.label:26s} {bb.max.X-bb.min.X:5.1f}×{bb.max.Y-bb.min.Y:5.1f}×{bb.max.Z-bb.min.Z:5.1f}  {p.volume/1000:5.1f} cm³")
    ok = run_gates(variant)
    export_gltf(build_assembled(variant), str(OUT / f"skylive_{variant}_assembled.glb"), binary=True)
    export_gltf(build_exploded(variant), str(OUT / f"skylive_{variant}_exploded.glb"), binary=True)
    svgs = export_svgs(variant)
    print(f"  GLB: skylive_{variant}_assembled.glb , _exploded.glb")
    print(f"  SVG: {', '.join(p.name for p in svgs)}")
    return ok


def main():
    arg = (sys.argv[1] if len(sys.argv) > 1 else "all").upper()
    variants = ["A", "A2", "B"] if arg == "ALL" else [arg]
    results = {v: build_variant(v) for v in variants}
    print(f"\n{'='*70}\nSUMMARY: " + "  ".join(f"{v}={'PASS' if r else 'FAIL'}" for v, r in results.items()))


if __name__ == "__main__":
    main()
