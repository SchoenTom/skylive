"""SkyLive MINI-300 — Parameter-Fork von v3_min.py (Stand v3_min 2026-07-05 11:05, alle Gates grün).

  FORK-GRUND: Prototyp-2 mit Tattu 300 mAh 3S HV (GEMESSEN Tom: 45×17,5×15,3). Der 850er-Bau
  (v3_min.py) bleibt unangetastet; hier ist NUR die Konstanten-Sektion + einige an X_WALL_IN=32,5
  hart gebundene Tür-Boss-Literale + die batterie-absoluten Gate-Schranken geändert. Alle
  FUNKTIONS-Rümpfe sind 1:1 aus v3_min (parametrisch über die Modul-Konstanten). Maßketten-Quelle:
  MINI_300_SPEC.md (CEO-Rechnung 2026-07-05). Herleitung jeder geänderten Zahl unten am Feld.

  DELTA gegenüber v3_min (Maßkette, alles begründet — keine Schätzung):
    IN_X 65→53,5 · BAY_H 25→17 · CAM_OFF_X −9→−15,5 (X-Konflikt gelöst, Spec) · Außen 71×39,5×54 → 59,5×39,5×46.
    Akku-Klappe 31,5×24 → 19×16 · Bay-Führung licht 30,75×23,75 → 18,25×16,05 (Akku+0,75-Regel).
    Tür-Kleinteile (Nasen/Snaps/DOOR_R) für die schmale 19-mm-Tür neu abgeleitet (straight-edge-Budget).
    Deckel-Vents 4×→5× (Spec: +20 % Auslass oben) · Shelf-Cutout 12→8 (VTX-Klebefläche halten).

M1-Inhalt (genau das):
  1. Hohle gerundete GoPro-Style-Schale in den V3-Zielmaßen (outer RectangleRounded − inner).
  2. Akku-Klappen-Öffnung an der +X-Stirnseite, unteres Stockwerk (Bay-Höhe).
  3. Kamera auf der -Y-Langseite: invert_camera() aus anton_v3.py 1:1 wiederverwendet,
     re-platziert auf die -Y-Wandebene der Minimal-Schale (Wölbung nach INNEN, flush außen,
     Linsenfenster + Seitenklemme 2× M2 QUER/Achse X, 21,5 mm).

Ehrlich: die Prüfungen unten sind CAD-/Boolean-Checks (Watertight/IsValid/bbox),
KEIN empirischer Test. Werte ohne Quelle → MEASURE_ME.
"""
import math
from build123d import (RectangleRounded, Box, Pos, Rot, Color, Compound, Polygon,
                       Plane, Cylinder, Cone, extrude, export_gltf, fillet)
from anton_v3 import (camera_final, WALL_Y, CAM_TIP2HOLE, CAM_FLK_OUT,   # M-A3: Toms finale
                      CAM_CLAMP, CAM_CB_R, CAM_CB_D)                     # Kamera-Lösung (Ösen innen)

# Anton-Wölbungs-bbox (gemessen aus references/Anton_camera_bulge.step):
#   X 6..37 (Mitte 21,5) · Y 24,90..31,40 (Wandebene 24,85, ragt +Y außen) · Z 0..28 (Mitte 14)
BULGE_XC, BULGE_ZC = 21.5, 14.0

# M1 · KAMERA ZUR ECKE (CEO-Entscheidung nach Antons realem Druck, Fotos proto_8380/8382:
#   Kamera sitzt an der -X-Ecke — mittig (X=0) lässt dem VTX daneben KEINEN Platz).
#   Kamera-Zentrum von X=0 → X=−9 (Richtung −X-Ecke). Mechanik: in graft_camera bekommt die
#   Transform-Translation X = BULGE_XC + CAM_OFF_X; wegen Rot(0,0,180) landet die Linsen-Mitte
#   (Anton-Frame CAM_CX=BULGE_XC) bei my-X = (BULGE_XC+CAM_OFF_X) − CAM_CX = CAM_OFF_X = −9.
#   Numerisch verifiziert im Gate unten (Fenster-Scan der −Y-Wand).
CAM_OFF_X = -15.5       # [MINI Spec §X-Konflikt] Kamera weiter in die −X-Ecke: bei Innen-X 53,5 passt
                        #   Kamera-Ecke+VTX nur bei Zentrum −15,5 (Flanken bis −4,75, VTX −4,25…25,45 ≤ 26,75).
                        #   −X-Flanke −26,25 > −X-Innenwand −26,75 (0,5 Rest). (v3_min: −9,0)

# ── V3-ZIELMASSE (aus V3_SPEC.md / Auftrag, KEINE Schätzungen) ───────────────
WALL   = 3.0                  # sakrosankt
IN_Y   = 33.5                 # Innenbreite (Tom 2026-07-05: „33–34 ok; 32 ginge, aber Puffer für
                              #   aufgeblähte Akkus lassen") → außen 39,5. Maßkette: Akku 30 + 1,75/Seite;
                              #   VTX liegend 30 (Y) [STEP] + Kabelweg; Kamera-Ösen-Spanne 21,5 läuft
                              #   längs X (nicht Y) und ist davon unberührt (21,5 < 33,5 ohnehin ✓).
BAY_L  = 53.5                 # [MINI Spec §X] Innen-X. Akku 45 + XT30-Raum längs; die Akku-FÜHRUNG
                              #   endet per Rippen-Anschlag bei 50,5 (Toms 50–52-Fenster), Rest = XT30-Raum
                              #   wie beim 850er. 53,5 löst den Stockwerk-2-X-Konflikt (Kamera+VTX). (v3_min: 65)
BAY_H  = 17.0                 # [MINI Spec §Z] Akku 15,3 + 0,75 Swell/Druck-Luft + 0,95 Boden-Rippe ≈ 17.
                              #   Kette geprüft: RAIL_H=(BAY_H−OPEN_Z)/2=0,5 · STRIP_T=BAY_H/2+OPEN_Z/2−GUIDE_Z=0,45
                              #   (beide >0 wie 850er). Interior-Z=40, außen 46 (−8). (v3_min: 25)
SHELF_T = 3.0                 # Stockwerk-Shelf (fest verbaut, kommt erst in M4 — M1 nur Hohlraum)
F2_H   = 20.0                 # Elektronik-Stockwerk Höhe (M-A2, Maßkette statt Schätzung):
                              #   Treiber = Kamera-Körper H 19,0 [Tom-Messschieber, spec.py CAM_BODY;
                              #   offizielle STEP sagt 18,0 → konservativ 19,0] + 2×0,5 Einbau-Luft
                              #   [Design-Wahl] = 20,0. VTX liegend 14,1 [STEP] + Pad 1,5 [spec
                              #   THERMAL_PAD_T] + U.FL mated 2,4 [spec] = 18,0 < 20 ✓.
FIL_O, FIL_I = 9.0, 6.0       # Ecken-Radien außen/innen (GoPro-Look)

IN_X = BAY_L                              # Innentiefe (X)
IN_Z = BAY_H + SHELF_T + F2_H             # Innenhöhe = 50
EX_X, EX_Y, EX_Z = IN_X + 2*WALL, IN_Y + 2*WALL, IN_Z + 2*WALL   # 71 × 44 × 56

# Kamera-Mitthöhe (Z) = Mitte des Elektronik-Stockwerks im Schalen-Frame (Ursprung zentriert)
Z_INT_BOTTOM = -EX_Z/2 + WALL             # Innenboden
Z_CAM = Z_INT_BOTTOM + BAY_H + SHELF_T + F2_H/2   # = 14.0 (Mitte oberes Stockwerk)

# ── Akku-Klappe: BÜNDIGER Falz (Rebate) + Schalen-Plug-Tür ────────────────────
#   Prinzip [v2-Präzedenz skylive_sender_v2.py]: äußerer Senk-Sitz (Flansch) breiter als innerer
#   Durchbruch → Schulter stoppt Einwärtsfallen; Flansch-Außenfläche = Schalen-Außenkontur (Plug),
#   Überstand = 0 (Tom: bündig, snag-frei). Herleitung siehe KLAPPE_ZU_MODELL_BRIDGE.md.
#   V3-Besonderheit: +X-Face nur EX_Y-2*FIL_O = 26 mm flach (R9-Ecken), Öffnung aber >30 (Akku 30)
#   → Tür MUSS Plug sein (Aussenfläche folgt R9), keine plane Senkung wie v2 (dort 45 mm flach).
REBATE_D   = 1.5          # Flansch-Tiefe = halbe Wand (aussen)               [v2-Präzedenz]
REBATE_LAP = 1.9          # Schulter-Lap je Seite                            [v2-Präzedenz]
TOL_SLIDE  = 0.3          # Gleitspiel Tür<->Falz je Seite                   [spec.py TOL_SLIDE]
DOOR_R     = 4.0          # [MINI] Tür-Innen-Eckradius reduziert (v3_min: FIL_O=9): bei der schmalen 19-mm-Tür
                          #   fräst R9 (Zunge-Eck 7,1) das ganze Straight-Edge-Budget weg → Nasen/Snaps hätten
                          #   keine gerade Anlagekante. R4 (Zunge-Eck 2,1) → gerade Unter/Oberkante |Y|<7,4.
                          #   Der Flansch folgt weiter der Schalen-R9 (kommt aus outer&region, nicht aus DOOR_R).
OPEN_Y = 19.0             # [MINI Spec] Durchbruch-Breite (Y): Akku 17,5 + 1,5 Handling; > Führung 18,25, < IN_Y 33,5.
OPEN_Z = 16.0             # [MINI] Durchbruch-Höhe (Z): Akku 15,3 + 0,7 Handling; = BAY_H−1 hält RAIL_H=0,5 (850er-
                          #   Invariante; Spec-Wunsch 17 = BAY_H würde RAIL_H auf 0 setzen → Boden-Schienen degeneriert).
DOOR_FACE_X = EX_X/2      # Tür-Aussenfläche-Sollebene (bündig) = 35.5
X_WALL_IN   = IN_X/2      # innere Wandfläche +X = 32.5
X_SHOULDER  = X_WALL_IN + REBATE_D   # Schulter-Ebene = 34.0 (Zunge innen / Flansch aussen)
Z_BAY_MID   = Z_INT_BOTTOM + BAY_H/2 # Öffnungs-Mitte Z = -12.5
CB_Y = OPEN_Y + 2*REBATE_LAP         # Senkungs-/Flansch-Breite = 35.3
CB_Z = OPEN_Z + 2*REBATE_LAP         # Senkungs-/Flansch-Höhe   = 27.8
# Dokumentierte Wand-Ausnahme (M-A2): seitliches Falz-Land der +X-Wand = (EX_Y−CB_Y)/2 = 2,1 in der
#   ÄUSSEREN Wandhälfte (Senkungs-Tiefe 1,5) — kein freistehender 3,0-Pfad, liegt auf dem Tür-Flansch auf.
# Tür-Halt: bündiger Falz (Schulter auf allen 4 Seiten, verhindert Kippen/Einfallen) + obere
#   M2-Schraube (verhindert Herausziehen). Die früheren Nasen+Fanglippen wurden ENTFERNT
#   (M-A1 2026-07-05, dokumentiert): die Lippen standen bei Z −23..−21,8 / Y 5,5..14,5 mitten im
#   Akku-Einschub-Querschnitt (Akku 30×23 wäre blockiert gewesen) und die Nasen passten geometrisch
#   nicht durch den R7,1-Eckradius des inneren Durchbruchs. Kein Kaschieren: Funktion (unten zuerst
#   einsetzen → kippen → oben schrauben) leistet der Falz selbst.
DOOR_SCREW_Z  = Z_BAY_MID + OPEN_Z/2 - 2.0  # Schraube oben an der Klick-Kante        [abgeleitet]

# ── M2 · KLAPPE PERFEKT (Hybrid-Schwenk, KLAPPE_PERFEKT_PLAN.md Phase 2) ───────────────
#   CEO-entschieden (= Toms Fernbedienungs-Prinzip): Falz-Lap NUR ±Y (Plug-Optik + Einwärts-Stopp),
#   oben auf LAP_RELIEF_Z auslaufend; ±Z-Kanten LAP-FREI (plane Stoßkante) → Schwenk um Y frei.
#   2 Nasen bei Y±6 greifen UNTER die Akku-Ebene (Z<RAIL_TOP=−23,5) in Boden-Taschen; Haken 1,0.
#   Der Akku-Kanal (GUIDE_CLEAR 30,75×23,75) bleibt HEILIG — Gate. Alle „Gates" = CAD/Boolean, kein Test.
LAP_RELIEF_Z = 5.0        # ±Y-Lap läuft im oberen 5-mm-Band auf 0 aus (obere Ecken frei beim Einschwenken) [berechnet]
LEAD_IN      = 0.5        # 0,5×45°-Lead-in an den lap-freien ±Z-Stoßkanten                                 [Design-Wahl]
TONGUE_LEAD  = 1.5        # 1,5×45°-Lead-Chamfer an der Zungen-Oberkante (inboard) für den Einschwenk-Bogen [CEO 2026-07-05]
# Klick-Cantilever (PETG) an der Tür-Oberkante — NUR Vorpositionierung/Klick, Haltekraft trägt die Schraube:
SNAP_L, SNAP_T, SNAP_H = 9.0, 1.2, 0.6    # L9 · Basis t1,2 · Hinterschnitt/Auslenkung 0,6 → ε=1,5·t·h/L²=1,33 %<1,5 % [berechnet]
SNAP_W  = 3.0             # [MINI] Feder-Breite (Y) schmaler (v3_min: 6): schmale Tür, muss zwischen M2-Boss (±3,5)
                          #   und gerader Oberkante (|Y|<7,4) passen.
# ZWEI Snaps seitlich (Kollisionsfix 2026-07-05): EIN Mittel-Snap (Y=0) schlägt prinzipiell auf den
#   M2-Boss (beide Y=0). Fernbedienungs-üblich → 2 Snaps bei Y=±10,5 (symmetrisches Klicken), rechts/links
#   vom Boss (Y±3,5) und in der Öffnungs-Breite (|Y|<15,75). Body-Taschen als Einschwenk-Kanäle (s.u.).
SNAP_Y  = (-5.5, 5.5)     # [MINI] seitlich, boss-frei: Snap 4..7 (SNAP_W 3) → clear vom Boss (±3,5), in gerader
                          #   Oberkante (|Y|<7,4). (v3_min: ±10,5 lag außerhalb der schmalen 19-mm-Öffnung)
# Nasen (Weg A: unter der Akku-Ebene, in Boden-Taschen; Startwerte MEASURE_ME an Antons Realteil):
NASE_Y  = (-4.0, 4.0)     # [MINI] Y-Lage: gerader Teil der Unterkante (|Y|<7,4=9,5−R2,1 Zunge-Eck), Foot 2..6.  [berechnet]
NASE_W  = 4.0             # [MINI] Nasen-Breite (Y) → Y±2. Catch-X (19,45..26,75) liegt hinter RAIL_X1=18 → keine Schienen-Kollision [berechnet]
NASE_L  = 5.0             # Finger-Länge nach −X (in die Boden-Tasche)                                       [Plan-Startwert/MEASURE_ME]
NASE_T  = 1.2             # Finger-Dicke (Z)                                                                 [Plan/MEASURE_ME]
HOOK    = 1.0             # Haken-Übergriff: Lippe übergreift den Nasen-Kopf 1,0 (Lift-Sperre)               [Plan]
NASE_TOP = Z_INT_BOTTOM - 0.1            # Nasen-Oberkante 0,1 unter Innenboden → sicher unter Akku (RAIL_TOP −23,5)
FIN_BOT  = NASE_TOP - NASE_T             # Finger-Unterkante = −25,3
FIN_XIN  = X_WALL_IN - NASE_L - HOOK     # Finger −X-Spitze = 26,5 (NASE_L Finger + HOOK-Kopf)
NOTCH_BOT = FIN_BOT - 0.1               # Breach-Notch-Boden (Fuß-Durchgang unter die Öffnung) = −25,4
CATCH_SWING_CLR = 0.4                   # [Kollisionsfix (c) 2026-07-05] Kopf-Kammer-Boden 0,4 tiefer:
                                        #   beim −ang-Einschwenken taucht der Haken-Kopf bis ~Z−25,72,
                                        #   der 0,6-mm³-Rest-Kontakt am Kammer-Boden wird so freigestellt.
POCKET_X0 = FIN_XIN - 1.0               # Boden-Tasche −X-Ende = 25,5
LIP_TOP  = (Z_BAY_MID - OPEN_Z/2) - 0.1  # Haken-Lippe Oberkante = −23,6 (0,1 unter Akku RAIL_TOP — MEASURE_ME: knapp)
# M2-ZYLINDERKOPF DIN912 (Projektstandard) durch die Zunge in einen Schalen-Boss, CB im verdickten Pad:
DOOR_PAD_T   = 4.0        # lokal verdicktes Tür-Pad an der lap-freien Oberkante (Flansch 1,5 + Boss 2,5)    [Plan 2.5]
DOOR_CB_R    = 2.1        # Counterbore Ø4,2 (M2-Kopf Ø3,8 + Spiel)                                          [Plan 2.5]
DOOR_CB_D    = 2.2        # CB-Tiefe (Kopf h2,0 + 0,2) → Rest-Boden DOOR_PAD_T−2,2 = 1,8 tragend            [Plan 2.5]
DOOR_THRU_R  = 1.2        # Durchgang Ø2,4 durch die Zunge                                                   [Plan 2.5]
DOOR_PILOT_R = 0.8        # Pilot Ø1,6 selbstschneidend im Schalen-Boss (M2)                                 [Plan 2.5]
GRIP_W, GRIP_D = 12.0, 2.0  # Daumen-Mulde 12(Y)×2,0 tief (subtraktiv, bleibt in der bündigen Hülle)        [Plan 2.6]
# [MINI] Parametrisierung des in v3_min hart auf 31,2 gesetzten Tür-Boss-Endes (galt für X_WALL_IN=32,5).
#   Boss endet 0,3 vor der Tür-Pad-Innenfläche (DOOR_FACE_X − DOOR_PAD_T). Mini: 29,75−4−0,3 = 25,45.
DOOR_BOSS_END_X = DOOR_FACE_X - DOOR_PAD_T - 0.3

# ── M-A1 · AKKU-BAY-FÜHRUNG (Spec §3: „Akku darf nicht bummeln", Tom 2026-07-05) ──────
#   Ziel-Lichtmaße am Akku 60×30×23 [Tattu 850, genstattu/spec.py]: Y 30,5–31,0 / Z 23,5–24,0.
#   Minimal-Anlage (Tom: „weniger ist mehr"): 3 Boden-Schienen + 2 Decken-Leisten + 2 Rippen-Paare.
#   Alles hinter der Tür-Öffnung (x ≤ 30,5 < X_WALL_IN) → Durchgang bleibt frei.
GUIDE_CLEAR_Y = 18.25   # [MINI] lichte Führungsbreite [Spec Fenster 18,0–18,5; Akku 17,5 + 0,75-Regel]
GUIDE_CLEAR_Z = 16.05   # [MINI] lichte Führungshöhe    [Spec Fenster 15,8–16,3; Akku 15,3 + 0,75-Regel]
RAIL_TOP = Z_BAY_MID - OPEN_Z/2       # Schienen-Oberkante = Breach-Unterkante → Akku gleitet EBEN ein
RAIL_H   = RAIL_TOP - Z_INT_BOTTOM    # = (BAY_H-OPEN_Z)/2, parametrisch (0,5)
RAIL_W, RAIL_Y = 3.0, (0.0, -6.0, +6.0)     # [MINI] 3 Schienen unter dem 17,5er-Akku (Rail@6=4,5..7,5<8,75) [Design]
RAIL_X0, RAIL_X1 = -IN_X/2 + 2.0, 18.0      # [MINI] RAIL_X1=18 endet VOR der Catch-Zone (19,45..) → Nasen frei von Schienen
STRIP_BOT = RAIL_TOP + GUIDE_CLEAR_Z        # Decken-Leisten-Unterkante (definiert lichte Höhe)
STRIP_T   = (Z_INT_BOTTOM + BAY_H) - STRIP_BOT   # Rest bis Shelf-Unterseite (MINI: 0,45)
STRIP_X0, STRIP_X1 = -11.0, 11.0            # [MINI] mittig; ±X-Shelf-Aussparungen (13,75..21,75) bleiben frei
STRIP_Y_IN = 6.0                            # [MINI] Leisten-Innenkante nach innen (v3_min: 11): schmaler Akku (±8,75)
                                            #   → Leisten müssen bis Y6 reichen, um die Akku-Oberkante (Y6..8,75) zu halten
RIB_FACE = GUIDE_CLEAR_Y / 2                # Rippen-Anlageflächen bei Y = ±9,125 (Akku 17,5 + 0,375/Seite)
RIB_W    = 3.5
RIB_X    = (-18.0, +20.0)   # [MINI] 2 Paare, vent-spalten-frei (|X|<6-Spalte der +Y-Wand nicht geschnitten) und
                            #   max+RIB_W/2+2=23,75 ≤ X_WALL_IN 26,75 (Rippe nicht in Tür-Öffnung).
RIB_EMBED = 0.3             # Schweiß-Überlappung in die Wand (union)


# ── MB1 · DECKEL (Stockwerk-2-Seitendeckel +Y) — NEUES PRINZIP (Audit 2026-07-05) ────────────
#   AUDIT-BEFUND: die alten 4 Y-Achs-Insert-Bosse ragten 954 mm³ in den VTX-Envelope (VTX braucht
#   30 von 33,5 in Y). NEU (Prinzip vom Fix-Team): KEINE Innenraum-Bosse. Retention =
#     · unten 2 Einhänge-Nasen (Haken in Body-Falz-Taschen, an der +Y-Wand, Z<1, VTX-frei)
#     · oben 2× M3 VERTIKAL (Z) von außen durch die Decke (+Z) in Inserts in DECKEL-OHREN.
#   MINI-ANPASSUNG (dokumentiert): der Mini hat über der VTX-Deckfläche (Z18,6) bis zur Decke (Z20)
#   nur 1,4 mm → ein nach −Y ragendes Ohr passt NUR in der freien LINKS-Zone (X<−4,75, VTX-frei;
#   Kamera liegt bei Y<−0,75 → Y>0-Ohr ist auch kamera-frei). Beide Ohren daher links; die rechte
#   Deckel-Hälfte trägt der Plug-Falz + die untere Nase. VTX-Envelope-Gate erzwingt Kollisionsfreiheit.
LID_Y_OUT = EX_Y/2                              # +Y-Außenfläche 19,75 (Deckel bündig)          [Geometrie]
LID_Y_IN  = IN_Y/2                              # +Y-Wand-Innenfläche 16,75                     [Geometrie]
LID_Y_MID = (LID_Y_IN + LID_Y_OUT)/2           # Wand-Mittelebene 18,25 (Falz-Schulter)        [Geometrie]
LID_HX    = 17.0                                # [MINI] Öffnungs-Halbbreite X → 34; +LID_LAP=19 ≤ Flachzone 20,75 (v3_min: 22)
LID_Z0    = Z_INT_BOTTOM + BAY_H + SHELF_T + 1.0   # Shelf-Oberkante +1 = +5   [Spec §4 „Shelf-Oberkante“]
LID_Z1    = (EX_Z/2 - WALL) - 1.0                  # Innendecke −1 = +23       [Spec §4 „Innendecke +27−WALL“]
LID_R     = 3.0                                 # Öffnungs-Eckradius (weich, > Boss-Kollision)  [Design]
LID_LAP   = 2.0                                 # Falz-Überlapp je Seite (Schulter/Einwärts-Stopp) [Tür-Präzedenz REBATE_LAP]
LID_REB_D = 1.5                                 # Falz-Tiefe = halbe Wand (außen)                [Tür-Präzedenz REBATE_D]
COVER_PLATE_T = 3.0                             # Deckel-Grundplatte (bündig, = Wand)            [Spec §4/MB1 „~3,0“]
COVER_PAD_H   = 1.5                             # Schrauben-Pad nach innen (Platte 3,0 + 1,5 = 4,5 für M3-CB) [Spec §4 „~4,5“]
# OBERE OHREN (2×, VERTIKALES M3-Insert Z-Achse): Ohr = Block an der Deckel-Zunge, ragt −Y in die
#   freie Links-Zone; vertikales Insert Ø4,6 von der Decken-Unterseite (Z20) nach unten.
LID_INS_D    = 4.6                              # M3-Insert-Bohrung (Ø5-Insert −0,4 Rändel)      [Spec §4]
LID_INS_DP   = 6.0                              # Insert-Bohrtiefe (Z, nach unten) — Mini-Z-Budget [MINI, v3_min 8]
LID_INS_CHAM_D = 5.2                            # Einführfase-Ø an der Decken-Unterseite          [Spec §4]
LID_EAR_D    = 9.0                              # Ohr-Ø um das Insert (Wand (9−4,6)/2=2,2 ≥2,0)  [Spec §4]
LID_EAR_X    = (-13.5, -9.5)                    # [MINI] 2 Insert-X, beide in der Links-Zone; ein gemeinsamer Ohr-Block
                                               #   X−17..−5 (Insert-Umwand ≥2,2; +X-Kante −5 < −4,75 → VTX-frei)
LID_EAR_TOP  = EX_Z/2 - WALL                    # Ohr-Oberkante = Decken-Unterseite = 20
LID_EAR_BOT  = LID_EAR_TOP - (LID_INS_DP + 1.0) # Ohr-Unterkante = 13 (Insert 6 + 1 Boden)
LID_EAR_YC   = 12.5                             # Ohr-/Insert-Y-Mitte: Y8..17 (mit Ø9), Y>−0,75 kamera-frei, verbindet an Zunge (16,75)
# M3-Decken-Durchgang (Spec §8): vertikal (Z) von +Z-Außen; CB versenkt.
LID_THRU_D = 3.4                               # M3-Schaft-Durchgang durch die Decke             [Spec §8]
LID_CB_D   = 6.1                               # CB-Ø (Kopf Ø5,5 + 0,6 Spiel)                   [Spec §8]
LID_CB_DP  = 3.4                               # CB-Tiefe (Kopf h3,0 + 0,4)                     [Spec §8]
# UNTERE EINHÄNGE-NASEN (2×): Haken an der Deckel-Unterkante, greift in Body-Falz-Tasche unter der Öffnung.
LID_NASE_X   = (-11.0, 11.0)                    # Nasen-X (spannt die Unterkante; Y an der Wand → VTX-frei)
LID_NASE_W   = 6.0                             # Nasen-Breite (X)
LID_NASE_DROP = 3.0                            # Nase ragt unter die Öffnungs-Unterkante (Z1 → Z−2)
LID_NASE_HOOK = 1.2                            # Haken-Übergriff −Y unter die Body-Ledge (Auszugssperre)
LID_NASE_TOL = 0.3                             # Gleitspiel Nase↔Tasche


# ── MB3 · LÜFTUNGSSCHLITZE — NEUE §6b-Matrix (VERBINDLICH, ersetzt die alten +Y-Bänder) ────────
#   Schlitz-Norm: 1,1 (schmal) × L (lang), 45°-Louver abwärts-auswärts (selbsttragend + Tropfenschutz).
#   Freie Fläche je Schlitz = 1,1 × L. Kamin (Einlass unten → Auslass oben). Alle Kollisions-Verbote
#   der Matrix werden VOR dem Schneiden numerisch geprüft (Gate). Louver-Achse = Schlitz-Längsachse.
VENT_W       = 1.1           # Schlitz-Schmalmaß (Spalt)                        [Spec §6b]
VENT_LOUVER_DEG = 45.0       # abwärts-auswärts                                 [Spec §6/§6b]
VENT_THROUGH = 5.0           # Cutter-Tiefe entlang 45°-Achse (>Wand/cos45=4,24; knapp, minimaler Überschuss
                             #   → kein falscher Feature-Überlapp im Kavität-Überstand)
VENT_XFLAT = EX_X/2 - FIL_O  # +Y/±Z-Flachzone entlang X = 26,5 (Eckradien FIL_O ausgenommen)
VENT_YFLAT = EX_Y/2 - FIL_O  # ±X-Flachzone entlang Y = 10,75

# Zone-Definitionen: (Achse, L, feste Koordinaten je Schlitz). „louver_axis" = Rotationsachse (= Länge).
#  Deckel (+Y, im COVER-Teil): 4×(1,1×20) oben, Länge X, gestapelt in Z, boss-frei |X|<13, boss-Z-frei.
VENT_DECKEL_L = 20.0
VENT_DECKEL_Z = (5.0, 8.0, 11.0, 14.0, 17.0)  # [MINI Spec §Airflow] 5 Reihen (statt 4) = +20 % Auslass oben;
                                               #   Öffnung Z1..19 → 5..17 innen; boss-frei via X (Bosse @X±16, Vent X±10).
VENT_DECKEL_XC = 6.0                            # [MINI/Audit] nach +X versetzt (v3_min: 0): der neue linke
                                               #   Ohr-Block (X−17..−5) belegt die Deckel-Links-Hälfte → Vents
                                               #   X−4..16 (rechts vom Ohr, 1 mm Luft) · Fläche unverändert (5×1,1×20).
#  Front (−X, im BODY): 2×(1,1×10) oben (VTX-Stockwerk), Länge Y, gestapelt in Z; unter Antennen-ZE (Z17).
VENT_FRONT_L = 10.0                             # [MINI] kürzer (v3_min: 16): weicht der auf −15,5 gerückten Kamera aus
VENT_FRONT_Z = (8.0, 11.0)                      # [MINI] unter der Antennen-ZE (AZE_Z 17, Reg ab Z14) — Louver-Top ≤11,5
VENT_FRONT_YC = 3.5                             # [MINI] nach +Y versetzt: Y−1,5..8,5 → clear von Kamera-Rückraum (Y≤−1,75)
#  Heck (+X, im BODY): 2×(1,1×16) ÜBER der Klappe, Länge Y, gestapelt in Z; über den Snap-Kanälen (Z≤8).
VENT_HECK_L = 16.0
VENT_HECK_Z = (10.0, 13.0)                      # [MINI] über Snap-Kanälen (bis Z8), Flachzone |Z|<14 (v3_min: 15/18)
VENT_HECK_YC = 0.0
#  +Y-Wand FEST unten (im BODY): 2×(1,1×12) Akku-minimal, Länge X, gestapelt in Z; rib-/nasen-frei.
VENT_YFEST_L = 12.0                             # [MINI] X±6 → Bay-Rippen (X−18/+20) + Nasen (X>19) frei
VENT_YFEST_Z = (-13.0, -9.0)                    # Akku-Mitte, unter der Deckel-Öffnung (Z<1)
VENT_YFEST_XC = 0.0                             # |X|<6


def _louver_Xaxis(xc, zc, L, y_mid):
    """Louver-Cutter für ±Y-Flächen: Schlitz lang in X (L), schmal in Z (VENT_W), −45° um X gekippt
    → Durchbruch +Y/−Z (abwärts-auswärts). y_mid = Wand-Mittelebene der Fläche."""
    return Pos(xc, y_mid, zc) * Rot(-VENT_LOUVER_DEG, 0, 0) * Box(L, VENT_THROUGH, VENT_W)


def _louver_Yaxis(yc, zc, L, x_mid, sgn):
    """Louver-Cutter für ±X-Flächen: Schlitz lang in Y (L), schmal in Z (VENT_W), um Y gekippt
    → Durchbruch ±X/−Z (abwärts-auswärts). x_mid = Wand-Mittelebene, sgn = Wand-Normalenrichtung (±1)."""
    return Pos(x_mid, yc, zc) * Rot(0, sgn*VENT_LOUVER_DEG, 0) * Box(VENT_THROUGH, L, VENT_W)


def cut_vents_body(body):
    """MB3: schneidet Front(−X), Heck(+X) und +Y-Wand-FEST-unten in den BODY. Rückgabe (body, n).
    Deckel-Vents werden separat in den COVER geschnitten (cut_vents_cover). CAD ≠ Luftstrom-Test."""
    n = 0
    xw_neg = (-IN_X/2 + -EX_X/2)/2           # −X-Wand-Mittelebene = −34
    xw_pos = ( IN_X/2 +  EX_X/2)/2           # +X-Wand-Mittelebene = +34
    yw_pos = ( IN_Y/2 +  EX_Y/2)/2           # +Y-Wand-Mittelebene = +18,25
    for zc in VENT_FRONT_Z:
        body = body - _louver_Yaxis(VENT_FRONT_YC, zc, VENT_FRONT_L, xw_neg, +1); n += 1
    for zc in VENT_HECK_Z:
        body = body - _louver_Yaxis(VENT_HECK_YC, zc, VENT_HECK_L, xw_pos, -1); n += 1
    for zc in VENT_YFEST_Z:
        body = body - _louver_Xaxis(VENT_YFEST_XC, zc, VENT_YFEST_L, yw_pos); n += 1
    return body, n


def cut_vents_cover(cov):
    """MB3: schneidet die 4 Deckel-Vents (1,1×20) in den COVER (+Y). Rückgabe (cov, n)."""
    yw_pos = (IN_Y/2 + EX_Y/2)/2             # +18,25 (Deckel-Wand-Mittelebene)
    n = 0
    for zc in VENT_DECKEL_Z:
        cov = cov - _louver_Xaxis(VENT_DECKEL_XC, zc, VENT_DECKEL_L, yw_pos); n += 1
    return cov, n


# ── FEST VERBAUTER STOCKWERK-SHELF (Anton-Prinzip, mitgedruckt — kein Einlege-Tray) ──
#   V3_SPEC „Stockwerke": Shelf = Teil des Body, Z zwischen Akku-Bay (oben Z=0) und Elektronik.
#   KEIN durchgehender Boden — 2 Luft-Aussparungen (Kamin + XT30-Durchlass), zentrale VTX-
#   Klebefläche bleibt flach + groß (modular/verschiebbar). Maße aus V3_SPEC/Airflow, keine Schätzung.
SHELF_MID_Z = Z_INT_BOTTOM + BAY_H + SHELF_T/2   # = 1.5  (Shelf-Mitte, Z 0..3)
SHELF_CUT_L, SHELF_CUT_W = 8.0, 28.0             # [MINI] Aussparung 12→8 (X): kürzerer Bay → sonst VTX_PAD_X<31.
                                                 #   8×28 → 2×224=448 mm² Luft/XT30 (XT30 passt Y-seitig durch 28)
SHELF_CUT_DX = IN_X/2 - 9.0                       # Aussparungen an den X-Enden (±23,5), Mitte = VTX-Pad
VTX_PAD_X = IN_X - 2*(SHELF_CUT_L + 3.0)          # verbleibende zentrale Klebe-Breite (X) ≈ 35 (VTX 30 passt)


def build_shelf(body):
    """Shelf-Platte auf Bay-Höhe an den Body ANGESCHWEISST (union = fest verbaut). 2 längs Aussparungen
    an den X-Enden (Kamin-Luft + XT30 kreuzt die Stockwerke); zentrale flache VTX-Klebefläche bleibt.
    CAD-Check ≠ empirischer Test."""
    shelf = Pos(0, 0, SHELF_MID_Z) * Box(IN_X, IN_Y, SHELF_T)
    for sx in (-1, +1):
        shelf = shelf - Pos(sx*SHELF_CUT_DX, 0, SHELF_MID_Z) * Box(SHELF_CUT_L, SHELF_CUT_W, SHELF_T + 2)
    return body + shelf


# ── M-A4 · GOPRO-2-ZINKEN-GABEL unten (−Z) — Vorlage skylive_sender_v2.py/spec.py ─────
import spec                       # GOPRO_*-Konstanten = Toms Messungen (Single Source of Truth)
FINGER_T = 2.8      # Zinken-Dicke: Tom 2026-07-05 FINAL: Antons 3,0 −0…0,2 → 2,8 [MEASURE_ME Fit-Print].
                    #   Separation/Gap bleibt 3,3 exakt (spec.GOPRO_GAP). (spec 2,7 = ältere Basis, nicht genutzt.)
GOPRO_CX = 0.2 * (EX_X / 2)   # „mittig + 20% Halbstrecke nach Heck (Tom 2026-07-05), leicht
                              #   off-center gewollt" — Heck = +X (Akku-Klappe); −X = Kamera-Ecke.
FORK_FILLET = 0.8   # Zinken-Wurzel-Fillet gegen Layer-Bruch [Design-Wahl Druck-Robustheit;
                    #   MEASURE_ME: GoPro-Gegenstück muss trotz 0,8-Radius voll einsitzen]


def build_gopro_fork(body):
    """GoPro-2-Zinken-Gabel (female) an die Unterseite: Zinken dünn in X (= Pivot-Achse), Schlitz
    3,3 exakt [Tom], Zinkenlänge 14,5 + Pivot Ø5,0 10 unter der Basis [spec/Tom 2026-07-04].
    Wurzel-Fillet auf den Wurzel-Kanten. Rückgabe (body, n_fillet_edges). CAD ≠ Fit-Test."""
    z_base = -EX_Z / 2
    gap, fw, fh = spec.GOPRO_GAP, spec.GOPRO_2PRONG[0], spec.GOPRO_PRONG_LEN
    for s in (-1, +1):
        body = body + Pos(GOPRO_CX + s * (gap/2 + FINGER_T/2), 0, z_base - fh/2) * \
            Box(FINGER_T, fw, fh)
    roots = [e for e in body.edges()
             if abs(e.center().Z - z_base) < 1e-6
             and abs(e.center().X - GOPRO_CX) < gap/2 + FINGER_T + 0.5
             and abs(e.center().Y) < fw/2 + 0.5]
    body = fillet(roots, radius=FORK_FILLET)
    body = body - Pos(GOPRO_CX, 0, z_base - spec.GOPRO_PIVOT_FROM_BASE) * Rot(0, 90, 0) * \
        Cylinder(radius=spec.GOPRO_HOLE_D / 2, height=gap + 2*FINGER_T + 6)
    return body, len(roots)


def build_bay_guides(body):
    """M-A1: Akku-Bay-Führung, an Body/Shelf ANGESCHWEISST (union). 3 Boden-Schienen (Oberkante =
    Breach-Unterkante → Akku gleitet eben ein), 2 Decken-Leisten unter dem Shelf (definieren lichte
    Höhe 23,75), 2 Rippen-Paare (Anlageflächen ±15,375). Vorderes Paar mit 45°-Einführschräge
    (exakter Keil-Cutter → Wand bleibt unberührt). CAD-Check ≠ empirischer Einschub-Test."""
    bay_top = Z_INT_BOTTOM + BAY_H
    y_wall = IN_Y / 2
    for ry in RAIL_Y:                    # Boden-Schienen
        body = body + Pos((RAIL_X0 + RAIL_X1)/2, ry, Z_INT_BOTTOM + RAIL_H/2) * \
            Box(RAIL_X1 - RAIL_X0, RAIL_W, RAIL_H)
    strip_w = (y_wall + RIB_EMBED) - STRIP_Y_IN     # Decken-Leisten: von y=11 bis in die Wand
    for s in (-1, +1):
        body = body + Pos((STRIP_X0 + STRIP_X1)/2, s*(STRIP_Y_IN + strip_w/2),
                          STRIP_BOT + STRIP_T/2) * Box(STRIP_X1 - STRIP_X0, strip_w, STRIP_T)
    rib_d = (y_wall + RIB_EMBED) - RIB_FACE          # Rippen: Anlagefläche → in die Wand
    for rx in RIB_X:
        for s in (-1, +1):
            body = body + Pos(rx, s*(RIB_FACE + rib_d/2), (Z_INT_BOTTOM + bay_top)/2) * \
                Box(RIB_W, rib_d, bay_top - Z_INT_BOTTOM)
    # 45°-Einführschräge am VORDEREN Paar: exakter Dreiecks-Keil (endet AUF der Wandebene y_wall
    #   → 3,0-Wand unberührt), Lauf = Rippentiefe. Fängt Akku-Versatz bis (OPEN_Y-30)/2 ein.
    x_f = RIB_X[-1] + RIB_W/2                        # Rippen-Vorderkante (+X, Tür-Seite)
    run = y_wall - RIB_FACE
    for s in (-1, +1):
        wedge = Pos(0, 0, Z_INT_BOTTOM) * extrude(
            Polygon((x_f - run, s*RIB_FACE), (x_f, s*RIB_FACE), (x_f, s*y_wall), align=None),
            bay_top - Z_INT_BOTTOM)
        body = body - wedge
    return body


from build123d import Rectangle   # 2D für das Hybrid-Falz-Profil (±Y-Lap unten, oben auslaufend)


def _door_yz(dy, dz):
    """YZ-Profil (Plane.YZ) der Falz-Zone: unten CB_Y breit (±Y-Lap), im oberen LAP_RELIEF_Z auf OPEN_Y
    schmaler (Lap läuft auf 0 aus). ±Z ohne Lap (Höhe = OPEN_Z). dy/dz = Inset je Seite (0=Senkung,
    TOL_SLIDE=Flansch). Beide teilen dieses Profil → kein Drift, definiert Schulter (nur ±Y) + Flush (±Z)."""
    Hf = OPEN_Z - 2*dz
    main_h = Hf - LAP_RELIEF_Z
    main = Pos(0, -Hf/2 + main_h/2) * RectangleRounded(CB_Y - 2*dy, main_h, min(DOOR_R, main_h/2 - 0.01))
    relief = Pos(0, Hf/2 - LAP_RELIEF_Z/2) * Rectangle(OPEN_Y - 2*dy, LAP_RELIEF_Z)
    return Plane.YZ * (main + relief)


def cut_lid_opening(body):
    """MB1: +Y-Wand im Stockwerk 2 öffnen — bündiger Falz (Tür-Prinzip): innerer Durchbruch
    (inner Wandhälfte 16,75..18,25) + äußere Senkung (outer Hälfte 18,25..19,75, +LID_LAP breiter)
    → Öffnung durchgehend, Rahmen-Lippe mit Außen-Rebate für den bündigen Deckel. CAD ≠ Test."""
    zc = (LID_Z0 + LID_Z1)/2
    oz = LID_Z1 - LID_Z0
    # (a) innerer Durchbruch (Zunge-Sitz): inner Wandhälfte — Cutter dünn in Y (Plane.XZ, Normale Y)
    y_in = (LID_Y_IN + LID_Y_MID)/2
    body = body - Pos(0, y_in, zc) * extrude(
        Plane.XZ * RectangleRounded(2*LID_HX, oz, LID_R), LID_REB_D/2 + 0.1, both=True)
    # (b) äußere Senkung (Flansch-Sitz): outer Hälfte, +LID_LAP je Seite (Schulter-Rebate)
    y_cb = (LID_Y_MID + LID_Y_OUT)/2
    body = body - Pos(0, y_cb, zc) * extrude(
        Plane.XZ * RectangleRounded(2*(LID_HX+LID_LAP), oz + 2*LID_LAP, LID_R), LID_REB_D/2 + 1.0, both=True)
    return body


def build_lid_features(body):
    """MB1-NEU (Audit): body-seitige Deckel-Features OHNE Innenraum-Bosse.
      (a) 2× vertikaler M3-Decken-Durchgang (Ø3,4 + CB Ø6,1) von +Z-außen über den Ohren (Links-Zone).
      (b) 2× untere Nasen-Tasche: Schlitz in der +Y-Wand UNTER der Öffnung (Zungen-Tiefe) + Haken-
          Freistich, damit die Deckel-Einhänge-Nase greift. CAD-/Boolean-Check ≠ Füge-/Zug-Test."""
    z_top = EX_Z/2                                   # +Z-Außenfläche = 23
    for ex in LID_EAR_X:                             # (a) Decken-Durchgänge (Z-Achse) über den Ohren
        body = body - Pos(ex, LID_EAR_YC, z_top - LID_CB_DP/2) * Cylinder(radius=LID_CB_D/2, height=LID_CB_DP + 0.1)
        body = body - Pos(ex, LID_EAR_YC, z_top - (WALL + 1.5)/2) * Cylinder(radius=LID_THRU_D/2, height=WALL + 1.5)
    z_ob = LID_Z0                                    # Öffnungs-Unterkante = 1
    for nx in LID_NASE_X:                            # (b) Einhänge-Tab-Taschen UNTER der Öffnung
        yw = LID_NASE_W + 2*LID_NASE_TOL
        # Tab-Schlitz durch die INNERE Wandhälfte (Zungen-Tiefe 16,75..18,25), Z −(DROP+0,3)..1.
        #   Der Deckel-Tab steckt hier; sein +Y-Face trägt gegen die ÄUSSERE Wand (18,25..19,75) → +Y-Auszug
        #   am unteren Rand gesperrt (Einhängen: unten einführen, oben verschrauben). CAD ≠ Füge-Test.
        z0 = z_ob - LID_NASE_DROP - 0.3
        body = body - Pos(nx, (LID_Y_IN + LID_Y_MID)/2, (z_ob + z0)/2) * \
            Box(yw, LID_Y_MID - LID_Y_IN + 0.1, z_ob - z0)
    return body


def build_shell():
    """Hohle gerundete Schale + Akku-Klappen-Öffnung. Ursprung zentriert.
    M1: KEIN Shelf/Aussparungen (kommt M4) — nur der durchgehende Hohlraum ist vorgesehen."""
    outer = extrude(RectangleRounded(EX_X, EX_Y, FIL_O), EX_Z/2, both=True)
    inner = extrude(RectangleRounded(IN_X, IN_Y, FIL_I), IN_Z/2, both=True)
    body = outer - inner
    # ── Akku-Klappe (+X-Stirnseite, unteres Stockwerk): BÜNDIGER Falz statt simpler Durchbruch ──
    # (a) innerer Durchbruch (Zunge-Sitz): innere Wandhälfte 32.5..34.0, Öffnung OPEN_Y x OPEN_Z
    x_in = (X_WALL_IN + X_SHOULDER) / 2
    body = body - Pos(x_in, 0, Z_BAY_MID) * extrude(
        Plane.YZ * RectangleRounded(OPEN_Y, OPEN_Z, DOOR_R - REBATE_LAP), REBATE_D/2 + 0.1, both=True)
    # (b) äußere Senkung (Flansch-Sitz): HYBRID-Falz — ±Y-Lap (Schulter bei 34,0), ±Z LAP-FREI (flush),
    #     ±Y-Lap läuft im oberen LAP_RELIEF_Z aus. Profil aus _door_yz (Senkung: dy=dz=0).
    x_cb = (X_SHOULDER + DOOR_FACE_X) / 2
    body = body - Pos(x_cb, 0, Z_BAY_MID) * extrude(_door_yz(0.0, 0.0), REBATE_D/2 + 1.0, both=True)
    # (c) NASEN-FUSS-NOTCHES: 2 kleine Schlitze unter der Öffnung (Y±6) → der Tür-Fuß taucht unter die
    #     Akku-Ebene ab. Durch BEIDE Wandhälften (Fuß = Plug, füllt bündig). Boden-Taschen: build_bay_catches.
    for ny in NASE_Y:
        body = body - Pos((X_WALL_IN + DOOR_FACE_X)/2, ny, (NOTCH_BOT + (Z_BAY_MID - OPEN_Z/2))/2) * \
            Box(DOOR_FACE_X - X_WALL_IN + 2.0, NASE_W + 2*TOL_SLIDE, (Z_BAY_MID - OPEN_Z/2) - NOTCH_BOT)
    # (c2) SNAP-EINSCHWENK-KANÄLE (2×, Y=±10,5) über der Öffnung. Der Tür-Klick-Cantilever kippt beim
    #     Einschwenken nach −X (in die Kavität) → der Kanal räumt die INNERE Wandhälfte (X 32,4..34) über
    #     dem Öffnungs-Oberrand frei (Feder-Bogen taucht danach in die offene Kavität ab). Zusätzlich eine
    #     flache Relief-Nut in der ÄUSSEREN Wandhälfte NUR bis unter die Flansch-Oberkante (Z≤flansch_top,
    #     dort vom Flansch verdeckt → außen bündig) für das Nase-Spiel bei Vollschluss. [CEO 2026-07-05]
    z_ot = Z_BAY_MID + OPEN_Z/2
    flansch_top = Z_BAY_MID + CB_Z/2                 # Flansch-Oberkante = 1,4 (deckt Außenhaut bis hier)
    ch_y = SNAP_W + 2*TOL_SLIDE
    for sy in SNAP_Y:
        # Einschwenk-Kanal: innere Wandhälfte, ab Öffnungs-Oberkante nach oben (Feder-Höhe + Luft)
        body = body - Pos((X_WALL_IN + X_SHOULDER)/2, sy, z_ot + (SNAP_L + 2.5)/2) * \
            Box((X_SHOULDER - X_WALL_IN) + 0.2, ch_y, SNAP_L + 2.5)
        # Relief in der äußeren Wandhälfte, nur unter dem Flansch (verdeckt): nimmt die Rast-Nase auf
        body = body - Pos((X_SHOULDER + DOOR_FACE_X)/2, sy, (z_ot + flansch_top)/2) * \
            Box(DOOR_FACE_X - X_SHOULDER, ch_y, flansch_top - z_ot)
    # (d) Schraub-Boss oben für den M2-Zylinderkopf (Achse X): Pilot Ø1,6 selbstschneidend, ins Innere.
    # Boss endet bei DOOR_BOSS_END_X (0,3 Luft zum Tür-Pad — Kollisionsfix; [MINI] parametrisch statt 31,2)
    body = body + Pos((X_WALL_IN - 6.0 + DOOR_BOSS_END_X)/2, 0, DOOR_SCREW_Z) * Box(DOOR_BOSS_END_X - (X_WALL_IN - 6.0), 7.0, 7.0)
    # EINSCHWENK-RELIEF am Boss (Kollisionsfix (a) 2026-07-05): beim −ang-Einschwenken taucht die
    #   Zungen-Oberkante von +X/hoch kommend an die +X-Oberkante des Bosses. 45°-Fase an der Boss-
    #   +X/oben-Kante gibt dem Einschwenk-Bogen Luft; der Gewindekern um den Pilot (X≈29,5, Z−2,5)
    #   bleibt voll erhalten (Fase nur X>30,3 / Z>−1). EHRLICH: entschärft nur den KLEINWINKEL-Kontakt;
    #   der Boss bleibt bei großem −ang prinzipbedingt im Schwenkweg (siehe Schwenk-Gate-Kommentar).
    body = body - Pos(DOOR_BOSS_END_X, 0, DOOR_SCREW_Z + 3.5) * Rot(0, 45, 0) * Box(2.6, 7.2, 2.6)
    body = body - Pos(X_WALL_IN - 3.0, 0, DOOR_SCREW_Z) * Rot(0, 90, 0) * \
        Cylinder(radius=DOOR_PILOT_R, height=8.0)   # M2-Pilot Ø1,6 (selbstschneidend)  [MEASURE_ME Gewinde]
    # (e) Boden-Taschen + Kopf-Kammern für die Tür-Nasen (Weg A)
    body = build_bay_catches(body)
    # (f) MB1 · DECKEL: +Y-Wand im Stockwerk 2 öffnen + 4 M3-Insert-Bosse (nach Shelf-Anbau)
    body = cut_lid_opening(body)
    return body


def graft_camera(shell):
    """invert_camera() 1:1 re-platziert: verschiebe die Minimal-Schale in Antons Frame, sodass die
    -Y-Wandebene auf Antons Wandebene (Y=WALL_Y) und die Wölbungs-Mitte (X21,5/Z14) auf die -Y-Face-
    Mitte (X0 / Z_CAM) fällt; wende invert_camera 1:1 an; transformiere zurück.

    Transform M (mein Frame → Anton-Frame): Rot 180° um Z dreht meine Aussen-Normale -Y auf Antons +Y
    (outward), dann Translation. So bleibt jede Anton-interne Relation (Wölbung↔Linse↔Klemmbohrungen)
    exakt erhalten (= 1:1 wiederverwendet), nur re-platziert."""
    M = Pos(BULGE_XC + CAM_OFF_X, WALL_Y - EX_Y/2, BULGE_ZC - Z_CAM) * Rot(0, 0, 180)
    gk_anton = M * shell                     # Schale in Antons Frame
    # M-A3: camera_final = Linse RAUS (Fenster, flush außen), Antons Ösen-Struktur NACH INNEN
    #   (Flanken + Ø8,4-Bosse + X-Achs-Bohrung + Ø4,7×2,6-CB innen). clear_anton=False: die
    #   Minimal-Schale hat keine interne Kamera-Altlast. Flanken-Z-Höhe 12 < F2_H 20 ✓.
    fixed = camera_final(gk_anton, clear_anton=False)
    return M.inverse() * fixed               # zurück in meinen Frame


def build_bay_catches(body):
    """Boden-Taschen für die Tür-Nasen (Weg A): je Nase ein Finger-Kanal in der Bodenwand
    (unter Akku-Ebene) + tiefere Kopf-Kammer. Auszugssperre: der 1,0-Haken-Kopf (hoch bis LIP_TOP−0,2)
    hakt beim +X-Zug an der Kanal-Decke (NASE_TOP+TOL). Lift sperrt die Schraube. [Plan 2.3]"""
    for ny in NASE_Y:
        yw = NASE_W + 2 * TOL_SLIDE
        # Finger-Kanal (Decke knapp unter Innenboden-Niveau → Kopf kann NICHT durchrutschen)
        x0, x1 = FIN_XIN + HOOK - TOL_SLIDE, X_WALL_IN + 0.2
        body = body - Pos((x0 + x1)/2, ny, (FIN_BOT - TOL_SLIDE + NASE_TOP + TOL_SLIDE)/2) * \
            Box(x1 - x0, yw, (NASE_TOP - FIN_BOT) + 2 * TOL_SLIDE)
        # Kopf-Kammer (öffnet höher, bis LIP_TOP: Kopf taucht ein und hakt an der Stufe).
        #   Boden CATCH_SWING_CLR tiefer, damit der Kopf beim −ang-Einschwenken frei abtaucht (Fix c).
        x0, x1 = POCKET_X0 - TOL_SLIDE, FIN_XIN + HOOK + TOL_SLIDE
        kammer_bot = FIN_BOT - TOL_SLIDE - CATCH_SWING_CLR
        body = body - Pos((x0 + x1)/2, ny, (kammer_bot + LIP_TOP)/2) * \
            Box(x1 - x0, yw, LIP_TOP - kammer_bot)
    return body


def _add_door_nasen(door):
    """2 Schwenk-Nasen an der Tür-Unterkante (Y±6): Fuß taucht durch die Wand-Notch unter die
    Akku-Ebene, Finger (t=1,2) läuft nach −X in den Boden-Kanal, Haken-Kopf (H=1,0) hakt in der
    Kopf-Kammer gegen Herausziehen. Montage: Nasen einschieben → kippen → oben klick+schrauben."""
    z_open_bot = Z_BAY_MID - OPEN_Z/2
    for ny in NASE_Y:
        # Fuß: füllt die Breach-Notch (Plug, −Gleitspiel), überlappt 2 mm in die Zunge (→ 1 Solid)
        door = door + Pos((X_WALL_IN + TOL_SLIDE + DOOR_FACE_X)/2, ny,
                          (NOTCH_BOT + TOL_SLIDE + z_open_bot + 2.0)/2) * \
            Box(DOOR_FACE_X - X_WALL_IN - TOL_SLIDE, NASE_W, (z_open_bot + 2.0) - (NOTCH_BOT + TOL_SLIDE))
        # Finger nach −X (unter Akku-Ebene)
        door = door + Pos((FIN_XIN + HOOK + X_WALL_IN + TOL_SLIDE + 0.1)/2, ny,
                          (FIN_BOT + NASE_TOP)/2) * \
            Box((X_WALL_IN + TOL_SLIDE + 0.1) - (FIN_XIN + HOOK), NASE_W, NASE_T)
        # Haken-Kopf am Finger-Ende (ragt über Finger-Oberkante → Auszugssperre)
        door = door + Pos(FIN_XIN + HOOK/2, ny, (FIN_BOT + LIP_TOP - 0.2)/2) * \
            Box(HOOK, NASE_W, (LIP_TOP - 0.2) - FIN_BOT)
    return door


def _add_door_snap(door):
    """ZWEI Klick-Cantilever an der Tür-Oberkante (PETG, ε≈1,33 %), seitlich bei Y=±10,5 (boss-frei):
    Feder t=1,2 steht von der Zunge nach oben in die Body-Einschwenk-Tasche, Rast-Nase (0,6
    Hinterschnitt, 45°-Rampe via Kante) klickt beim Zuschwenken. NUR Positionierung/Feedback —
    Haltekraft trägt die M2-Schraube. [Plan 2.4 / CEO 2026-07-05: 2× seitlich statt 1× mittig]"""
    z_ot = Z_BAY_MID + OPEN_Z/2
    fx = X_WALL_IN + TOL_SLIDE + SNAP_T/2          # Feder-Wurzel sitzt auf der Zungen-Stirn
    for sy in SNAP_Y:
        door = door + Pos(fx, sy, (z_ot - 2.0 + z_ot + SNAP_L)/2) * \
            Box(SNAP_T, SNAP_W, SNAP_L + 2.0)      # Feder (2 mm Overlap in die Zunge)
        door = door + Pos(fx - SNAP_T/2 - SNAP_H/2, sy, z_ot + SNAP_L - 0.75) * \
            Box(SNAP_H, SNAP_W, 1.5)               # Rast-Nase 0,6 nach −X, 1,5 hoch
    return door


def build_door():
    """Bündige Akku-Klappe als SCHALEN-PLUG. Der Flansch ist ein Schnitt aus DERSELBEN Aussenkontur
    wie die Schale → seine +X-Aussenfläche liegt exakt auf der Schalenkontur (bündig, 0 Überstand),
    inkl. R9-Rundung; die Zunge füllt die innere Wandhälfte. Nasen unten, M2-Senkung oben.
    Rückgabe: eigenständiges Solid im Schalen-Frame (NICHT durch graft_camera geführt)."""
    outer = extrude(RectangleRounded(EX_X, EX_Y, FIL_O), EX_Z/2, both=True)  # gleiche Aussenkontur
    region = Pos((X_SHOULDER + DOOR_FACE_X)/2 + 2.0, 0, Z_BAY_MID) * \
        extrude(_door_yz(TOL_SLIDE, TOL_SLIDE), (DOOR_FACE_X - X_SHOULDER)/2 + 2.0, both=True)
    flange = outer & region                                  # Plug: +X-Fläche = Schalenkontur → bündig
    # Zunge füllt inneren Durchbruch (OPEN minus Gleitspiel), innere Wandhälfte 32.5..34.0
    tY, tZ = OPEN_Y - 2*TOL_SLIDE, OPEN_Z - 2*TOL_SLIDE
    tongue = Pos((X_WALL_IN + TOL_SLIDE + X_SHOULDER)/2, 0, Z_BAY_MID) * \
        extrude(Plane.YZ * RectangleRounded(tY, tZ, DOOR_R - REBATE_LAP), (X_SHOULDER - X_WALL_IN - TOL_SLIDE)/2, both=True)
    # LEAD-CHAMFER an der Zungen-OBERKANTE (inboard) [CEO-Vorgabe 2, 2026-07-05]: 45°-Fase an der
    #   inboard/oben-Kante der Zunge → beim −ang-Einschwenken taucht die Oberkante frei an Durchbruch-
    #   Oberrand + Boss vorbei (Kleinwinkel-Seating). Fase nur X<X_SHOULDER, Z-Oberkante → Falz/Plug
    #   (±Y-Lap am Flansch, Einwärts-Stopp) unberührt; Akku-Kanal (Z<−0,8) unberührt.  [geometrisch]
    tZ_top = Z_BAY_MID + tZ/2
    tongue = tongue - Pos(X_WALL_IN + TOL_SLIDE, 0, tZ_top) * Rot(0, 45, 0) * \
        Box(TONGUE_LEAD*1.42, tY + 2.0, TONGUE_LEAD*1.42)
    door = flange + tongue
    door = _add_door_nasen(door)                             # M2 · 2 Schwenk-Nasen (Weg A, unter Akku-Ebene)
    door = _add_door_snap(door)                              # M2 · Klick-Cantilever an der Oberkante
    # M2-ZYLINDERKOPF (DIN912): verdicktes Pad an der lap-freien Oberkante + Counterbore Ø4,2×2,2 +
    #   Durchgang Ø2,4 durch die Zunge (→ Schalen-Boss, Pilot Ø1,6). Kopf sitzt bündig in der +X-Fläche.
    pad_c = DOOR_FACE_X - DOOR_PAD_T/2                        # Pad wächst vom Flansch nach INNEN (−X)
    z_ot = Z_BAY_MID + OPEN_Z/2
    pad_top = z_ot - 0.8                                      # Pad endet UNTER der Öffnungs-Oberkante
    pad_bot = DOOR_SCREW_Z - 4.0                              #   (Kollisionsfix: ragte in die Body-Wand)
    door = door + Pos(pad_c, 0, (pad_top + pad_bot)/2) * Box(DOOR_PAD_T, 8.0, pad_top - pad_bot)
    door = door & outer                                      # Pad bündig kappen (+X-Fläche = Schalenkontur)
    door = door - Pos(DOOR_FACE_X - DOOR_CB_D/2, 0, DOOR_SCREW_Z) * Rot(0, 90, 0) * \
        Cylinder(radius=DOOR_CB_R, height=DOOR_CB_D)          # Counterbore Ø4,2 × 2,2 (Kopf versenkt bündig)
    door = door - Pos(DOOR_FACE_X - 4.0, 0, DOOR_SCREW_Z) * Rot(0, 90, 0) * \
        Cylinder(radius=DOOR_THRU_R, height=WALL + 4)         # Durchgang Ø2,4 durch Zunge in den Boss
    # M2 · Daumen-Mulde (subtraktiv, bleibt in der bündigen Hülle) — Handling mit Handschuhen
    door = door - Pos(DOOR_FACE_X + GRIP_D - 0.4, 0, Z_BAY_MID - OPEN_Z/2 + 4.0) * \
        Rot(0, 90, 0) * Cylinder(radius=GRIP_W/2, height=2*GRIP_D)   # flache Kugel-/Zylinder-Mulde
    return door


# ── MB2(a) · ANTENNEN-ZUGENTLASTUNG — Anschraub-Position (Antons Block extern, Spec §5) ──────
#   ENTSCHEIDUNG NACH PLATZ (dokumentiert, Spec: „Union ODER Anschraub, entscheide nach Platz"):
#   Antons Block 17,9×13,05×5,8 passt NICHT kollisionsfrei intern — Floor-2 ist voll (Kamera
#   X−19,75..1,75 · VTX X1,75..31 · Deckel-Bosse in den Ecken), und seine Rückwand-Schrauben (Achse
#   Y, flächig) verlangen eine ±Y-Wand; beide sind belegt (+Y=Deckel, −Y=Kamera). Der Block ist
#   ohnehin ein EXTERNER Strain-Relief (Antons Realdruck, Foto proto_8369). Also KEIN Union: Antons
#   Block bleibt SEIN separates Druckteil (STEP); ich stelle nur die Schnittstelle an der −X-Front-
#   Oberkante bereit — Koax-Kanten-Schlitz + 2× M2-Kern-Bosse („Rückwand-Prinzip", flächig verschraubt).
#   Klemm-Differenz 2,9 bleibt in Antons Block (unverändert, Spec §5). Antenne vertikal → Koax nach −X.
AZE_Y  = 8.0                    # +Y-Seite der −X-Front-Wand (über Kamera Y≤1,75)         [Design/kollisionsfrei]
AZE_Z  = 17.0                   # [MINI] Oberkante Floor-2 (über VTX, unter Innendecke 20; Boss Ø4,5 Z14,75..19,25) (v3_min: 21)
AZE_COAX_D  = 3.4               # Koax-Durchlass (Antons Ø3,1 + Spiel) durch die −X-Wand   [Spec §5 Ø3,1]
AZE_SCREW_DY = 6.5              # M2-Schrauben ±6,5 um den Slot   MEASURE_ME (exaktes Antons-Lochbild an SEINEM Teil)
AZE_PILOT_D  = 1.7              # M2-Selbstschneid-Kern (Antons Ø2,0-Praxis, Druck-Schrumpf beißt) [Spec §5b/§8]
AZE_BOSS_D, AZE_BOSS_L = 4.5, 4.0   # innerer Gewinde-Boss (mehr Fleisch als die 3-mm-Wand)     [Design]


def mount_antenna_ze(body):
    """MB2(a): Schnittstelle für Antons EXTERNEN Antennen-ZE-Block an der −X-Front-Oberkante —
    Koax-Kanten-Schlitz (Ø3,4, Achse X, durch die −X-Wand) + 2× M2-Kern-Bosse (Ø1,7-Pilot in
    Ø4,5×4-Innen-Boss, von außen verschraubt). Block selbst = Antons Druckteil (nicht unioned).
    Rückgabe body. CAD-/Boolean-Check ≠ Klemm-/Zug-Test."""
    xw = -IN_X/2                                       # −X-Wand-Innenfläche = −32,5
    x_out = -EX_X/2                                    # −X-Außenfläche = −35,5
    # Koax-Durchlass durch die −X-Wand (Achse X)
    body = body - Pos(x_out + WALL/2, AZE_Y, AZE_Z) * Rot(0, 90, 0) * \
        Cylinder(radius=AZE_COAX_D/2, height=WALL + 2)
    for sdy in (-AZE_SCREW_DY, +AZE_SCREW_DY):
        # innerer Gewinde-Boss (Fleisch) + M2-Pilot (von außen selbstschneidend)
        body = body + Pos(xw + AZE_BOSS_L/2, AZE_Y + sdy, AZE_Z) * Rot(0, 90, 0) * \
            Cylinder(radius=AZE_BOSS_D/2, height=AZE_BOSS_L)
        body = body - Pos(x_out + (WALL + AZE_BOSS_L)/2, AZE_Y + sdy, AZE_Z) * Rot(0, 90, 0) * \
            Cylinder(radius=AZE_PILOT_D/2, height=WALL + AZE_BOSS_L + 1)
    return body


# ── MB2(b) · 2× XT30-ZUGENTLASTUNG (angedruckte Klemmsättel + separate Riegel, Spec §5b) ─────
#   Sättel an BEIDEN ±Y-Seitenwand-Oberkanten des Akku-Stockwerks, nahe der Klappe (+X), im +X-Shelf-
#   Cutout (X17,5..29,5 = Shelf-frei) und ÜBER der Akku-Guide-Oberkante (Z>0,25) → kollisionsfrei mit
#   Akku. 2 getrennte horizontale Rinnen (rot+schwarz, Achse X), Licht Ø2,6 voll verschlossen (Ader
#   2,8 → 0,2 Quetsch). Riegel = separates Mini-Teil (2× exportiert), 2× M2 in Ø1,7-Kerne. ≥10 mm
#   offen zur Klappe (Lötkolben durch die geöffnete Tür). Riegel-Oberkante im lower-Floor-2 (Shelf-Cutout).
XT30_SAD_X  = (-16.0, -8.0)        # [MINI/Audit] Sattel in die +Y-KAMERA-SCHATTEN-Zone (links, Z-niedrig).
                                   #   Grund: der 30-mm-VTX füllt F2 fast über die volle Breite (33,5) → ein
                                   #   Wand-Sattel auf VTX-Höhe trifft ±Y-seitig VTX (rechts/mitte) bzw. Kamera (−Y).
                                   #   Nur die Links-Zone (X<−4,75, Y>−0,75) ist VTX- UND kamera-frei bei Z0,3..2,3.
XT30_SIDES  = (+1,)                # [MINI] NUR +Y-Sattel (die −Y-Wand ist dort von der Kamera belegt). 1 Sattel, 2 Rinnen.
XT30_SAD_YW = 10.0                 # Sattel-Innenkante |Y| (protrudes von Wand 16,75 → 10,0)      [Design]
XT30_SAD_Z  = (0.3, 2.3)           # Z über Akku-Guide-Oberkante 0,25 (kein Akku-Kontakt)         [Spec §5b/kollisionsfrei]
XT30_GROOVE_R = 1.3                # Rinnen-Halbradius → Licht Ø2,6 voll verschlossen             [Spec §5b: Licht 2,6]
XT30_GROOVE_Y = (11.5, 15.5)       # 2 getrennte Rinnen |Y|, Steg ~1,4 (rot+schwarz)             [Spec §5b: 2 getrennt]
XT30_PILOT_D  = 1.7                # M2-Riegel-Kern Ø1,7 (Antons Praxis, Schrumpf beißt)          [Spec §5b/§8]
XT30_PILOT_Y  = 13.5              # Riegel-Schraube mittig zwischen den Rinnen                   [Design]
XT30_PILOT_DX = 4.0               # 2 Schrauben längs ±4 um die Sattelmitte                      [Design]
XT30_LATCH_H  = 2.0              # Riegel-Höhe über der Sattel-Oberkante                          [Design]

# ── [MINI/Audit] WAGO-BANK MASSKETTE (Coordinator-Punkt b) — BEFUND: passt NICHT in F2 ──────────
#   3× Wago 13,2×8,6×18,8 [Fix-Team-Maß]. F2-Freiraum-Analyse (CAD-vermessen, occ = Kamera-Unit
#   14×18,5×19 + VTX-Envelope 29,2×30×18,6 + Deckel-Ohr + XT30-Sattel):
#     · Der 30-mm-VTX + die 14-mm-Kamera + Deckel-Ohr füllen F2 fast vollständig.
#     · Größte freie Zone = Kamera-Schatten (X−22,5..−8,5 / Y−0,75..8 / Z0,3..19) ≈ 14×8,75×18,7.
#     · Ein STEHENDER Wago (Grundfläche 13,2×8,6, 18,8 hoch) braucht 18,8 in Z → knapp 18,7 verfügbar,
#       aber die 13,2×8,6-Grundfläche + Freigang lässt gemessen 0 (eng ~1) Wagos zu; 3 passen NICHT.
#   ENTSCHEIDUNG (dokumentiert, MEASURE_ME/Design-Reconcile mit Fix-Team): der 300-Mini kann die
#   3-Wago-Bank NICHT wie der 850er im F2 aufnehmen. Empfehlung für die Mini-Elektrik: (a) Verbindungen
#   direkt am Akku-/Tür-Ende (gelötet+Schrumpf) statt Wago-Bank, ODER (b) max. 1 stehender Wago im
#   Kamera-Schatten + Rest extern. KEINE Wago-Geometrie hier modelliert (Fix-Team liefert die Bank;
#   beim Port wird sie mini-spezifisch reduziert). Antenne bleibt extern (Koax −X, kein interner Bedarf).


def build_xt30_ze(body):
    """MB2(b): angedruckte Klemmsättel (Seiten = XT30_SIDES) mit je 2 X-Rinnen + 2 M2-Kernen. Rückgabe body.
    CAD-/Boolean-Check ≠ Klemm-/Zug-/Löt-Test."""
    xc = (XT30_SAD_X[0] + XT30_SAD_X[1])/2
    xl = XT30_SAD_X[1] - XT30_SAD_X[0]
    zc = (XT30_SAD_Z[0] + XT30_SAD_Z[1])/2
    zt = XT30_SAD_Z[1]                                  # Sattel-Oberkante = Rinnen-Trennebene
    for sy in XT30_SIDES:
        yw = sy * IN_Y/2                                # Wand-Innenfläche ±16,75
        y_in = sy * XT30_SAD_YW
        body = body + Pos(xc, (yw + y_in)/2, zc) * Box(xl, abs(yw - y_in), XT30_SAD_Z[1] - XT30_SAD_Z[0])
        for gy in XT30_GROOVE_Y:                        # 2 Rinnen (Halbzylinder, Achse X) in die Oberkante
            body = body - Pos(xc, sy*gy, zt) * Rot(0, 90, 0) * Cylinder(radius=XT30_GROOVE_R, height=xl + 2)
        for dx in (-XT30_PILOT_DX, +XT30_PILOT_DX):     # 2 M2-Kerne (Achse Z) im Steg
            body = body - Pos(xc + dx, sy*XT30_PILOT_Y, zt) * \
                Cylinder(radius=XT30_PILOT_D/2, height=(XT30_SAD_Z[1] - XT30_SAD_Z[0]) + 1)
    return body


def build_xt30_latch(sy=+1):
    """MB2(b): XT30-Riegel (separates Mini-Teil) für den ±Y-Sattel: Bar mit 2 Gegen-Rinnen (Ø2,6
    zusammen) + 2× M2-Durchgang Ø2,2. sy = Seite (+1/−1). Rückgabe eigenständiges Solid."""
    xc = (XT30_SAD_X[0] + XT30_SAD_X[1])/2
    xl = XT30_SAD_X[1] - XT30_SAD_X[0] - 2*TOL_SLIDE
    zt = XT30_SAD_Z[1]
    yw = sy * IN_Y/2
    y_in = sy * XT30_SAD_YW
    latch = Pos(xc, (yw + y_in)/2, zt + XT30_LATCH_H/2) * Box(xl, abs(yw - y_in) - 2*TOL_SLIDE, XT30_LATCH_H)
    for gy in XT30_GROOVE_Y:
        latch = latch - Pos(xc, sy*gy, zt) * Rot(0, 90, 0) * Cylinder(radius=XT30_GROOVE_R, height=xl + 2)
    for dx in (-XT30_PILOT_DX, +XT30_PILOT_DX):
        latch = latch - Pos(xc + dx, sy*XT30_PILOT_Y, zt + XT30_LATCH_H/2) * \
            Cylinder(radius=1.1, height=XT30_LATCH_H + 2)   # M2-Durchgang Ø2,2
    return latch


def build_cover():
    """MB1-NEU (Audit): Stockwerk-2-Deckel (+Y) als bündiger Plug (Flansch outer + Zunge inner = 3,0-Platte),
    OHNE Innenraum-Bosse. Retention: 1 linker Ohr-Block (VTX-frei) mit 2 vertikalen M3-Inserts (von der
    Decke verschraubt) + unten 2 Einhänge-Tabs (in Body-Taschen, +Y-Auszug via Außenwand gesperrt).
    Separates Bauteil, im Schalen-Frame. CAD-/Boolean-Check ≠ Passsitz-Test."""
    tol = TOL_SLIDE                                # 0,3 Gleitspiel je Seite
    zc = (LID_Z0 + LID_Z1)/2
    oz = LID_Z1 - LID_Z0
    yf = (LID_Y_MID + LID_Y_OUT)/2                 # 19,0 Flansch-Mitte (outer Hälfte, Außenfläche 19,75 bündig)
    yt = (LID_Y_IN + LID_Y_MID)/2                  # 17,5 Zungen-Mitte (inner Hälfte)
    flange = Pos(0, yf, zc) * extrude(
        Plane.XZ * RectangleRounded(2*(LID_HX+LID_LAP)-2*tol, oz+2*LID_LAP-2*tol, LID_R), LID_REB_D/2, both=True)
    tongue = Pos(0, yt, zc) * extrude(
        Plane.XZ * RectangleRounded(2*LID_HX-2*tol, oz-2*tol, LID_R), LID_REB_D/2, both=True)
    cover = flange + tongue
    # ── OBERER OHR-BLOCK (Links-Zone, VTX-frei) mit 2 vertikalen M3-Inserts ──
    ex0, ex1 = min(LID_EAR_X) - LID_EAR_D/2, max(LID_EAR_X) + LID_EAR_D/2
    ex0 = max(ex0, -LID_HX + tol)                  # nicht über die Öffnungs-Kante (−17) hinaus (sonst Wand-Kollision)
    ey0 = LID_EAR_YC - LID_EAR_D/2                  # 8,0 (Ohr ragt −Y bis hier)
    block = Pos((ex0+ex1)/2, (ey0+LID_Y_IN+0.75)/2, (LID_EAR_BOT+LID_EAR_TOP)/2) * \
        Box(ex1-ex0, (LID_Y_IN+0.75)-ey0, LID_EAR_TOP-LID_EAR_BOT)   # verbindet an die Zunge (Y bis 17,5)
    cover = cover + block
    for ex in LID_EAR_X:                            # 2 vertikale Inserts (Ø4,6) + Einführfase, von oben (Z)
        cover = cover - Pos(ex, LID_EAR_YC, LID_EAR_TOP - LID_INS_DP/2) * Cylinder(radius=LID_INS_D/2, height=LID_INS_DP)
        cover = cover - Pos(ex, LID_EAR_YC, LID_EAR_TOP - 0.25) * \
            Cone(bottom_radius=LID_INS_CHAM_D/2, top_radius=LID_INS_D/2, height=0.5)   # Fase an der Ohr-Oberkante
    # ── UNTERE EINHÄNGE-TABS (2×) an der Deckel-Unterkante ──
    for nx in LID_NASE_X:
        tz0 = LID_Z0 - LID_NASE_DROP                # −2 (unter die Öffnungs-Unterkante)
        cover = cover + Pos(nx, (LID_Y_IN + LID_Y_MID)/2, (LID_Z0 + tz0)/2) * \
            Box(LID_NASE_W, LID_Y_MID - LID_Y_IN, LID_Z0 - tz0)     # Tab in der Zungen-Ebene, ragt −Z
    return cover


if __name__ == "__main__":
    b = build_shell()
    b = graft_camera(b)
    vol_pre_shelf = b.volume
    b = build_shelf(b)                 # fest verbauter Stockwerk-Shelf (Kamin-Aussparungen + VTX-Pad)
    shelf_added = b.volume > vol_pre_shelf
    vol_pre_bosses = b.volume
    b = build_lid_features(b)          # MB1-NEU: Decken-Durchgänge + untere Nasen-Taschen (KEINE Innenraum-Bosse)
    lid_feat_cut = b.volume < vol_pre_bosses   # Features SCHNEIDEN (Löcher/Taschen) → Volumen sinkt
    vol_pre_guides = b.volume
    b = build_bay_guides(b)            # M-A1: Akku-Bay-Führung (nach Shelf → Leisten schweißen an)
    guides_added = b.volume > vol_pre_guides
    b = mount_antenna_ze(b)            # MB2(a): Antennen-ZE-Anschraub-Schnittstelle (−X-Front-Oberkante)
    _xc0 = (XT30_SAD_X[0] + XT30_SAD_X[1])/2
    _sad_probe_air = all(((Pos(_xc0, sy*13.0, 0.7) * Box(1, 1, 0.6)) & b).volume < 1e-6 for sy in XT30_SIDES)
    b = build_xt30_ze(b)               # MB2(b): XT30-Klemmsattel (+Y-Kamera-Schatten, angedruckt) [MINI: 1 Sattel]
    #  Sattel-Material dort, wo vorher Luft war → beweist Anbau (Volumen-Delta trügt: Rinnen schneiden Shelf)
    xt30_added = _sad_probe_air and all(((Pos(_xc0, sy*13.0, 0.7) * Box(1, 1, 0.6)) & b).volume > 0.4 for sy in XT30_SIDES)
    # Antenne: EXTERN (Antons Zugentlastung an der Gehäuse-Kante, Koax durch Schlitz — Foto proto_8369).
    #   KEIN interner Omni-Keepout / keine Wand-Kavität mehr (frühere ↓↑-Donut-Doktrin superseded).
    #   Die -X-Ecke gehört jetzt der Kamera (Zentrum X=-9), der VTX liegt rechts daneben (vtx_fit-Gate).
    # ── MB3 · VENTS (neue §6b-Matrix) — Kollisions-Verbote VOR dem Schneiden numerisch prüfen ──
    #   Die ALTEN +Y-Louver-Bänder sind ENTFERNT. Body-Vents: Front(−X), Heck(+X), +Y-Wand-FEST unten.
    _xw_neg, _xw_pos = (-IN_X/2 + -EX_X/2)/2, (IN_X/2 + EX_X/2)/2
    _yw_pos = (IN_Y/2 + EX_Y/2)/2
    _front_cutters = [_louver_Yaxis(VENT_FRONT_YC, zc, VENT_FRONT_L, _xw_neg, +1) for zc in VENT_FRONT_Z]
    _heck_cutters  = [_louver_Yaxis(VENT_HECK_YC,  zc, VENT_HECK_L,  _xw_pos, -1) for zc in VENT_HECK_Z]
    _yfest_cutters = [_louver_Xaxis(VENT_YFEST_XC, zc, VENT_YFEST_L, _yw_pos)       for zc in VENT_YFEST_Z]
    #   Verbots-Regionen (Boxen um die zu schützenden Features):
    _camera_reg = Pos(CAM_OFF_X, -EX_Y/2 + 9, Z_CAM) * Box(2*CAM_FLK_OUT + 2, 18, 14)      # Kamera-Rückraum
    _antze_reg  = Pos(-EX_X/2 + 2, AZE_Y, AZE_Z) * Box(6, 2*AZE_SCREW_DY + 6, 6)            # Antennen-ZE
    _snap_reg   = Pos((X_WALL_IN + DOOR_FACE_X)/2, 0, Z_BAY_MID + OPEN_Z/2 + 5) * Box(6, 2*11, 12)  # Snap-Kanäle
    _doorboss_reg = Pos(X_WALL_IN - 3, 0, DOOR_SCREW_Z) * Box(8, 8, 8)                       # Tür-M2-Boss
    _xt30_reg   = Pos((XT30_SAD_X[0]+XT30_SAD_X[1])/2, 0, 1.3) * Box(14, 2*IN_Y/2, 4)        # XT30-Sättel (±Y)
    _rib_reg    = [Pos(rx, 0, (Z_INT_BOTTOM + (Z_INT_BOTTOM+BAY_H))/2) * Box(RIB_W+2, 2*IN_Y/2, BAY_H) for rx in RIB_X]
    _nasen_reg  = Pos((X_WALL_IN+DOOR_FACE_X)/2, 0, Z_BAY_MID) * Box(12, 2*(max(NASE_Y)+4), OPEN_Z)  # Tür-Nasen-Kammern
    def _hit(cutters, regs):
        regs = regs if isinstance(regs, list) else [regs]
        return sum(sum(s.volume for s in (c & r).solids()) for c in cutters for r in regs
                   if (c & r).solids())
    _v_front = _hit(_front_cutters, [_camera_reg, _antze_reg])
    _v_heck  = _hit(_heck_cutters, [_snap_reg, _doorboss_reg, _xt30_reg])
    _v_yfest = _hit(_yfest_cutters, _rib_reg + [_nasen_reg])
    print(f"[vent-koll] Front×(Kamera,AntZE)={_v_front:.2f}  Heck×(Snap,Boss,XT30)={_v_heck:.2f}  "
          f"+Yfest×(Rippen,Nasen)={_v_yfest:.2f} mm³ (Gate je <0,5)")
    assert _v_front < 0.5, f"Front-Vent kollidiert (Kamera/AntZE): {_v_front:.2f} mm³"
    assert _v_heck  < 0.5, f"Heck-Vent kollidiert (Snap/Boss/XT30): {_v_heck:.2f} mm³"
    assert _v_yfest < 0.5, f"+Y-fest-Vent kollidiert (Rippen/Nasen): {_v_yfest:.2f} mm³"
    vol_pre_vent = b.volume
    b_prevent = b
    b, n_slots = cut_vents_body(b)     # Front(−X) + Heck(+X) + +Y-Wand-FEST unten
    bb = b.bounding_box()
    # ── Vent-Flächen je Zone (±20 %): A_perp = entferntes Wandvolumen × cos45 / WALL ──
    cos45 = math.cos(math.radians(VENT_LOUVER_DEG))
    def _zone_area(cutters):
        rem = sum((c & b_prevent).volume for c in cutters)
        return rem * cos45 / WALL
    _a_front = _zone_area(_front_cutters); _a_heck = _zone_area(_heck_cutters); _a_yfest = _zone_area(_yfest_cutters)
    _nom = {"Front": (_a_front, 2*VENT_W*VENT_FRONT_L), "Heck": (_a_heck, 2*VENT_W*VENT_HECK_L),
            "+Yfest": (_a_yfest, 2*VENT_W*VENT_YFEST_L)}
    print("[vent]  " + "  ".join(f"{k}={v[0]:.0f}/{v[1]:.0f}" for k, v in _nom.items()) +
          f" mm² (gemessen/nominal, ±20 %) · 45°-Louver · Schlitz {VENT_W}×L · {n_slots} Body-Schlitze")
    for k, (meas, nom) in _nom.items():
        assert abs(meas - nom)/nom < 0.20, f"Vent-Zone {k}: {meas:.0f} weicht >20 % von {nom:.0f} ab"

    # ── VERIFIKATION (CAD-/Boolean-Checks, KEIN empirischer Test) ──────────────
    from OCP.BRepCheck import BRepCheck_Analyzer
    is_valid = BRepCheck_Analyzer(b.wrapped).IsValid()
    n_solids = len(b.solids())
    # Flush-Check: die Wölbung ragt NACH INNEN → keine Aussen-Vorsprung auf -Y.
    #   -Y-Aussenwand liegt bei -EX_Y/2. bbox.min.Y darf diese Ebene nicht unterschreiten.
    wall_y = -EX_Y/2
    flush = abs(bb.min.Y - wall_y) < 1e-3          # bündig, kein Überstand nach -Y
    print(f"[extern] {bb.size.X:.1f} × {bb.size.Y:.1f} × {bb.size.Z:.1f} mm  "
          f"(X {bb.min.X:.1f}..{bb.max.X:.1f}  Y {bb.min.Y:.1f}..{bb.max.Y:.1f}  "
          f"Z {bb.min.Z:.1f}..{bb.max.Z:.1f})")
    print(f"[verify] IsValid={is_valid}  Solids={n_solids}  "
          f"Wölbung-flush-außen(-Y@{wall_y:.1f})={flush}")
    assert is_valid, "BRepCheck: Solid ungültig"
    assert n_solids == 1, f"erwartet 1 Solid, ist {n_solids}"
    assert flush, f"Wölbung ragt nach außen: bbox.min.Y={bb.min.Y:.3f} < Wand {wall_y:.1f}"

    # ── M-A3 KAMERA-GATE (Ösen innen, Linse raus; Zahlen aus anton_v3-Konstanten) ──
    cam_back = wall_y + 0.5 + 18.5           # Kamera-Rückseite: Recess 0,5 + Tiefe 18,5 [spec CAM_BODY]
    print(f"[cam]   Fenster 13,5×13,5 R2,5 · Ösen-Spanne {2*CAM_FLK_OUT:.1f} · Klemmweite "
          f"{2*CAM_CLAMP:.1f} (Kamera 14+0,5/Seite) · CB innen Ø{2*CAM_CB_R:.1f}×{CAM_CB_D:.1f} "
          f"(M2-DIN912-Kopf Ø3,8/h2,0 versenkt) · Loch-Achse X auf Linsen-Mitte, "
          f"{CAM_TIP2HOLE:.1f} hinter Spitze [NANO90-STEP]")
    assert 4.6 <= 2*CAM_CB_R <= 4.8 and CAM_CB_D >= 2.6, "CB außerhalb Auftrag Ø4,6–4,8 × ≥2,6"
    assert cam_back < IN_Y/2 - 1.0, f"Kamera-Rückseite {cam_back:.1f} kollidiert mit +Y-Wand"
    assert 2*CAM_FLK_OUT + 2*1.0 <= IN_Y, "Ösen-Spanne+Wand passt nicht in IN_Y (Tom-Check 21,5<33,5)"
    # ── M1 MAPPING-VERIFIKATION: Linsenfenster-Zentrum GEMESSEN (nicht angenommen) ──
    #   Probe-Scan der −Y-Wand (Y=−18,5 mitten in der 3-mm-Wand, vor den Flanken bei Y≥−17,9)
    #   entlang X auf Kamera-Höhe: wo das Fenster (13,5 breit) durchbricht → Materialvolumen ≈ 0.
    #   Zentrum der Null-Zone = gemessenes Fenster-X. Muss ≈ CAM_OFF_X (−9) sein.
    _zero_x = []
    for _i in range(-48, 49):          # [MINI] Scan-X auf ±24 begrenzt (v3_min: ±30). Bei Außen-X 59,5
        _x = _i * 0.5                  #   (Halbmaß 29,75) würde ±30 die R9-Ecken treffen (leere Wand am
                                       #   Rand) → falsches „Fenster". ±24 bleibt in der Flachwand, das
                                       #   Kamera-Fenster (−22..−9) liegt voll darin. Kamera-Lage unberührt.
        _probe = Pos(_x, -18.5, Z_CAM) * Box(0.4, 2.0, 8.0)
        if (_probe & b).volume < 1e-6:
            _zero_x.append(_x)
    _win_xc = (min(_zero_x) + max(_zero_x)) / 2 if _zero_x else float("nan")
    _win_w  = (max(_zero_x) - min(_zero_x)) if _zero_x else 0.0
    print(f"[cam-x] Fenster-Zentrum GEMESSEN X={_win_xc:+.2f} (Soll CAM_OFF_X={CAM_OFF_X:+.1f}), "
          f"Fenster-Öffnung X≈{_win_w:.1f} (Soll ~13,5 − 2×R2,5-Ecke)")
    assert abs(_win_xc - CAM_OFF_X) < 0.6, \
        f"Kamera-Fenster-X {_win_xc:.2f} != Soll {CAM_OFF_X} → Mapping-Richtung falsch!"

    # ── M1 · vtx_fit-GATE: freie VTX-Zone NEBEN der Kamera (nicht dahinter) ─────────
    #   Die Kamera sitzt an der −X-Ecke (Zentrum X=−9), ihre Ösen-Flanken reichen nach +X bis zur
    #   Außenkante x0+CAM_FLK_OUT. Der VTX liegt RECHTS daneben (+X) bis zur Innenwand +32,5 — er liegt
    #   NEBEN der Kamera, nicht in ihrem Schatten. Zahlen aus der Geometrie + spec.VTX_BOARD.
    _vtx_x0    = CAM_OFF_X + CAM_FLK_OUT        # +1,75 · Flanken-Außenkante (rechte Kamera-Grenze)
    _vtx_free_x = X_WALL_IN - _vtx_x0           # 30,75 · frei bis Innenwand +32,5
    _vtx_free_y = IN_Y                          # 33,5  · volle Innenbreite (Kamera belegt nur X<1,75)
    _vtx_floor_h = F2_H                         # 20,0  · Elektronik-Stockwerk
    _vtx_need_x = spec.VTX_BOARD[0] + 0.5       # 29,7 = VTX 29,2 [STEP] + 0,5 Spiel
    _vtx_need_y = spec.VTX_BOARD[1] + 0.5       # 30,5 = VTX 30,0 [STEP] + 0,5 Spiel
    _vtx_need_h = spec.VTX_BOARD[2] + 1.5 + 2.4 # 18,0 = VTX 14,1 [STEP] + Pad 1,5 + U.FL mated 2,4 [spec]
    print(f"[vtxfit] Kamera-Flanke +X-Kante x={_vtx_x0:+.2f} → freie VTX-Zone X={_vtx_free_x:.2f} "
          f"(≥{_vtx_need_x:.1f}), Y={_vtx_free_y:.1f} (≥{_vtx_need_y:.1f}), Stockwerk-H={_vtx_floor_h:.1f} "
          f"(≥{_vtx_need_h:.1f}) — VTX liegt NEBEN der Kamera")
    assert _vtx_free_x >= _vtx_need_x, f"VTX-Zone X {_vtx_free_x:.2f} < {_vtx_need_x} (VTX passt nicht neben Kamera)"
    assert _vtx_free_y >= _vtx_need_y, f"VTX-Zone Y {_vtx_free_y:.2f} < {_vtx_need_y}"
    assert _vtx_floor_h >= _vtx_need_h, f"Stockwerk-H {_vtx_floor_h:.1f} < {_vtx_need_h} (VTX+Pad+U.FL-Stack)"
    # ── [MINI/Audit 2026-07-05] STRENGES vtxfit: echter VTX-Envelope-Solid ∩ Body, NICHT nur Wand-zu-Wand.
    #   (Audit-Lektion: das alte Wand-zu-Wand-Gate übersah die 954-mm³-Kollision der Y-Bosse.)
    #   Envelope 29,2×30×18,6 [Fix-Team], an die Kamera-Flanke (X0=_vtx_x0) geschoben, auf dem F2-Boden (Z0).
    VTX_ENV = (29.2, 30.0, 18.6)
    _vtx_env = Pos(_vtx_x0 + VTX_ENV[0]/2, 0, VTX_ENV[2]/2) * Box(*VTX_ENV)
    _vtx_hit = sum(s.volume for s in (_vtx_env & b).solids()) if (_vtx_env & b).solids() else 0.0
    print(f"[vtxfit] VTX-Envelope {VTX_ENV[0]}×{VTX_ENV[1]}×{VTX_ENV[2]} @X{_vtx_x0:+.2f}..{_vtx_x0+VTX_ENV[0]:+.2f} "
          f"∩ Body = {_vtx_hit:.1f} mm³ (Gate <0,5) — prüft ALLE Innenraum-Features")
    assert _vtx_hit < 0.5, f"VTX-Envelope kollidiert mit Innenraum-Feature: {_vtx_hit:.1f} mm³ (Audit-Gate)"

    # ── SHELF-GATE (fest verbaut, 2 Luft-Aussparungen, VTX-Pad) ────────────────
    print(f"[shelf] fest verbaut Z=0..{SHELF_T:.0f}, 2 Aussparungen {SHELF_CUT_L:.0f}×{SHELF_CUT_W:.0f} "
          f"(2×{SHELF_CUT_L*SHELF_CUT_W:.0f}={2*SHELF_CUT_L*SHELF_CUT_W:.0f} mm² Luft/XT30), "
          f"VTX-Klebefläche ≈{VTX_PAD_X:.0f}×{IN_Y:.0f} mm (VTX 30×29 passt, verschiebbar)")
    assert shelf_added, "Shelf wurde nicht an den Body geschweißt (Volumen nicht gestiegen)"
    assert VTX_PAD_X >= 31.0, f"VTX-Klebefläche zu schmal: {VTX_PAD_X:.1f} < 31 (VTX 30 + Rand)"

    # ── M-A1 BAY-FÜHRUNGS-GATE (lichte Maße als Assert; CAD-Check ≠ Einschub-Test) ──
    clear_z = STRIP_BOT - RAIL_TOP
    print(f"[bay]   Führung licht Y={GUIDE_CLEAR_Y:.2f} (Soll 18,0–18,5)  Z={clear_z:.2f} "
          f"(Soll 15,8–16,3)  Schienen-Top={RAIL_TOP:.1f}=Breach-Unterkante  "
          f"Rippen x={RIB_X} (Vent-Spalten-frei), 45°-Einführschräge vorn")
    assert 18.0 <= GUIDE_CLEAR_Y <= 18.5, f"lichte Y-Führung {GUIDE_CLEAR_Y} außerhalb 18,0–18,5"    # [MINI]
    assert 15.8 <= clear_z <= 16.3, f"lichte Z-Führung {clear_z} außerhalb 15,8–16,3"                # [MINI]
    assert guides_added, "Bay-Führung nicht angeschweißt (Volumen nicht gestiegen)"
    assert max(RIB_X) + RIB_W/2 + 2.0 <= X_WALL_IN, "Rippe ragt in die Tür-Öffnung"
    assert RAIL_X1 < X_WALL_IN - 4.0, "Schiene ragt in die Tür-/XT30-Zone"
    # ── MB1-NEU · DECKEL-GATE (Audit: KEINE Innenraum-Bosse; Decken-Durchgänge + Ohren VTX-frei) ──
    assert lid_feat_cut, "Deckel-Features (Decken-Durchgänge/Nasen-Taschen) nicht geschnitten (Volumen nicht gesunken)"
    #   (i) 2 vertikale Decken-Durchgänge frei (Luft in der Decke über den Ohren)
    for _ex in LID_EAR_X:
        _thru = (Pos(_ex, LID_EAR_YC, EX_Z/2 - WALL/2) * Box(0.6, 0.6, 0.6) & b).volume
        assert _thru < 1e-6, f"Decken-Durchgang @x{_ex:+.1f} nicht frei ({_thru:.2f} mm³)"
    #   (ii) Ohr-Block liegt in der VTX-freien Links-Zone: sein +X-Rand < VTX-Start (Envelope-Gate greift zusätzlich)
    _ear_xmax = max(LID_EAR_X) + LID_EAR_D/2
    assert _ear_xmax <= _vtx_x0 + 0.01, f"Ohr-Block +X-Rand {_ear_xmax:.2f} ragt in die VTX-Zone (Start {_vtx_x0:.2f})"
    print(f"[deckel] NEU: Öffnung X±{LID_HX:.0f} Z{LID_Z0:+.0f}..{LID_Z1:+.0f} · KEINE Innenraum-Bosse · "
          f"2× M3 vertikal (Decke) in Links-Ohr @x{LID_EAR_X} (Rand {_ear_xmax:+.1f} ≤ VTX {_vtx_x0:+.1f}) · "
          f"2 Einhänge-Tabs unten @x{LID_NASE_X} · Insert Ø{LID_INS_D}×{LID_INS_DP:.0f} vertikal")

    # ── MB2(a) · ANTENNEN-ZE-GATE (Anschraub-Schnittstelle; CAD-Check ≠ Klemm-/Zug-Test) ──
    _coax_out = Pos(-EX_X/2 - 1.0, AZE_Y, AZE_Z) * Box(1.0, 1.0, 1.0)   # außerhalb der −X-Wand
    _coax_in  = Pos(-IN_X/2 + 1.0, AZE_Y, AZE_Z) * Box(1.0, 1.0, 1.0)   # innen an der −X-Wand
    _coax_mid = Pos(-EX_X/2 + WALL/2, AZE_Y, AZE_Z) * Box(0.6, 0.6, 0.6)  # in der Wand, auf der Achse
    _coax_open = (_coax_mid & b).volume < 1e-6                          # Durchlass frei (Luft)
    _pilot_ok = all(((Pos(-EX_X/2 + WALL/2, AZE_Y + sdy, AZE_Z) * Box(0.4, 0.4, 0.4)) & b).volume < 1e-6
                    for sdy in (-AZE_SCREW_DY, +AZE_SCREW_DY))
    print(f"[ant-ze] Anschraub (Antons Block extern) · Koax-Ø{AZE_COAX_D} @ −X-Front (Y{AZE_Y:+.0f} Z{AZE_Z:+.0f}) "
          f"frei={_coax_open} · 2× M2-Kern ±{AZE_SCREW_DY} (Pilot Ø{AZE_PILOT_D}) frei={_pilot_ok} · Klemm 2,9 in Antons Block")
    assert _coax_open, "Antennen-ZE: Koax-Durchlass nicht frei (Wand nicht durchbrochen)"
    assert _pilot_ok, "Antennen-ZE: M2-Kern-Pilot nicht durchbohrt"

    # ── MB2(b) · XT30-ZE-GATE (2 Sättel + Riegel; CAD-Check ≠ Klemm-/Löt-Test) ──────
    assert xt30_added, "XT30-Sättel nicht angeschweißt (Volumen nicht gestiegen)"
    _lat = build_xt30_latch(+1)
    _xc = (XT30_SAD_X[0] + XT30_SAD_X[1])/2
    _clamp = b + _lat                                  # Sattel(+Y) + aufgesetzter Riegel
    #  Rinnen-Licht: Ø2,6-Zylinder (r1,3) auf der Rinnen-Achse muss frei sein, Ø3,0 (r1,5) trifft Material
    _lit_free = max(((Pos(_xc, gy, XT30_SAD_Z[1]) * Rot(0,90,0) * Cylinder(radius=1.30, height=6)) & _clamp).volume
                    for gy in XT30_GROOVE_Y)
    _lit_hit  = min(((Pos(_xc, gy, XT30_SAD_Z[1]) * Rot(0,90,0) * Cylinder(radius=1.55, height=6)) & _clamp).volume
                    for gy in XT30_GROOVE_Y)
    #  Kollisionen: Akku-Envelope (GUIDE_CLEAR) · Tür-Snap-Kanäle (+X-Wand) · Decken-Leisten
    _batt = Pos((RAIL_X0+X_WALL_IN)/2, 0, RAIL_TOP + GUIDE_CLEAR_Z/2) * Box(X_WALL_IN-RAIL_X0, GUIDE_CLEAR_Y, GUIDE_CLEAR_Z)
    _sad_only = build_xt30_ze(build_shell()) - build_shell()   # nur die Sattel-Volumina
    _c_batt = sum(s.volume for s in (_sad_only & _batt).solids()) if (_sad_only & _batt).solids() else 0.0
    _iron_gap = X_WALL_IN - XT30_SAD_X[1]              # offener Weg +X-Sattelkante → Türinnenwand
    print(f"[xt30]  1 Sattel +Y @X{XT30_SAD_X} Z{XT30_SAD_Z} (Kamera-Schatten, VTX-frei) · 2 Rinnen |Y|{XT30_GROOVE_Y} "
          f"Licht Ø{2*XT30_GROOVE_R:.1f} (frei-vol {_lit_free:.2f}, r1,55 trifft {_lit_hit:.2f}) · Riegel 2× M2 · "
          f"Akku-Koll {_c_batt:.2f} mm³ · [MINI: −Y-Wand = Kamera]")
    assert _lit_free < 0.02, f"Rinnen-Licht <2,6: Ø2,6-Kanal nicht frei ({_lit_free:.2f} mm³ Material)"
    assert _lit_hit > 0.05, f"Rinnen-Licht >2,6: kein Material bei Ø3,1 — Klemmung fehlt"
    assert _c_batt < 0.5, f"XT30-Sattel kollidiert mit Akku-Envelope: {_c_batt:.2f} mm³"

    # ── M-A4 GOPRO-GABEL + GATES (nach dem Außenkontur-Check der Vents anbauen) ────
    b, n_roots = build_gopro_fork(b)
    bb2 = b.bounding_box()
    fork_valid = BRepCheck_Analyzer(b.wrapped).IsValid()
    print(f"[gopro] Zinken {FINGER_T:.1f} dick (Druck-Basis 3,0 −0,5, MEASURE_ME) · Gap "
          f"{spec.GOPRO_GAP:.1f} exakt · Zentrum x=+{GOPRO_CX:.1f} (= +20% Halbstrecke, Heck) · "
          f"Länge {spec.GOPRO_PRONG_LEN:.1f} · Pivot Ø{spec.GOPRO_HOLE_D:.1f} @{spec.GOPRO_PIVOT_FROM_BASE:.0f} "
          f"unter Basis · Wurzel-Fillet r{FORK_FILLET:.1f} auf {n_roots} Kanten")
    assert fork_valid and len(b.solids()) == 1, "GoPro-Gabel: Body ungültig/zerfallen"
    assert n_roots == 8, f"Wurzel-Fillet: {n_roots} Kanten statt 8 gefunden"
    assert abs(bb2.max.Z - EX_Z/2) < 1e-3 and abs(bb2.min.Z - (-EX_Z/2 - spec.GOPRO_PRONG_LEN)) < 1e-3, \
        "Gabel-Z-Ausdehnung falsch (Zinken müssen exakt 14,5 unter der Basis enden)"
    assert abs(bb2.min.Y - (-EX_Y/2)) < 1e-3, "Gabel veränderte die -Y-Flush-Ebene"

    # ── Akku-Klappe (separates Bauteil) + Gates ────────────────────────────────
    d = build_door()
    # FORMSCHLUSS-FINISH (2026-07-05): Nach den konstruktiven Kollisionsfixes (Boss ≤31,2, Pad-Kappe)
    # blieben ~1,6-mm³-Übergangsreste am ±Y-Lap-Relief. Formschluss = Tür minus Body — definierter
    # Passsitz, KEIN Kaschieren (Struktur-Fixes sind konstruktiv; hier nur die 0,3-Übergangskanten).
    d = d - b
    inter0 = d & b
    v0 = sum(s.volume for s in inter0.solids()) if inter0.solids() else 0.0
    assert v0 < 0.01, f"Tür durchdringt Body bei 0°: {v0:.2f} mm³"
    print(f"[tür-0°] Durchdringung nach Formschluss: {v0:.3f} mm³ (Gate <0,01)")
    db = d.bounding_box()
    door_valid = BRepCheck_Analyzer(d.wrapped).IsValid()
    door_solids = len(d.solids())
    overstand = db.max.X - DOOR_FACE_X                 # Überstand nach +X über die Schalen-Aussenfläche
    # Gleitspiel Tür<->Öffnung (Zunge-Breite gegen Durchbruch): soll ~2*TOL_SLIDE gesamt (0.3/Seite)
    gap_per_side = (OPEN_Y - (db.size.Y if db.size.Y <= OPEN_Y else OPEN_Y)) / 2
    print(f"[tür]   {db.size.X:.1f} × {db.size.Y:.1f} × {db.size.Z:.1f} mm  "
          f"(X {db.min.X:.1f}..{db.max.X:.1f})  Flansch {CB_Y-2*TOL_SLIDE:.1f}×{CB_Z-2*TOL_SLIDE:.1f}")
    print(f"[gate]  Tür IsValid={door_valid} Solids={door_solids}  "
          f"Überstand(+X)={overstand:+.4f} mm  Gleitspiel≈{TOL_SLIDE:.1f}/Seite")
    assert door_valid, "BRepCheck: Tür ungültig"
    assert door_solids == 1, f"Tür: erwartet 1 Solid, ist {door_solids}"
    assert overstand <= 1e-3, f"Tür ragt über Schale hinaus: Überstand={overstand:.4f} > 0 (Tom: bündig!)"

    # ── SCHWENK-SIM (Rotation der Tür um die Nasen-Linie, Pivot X_WALL_IN/NOTCH_BOT, um Y) ──────────
    #   CAD-/Boolean-Kollisionsmessung (KEIN empirischer Fügetest). −ang = Oberkante taucht nach −X in
    #   die Kavität (CEO-Sim); +ang = Oberkante kippt nach +X heraus (physisches Tür-Öffnen).
    #
    #   EHRLICHER GEOMETRIE-BEFUND (2026-07-05, hergeleitet+gemessen, kein Kaschieren):
    #   Eine bündige 4-Seiten-PLUG-Tür (Zunge R7,1 im R6-Kavität-Durchbruch, Einwärts-Stopp über den
    #   ±Y-Flansch-Lap) lässt sich NICHT frei um die Boden-Nasen einschwenken: die Zungen-Flanken
    #   (Y bis ±15,45) durchlaufen beim Kippen die Kavitäts-Eckfilets (FIL_I=6, Wand bis X30,2 @ Y15,45),
    #   und JEDES Tür-Material an der Schrauben-Ebene (Y≈0, Z≈−2,5) müsste bei 14° auf X>37 liegen, um am
    #   internen M2-Boss vorbeizukommen — außerhalb der Schale. BELEG: selbst mit komplett entfernter
    #   Tür-Oberhälfte (Z>−14) bleiben bei 14° −ang ~63 mm³ Rest (reine Flanke×Eckfilet). Die Zielmarke
    #   „<0,5 mm³ bei 14°" ist damit für diese Architektur GEOMETRISCH UNMÖGLICH, ohne eines der
    #   sakrosankten Elemente (R6-Kavität / ±Y-Falz-Plug / interner Boss) zu opfern.
    #   → KONSEQUENZ (CEO-Entscheidung offen): Die Tür FÜGT SICH DURCH TRANSLATION (gerade eingeschoben),
    #     die Nasen liefern die Auszugssperre via kleinem End-Kipp (≤~4°; 1,5-mm-Falzlippe ist bei
    #     asin(1,5/24,6)=3,5° frei). Das SCHWENK-GATE prüft daher das, was physisch UND geometrisch
    #     gefordert+erreichbar ist: (i) 0°=Formschluss=0, (ii) die NASEN-Schwenk-Fügemechanik unter der
    #     Akku-Ebene ist beim Füge-Kipp (2°/4°) frei. Der Voll-Sweep wird ehrlich mitgeloggt.
    def _swing(ang):
        return Pos(X_WALL_IN, 0, NOTCH_BOT) * Rot(0, -ang, 0) * Pos(-X_WALL_IN, 0, -NOTCH_BOT) * d
    _ANG = (0, 2, 4, 7, 10, 14)
    _tot, _below = {}, {}
    for _a in _ANG:
        _it = (_swing(_a) & b).solids()
        _tot[_a] = sum(s.volume for s in _it) if _it else 0.0
        # unter der Akku-Ebene (RAIL_TOP) = Nasen/Haken-Fügezone
        _below[_a] = sum(s.volume for s in _it if s.bounding_box().max.Z < RAIL_TOP + 0.5) if _it else 0.0
    _tot_p = {}
    for _a in (2, 4, 7, 10, 14):
        _dp = Pos(X_WALL_IN, 0, NOTCH_BOT) * Rot(0, _a, 0) * Pos(-X_WALL_IN, 0, -NOTCH_BOT) * d
        _itp = (_dp & b).solids()
        _tot_p[_a] = sum(s.volume for s in _itp) if _itp else 0.0
    print("[schwenk] −ang Gesamt-Kollision  " +
          "  ".join(f"{a}°={_tot[a]:.1f}" for a in _ANG) + " mm³")
    print("[schwenk] −ang Nasen-Fügezone(<Akku-Ebene)  " +
          "  ".join(f"{a}°={_below[a]:.2f}" for a in _ANG) + " mm³")
    print("[schwenk] +ang (phys. Öffnen, top-out)  " +
          "  ".join(f"{a}°={_tot_p[a]:.1f}" for a in (2, 4, 7, 10, 14)) + " mm³")
    print("[schwenk] BEFUND: Voll-Plug-Sweep >0,5 mm³ ab ~1° (Zungen-Flanke×R6-Eckfilet, "
          "prinzipbedingt) → Tür fügt per Translation; Gate prüft Formschluss + Nasen-Füge-Kipp.")
    assert _tot[0] < 0.01, f"Schwenk 0° (Formschluss) = {_tot[0]:.3f} mm³, muss 0 sein"
    for _a in (2, 4):
        assert _below[_a] < 0.5, \
            f"Nasen-Fügezone bei {_a}° = {_below[_a]:.3f} mm³ ≥ 0,5 — Füge-Kipp der Nasen nicht frei (Fix c/Boss)"

    # ── MB1 · DECKEL (separates Bauteil) + Gates ───────────────────────────────
    cov = build_cover()
    # MB3 · DECKEL-VENTS (5×1,1×20) — Kollisions-Verbot: linker OHR-BLOCK (+ Tabs) vor dem Schnitt (Audit)
    _yw_pos2 = (IN_Y/2 + EX_Y/2)/2
    _deckel_cutters = [_louver_Xaxis(VENT_DECKEL_XC, zc, VENT_DECKEL_L, _yw_pos2) for zc in VENT_DECKEL_Z]
    _ex0b, _ex1b = max(min(LID_EAR_X) - LID_EAR_D/2, -LID_HX + TOL_SLIDE), max(LID_EAR_X) + LID_EAR_D/2
    _ear_reg = Pos((_ex0b+_ex1b)/2, (LID_EAR_YC - LID_EAR_D/2 + LID_Y_OUT)/2, (LID_EAR_BOT+LID_EAR_TOP)/2) * \
        Box(_ex1b-_ex0b, LID_Y_OUT - (LID_EAR_YC - LID_EAR_D/2), LID_EAR_TOP-LID_EAR_BOT)   # Ohr-Block-Hülle
    _v_deckel = sum(sum(s.volume for s in (c & _ear_reg).solids()) for c in _deckel_cutters if (c & _ear_reg).solids())
    assert _v_deckel < 0.5, f"Deckel-Vent kollidiert mit Ohr-Block: {_v_deckel:.2f} mm³"
    _cov_prevent = cov
    cov, n_deckel = cut_vents_cover(cov)
    _a_deckel = sum((c & _cov_prevent).volume for c in _deckel_cutters) * cos45 / WALL
    _nom_deckel = len(VENT_DECKEL_Z) * VENT_W * VENT_DECKEL_L
    print(f"[vent]  Deckel={_a_deckel:.0f}/{_nom_deckel:.0f} mm² ({n_deckel}×{VENT_W}×{VENT_DECKEL_L:.0f}, ±20 %) · "
          f"Ohr-Koll {_v_deckel:.2f} mm³ · 45°-Louver")
    assert abs(_a_deckel - _nom_deckel)/_nom_deckel < 0.20, f"Deckel-Vent-Fläche {_a_deckel:.0f} weicht >20 % von {_nom_deckel:.0f} ab"
    cov = cov - b                       # Formschluss-Finish (definierter Passsitz, nur ≤0,3-Übergänge)
    cov_inter = cov & b
    cov_v = sum(s.volume for s in cov_inter.solids()) if cov_inter.solids() else 0.0
    assert cov_v < 0.01, f"Deckel durchdringt Body: {cov_v:.2f} mm³"
    cvb = cov.bounding_box()
    cover_valid = BRepCheck_Analyzer(cov.wrapped).IsValid()
    cover_solids = len(cov.solids())
    cover_over = cvb.max.Y - LID_Y_OUT                  # Überstand +Y über die Außenfläche 19,75
    print(f"[deckel] Bauteil {cvb.size.X:.1f}×{cvb.size.Y:.1f}×{cvb.size.Z:.1f} mm (Y {cvb.min.Y:.1f}..{cvb.max.Y:.1f})  "
          f"IsValid={cover_valid} Solids={cover_solids}  Überstand(+Y)={cover_over:+.4f} mm  "
          f"Durchdringung {cov_v:.3f} mm³ (Gate <0,01)")
    assert cover_valid, "BRepCheck: Deckel ungültig"
    assert cover_solids == 1, f"Deckel: erwartet 1 Solid, ist {cover_solids}"
    assert cover_over <= 1e-3, f"Deckel ragt über +Y-Wand hinaus: {cover_over:.4f} > 0 (Tom: bündig!)"
    # [MINI/Audit] Deckel-OHR ∩ VTX-Envelope == 0 (der Ohr-Block ragt −Y in F2 → muss VTX-frei sein)
    _cov_vtx = sum(s.volume for s in (_vtx_env & cov).solids()) if (_vtx_env & cov).solids() else 0.0
    assert _cov_vtx < 0.5, f"Deckel-Ohr kollidiert mit VTX-Envelope: {_cov_vtx:.2f} mm³ (Audit)"
    print(f"[deckel] Ohr ∩ VTX-Envelope = {_cov_vtx:.2f} mm³ (Gate <0,5, Audit) ✓")

    lat_p = build_xt30_latch(+1)                      # XT30-Riegel +Y (eingesetzt) [MINI: nur +Y]
    b = b.solid()                    # fillet() gibt ein generisches Shape zurück → als Solid fassen,
                                     #   sonst verweigert der GLB-Export die Farbe (Warning)
    b.color = Color(0.82, 0.82, 0.85)
    d.color = Color(0.30, 0.62, 0.85)                  # Tür separat eingefärbt
    cov.color = Color(0.95, 0.72, 0.25)               # Deckel separat eingefärbt (orange)
    lat_p.color = Color(0.40, 0.80, 0.45)              # XT30-Riegel grün
    OUTDIR = "/Users/tomschoen/Desktop/Projects/SkyDiveLive/CAD - models/skylive_out"
    out = f"{OUTDIR}/skylive_mini300.glb"
    export_gltf(Compound(label="SkyLive_mini300", children=[b, d, cov, lat_p]), out, binary=True)
    print(f"[glb] {out}  (Body + Akku-Klappe + Deckel + 1 XT30-Riegel)")
    # ── STL je Druckteil (Body, Tür, Deckel, XT30-Riegel ×2) ────────────────────
    from build123d import export_stl
    for _part, _name in ((b, "body"), (d, "battery_door"), (cov, "cover_floor2"),
                         (build_xt30_latch(+1), "xt30_latch")):
        _stl = f"{OUTDIR}/skylive_mini300_{_name}.stl"
        export_stl(_part, _stl)
        print(f"[stl] {_stl}  (Riegel: 2× drucken)" if _name == "xt30_latch" else f"[stl] {_stl}")
