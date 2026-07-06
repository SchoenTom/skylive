"""SkyLive V3 — des Referenz-Prototyps Grundkörper 1:1 übernommen.

Referenz-Prototyp hat DIESEN Sender mit Tom entwickelt; jede Komponente hat bereits ihren perfekten Platz.
Wir übernehmen die Schale 1:1 (Grundkörper + Deckel) und bauen darauf auf:
  Schritt 1 (hier):  Baseline — importieren + als GLB sichtbar machen ("auf einen Stand kommen").
  Schritt 2 (folgt): unser Kamera-Fix 1:1 (Wölbung invertiert → flush + 4× M2 Senkkopf 13,5×17,5).
  Schritt 3 (folgt): Lüftungsschlitze einbauen.
  Schritt 4 (folgt): Akku-Bereich etwas schmaler → Gerät schmaler (dann Akku-Layout besprechen).

Roh-STEP ohne Feature-Historie → Änderungen laufen über Boolean-Chirurgie. des Referenz-Prototyps Look bleibt.
"""
import sys
import glob
from build123d import (import_step, Compound, Color, Pos, Rot, Box, Cylinder, Cone, mirror, Plane,
                       RectangleRounded, extrude, export_gltf, export_step)

REFERENZ = "/Users/tomschoen/Desktop/Projects/des Referenz-Prototyps prototy"
OUT = "/Users/tomschoen/Desktop/Projects/SkyDiveLive/CAD - models/skylive_out"
REFS = "/Users/tomschoen/Desktop/Projects/SkyDiveLive/CAD - models/references"

# des Referenz-Prototyps Wölbung im Grundkörper-Frame (aus Extraktion): bbox X6..37 (Mitte 21,5), Z0..28 (Mitte 14),
# Wandebene Y≈24,85, ragt +Y nach außen (Spitze ≈31,4). Kamera-Fix = Wölbung invertieren (nach innen).
# MITTIGER (Tom 2026-07-04): Linse+Schrauben auf die DOME-Mitte X21,5/Z14 zentriert (vorher X26/Z12,5
# = 4,5 mm aus der Mitte, vom M1-Agenten geflaggt).
CAM_CX, CAM_CZ, WALL_Y = 21.5, 14.0, 24.85


def invert_camera(gk, collar_wh=(27, 27), clear_ref=True):
    """Unser Kamera-Fix: flush außen + zentrierter symmetrischer Collar nach innen + Linsenfenster +
    2× M2-Zylinderkopf-Counterbore von außen (des Referenz-Prototyps Standard Ø2,4/Ø4,4). Parametrisch, damit dieselbe
    Chirurgie auf des Referenz-Prototyps GROSSER Schale UND der Minimal-Schale v3_min passt:
      collar_wh = (Breite X, Höhe Z) des Collars — an die Schale/das Stockwerk anpassen.
      clear_ref = des Referenz-Prototyps interne Kamera-Altlast freiräumen. Nur bei der VOLL-Schale nötig; die Minimal-
                    Schale hat keine → False (sonst durchstößt die Freiräum-Box die enge Oberwand)."""
    # 1) outward Wölbung flush (nur Y>WALL_Y entfernen) — bei der Minimal-Schale ohne Wirkung (nichts außen).
    gk = gk - Pos(21.5, WALL_Y + 4.0, 14.0) * Box(36, 8.0, 32)
    # 1b) des Referenz-Prototyps INTERNE Kamera-Altlast (Aussparung/Bosse an seiner X26) freiräumen — NUR Voll-Schale.
    if clear_ref:
        gk = gk - Pos(21.5, WALL_Y - 3.0 - 8.0, 14.0) * Box(40, 16.0, 34)
    # 2) SAUBERER SYMMETRISCHER Kamera-Collar nach INNEN (Tom: „Kamera optimal + symmetrisch, die zwei
    #    Ösen seitlich exakt auf gleicher Höhe"). Zentriert → links=rechts identisch, außen flush.
    cw, ch = collar_wh
    gk = gk + Pos(CAM_CX, WALL_Y - 6.0, CAM_CZ) * Rot(90, 0, 0) * \
        extrude(RectangleRounded(cw, ch, 4), 3.0, both=True)
    # 3) Linsenfenster Ø13,5 durch die (jetzt flache) Frontwand
    gk = gk - Pos(CAM_CX, WALL_Y - 1.5, CAM_CZ) * Rot(90, 0, 0) * \
        extrude(RectangleRounded(13.5, 13.5, 2.5), 6, both=True)
    # 4) REFERENZ KAMERA-SCHRAUBEN — KORRIGIERT 2026-07-04 (Tom: „zu nah an der Außenwand, Schraube passt
    #    nicht ins Loch, du hast Wandstärke + Zylinderkopf-Ø vernachlässigt, Spiegel zu früh gezogen").
    #    des Referenz-Prototyps echte Region (Render refcam_back) zeigt: 2 Bosse SEITLICH neben der Linse, Löcher
    #    zeigen nach AUSSEN (Achse Y, parallel zur Linse) — „Seitenklemme" = Seiten-BOSSE, Schraube aber
    #    VON AUSSEN. (Der frühere Agent hatte die X-Positionen 15,5/37 richtig, aber die Achse falsch.)
    #    → 2× M2 Zylinderkopf von der flush +Y-Front, Abstand 21,5, Counterbore Ø4,4×2,4 IN der
    #    Außenfläche (Kopf versinkt, Wand 3,0 → 0,6 PETG-Ledge unter dem Kopf), Schaft Ø2,4 durch
    #    Wand+Collar in die Kamera. Counterbore sitzt sauber IN der Wand, ragt NICHT ins Interieur.
    CB_R, SHAFT_R, CB_DEPTH = 2.2, 1.2, 2.4          # Ø4,4 Kopf-Senkung, Ø2,4 Schaft, 2,4 tief (Referenz-Prototyp)
    for hx in (CAM_CX - 10.75, CAM_CX + 10.75):      # 21,5 mm Abstand, flankieren das Linsenfenster
        # Schaft Ø2,4 von der Front nach innen (durch Wand + Collar in die Kamera-Frontlöcher)
        gk = gk - Pos(hx, WALL_Y - 8.0, CAM_CZ) * Rot(90, 0, 0) * Cylinder(radius=SHAFT_R, height=18.0)
        # Counterbore Ø4,4 × 2,4 in der flush Außenfläche (Zylinderkopf versenkt)
        gk = gk - Pos(hx, WALL_Y - CB_DEPTH / 2, CAM_CZ) * Rot(90, 0, 0) * Cylinder(radius=CB_R, height=CB_DEPTH)
    return gk


# ── M-A3 KAMERA FINAL (Tom 2026-07-05): Linse schaut RAUS, die tragende Ösen-Struktur hängt DRIN ──
# Quellen je Zahl: [REFERENZ] = KAMERA_MOUNT_DEFINITIV.md §2 (aus reference_camera_bulge.step gemessen);
# [NANO90] = offizielle HDZero_Nano90.stp, selbst vermessen 2026-07-05: Seitenlöcher Ø2,0 Achse X,
# je ±X-Flanke bei (Y=−4,0 / Z=0,0) = EXAKT auf Linsenachsen-Höhe; Linsenspitze Y=−14,5
# → Spitze→Seitenloch = 10,5. Kamera-Body 14,0 breit [NANO90+Tom].
CAM_TIP2HOLE = 10.5    # Linsenspitze → Seitenloch-Achse                                  [NANO90]
CAM_FLK_OUT  = 10.75   # Flanken-Außenflächen ±10,75 → Spanne 21,5                        [REFERENZ]
CAM_FLK_T    = 2.0     # Flanken-Platte 2,0 (Referenz-Prototyp X 15,5..17,5)                          [REFERENZ]
CAM_BOSS_R   = 4.2     # Ösen-Boss Ø8,4 („Wölbung")                                       [REFERENZ]
CAM_BOSS_H   = 1.25    # Boss steht 1,25 von der Platte zur Kamera vor (Referenz-Prototyp 17,5..18,75) [REFERENZ]
CAM_CLAMP    = 7.5     # Klemmflächen ±7,5 → 15,0 licht (Kamera 14 + 0,5/Seite)            [REFERENZ]
CAM_SHAFT_R  = 1.2     # Schaft Ø2,4                                                      [REFERENZ]
CAM_CB_R     = 2.35    # Counterbore Ø4,7: Referenz-Prototyp Ø4,4 + 0,3 „problemlos"-Reserve   [REFERENZ+Reserve]
CAM_CB_D     = 2.6     # CB-Tiefe 2,6: Referenz-Prototyp 2,4 + 0,2 Reserve (M2-DIN912-Kopf h=2,0) [REFERENZ+Reserve]


def camera_final(gk, clear_ref=False, recess=0.5):
    """Toms finale Kamera-Lösung: (a) Außenwand flush + Linsenfenster 13,5×13,5 R2,5 (bewährt),
    Linse schaut RAUS (Spitze `recess`=0,5 hinter der Außenfläche [Design-Wahl: snag-arm +
    Kratzschutz]); (b) des Referenz-Prototyps tragende Ösen-Geometrie NACH INNEN: 2 Flanken-Platten mit Ø8,4-
    Bossen, 2 Quer-Löcher Achse X auf Linsen-Mitte, Spanne 21,5 — Querschnitt exakt des Referenz-Prototyps
    gemessene Maße, nur die Loch-Y-Position folgt der [NANO90]-Kamera (Spitze→Loch 10,5), damit
    die Linse wirklich bündig sitzt. Innen je ein Ø4,7×2,6-CB → M2-Zylinderkopf versenkt
    problemlos. KEIN flacher Collar — die Ösen tragen. CAD-Check ≠ empirischer Test."""
    y_hole = WALL_Y - recess - CAM_TIP2HOLE          # 13,85: Seitenloch-Achse (wandrelativ)
    # (1) außen flush räumen (bei der Minimal-Schale wirkungslos) + optional des Referenz-Prototyps Altlast
    gk = gk - Pos(CAM_CX, WALL_Y + 4.0, CAM_CZ) * Box(36, 8.0, 32)
    if clear_ref:
        gk = gk - Pos(CAM_CX, WALL_Y - 3.0 - 8.0, CAM_CZ) * Box(40, 16.0, 34)
    # (2) Flanken-Platten: von 1,15 in der Wand (Schweiß-Union) bis Boss-Unterkante nach innen
    y_in, y_deep = WALL_Y - 3.0 + 1.15, y_hole - (CAM_BOSS_R + 0.3)
    for s in (-1, +1):
        px = CAM_CX + s * (CAM_FLK_OUT - CAM_FLK_T/2)
        gk = gk + Pos(px, (y_in + y_deep)/2, CAM_CZ) * Box(CAM_FLK_T, y_in - y_deep, 12.0)
        gk = gk + Pos(CAM_CX + s * (CAM_CLAMP + CAM_BOSS_H/2), y_hole, CAM_CZ) * \
            Rot(0, 90, 0) * Cylinder(radius=CAM_BOSS_R, height=CAM_BOSS_H)   # Öse/„Wölbung" innen
    # (3) Linsenfenster durch die Wand (bewährtes Maß 13,5×13,5 R2,5)
    gk = gk - Pos(CAM_CX, WALL_Y - 1.5, CAM_CZ) * Rot(90, 0, 0) * \
        extrude(RectangleRounded(13.5, 13.5, 2.5), 6, both=True)
    # (4) Quer-Bohrung Ø2,4 Achse X durch beide Flanken + Ösen (eine gemeinsame Achslinie, Referenz-Prototyp)
    gk = gk - Pos(CAM_CX, y_hole, CAM_CZ) * Rot(0, 90, 0) * Cylinder(radius=CAM_SHAFT_R, height=26)
    # (5) M2-Zylinderkopf-Counterbores auf den Platten-AUSSENSEITEN (= Case-INNENSEITE, Tom)
    for s in (-1, +1):
        gk = gk - Pos(CAM_CX + s * (CAM_FLK_OUT - CAM_CB_D/2), y_hole, CAM_CZ) * \
            Rot(0, 90, 0) * Cylinder(radius=CAM_CB_R, height=CAM_CB_D)
    return gk


def _find(pattern):
    hits = glob.glob(f"{REFERENZ}/{pattern}")
    if not hits:
        raise FileNotFoundError(pattern)
    return hits[0]


def load_shell():
    body = import_step(_find("Grundk*.STEP"))
    deckel = import_step(_find("Deckel.STEP"))
    return body, deckel


def report(body, deckel):
    for name, part in (("Grundkörper", body), ("Deckel", deckel)):
        b = part.bounding_box()
        print(f"{name:12s} bbox  X {b.min.X:7.1f}..{b.max.X:7.1f}   "
              f"Y {b.min.Y:7.1f}..{b.max.Y:7.1f}   Z {b.min.Z:7.1f}..{b.max.Z:7.1f}")


if __name__ == "__main__":
    body, deckel = load_shell()
    report(body, deckel)
    body = invert_camera(body)     # unser Fix auf des Referenz-Prototyps echter Wölbung
    from OCP.BRepCheck import BRepCheck_Analyzer
    print("Nach Kamera-Inversion — IsValid:", BRepCheck_Analyzer(body.wrapped).IsValid(),
          "| Solids:", len(body.solids()))
    body.color = Color(0.82, 0.82, 0.85)
    asm = Compound(label="SkyLive_V3_Ref_invcam", children=[body])
    glb = f"{OUT}/skylive_V3_ref.glb"
    export_gltf(asm, glb, binary=True)
    print(f"\nGLB (Referenz-Prototyp + invertierte Wölbung): {glb}")
