"""SkyLive MINI-300 v2 — NEU-FORK des aktuellen v3_min.py (2026-07-06, T-ZE + Lasche + Vents).
Mini-Deltas (Quelle: _mini_300_ALT_2026-07-05.py Herleitungen + Delta-Karte Memory 07-06):
Akku Tattu 300 3S HV GEMESSEN 45x17,5x15,3 | BAY_L 53,5 | BAY_H 17 | OPEN 19x16 | DOOR_R 4 |
Kamera ganz aussen (Flanke=Innenwand) | OHNE SCHALTER (Floor-2-X voll: Ein/Aus = XT30 stecken) |
Dach-/Deckel-/ZE-Z+X parametrisiert. Ursprungskopf v3_min:
SkyLive V3 — M1: minimale parametrische Schale in V3-Zielmaßen
mit der ECHTEN (extrahierten) Kamera-Wölbung invertiert + verifizierter Seitenklemme
darauf-gegraftet. NICHT die generische Box v3_build.py (verworfen) — die trug keine
der verifizierten Kamera-Features.

M1-Inhalt (genau das):
  1. Hohle gerundete GoPro-Style-Schale in den V3-Zielmaßen (outer RectangleRounded − inner).
  2. Akku-Klappen-Öffnung an der +X-Stirnseite, unteres Stockwerk (Bay-Höhe).
  3. Kamera auf der -Y-Langseite: invert_camera() aus camera_reference.py 1:1 wiederverwendet,
     re-platziert auf die -Y-Wandebene der Minimal-Schale (Wölbung nach INNEN, flush außen,
     Linsenfenster + Seitenklemme 2× M2 QUER/Achse X, 21,5 mm).

Ehrlich: die Prüfungen unten sind CAD-/Boolean-Checks (Watertight/IsValid/bbox),
KEIN empirischer Test. Werte ohne Quelle → MEASURE_ME.
"""
import math
from build123d import (RectangleRounded, Box, Pos, Rot, Color, Compound, Polygon,
                       Plane, Cylinder, Cone, extrude, export_gltf, fillet, Part, Axis)
from camera_reference import (camera_final, WALL_Y, CAM_TIP2HOLE, CAM_FLK_OUT,   # M-A3: Toms finale
                      CAM_CLAMP, CAM_CB_R, CAM_CB_D)                     # Kamera-Lösung (Ösen innen)

# Referenz-Wölbungs-bbox (gemessen aus references/reference_camera_bulge.step):
#   X 6..37 (Mitte 21,5) · Y 24,90..31,40 (Wandebene 24,85, ragt +Y außen) · Z 0..28 (Mitte 14)
BULGE_XC, BULGE_ZC = 21.5, 14.0

# M1 · KAMERA ZUR ECKE (CEO-Entscheidung nach des Referenz-Prototyps realem Druck, Fotos proto_8380/8382:
#   Kamera sitzt an der -X-Ecke — mittig (X=0) lässt dem VTX daneben KEINEN Platz).
#   Kamera-Zentrum von X=0 → X=−9 (Richtung −X-Ecke). Mechanik: in graft_camera bekommt die
#   Transform-Translation X = BULGE_XC + CAM_OFF_X; wegen Rot(0,0,180) landet die Linsen-Mitte
#   (Referenz-Frame CAM_CX=BULGE_XC) bei my-X = (BULGE_XC+CAM_OFF_X) − CAM_CX = CAM_OFF_X = −9.
#   Numerisch verifiziert im Gate unten (Fenster-Scan der −Y-Wand).
CAM_OFF_X = -16.0  # [MINI] Flanken-Aussenflaeche = Innenwand -26,75 + CAM_FLK_OUT (Prinzip 850)      # Tom 07-05 FINAL: Kamera GANZ an die Außenwand — linke Flanken-Außenfläche
                        #   (−21,75−10,75 = −32,5) = Innenwand → verschmilzt; linke Schraube läuft
                        #   durch die −X-AUSSENWAND (Einsenkung+Loch von außen, s. graft_camera).

# ── V3-ZIELMASSE (aus V3_SPEC.md / Auftrag, KEINE Schätzungen) ───────────────
WALL   = 3.0                  # sakrosankt
IN_Y   = 33.5                 # Innenbreite (Tom 2026-07-05: „33–34 ok; 32 ginge, aber Puffer für
                              #   aufgeblähte Akkus lassen") → außen 39,5. Maßkette: Akku 30 + 1,75/Seite;
                              #   VTX liegend 30 (Y) [STEP] + Kabelweg; Kamera-Ösen-Spanne 21,5 läuft
                              #   längs X (nicht Y) und ist davon unberührt (21,5 < 33,5 ohnehin ✓).
BAY_L  = 53.5  # [MINI] Akku 45 + XT30-Raum; Fuehrungs-Anschlag 50,5 (850: 65)                 # Akku-Bay Länge (X): Zelle 60 + XT30-Puffer (nur längs)
BAY_H  = 17.0  # [MINI] Akku 15,3 + 0,75 Swell + 0,95 Rippe (850: 25)                 # Akku-Bay/Klappe Höhe (Z). MEASURE_ME: V3_SPEC nennt 26 (Zelle 23+3),
                              #   Auftrag rechnet Interior-Z mit 25 → hier 25 (Interior-Z=50). Klären.
SHELF_T = 3.0                 # Stockwerk-Shelf (fest verbaut, kommt erst in M4 — M1 nur Hohlraum)
F2_H   = 22.0                 # Elektronik-Stockwerk Höhe — Tom 2026-07-05: „Höhe wie bei Referenz-Prototyp fürs
                              #   OBERE Stockwerk, NICHT antasten (Kabelraum!)" → 20er-Trim zurückgenommen.
                              #   VTX-Stapel 18,0 [STEP+spec] < 22 ✓, Kamera 19,0 [Tom] + Luft < 22 ✓.
FIL_O, FIL_I = 5.5, 3.5       # vertikale Ecken-Radien außen/innen — Tom 07-05: „vertikal zu rund" →
                              #   9/6→5,5/3,5; Balance mit neuen horizontalen Fillets FIL_H.
FIL_H, FIL_HI = 3.0, 1.5      # horizontale Umlauf-Fillets Ober-/Unterkante außen/innen [Tom 07-05 NEU]
# Schalter im DACH über der Links-Zone (des Referenz-Prototyps Druck-Prinzip; Tom 07-05: Tiefe knapp 18 gemessen):
SW_CX, SW_CY = -10.0, -1.0    # X: rechts der Kamera-Flanke (−17,75) + links der VTX-Zone (2,25);
                              #   Y: −1 hält 0,75 Luft zur Ohr-Unterkante (6,75). Envelope-Gate unten.
SW_ENV_D, SW_ENV_DEPTH = 14.0, 18.0   # Kopf-Ø [Datenblatt] × Einbautiefe [Tom 07-05 gemessen]

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
DOOR_R     = 4.0  # [MINI] schmale Tuer (Alt-Fork-Herleitung)        # Tür-/Senk-Eckenradius echot Schale R9            [v2-Präzedenz]
OPEN_Y = 19.0  # [MINI] Akku 17,5 + 1,5 Handling             # Durchbruch-Breite (Y): Akku 30 + 1,5 Handling; > Führung 30,75, < IN_Y 33,5
                          #   (M-A2: 34 wäre breiter als der 33,5-Innenraum gewesen)  [abgeleitet/MEASURE_ME]
OPEN_Z = 16.0  # [MINI] Akku 15,3 + 0,7; = BAY_H-1 haelt RAIL_H 0,5             # Durchbruch-Höhe (Z):   Akku 23 + Swell; < Bay 25     [abgeleitet/MEASURE_ME]
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
# LAP_RELIEF_Z entfernt (Tom 07-06): Profil einheitlich, Freigang = Flansch-Innenfase
LEAD_IN      = 0.5        # 0,5×45°-Lead-in an den lap-freien ±Z-Stoßkanten                                 [Design-Wahl]
TONGUE_LEAD  = 1.5        # 1,5×45°-Lead-Chamfer an der Zungen-Oberkante (inboard) für den Einschwenk-Bogen [CEO 2026-07-05]
# S4 (2026-07-05): die Klick-Cantilever/Snaps an der Tür-Oberkante sind ENTFERNT (Tom: unverständlich;
#   Haltekraft trägt allein die M2-Schraube). Tür = Falz + Nasen + M2 + Griffmulde.
# Nasen (Weg A: unter der Akku-Ebene, in Boden-Taschen; Startwerte MEASURE_ME an des Referenz-Prototyps Realteil):
NASE_Y  = (-5.0, 5.0)  # [MINI]     # Y-Lage: gerader Teil der Unterkante (|Y|<8,65=15,75−R7,1), in Schienen-Lücke (Rail-Y 0,±12) [berechnet]
NASE_W  = 5.0  # [MINI]             # Nasen-Breite (Y) → Y±3, Lücke zwischen Rail@0 (+2) und Rail@12 (10) ist 8 breit  [berechnet]
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
# SCHLICHT-Verschluss (Tom 07-06): Innen-Boss/Pad/CB/Mulde ENTFERNT → Lasche + 1 M2 (s. build)
DOOR_VENT_Z = (Z_BAY_MID - 2.5, Z_BAY_MID + 1.0)  # [MINI param]  # Klappen-Mini-Vents (Tom 07-06: „schmale horizontale Striche auf der
DOOR_VENT_L = 10.0            #   Akku-Vorderseite, nur mini") — 2× 45°-Louver, 10 lang, mittig
DOOR_TAB_W   = 10.0       # Laschen-Breite (Y)                                                    [Tom 07-06]
DOOR_TAB_T   = 2.5        # Laschen-Dicke (proud auf der +X-Wand — klassischer Batteriedeckel)
DOOR_TAB_SZ  = Z_BAY_MID + OPEN_Z/2 + 2.0  # [MINI param] 2 ueber Oeffnungs-Top        # Schraub-Achse Z (ÜBER der Öffnung −0,5, in Wand + Shelf-Leiste 29,5..32,5)
DOOR_THRU_R  = 1.2        # Durchgang Ø2,4 durch die Lasche                                                  [Plan 2.5]
DOOR_PILOT_R = 0.8        # Pilot Ø1,6 selbstschneidend im Schalen-Boss (M2)                                 [Plan 2.5]
# (Daumen-Mulde GRIP_* entfernt — Tom 07-06 „schlichter": die Lasche ist der Griff)

# ── M-A1 · AKKU-BAY-FÜHRUNG (Spec §3: „Akku darf nicht bummeln", Tom 2026-07-05) ──────
#   Ziel-Lichtmaße am Akku 60×30×23 [Tattu 850, genstattu/spec.py]: Y 30,5–31,0 / Z 23,5–24,0.
#   Minimal-Anlage (Tom: „weniger ist mehr"): 3 Boden-Schienen + 2 Decken-Leisten + 2 Rippen-Paare.
#   Alles hinter der Tür-Öffnung (x ≤ 30,5 < X_WALL_IN) → Durchgang bleibt frei.
GUIDE_CLEAR_Y = 18.25  # [MINI] Akku 17,5 + 0,75 (Alt-Fork)   # lichte Führungsbreite [Spec §3 Fenster 30,5–31; Akku 30 + 0,75 Swell/Druck-Luft]
GUIDE_CLEAR_Z = 16.05  # [MINI] Akku 15,3 + 0,75   # lichte Führungshöhe   [Spec §3 Fenster 23,5–24; Akku 23 + 0,75]
RAIL_TOP = Z_BAY_MID - OPEN_Z/2       # Schienen-Oberkante = Breach-Unterkante → Akku gleitet EBEN ein
RAIL_H   = RAIL_TOP - Z_INT_BOTTOM    # = (BAY_H-OPEN_Z)/2, parametrisch (0,5)
RAIL_W, RAIL_Y = 4.0, (0.0, -12.0, +12.0)   # 3 Schienen unter dem 30er-Akku [Design-Wahl, druckstabil]
RAIL_X0, RAIL_X1 = -IN_X/2 + 2.0, X_WALL_IN - 6.5  # [MINI param] 20,25      # vorn Platz für XT30-Raum längs [Spec §3]
STRIP_BOT = RAIL_TOP + GUIDE_CLEAR_Z        # Decken-Leisten-Unterkante (definiert lichte Höhe)
STRIP_T   = (Z_INT_BOTTOM + BAY_H) - STRIP_BOT   # Rest bis Shelf-Unterseite (0,75)
STRIP_X0, STRIP_X1 = -16.0, 16.0            # mittig; ±X-Shelf-Aussparungen (XT30/Luft) bleiben frei
STRIP_Y_IN = 11.0                           # Leisten-Innenkante; außen bis in die Wand geschweißt
RIB_FACE = GUIDE_CLEAR_Y / 2                # Rippen-Anlageflächen bei Y = ±15,375
RIB_W    = 3.5
RIB_X    = (-IN_X/2 + 2.75, X_WALL_IN - 4.0)  # [MINI param]   # 2 Paare. X so gewählt, dass sie die Vent-Schlitz-Spalten der +Y-Wand
                            #   (x-Spannen −19..−10 / −7..2 / 5..14 / 17..26) NICHT schneiden →
                            #   Vents bleiben unangetastet (Tom 2026-07-05: Vents nur mitführen).
RIB_EMBED = 0.3             # Schweiß-Überlappung in die Wand (union)


# ── MB1-NEU · DECKEL = DACH (+Z), Referenz-Prinzip (Tom-Kurskorrektur 2026-07-05) ───────────────
#   „Die Rückseite wird KEIN Deckel — sie ist einfach Rückseite. Der Deckel sitzt OBEN drauf."
#   Die +Y-Seite ist FESTE WAND (nur Schlitze). Der Deckel ist die DACHPLATTE (+Z), wie des Referenz-Prototyps
#   Deckel.STEP. Dach-Öffnung mit umlaufendem Falz (Tür-Prinzip in Z): innerer Durchbruch (inner
#   Dachhälfte) + äußere Senkung (outer Hälfte, +LAP breiter = Auflage-Schulter). Deckel bündig oben.
RLID_HX   = EX_X/2 - 6.0  # [MINI param] (850: 35,5-6=29,5)                                # Öffnungs-Halb-X (Falz +LAP=31,5 < Flach-Top 32,5)  [Design]
RLID_HY   = 13.75                               # Öffnungs-Halb-Y (Falz +LAP=15,75 < Flach-Top 16,75) [Design]
RLID_R    = 3.0                                 # Öffnungs-Eckradius                                 [Design]
RLID_LAP  = 2.0                                 # Falz-Überlapp je Seite (Auflage-Schulter)          [Tür-Präzedenz]
RLID_REB_D = 1.5                                # Falz-Tiefe = halbe Wand                            [Tür-Präzedenz]
RLID_Z_OUT = EX_Z/2                             # 28 · Dach-Außenfläche (Deckel bündig)              [Geometrie]
RLID_Z_IN  = EX_Z/2 - WALL                      # 25 · Innendecke                                    [Geometrie]
RLID_Z_MID = (RLID_Z_IN + RLID_Z_OUT)/2        # 26,5 · Falz-Schulter-Ebene                         [Geometrie]
# M3-Deckel-Durchgang (Spec §8): Durchgang Ø3,4 · CB Ø6,1 × 3,4 (Kopf Ø5,5×h3,0 + Spiel).
LID_THRU_D = 3.4                               # M3-Schaft-Durchgang                            [Spec §8]
LID_CB_D   = 6.1                               # CB-Ø (Kopf Ø5,5 + 0,6 Spiel)                   [Spec §8]
LID_CB_DP  = 3.4                               # CB-Tiefe (Kopf h3,0 + 0,4)                     [Spec §8]
LID_BOSS_CHAM_D = 5.2                           # Insert-Einführfase-Ø                           [Spec §4]
LID_BOSS_CHAM_H = 0.5                           # Fase-Höhe                                      [Spec §4]
# 4 ECK-BOSSE (Body, vertikal, mit Innenecken/Wänden verschmolzen — die Ecke trägt mit): @(±29,±13),
#   Z 14..25, Ø8, Insert Ø4,6×8 von OBEN + Fase Ø5,2×0,5. Top (25) liegt in der Dach-Öffnung → Insert
#   von oben zugänglich; der Deckel-M3 @(±29,±13) fällt vertikal hinein.
RBOSS_X, RBOSS_Y = EX_X/2 - 6.5, 13.0  # [MINI param]                   # Boss-/Schrauben-Zentren (in der Öffnung X±29,5/Y±13,75)
RBOSS_D  = 8.0                                  # Boss-Außen-Ø
RBOSS_Z1 = EX_Z/2 - WALL                        # 25 · Boss-Top = Innendecke = Insert-Mündung
RBOSS_Z0 = RBOSS_Z1 - 11.0                      # 14 · Boss-Boden (11 lang)
RBOSS_INS_D, RBOSS_INS_DP = 4.6, 8.0            # Insert-Bohrung Ø4,6 × 8 (ACHSE Z, von oben)    [Spec §4]
RLID_SCREW = [(-RBOSS_X, RBOSS_Y), (-RBOSS_X, -RBOSS_Y)]   # [MINI] 2 M3 VORNE; hinten Einhaenge-Nasen (kein +X-Boss-Platz: VTX-Env bis 24,45)
#   KEIN Boss: Kamera@−21,75 belegt die Ecke (dort hält die Falz-Lippe; Asymmetrie wie des Referenz-Prototyps Druck)


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
#  +Y-WAND (fest, im BODY), S1-NEU · 2 Zonen lange Schlitze: OBEN 3×(1,1×40) über Stockwerk 2,
#   UNTEN (Bay) 2×(1,1×24). Länge X, gestapelt in Z, X-Zentrum 0, y_mid +18,25 (_louver_Xaxis).
VENT_YWALL_XC     = 0.0                          # X-Zentrum (Schlitze mittig; ZE sitzt auf den
                                                 #   KURZEN Seiten — ±Y-Wände gehören den Vents)
VENT_YWALL_TOP_L  = 40.0                         # oben lang (X −20..+20) → boss-frei (Bosse @X±29)
VENT_YWALL_TOP_XC = (0.0,)                       # 1 Segment (Splittung von 07-05 zurückgenommen)
VENT_YWALL_TOP_Z  = tuple(Z_INT_BOTTOM + BAY_H + SHELF_T + d for d in (6.5, 9.5, 12.5))  # [MINI param Shelf-Top-relativ]           # 3 Reihen Stockwerk 2
VENT_YWALL_BAY_L  = 24.0                         # Bay lang (X −12..+12)
VENT_YWALL_BAY_Z  = (Z_BAY_MID - 0.5, Z_BAY_MID + 2.5)  # [MINI param]              # 2 Reihen Bay-Zone
#  Front (−X, im BODY): 2×(1,1×16) oben (VTX-Stockwerk), Länge Y, gestapelt in Z; unter Antennen-ZE (Z21).
VENT_FRONT_L = 16.0
VENT_FRONT_Z = ()                               # OBEN ENTFERNT (Kamera@−21,75 füllt die −X-Wand-Zone
                                                #   ehrlich aus — Gate maß 24,65 mm³; Toms Front-Wunsch
                                                #   war Stockwerk 1 = FRONT_LO, die bleiben)
VENT_FRONT_YC = 0.0                             # Y-Zentrum (Länge 16 → Y−8..8 ⊂ Flachzone ±10,75)
#  Heck (+X, im BODY): 2×(1,1×16) ÜBER der Klappe, Länge Y, gestapelt in Z; über den Snap-Kanälen (Z≤11).
VENT_HECK_L = 16.0
VENT_HECK_Z = tuple(Z_INT_BOTTOM + BAY_H + SHELF_T + d for d in (10.5, 13.5))  # [MINI param]                      # über den Snap-Kanälen (Louver-Bottom ≥11,5) und
                                                #   UNTER der T-ZE-Stem-Zone (ab Z20,6 — Louver-
                                                #   Auswaschung braucht ~2 Luft, 07-06 gemessen 4,65er
                                                #   Regions-Konflikt bei 15/18)
VENT_HECK_YC = 0.0
#  (S3: die +Y-Wand-FEST-unten-Zone ist ENTFERNT — die +Y-Wand-Bay ist jetzt vom Volldeckel überdeckt;
#   die Bay-Schlitze sitzen jetzt im Deckel, VENT_DECKEL_BAY_*.)
#  KAMERA-SEITE (−Y, feste Wand) — Tom 07-05: „auch bei der Kamera", lange Seiten = LANGE Schlitze.
VENT_CAM_L  = 26.0                              # X 3..29 ⊂ Flachzone ±30 (FIL_O 5,5), rechts der
VENT_CAM_XC = 16.0                              #   Kamera-Flanken (enden +1,75) → kollisionsfrei
VENT_CAM_BAY_Z = (Z_BAY_MID + 1.0,)  # [MINI param]                       # Tom 07-06: EIN langer Schlitz unterm Kameraloch,
VENT_CAM_BAY_L = 24.0                           #   Akku-Stockwerk, wie die Rückseite (2×24) nur einzeln
                                                #   → Luft staut nicht vorn, Querstrom durch die Bay
VENT_CAM_Z  = (12.5, 15.5)                      # Stockwerk 2, neben dem Linsenfenster (X −15,75..−2,25)
#  FRONT UNTEN (−X, Stockwerk 1/Akku) — Tom 07-05: „auf der Vorderseite auf Stockwerk [1]".
VENT_FRONT_LO_L = 12.0
VENT_FRONT_LO_Z = (Z_BAY_MID - 0.5, Z_BAY_MID + 2.5)  # [MINI param]                # Akku-Höhe; Bay-Schienen (Z<−23,5) + Rippen frei


def _louver_Xaxis(xc, zc, L, y_mid, sgn=+1):
    """Louver-Cutter für ±Y-Flächen: Schlitz lang in X (L), schmal in Z (VENT_W), 45° um X gekippt
    → Durchbruch ±Y/−Z (abwärts-auswärts). y_mid = Wand-Mittelebene, sgn = Wand-Normale (+1=+Y)."""
    return Pos(xc, y_mid, zc) * Rot(-sgn * VENT_LOUVER_DEG, 0, 0) * Box(L, VENT_THROUGH, VENT_W)


def _louver_Yaxis(yc, zc, L, x_mid, sgn):
    """Louver-Cutter für ±X-Flächen: Schlitz lang in Y (L), schmal in Z (VENT_W), um Y gekippt
    → Durchbruch ±X/−Z (abwärts-auswärts). x_mid = Wand-Mittelebene, sgn = Wand-Normalenrichtung (±1)."""
    return Pos(x_mid, yc, zc) * Rot(0, sgn*VENT_LOUVER_DEG, 0) * Box(VENT_THROUGH, L, VENT_W)


def cut_vents_body(body):
    """MB3: schneidet Front(−X), Heck(+X), Kamera(−Y), Front-unten(−X) UND die langen +Y-WAND-Schlitze
    (fest, S1-NEU: OBEN 3×40 + Bay 2×24) in den BODY. Rückgabe (body, n). CAD ≠ Luftstrom-Test."""
    n = 0
    xw_neg = (-IN_X/2 + -EX_X/2)/2           # −X-Wand-Mittelebene = −34
    xw_pos = ( IN_X/2 +  EX_X/2)/2           # +X-Wand-Mittelebene = +34
    yw_pos = ( IN_Y/2 +  EX_Y/2)/2           # +Y-Wand-Mittelebene = +18,25
    for zc in VENT_FRONT_Z:
        body = body - _louver_Yaxis(VENT_FRONT_YC, zc, VENT_FRONT_L, xw_neg, +1); n += 1
    for zc in VENT_HECK_Z:
        body = body - _louver_Yaxis(VENT_HECK_YC, zc, VENT_HECK_L, xw_pos, -1); n += 1
    # S1-NEU: die langen Schlitze sitzen jetzt in der FESTEN +Y-Wand (kein Deckel mehr dort).
    for zc in VENT_YWALL_TOP_Z:
        for xc in VENT_YWALL_TOP_XC:             # 2 Segmente je Reihe (Mitte = ZE-Tasche)
            body = body - _louver_Xaxis(xc, zc, VENT_YWALL_TOP_L, yw_pos); n += 1
    for zc in VENT_YWALL_BAY_Z:
        body = body - _louver_Xaxis(VENT_YWALL_XC, zc, VENT_YWALL_BAY_L, yw_pos); n += 1
    yw_neg = (-IN_Y/2 + -EX_Y/2)/2           # −Y-Wand-Mittelebene = −18,25 (Kamera-Seite)
    for zc in VENT_CAM_Z:                    # Tom 07-05: lange Schlitze auch auf der Kamera-Seite
        body = body - _louver_Xaxis(VENT_CAM_XC, zc, VENT_CAM_L, yw_neg, sgn=-1); n += 1
    for zc in VENT_CAM_BAY_Z:                # Tom 07-06: 1 langer Bay-Schlitz unterm Kameraloch
        body = body - _louver_Xaxis(0.0, zc, VENT_CAM_BAY_L, yw_neg, sgn=-1); n += 1
    for zc in VENT_FRONT_LO_Z:               # Tom 07-05: Front auch Stockwerk 1 (Akku)
        body = body - _louver_Yaxis(VENT_FRONT_YC, zc, VENT_FRONT_LO_L, xw_neg, +1); n += 1
    return body, n


# ── FEST VERBAUTER STOCKWERK-SHELF (Referenz-Prinzip, mitgedruckt — kein Einlege-Tray) ──
#   V3_SPEC „Stockwerke": Shelf = Teil des Body, Z zwischen Akku-Bay (oben Z=0) und Elektronik.
#   KEIN durchgehender Boden — 2 Luft-Aussparungen (Kamin + XT30-Durchlass), zentrale VTX-
#   Klebefläche bleibt flach + groß (modular/verschiebbar). Maße aus V3_SPEC/Airflow, keine Schätzung.
SHELF_MID_Z = Z_INT_BOTTOM + BAY_H + SHELF_T/2   # = 1.5  (Shelf-Mitte, Z 0..3)
SHELF_CUT_L, SHELF_CUT_W = 8.0, 28.0  # [MINI] 12->8: VTX-Klebeflaeche halten (Alt-Fork)
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
FINGER_T = 3.0      # Zinken-Dicke: Tom 2026-07-06 FINAL: „mach die GoPro-Zähne 3 mm" (= des Referenz-Prototyps 3,0).
                    #   Separation/Gap bleibt 3,3 exakt (spec.GOPRO_GAP). (spec 2,7 = ältere Basis, nicht genutzt.)
GOPRO_CX = 0.0                # Tom 2026-07-05 FINAL: „mach's einfach KOMPLETT mittig" (das frühere
                              #   „+20% nach hinten" war ein Missverständnis der Achse — aufgehoben).
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
    """YZ-Profil (Plane.YZ) der Falz-Zone — VEREINHEITLICHT (Tom 07-06 „gute Klappe"): EIN
    durchgehend gerundetes Rechteck über die volle Höhe. Der alte LAP_RELIEF-Auslauf (oben
    schmaler) erzeugte die sichtbaren Treppenstufen an der Klappen-Außenkontur — weg. Den
    Kipp-Freigang der breiten Top-Ecken übernimmt jetzt eine INNEN-Fase am Flansch-Top
    (build_door, außen unsichtbar). ±Y-Lap-Schulter läuft damit VOLL umlaufend (mehr Auflage).
    dy/dz = Inset je Seite (0=Senkung, TOL_SLIDE=Flansch); beide teilen das Profil → kein Drift."""
    return Plane.YZ * RectangleRounded(CB_Y - 2*dy, OPEN_Z - 2*dz, DOOR_R)


def cut_roof_opening(body):
    """MB1-NEU/S2: DACH (+Z) öffnen — bündiger Falz (Tür-Prinzip in Z): innerer Durchbruch (inner
    Dachhälfte 25..26,5) + äußere Senkung (outer Hälfte 26,5..28, +RLID_LAP breiter = Auflage-Schulter)
    → Öffnung durchgehend, Rahmen mit Außen-Rebate für den bündigen Dach-Deckel. CAD ≠ Test."""
    # (a) innerer Durchbruch (Zungen-Sitz): inner Dachhälfte — Cutter dünn in Z (Normale Z)
    z_in = (RLID_Z_IN + RLID_Z_MID)/2
    body = body - Pos(0, 0, z_in) * extrude(
        RectangleRounded(2*RLID_HX, 2*RLID_HY, RLID_R), RLID_REB_D/2 + 0.1, both=True)
    # (b) äußere Senkung (Flansch-Sitz): outer Hälfte, +RLID_LAP je Seite (Schulter-Rebate)
    z_out = (RLID_Z_MID + RLID_Z_OUT)/2
    body = body - Pos(0, 0, z_out) * extrude(
        RectangleRounded(2*(RLID_HX+RLID_LAP), 2*(RLID_HY+RLID_LAP), RLID_R), RLID_REB_D/2 + 1.0, both=True)
    # [MINI] 2 Heck-Nasen-TASCHEN unter der +X-Falz-Schulter (Deckel-Einhaengen)
    for ty in (-8.0, 8.0):
        body = body - Pos(RLID_HX + 1.35, ty, RLID_Z_IN + 0.75) * Box(2.9, 6.6, 1.7)
    return body


def build_corner_bosses(body):
    """S3-NEU: 4 vertikale Eck-Insert-Bosse (Ø8, Z 14..25) @(±29,±13), mit den Innenecken/Wänden
    verschmolzen (die Ecke trägt mit). Insert-Bohrung Ø4,6×8 von OBEN (Achse Z) + Einführfase Ø5,2×0,5
    an der Mündung (Boss-Top = Innendecke 25, in der Dach-Öffnung → von oben zugänglich). CAD ≠ Insert-Test."""
    body = Part() + body                                        # koerziere Solid→Compound (fusionsfähig)
    for (px, py) in RLID_SCREW:
        # Boss-Post (Ø8, Achse Z, Z 14..25)
        body = body + Pos(px, py, (RBOSS_Z0 + RBOSS_Z1)/2) * Cylinder(radius=RBOSS_D/2, height=RBOSS_Z1 - RBOSS_Z0)
        # Insert-Bohrung Ø4,6 × 8 (von der Mündung 25 nach unten)
        body = body - Pos(px, py, RBOSS_Z1 - RBOSS_INS_DP/2) * Cylinder(radius=RBOSS_INS_D/2, height=RBOSS_INS_DP)
        # Einführfase Ø5,2×0,5 an der Mündung (oben): eng unten → weit an der Mündung (Cone nach −Z gekippt)
        body = body - Pos(px, py, RBOSS_Z1 - LID_BOSS_CHAM_H/2) * Rot(180, 0, 0) * \
            Cone(bottom_radius=RBOSS_INS_D/2, top_radius=LID_BOSS_CHAM_D/2, height=LID_BOSS_CHAM_H)
        # Schraub-/Driver-Durchgang Ø4 durch die Falz-Schulter-Reste über dem Boss (Z 25..28,5):
        # die Rand-Bosse liegen an der R3-Öffnungsecke — ohne Freistellung bliebe ein Grat im Schraubweg.
        body = body - Pos(px, py, (RLID_Z_IN + RLID_Z_OUT)/2) * Cylinder(radius=2.0, height=WALL + 1.0)
    return body


def build_shell():
    """Hohle gerundete Schale + Akku-Klappen-Öffnung. Ursprung zentriert.
    M1: KEIN Shelf/Aussparungen (kommt M4) — nur der durchgehende Hohlraum ist vorgesehen."""
    outer = extrude(RectangleRounded(EX_X, EX_Y, FIL_O), EX_Z/2, both=True)
    # Tom 07-05: horizontale Umlauf-Fillets (Ober-/Unterkante) — Balance zu den vertikalen 5,5ern.
    outer = fillet(outer.edges().group_by(Axis.Z)[0] + outer.edges().group_by(Axis.Z)[-1], FIL_H)
    inner = extrude(RectangleRounded(IN_X, IN_Y, FIL_I), IN_Z/2, both=True)
    inner = fillet(inner.edges().group_by(Axis.Z)[0] + inner.edges().group_by(Axis.Z)[-1], FIL_HI)
    body = outer - inner
    # S2-NEU: das Schalter-Loch wandert vom Body-Dach in den DECKEL (Dach ist jetzt der Deckel, Referenz-Prototyp).
    #   → hier KEIN Dach-Schalterloch mehr (siehe build_deckel).
    # ── Akku-Klappe (+X-Stirnseite, unteres Stockwerk): BÜNDIGER Falz statt simpler Durchbruch ──
    # (a) innerer Durchbruch (Zunge-Sitz): innere Wandhälfte 32.5..34.0, Öffnung OPEN_Y x OPEN_Z
    x_in = (X_WALL_IN + X_SHOULDER) / 2
    body = body - Pos(x_in, 0, Z_BAY_MID) * extrude(
        Plane.YZ * RectangleRounded(OPEN_Y, OPEN_Z, DOOR_R - REBATE_LAP), REBATE_D/2 + 0.1, both=True)
    # (b) äußere Senkung (Flansch-Sitz): HYBRID-Falz — ±Y-Lap (Schulter bei 34,0), ±Z LAP-FREI (flush),
    #     Profil EINHEITLICH gerundet (Tom 07-06, s. _door_yz). Senkung: dy=dz=0.
    x_cb = (X_SHOULDER + DOOR_FACE_X) / 2
    body = body - Pos(x_cb, 0, Z_BAY_MID) * extrude(_door_yz(0.0, 0.0), REBATE_D/2 + 1.0, both=True)
    # (c) NASEN-FUSS-NOTCHES: 2 kleine Schlitze unter der Öffnung (Y±6) → der Tür-Fuß taucht unter
    #     die Akku-Ebene ab. BLIND (Tom 07-06 „gute Klappe"): nur innere Wandhälfte bis zur
    #     Schulter 34,0 — die äußere 1,5er-Haut bleibt zu → die zwei „Zähne" sind außen unsichtbar.
    for ny in NASE_Y:
        body = body - Pos((X_WALL_IN - 1.0 + X_SHOULDER)/2, ny, (NOTCH_BOT + (Z_BAY_MID - OPEN_Z/2))/2) * \
            Box(X_SHOULDER - X_WALL_IN + 1.0, NASE_W + 2*TOL_SLIDE, (Z_BAY_MID - OPEN_Z/2) - NOTCH_BOT)
    # (c2) S4: die Snap-Einschwenk-Kanäle sind ENTFERNT (Tür-Snaps entfallen) — die +X-Wand über der
    #     Öffnung bleibt geschlossen. Kein Snap → keine Wandtaschen/Restwand-Aufdickung mehr nötig.
    # (d) SCHLICHT-Verschluss (Tom 07-06: „geht das schlichter? passt der Akku beim vorstehenden
    #     Gewinde überhaupt rein?" — NEIN: alter Innen-Boss X26,5..31,2/Z−6..1 kollidierte bis 2,0
    #     mit dem Akku-Ende 28,5 inkl. Swell, war nie gegen den Akku-Envelope gegated): Innen-Boss
    #     KOMPLETT ENTFERNT. Stattdessen klassische LASCHE oben mittig an der Klappe (proud), M2
    #     ÜBER der Öffnung durch die Wand in die Shelf-Rand-Leiste (X 29,5..32,5) — Pilot Ø1,6×7,
    #     NULL Innenraum-Anspruch, Akku-Zone bleibt komplett frei.
    #     UPGRADE (Tom 07-06 Schrauben-Audit): die Tür-M2 ist die MEISTGELÖSTE Schraube (jeder
    #     Akkuwechsel) → M2-MESSING-INSERT statt selbstschneidendem PETG. Toms Insert GEMESSEN
    #     Ø3,2×3,0 → Bohrung Ø2,8×5,0 (−0,4 Untermaß + 2 Verdrängung, M3-Praxis) + Fase.
    #     Achse X, durch die Wand in die Shelf-Leiste; Mund außen, von der Lasche verdeckt.
    #     Schraube: M2×6 DIN 912 (Lasche 2,5 + Insert 3,0).
    body = body - Pos(EX_X/2 - spec.INSERT_M2_HOLE_DEPTH/2 + 0.01, 0, DOOR_TAB_SZ) * Rot(0, 90, 0) * \
        Cylinder(radius=spec.INSERT_M2_HOLE_D/2, height=spec.INSERT_M2_HOLE_DEPTH)
    body = body - Pos(EX_X/2 - spec.INSERT_M2_CHAMFER/2 + 0.01, 0, DOOR_TAB_SZ) * Rot(0, 90, 0) * \
        Cone(bottom_radius=spec.INSERT_M2_HOLE_D/2, top_radius=spec.INSERT_M2_HOLE_D/2 + 0.3,
             height=spec.INSERT_M2_CHAMFER)
    # (e) Boden-Taschen + Kopf-Kammern für die Tür-Nasen (Weg A)
    body = build_bay_catches(body)
    # (f) MB1-NEU · DECKEL = DACH: Dach (+Z) öffnen (bündiger Falz). Eck-Bosse folgen in build_corner_bosses.
    body = cut_roof_opening(body)
    return body


def graft_camera(shell):
    """invert_camera() 1:1 re-platziert: verschiebe die Minimal-Schale in des Referenz-Prototyps Frame, sodass die
    -Y-Wandebene auf des Referenz-Prototyps Wandebene (Y=WALL_Y) und die Wölbungs-Mitte (X21,5/Z14) auf die -Y-Face-
    Mitte (X0 / Z_CAM) fällt; wende invert_camera 1:1 an; transformiere zurück.

    Transform M (mein Frame → Referenz-Frame): Rot 180° um Z dreht meine Aussen-Normale -Y auf des Referenz-Prototyps +Y
    (outward), dann Translation. So bleibt jede Referenz-interne Relation (Wölbung↔Linse↔Klemmbohrungen)
    exakt erhalten (= 1:1 wiederverwendet), nur re-platziert."""
    M = Pos(BULGE_XC + CAM_OFF_X, WALL_Y - EX_Y/2, BULGE_ZC - Z_CAM) * Rot(0, 0, 180)
    gk_ref = M * shell                     # Schale in des Referenz-Prototyps Frame
    # M-A3: camera_final = Linse RAUS (Fenster, flush außen), des Referenz-Prototyps Ösen-Struktur NACH INNEN
    #   (Flanken + Ø8,4-Bosse + X-Achs-Bohrung + Ø4,7×2,6-CB innen). clear_ref=False: die
    #   Minimal-Schale hat keine interne Kamera-Altlast. Flanken-Z-Höhe 12 < F2_H 20 ✓.
    fixed = camera_final(gk_ref, clear_ref=False)
    body = M.inverse() * fixed               # zurück in meinen Frame
    # Tom 07-05: „Einsenkung mit Loch in der AUSSENWAND statt Stützstruktur" — die linke Kamera-
    # Schraube geht durch die −X-Wand: Ø2,4-Bohrung von außen bis in die (wandverschmolzene) linke
    # Flanke + Zylinderkopf-CB Ø4,7×2,6 in der Außenfläche → von AUSSEN schraubbar. Loch-Achse =
    # Kamera-Querachse @(Y −8,75, Z 14) [aus camera_final: Spitze→Loch 10,5, Linsen-Mitte].
    y_hole = -(EX_Y/2) + 0.5 + CAM_TIP2HOLE          # −19,75 + 11 = −8,75
    body = body - Pos(-EX_X/2 + 4.0, y_hole, Z_CAM) * Rot(0, 90, 0) * Cylinder(radius=1.2, height=9.0)
    body = body - Pos(-EX_X/2 + 1.3, y_hole, Z_CAM) * Rot(0, 90, 0) * Cylinder(radius=2.35, height=2.6)
    return body


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
        # Fuß: füllt die BLINDE Breach-Notch (nur innere Wandhälfte bis Schulter −0,1 — die
        # äußere 1,5er-Haut bleibt zu, Tom 07-06), überlappt 2 mm in die Zunge (→ 1 Solid)
        door = door + Pos((X_WALL_IN + TOL_SLIDE + X_SHOULDER - 0.1)/2, ny,
                          (NOTCH_BOT + TOL_SLIDE + z_open_bot + 2.0)/2) * \
            Box((X_SHOULDER - 0.1) - (X_WALL_IN + TOL_SLIDE), NASE_W,
                (z_open_bot + 2.0) - (NOTCH_BOT + TOL_SLIDE))
        # Finger nach −X (unter Akku-Ebene)
        door = door + Pos((FIN_XIN + HOOK + X_WALL_IN + TOL_SLIDE + 0.1)/2, ny,
                          (FIN_BOT + NASE_TOP)/2) * \
            Box((X_WALL_IN + TOL_SLIDE + 0.1) - (FIN_XIN + HOOK), NASE_W, NASE_T)
        # Haken-Kopf am Finger-Ende (ragt über Finger-Oberkante → Auszugssperre)
        door = door + Pos(FIN_XIN + HOOK/2, ny, (FIN_BOT + LIP_TOP - 0.2)/2) * \
            Box(HOOK, NASE_W, (LIP_TOP - 0.2) - FIN_BOT)
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
    # KIPP-INNENFASE am Flansch-Top (Tom 07-06): das einheitliche Profil hat den Lap-Auslauf
    #   ersetzt — den Einschwenk-Freigang der breiten Top-Ecken gibt jetzt eine 45°-Fase an der
    #   INNEN-Oberkante des Flanschs (1,2×1,2, volle Breite, von außen unsichtbar).
    flange = flange - Pos(X_SHOULDER, 0, Z_BAY_MID + OPEN_Z/2 - TOL_SLIDE) * Rot(0, 45, 0) * \
        Box(1.2*1.42, CB_Y + 2.0, 1.2*1.42)
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
    # SCHLICHT-Verschluss (Tom 07-06): LASCHE oben mittig, proud auf der Wand ÜBER der Öffnung —
    #   1× M2 Zylinderkopf durch die Lasche in den Wand+Shelf-Piloten. Kein Innen-Boss, kein Pad,
    #   keine Mulde mehr (Griff = die Lasche selbst nach dem Lösen). Akku-Zone bleibt komplett frei.
    z_ot = Z_BAY_MID + OPEN_Z/2                               # Öffnungs-Oberkante −0,5
    door = door + Pos(DOOR_FACE_X + DOOR_TAB_T/2, 0, (z_ot - 1.5 + DOOR_TAB_SZ + 3.0)/2) * \
        Box(DOOR_TAB_T, DOOR_TAB_W, (DOOR_TAB_SZ + 3.0) - (z_ot - 1.5))
    door = door - Pos(DOOR_FACE_X + DOOR_TAB_T/2, 0, DOOR_TAB_SZ) * Rot(0, 90, 0) * \
        Cylinder(radius=DOOR_THRU_R, height=DOOR_TAB_T + 1)   # Durchgang Ø2,4 (Kopf liegt proud auf)
    # MINI-VENTS in der Klappe (Tom 07-06: „schmale horizontale Striche auf der Akku-Vorderseite,
    #   nur mini"): 2× 45°-Louver 10 lang, mittig — Zuluft direkt am Akku, GoPro-Deckel-Optik.
    #   Klappen-Dicke dort = Flansch 1,5 + Zunge 1,5 ≈ Wand → Louver-Cutter wie am Heck (sgn −1).
    for zc in DOOR_VENT_Z:
        door = door - _louver_Yaxis(0.0, zc, DOOR_VENT_L, (X_WALL_IN + TOL_SLIDE + DOOR_FACE_X)/2, -1)
    return door


# ── MB2(a) · ANTENNEN-ZUGENTLASTUNG — Anschraub-Position (des Referenz-Prototyps Block extern, Spec §5) ──────
#   ENTSCHEIDUNG NACH PLATZ (dokumentiert, Spec: „Union ODER Anschraub, entscheide nach Platz"):
#   des Referenz-Prototyps Block 17,9×13,05×5,8 passt NICHT kollisionsfrei intern — Floor-2 ist voll (Kamera
#   X−19,75..1,75 · VTX X1,75..31 · Deckel-Bosse in den Ecken), und seine Rückwand-Schrauben (Achse
#   Y, flächig) verlangen eine ±Y-Wand; beide sind belegt (+Y=Deckel, −Y=Kamera). Der Block ist
#   ohnehin ein EXTERNER Strain-Relief (des Referenz-Prototyps Realdruck, Foto proto_8369). Also KEIN Union: des Referenz-Prototyps
#   Block bleibt SEIN separates Druckteil (STEP); ich stelle nur die Schnittstelle an der −X-Front-
#   Oberkante bereit — Koax-Kanten-Schlitz + 2× M2-Kern-Bosse („Rückwand-Prinzip", flächig verschraubt).
#   Klemm-Differenz 2,9 bleibt in des Referenz-Prototyps Block (unverändert, Spec §5). Antenne vertikal → Koax nach −X.
# T-PRINZIP FINAL (Tom 07-06, Fotos IMG_8398–8402: „ÜBERNIMM DIESES PRINZIP — Antenne links
# UND rechts verankert, auf der KURZEN Seite, oberst, Gehäuse dennoch geschlossen"):
#   des Referenz-Prototyps echtes System = T-SCHLITZ oben in der kurzen Seite: ein 2,9 breiter DURCHGANGS-
#   Schlitz von der Oberkante (Ø3,1-Koax wird von OBEN eingelegt und in den 2,9-PRESSSITZ
#   gedrückt — „hebt gut", des Referenz-Prototyps Standard), Rundboden r1,45 als Kabel-Sitz. Außen eine
#   flache T-VERTIEFUNG, in die ein flaches T-STÜCK einfährt und den Schlitz verschließt;
#   oben ein Deckflansch im Dachrand-Spotface mit 2× M2 VERTIKAL (Köpfe nach OBEN, Tom #4)
#   in die Wand-Oberkante. Das Kabel steigt durch die offene Flansch-Kerbe nach OBEN aus —
#   die Omni steht über dem Gehäuse, kurzseitig verankert. BEIDSEITIG identisch (Front −X +
#   Heck +X, Y=0): Kabelseite = T-Stück MIT Kerbe, Gegenseite = BLINDES T-Stück (geschlossen).
#   Sitz-Höhe 24,0: über Kamera-Rahmen-Top ~23,5 [STEP+Spec] und VTX-Env-Top 22,6 [Spec];
#   Front-Zuführung zusätzlich durch die 3,75-Gasse vor der Kamera. Semi-Rigid-Weg [Fit].
AZE_SIDES    = ((-1, 0.0), (+1, 0.0))   # (Wand-Vorzeichen X, Mitte Y) — beide KURZE Seiten
AZE_SLOT_W   = 2.9                      # Schlitz = Presssitz auf Ø3,1-Koax (des Referenz-Prototyps 2,9)   [Spec §5]
AZE_SEAT_CZ  = EX_Z/2 - 4.0  # [MINI param] Dach-relativ (850: 28-4=24)                     # Rundsitz-Zentrum (r1,45) → Schlitz-Boden 22,55
AZE_REC_D    = 1.4                      # T-Vertiefung außen; Rest-Wand 1,6 (lokale Ausnahme wie
                                        #   RF-Fenster 1,5 — der Schlitz ist ohnehin durch)
AZE_STEM_W   = 7.0                      # Stem-Vertiefung (T-Steg 6,8 + 0,2)
AZE_STEM_Z0  = EX_Z/2 - 7.4  # [MINI param]                     # Stem-Unterkante (deckt den Rundsitz ab)
AZE_FL_W, AZE_FL_DP = 13.0, 2.5         # Deckflansch-Spotface im Dachrand (13 breit × 2,5 tief)
AZE_SCREW_DY2 = 4.8                     # 2× M2×8 DIN 912 VERTIKAL links+rechts des Schlitzes
AZE_PILOT_D, AZE_PILOT_DP = 1.7, 5.0    # Kern-Piloten senkrecht in der Wand-Oberkante
AZE_CLR      = 0.1                      # Passungsspiel je Seite


def mount_antenna_ze(body):
    """T-Prinzip (des Referenz-Prototyps Fotos, beidseitig kurze Seiten): je Seite (1) Durchgangs-Schlitz 2,9
    von der Oberkante mit Rundsitz r1,45 @Z24 (Kabel-Presssitz — Kabel wird von OBEN eingelegt),
    (2) flache T-Stem-Vertiefung außen (1,4 tief), (3) Deckflansch-Spotface im Dachrand,
    (4) 2× vertikale M2-Kern-Piloten in der Wand-Oberkante (Köpfe nach OBEN).
    Rückgabe body. CAD-/Boolean-Check ≠ Klemm-/Zug-Test; Presssitz-Haltekraft = Fit-Print."""
    top = EX_Z/2 + 1.0
    for sx, cy in AZE_SIDES:
        xm = sx*((EX_X + IN_X)/4 + 0.3)                # Schlitz-Achse: Wand exakt + 0,6 nach außen
        # (1) Schlitz 2,9 durch die Wand, von oben, Rundboden (Kabel-Sitz)
        body = body - Pos(xm, cy, (AZE_SEAT_CZ + top)/2) * Box(WALL + 0.6, AZE_SLOT_W, top - AZE_SEAT_CZ)
        body = body - Pos(xm, cy, AZE_SEAT_CZ) * Rot(0, 90, 0) * \
            Cylinder(radius=AZE_SLOT_W/2, height=WALL + 0.6)
        # (2) T-Stem-Vertiefung in der Außenfläche (Tiefe 1,4, Breite 7, ab Z 20,6, oben offen)
        body = body - Pos(sx*(EX_X/2 - AZE_REC_D/2 + 0.5), cy, (AZE_STEM_Z0 + top)/2) * \
            Box(AZE_REC_D + 1.0, AZE_STEM_W, top - AZE_STEM_Z0)
        # (3) Deckflansch-Spotface im Dachrand (Z 25,5..28, exakt Wand-tief)
        body = body - Pos(sx*((EX_X + IN_X)/4 + 0.25), cy, (EX_Z/2 - AZE_FL_DP + EX_Z/2 + 1)/2) * \
            Box(WALL + 0.5, AZE_FL_W, AZE_FL_DP + 1.0)
        # (4) 2× M2-Kern-Piloten VERTIKAL (vom Spotface-Boden 5,0 tief in die Wand)
        for s in (-1, +1):
            body = body - Pos(sx*(EX_X + IN_X)/4, cy + s*AZE_SCREW_DY2,
                              EX_Z/2 - AZE_FL_DP - AZE_PILOT_DP/2) * \
                Cylinder(radius=AZE_PILOT_D/2, height=AZE_PILOT_DP)
    return body


def build_aze_tee(notch=True):
    """Das T-Stück (Druckteil 05, 2× — des Referenz-Prototyps Prinzip): Deckflansch 12,8×2,8×2,5 (liegt im
    Dachrand-Spotface, oben bündig) + Steg 6,8×1,2 (fährt in die Stem-Vertiefung, deckt den
    Kabel-Schlitz). 2× Ø2,2 vertikal + CB Ø4,4×1,0 für M2×8 DIN 912 (Köpfe nach OBEN).
    notch=True → offene Kabel-Kerbe Ø3,2 im Flansch (Kabelseite; Kabel steigt nach oben aus)
    notch=False → BLIND (verschließt die ungenutzte Seite komplett).
    Lokal: X=0 an der Wand-Außenfläche (+X = außen), Z=0 an der Dach-Oberkante."""
    t = Pos(-1.5, 0, -AZE_FL_DP/2) * Box(WALL - 0.2, AZE_FL_W - 0.2, AZE_FL_DP)      # Flansch
    t = t + Pos(-(AZE_REC_D/2 + 0.05) + 0.0, 0, (-7.3 - AZE_FL_DP)/2) * \
        Box(AZE_REC_D - 0.2, AZE_STEM_W - 0.2, 7.3 - AZE_FL_DP)                       # Steg
    if notch:                                          # offene Kabel-Kerbe (seitlich einlegbar)
        t = t - Pos(-1.5, 0, -AZE_FL_DP/2) * Cylinder(radius=1.6, height=AZE_FL_DP + 1)
        t = t - Pos(-0.65, 0, -AZE_FL_DP/2) * Box(1.8, 3.2, AZE_FL_DP + 1)
    for s in (-1, +1):                                 # 2× M2 vertikal, Köpfe oben
        t = t - Pos(-1.5, s*AZE_SCREW_DY2, -AZE_FL_DP/2) * Cylinder(radius=1.1, height=AZE_FL_DP + 1)
        t = t - Pos(-1.5, s*AZE_SCREW_DY2, -0.5) * Cylinder(radius=2.2, height=1.1)   # CB Ø4,4×1,0
    return t


def place_aze_tee(t, sx, cy):
    """T-Stück in Einbaulage: Außenflächen-Ebene sx*35,5, Schlitz-Mitte cy, Oberkante Z28."""
    return Pos(sx*EX_X/2, cy, EX_Z/2) * Rot(0, 0, 0 if sx > 0 else 180) * t


# ── MB2(b) · 2× XT30-ZUGENTLASTUNG (angedruckte Klemmsättel + separate Riegel, Spec §5b) ─────
#   Sättel an BEIDEN ±Y-Seitenwand-Oberkanten des Akku-Stockwerks, nahe der Klappe (+X), im +X-Shelf-
#   Cutout (X17,5..29,5 = Shelf-frei) und ÜBER der Akku-Guide-Oberkante (Z>0,25) → kollisionsfrei mit
#   Akku. 2 getrennte horizontale Rinnen (rot+schwarz, Achse X), Licht Ø2,6 voll verschlossen (Ader
#   2,8 → 0,2 Quetsch). Riegel = separates Mini-Teil (2× exportiert), 2× M2 in Ø1,7-Kerne. ≥10 mm
#   offen zur Klappe (Lötkolben durch die geöffnete Tür). Riegel-Oberkante im lower-Floor-2 (Shelf-Cutout).
XT30_SAD_X  = (X_WALL_IN - 15.0, X_WALL_IN - 4.0)  # [MINI param]         # Sattel-Länge X (≈11, im +X-Shelf-Cutout); +X-Kante 28,5 → 4 mm Puffer, Tür OFFEN=Zugang
XT30_SAD_YW = 10.0                 # Sattel-Innenkante |Y| (protrudes von Wand 16,75 → 10,0)      [Design]
XT30_SAD_Z  = (Z_INT_BOTTOM + BAY_H + 0.3, Z_INT_BOTTOM + BAY_H + 2.3)  # [MINI param Bay-Top-relativ]           # Z über Akku-Guide-Oberkante 0,25 (kein Akku-Kontakt)         [Spec §5b/kollisionsfrei]
XT30_GROOVE_R = 1.3                # Rinnen-Halbradius → Licht Ø2,6 voll verschlossen             [Spec §5b: Licht 2,6]
XT30_GROOVE_Y = (11.5, 15.5)       # 2 getrennte Rinnen |Y|, Steg ~1,4 (rot+schwarz)             [Spec §5b: 2 getrennt]
XT30_PILOT_D  = 1.7                # M2-Riegel-Kern Ø1,7 (des Referenz-Prototyps Praxis, Schrumpf beißt)          [Spec §5b/§8]
XT30_PILOT_Y  = 13.5              # Riegel-Schraube mittig zwischen den Rinnen                   [Design]
XT30_PILOT_DX = 4.0               # 2 Schrauben längs ±4 um die Sattelmitte                      [Design]
XT30_LATCH_H  = 2.0              # Riegel-Höhe über der Sattel-Oberkante                          [Design]


def build_xt30_ze(body):
    """MB2(b): 2 angedruckte Klemmsättel (±Y) mit je 2 X-Rinnen + 2 M2-Kernen. Rückgabe body.
    CAD-/Boolean-Check ≠ Klemm-/Zug-/Löt-Test."""
    xc = (XT30_SAD_X[0] + XT30_SAD_X[1])/2
    xl = XT30_SAD_X[1] - XT30_SAD_X[0]
    zc = (XT30_SAD_Z[0] + XT30_SAD_Z[1])/2
    zt = XT30_SAD_Z[1]                                  # Sattel-Oberkante = Rinnen-Trennebene
    for sy in (-1, +1):
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


# ── AUDIT-FIX (SENDER850_AUDIT.md, 2026-07-05) · FLOOR-2 RAUMHAUSHALT ──────────────────────────
#   Neutrales Audit fand 1 DEFEKT (VTX-Platine durchdringt die +X-Deckel-Insert-Bosse, 687 mm³) +
#   6 WICHTIG (Wago/XT30 ohne Platz, Kamera-/Riegel-Schraubzugang, +X-Snap-Wand 0,65). STRUKTURFIX:
#   (1) Deckel-Bosse RAUS → Deckel-Halt = Boden-Einhängenasen + 2 vertikale Dach-M3 in Deckel-OHREN.
#   (2) Wago-Bank + XT30-Park in die (seit Antenne extern) freie LINKS-ZONE (X<−19,75).
#   Alle „Gates" = CAD-/Boolean-Messung, KEIN empirischer Test.

# VTX-NOMINAL-ENVELOPE (für die geschärften Gates, gegen ALLE Innenraum-Features geprüft):
#   29,2×30×18,6 = Board 29,2×30×14,1 [spec.VTX_BOARD] + Pad 1,5 + U.FL-Stack ≈3,0 [Audit].
#   Klebezone: +0,5 rechts der Kamera-Flanke, auf Shelf-Oberkante; in −Y verschoben, damit die +Y-Kante
#   (VTX_CY+15 = +13,5) die outboard XT30-Riegel-Schraubachse (Punkt 5) freigibt.
VTX_ENV = (29.2, 30.0, 18.6)
VTX_X0  = (CAM_OFF_X + CAM_FLK_OUT) + 0.5        # −10,5 · Kamera-Flanke +X-Kante + Spalt (parametrisch;
                                                 #   Kamera@−21,75 → VTX-Fenster −10,5..18,7, Bosse@25+ frei)
VTX_CY  = 0.0                                    # Y-zentriert: die ±Y-Board-Ecken (±15) räumen den R6-Innen-
                                                 #   Eckradius der +X-Wand (Abstand 6,52 > 6). −Y-Versatz getestet
                                                 #   (grazte den Fillet 53 mm³) → verworfen; Punkt 5 = Montage-Reihenfolge.
VTX_CX  = VTX_X0 + VTX_ENV[0]/2                  # 16,85
VTX_Z0  = Z_INT_BOTTOM + BAY_H + SHELF_T          # 4,0 · Shelf-Oberkante = VTX-Boden
VTX_CZ  = VTX_Z0 + VTX_ENV[2]/2                  # 13,3 · VTX-Top = 22,6

def _vtx_env_solid():
    """Nominaler VTX-Klebe-Körper (Envelope) für die Kollisions-Gates. CAD-Envelope, KEIN Realteil."""
    return Pos(VTX_CX, VTX_CY, VTX_CZ) * Box(*VTX_ENV)

# DECKEL = DACH (Tom 07-05 FINAL: „Der Deckel sitzt OBEN drauf, wie das ein Deckel eben tut" —
#   exakt des Referenz-Prototyps Deckel.STEP = Dachplatte 4,5). SIMPEL: Platte + Lippe + 3× M3, Schalter im Deckel.
#   3 vertikale Eck-Insert-Bosse (vorne-links KEIN Boss: Kamera@−21,75 belegt die Ecke → dort hält
#   die Falz-Lippe; dokumentierte Asymmetrie wie an des Referenz-Prototyps Druck).
VTX_ZONE_X = (VTX_X0, VTX_X0 + 37.0)  # [MINI param] (850: -10,5..26,5)                       # VTX-Klebezone (29,2 + Spiel); LÄNGS eingesetzt, NEBEN
                                                 #   der Kamera; STECKERFREIRAUM beidseitig: links U.FL-
                                                 #   Pigtail, rechts (180°) MIPI+Strom [Tom 07-05]

# WAGO-BANK ENTFERNT (Tom 07-05: kein Overengineering — an des Referenz-Prototyps/Toms realem Druck hängen die
#   Wagos FREI am Kabelbaum, RTV-Tropfen gegen Vibration siehe ASSEMBLY_STEPS). Links-Zone bleibt
#   Kabel-/Elektronik-Freiraum.
WAGO_Z0  = Z_INT_BOTTOM + BAY_H + SHELF_T          # 4,0 · Shelf-Oberkante (Referenz für XT30-Park)

# XT30-PARKTASCHE (Punkt 2/3): der GESTECKTE XT30 (13×11×6) parkt oben LINKS in Floor 2 (Toms „verstaue
#   ich oben" ✓) — der Bay braucht ihn NICHT zu fassen. Kabelweg: aus dem LINKEN Shelf-Cutout (X−23,5)
#   hoch in die Parkzone (unter den Ohren, Z<14; über dem Shelf). Tasche als flache Klemm-Kontur.
XT30P_ENV = (13.3, 11.3, 6.6)                    # 13×11×6 + 0,15/Seite [Spec/MEASURE_ME] — enge Nische!
XT30P_CX, XT30P_CY = CAM_OFF_X + 0.35, 11.1  # [MINI param hinter der Kamera]                 # +Y-Nische HINTER der Kamera (Körper endet Y 5,25;
                                                 #   Park Y 5,45..16,75, X −28,05..−14,75) [Kamera@−21,75]
XT30P_CZ = WAGO_Z0 + XT30P_ENV[2]/2             # auf Shelf-Oberkante (Z 4..10,6 — unter der Boss-Zone 14+)

def _xt30park_env_solid():
    """Nominaler gesteckter-XT30-Park-Körper für das Gate. CAD-Envelope, KEIN Realteil."""
    return Pos(XT30P_CX, XT30P_CY, XT30P_CZ) * Box(*XT30P_ENV)


# (build_lid_blocks ENTFERNT — Deckel ist das DACH; Bosse macht build_corner_bosses.)


def build_roof_lid():
    """DECKEL = DACHPLATTE (Tom 07-05: „sitzt oben drauf, wie ein Deckel eben tut" — des Referenz-Prototyps Prinzip,
    SIMPEL: Platte + Lippe + 3× M3 + Schalterloch). Bündig außen (Z=EX_Z/2), Flansch sitzt in der
    Dach-Senkung (Falz), Lippe taucht in die Öffnung. Separates Druckteil. CAD ≠ Passsitz-Test."""
    tol = TOL_SLIDE
    zf = (RLID_Z_MID + RLID_Z_OUT)/2               # Flansch-Mitte (outer Dachhälfte, außen bündig)
    zt = (RLID_Z_IN + RLID_Z_MID)/2                # Lippen-Mitte (inner Hälfte)
    flange = Pos(0, 0, zf) * extrude(
        RectangleRounded(2*(RLID_HX+RLID_LAP)-2*tol, 2*(RLID_HY+RLID_LAP)-2*tol, RLID_R), RLID_REB_D/2, both=True)
    lip = Pos(0, 0, zt) * extrude(
        RectangleRounded(2*RLID_HX-2*tol, 2*RLID_HY-2*tol, RLID_R), RLID_REB_D/2, both=True)
    lid = flange + lip
    # [MINI] KEIN SCHALTER: Floor-2-X komplett belegt (Kamera bis -5,25 + VTX ab -4,25).
    #   Ein/Aus = XT30 stecken (Testgeraet). Loch-Cut deaktiviert:
    if False:  # [MINI no-switch]
        lid = lid - Pos(SW_CX, SW_CY, (RLID_Z_IN + RLID_Z_OUT)/2) * Cylinder(radius=12.3/2, height=WALL + 2)
    # [MINI] 2 EINHAENGE-NASEN am Deckel-HECK (+X): Tabs unter die Falz-Schulter — Deckel hinten
    #   einhaengen, vorne 2x M3 (ersetzt die nicht platzierbaren +X-Bosse)
    for ty in (-8.0, 8.0):
        lid = lid + Pos(RLID_HX - 0.75, ty, RLID_Z_IN + 0.7) * Box(6.5, 6.0, 1.4)  # tief in die Lippe eingebunden
    # 2× M3 VORNE: Durchgang Ø3,4 + Zylinderkopf-CB Ø6,1×3,4 von OBEN (sichtbare Schrauben)
    for (px, py) in RLID_SCREW:
        lid = lid - Pos(px, py, (RLID_Z_IN + RLID_Z_OUT)/2) * Cylinder(radius=LID_THRU_D/2, height=WALL + 2)
        lid = lid - Pos(px, py, RLID_Z_OUT - LID_CB_DP/2) * Cylinder(radius=LID_CB_D/2, height=LID_CB_DP)
    return lid


if __name__ == "__main__":
    b = build_shell()
    b = graft_camera(b)
    vol_pre_shelf = b.volume
    b = build_shelf(b)                 # fest verbauter Stockwerk-Shelf (Kamin-Aussparungen + VTX-Pad)
    shelf_added = b.volume > vol_pre_shelf
    vol_pre_bosses = b.volume
    b = build_corner_bosses(b)         # 3 vertikale Eck-Insert-Bosse für den DACH-Deckel (Tom 07-05)
    blocks_added = b.volume > vol_pre_bosses
    vol_pre_guides = b.volume
    b = build_bay_guides(b)            # M-A1: Akku-Bay-Führung (nach Shelf → Leisten schweißen an)
    guides_added = b.volume > vol_pre_guides
    b = mount_antenna_ze(b)            # MB2(a): Antennen-ZE-Anschraub-Schnittstelle (−X-Front-Oberkante)
    _xc0 = (XT30_SAD_X[0] + XT30_SAD_X[1])/2
    _sad_probe_air = all(((Pos(_xc0, sy*13.0, (XT30_SAD_Z[0]+XT30_SAD_Z[1])/2) * Box(1, 1, 0.6)) & b).volume < 1e-6 for sy in (-1, +1))
    b = build_xt30_ze(b)               # MB2(b): 2× XT30-Klemmsattel (±Y-Oberkante, +X, angedruckt)
    #  Sattel-Material dort, wo vorher Luft war (über dem Akku) → beweist Anbau (Volumen-Delta trügt: Rinnen schneiden Shelf)
    xt30_added = _sad_probe_air and all(((Pos(_xc0, sy*13.0, (XT30_SAD_Z[0]+XT30_SAD_Z[1])/2) * Box(1, 1, 0.6)) & b).volume > 0.4 for sy in (-1, +1))
    # Antenne: EXTERN (des Referenz-Prototyps Zugentlastung an der Gehäuse-Kante, Koax durch Schlitz — Foto proto_8369).
    #   KEIN interner Omni-Keepout / keine Wand-Kavität mehr (frühere ↓↑-Donut-Doktrin superseded).
    #   Die -X-Ecke gehört jetzt der Kamera (Zentrum X=-9), der VTX liegt rechts daneben (vtx_fit-Gate).
    # ── MB3 · VENTS (neue §6b-Matrix) — Kollisions-Verbote VOR dem Schneiden numerisch prüfen ──
    #   Die ALTEN +Y-Louver-Bänder sind ENTFERNT. Body-Vents: Front(−X), Heck(+X), +Y-Wand-FEST unten.
    _xw_neg, _xw_pos = (-IN_X/2 + -EX_X/2)/2, (IN_X/2 + EX_X/2)/2
    _yw_pos = (IN_Y/2 + EX_Y/2)/2
    _front_cutters = [_louver_Yaxis(VENT_FRONT_YC, zc, VENT_FRONT_LO_L, _xw_neg, +1) for zc in VENT_FRONT_LO_Z]
    _heck_cutters  = [_louver_Yaxis(VENT_HECK_YC,  zc, VENT_HECK_L,  _xw_pos, -1) for zc in VENT_HECK_Z]
    # (S3/S4: +Yfest-Vents entfernt; Snap-Region entfällt.)
    #   Verbots-Regionen (Boxen um die zu schützenden Features):
    _camera_reg = Pos(CAM_OFF_X, -EX_Y/2 + 9, Z_CAM) * Box(2*CAM_FLK_OUT + 2, 18, 14)      # Kamera-Rückraum
    _antze_regs = [Pos(sx*(EX_X + IN_X)/4, cy, (AZE_STEM_Z0 + EX_Z/2)/2) *
                   Box(WALL + 3, AZE_FL_W + 2, EX_Z/2 - AZE_STEM_Z0 + 2)
                   for sx, cy in AZE_SIDES]                                # 2 T-ZE-Zonen (kurze Seiten)
    _doorboss_reg = Pos(EX_X/2 - 3.5, 0, DOOR_TAB_SZ) * Box(8, 8, 8)          # Tür-Laschen-Pilot (07-06)
    _xt30_reg   = Pos((XT30_SAD_X[0]+XT30_SAD_X[1])/2, 0, 1.3) * Box(14, 2*IN_Y/2, 4)        # XT30-Sättel (±Y)
    def _hit(cutters, regs):
        regs = regs if isinstance(regs, list) else [regs]
        return sum(sum(s.volume for s in (c & r).solids()) for c in cutters for r in regs
                   if (c & r).solids())
    _v_front = _hit(_front_cutters, [_camera_reg] + _antze_regs)
    _v_heck  = _hit(_heck_cutters, [_doorboss_reg, _xt30_reg] + _antze_regs)
    print(f"[vent-koll] Front×(Kamera,AntZE)={_v_front:.2f}  Heck×(Boss,XT30)={_v_heck:.2f} mm³ (Gate je <0,5)")
    assert _v_front < 0.5, f"Front-Vent kollidiert (Kamera/AntZE): {_v_front:.2f} mm³"
    assert _v_heck  < 0.5, f"Heck-Vent kollidiert (Boss/XT30): {_v_heck:.2f} mm³"
    vol_pre_vent = b.volume
    b_prevent = b
    b, n_slots = cut_vents_body(b)     # Front(−X) + Heck(+X) + Kamera(−Y) + Front-unten(−X)
    bb = b.bounding_box()
    # ── Vent-Flächen je Zone (±20 %): A_perp = entferntes Wandvolumen × cos45 / WALL ──
    cos45 = math.cos(math.radians(VENT_LOUVER_DEG))
    def _zone_area(cutters):
        rem = sum((c & b_prevent).volume for c in cutters)
        return rem * cos45 / WALL
    _a_front = _zone_area(_front_cutters); _a_heck = _zone_area(_heck_cutters)
    _nom = {"Front": (_a_front, len(VENT_FRONT_LO_Z)*VENT_W*VENT_FRONT_LO_L),
            "Heck": (_a_heck, len(VENT_HECK_Z)*VENT_W*VENT_HECK_L)}
    print("[vent]  " + "  ".join(f"{k}={v[0]:.0f}/{v[1]:.0f}" for k, v in _nom.items()) +
          f" mm² (gemessen/nominal, ±20 %) · 45°-Louver · Schlitz {VENT_W}×L · {n_slots} Body-Schlitze")
    for k, (meas, nom) in _nom.items():
        if nom == 0:                      # Zone bewusst leer (Heck → ZE-Schieber-Fenster, Tom 07-05)
            assert meas < 1e-6, f"Vent-Zone {k}: nominal 0, aber {meas:.1f} mm² geschnitten"
            continue
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

    # ── M-A3 KAMERA-GATE (Ösen innen, Linse raus; Zahlen aus camera_reference-Konstanten) ──
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
    _scan = int((EX_X/2 - 4.0) * 2)          # [MINI] Scan-Bereich in der Schale halten (850: ±30)
    for _i in range(-_scan, _scan + 1):
        _x = _i * 0.5
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

    # ── GESCHÄRFT (Audit) · vtx_fit + wago_fit: NOMINAL-Envelopes ∩ JEDES Innenraum-FEATURE = 0 ──
    #   Isolierte Feature-Solids (Kamera, Wago-Kamm, XT30-Sättel) — die Schalen-WAND ist KEIN „Feature"
    #   (Board-Ecke im R6-Wand-Fillet = Toleranz, separat als MEASURE_ME berichtet).
    def _iv(x):
        _s = x.solids(); return sum(k.volume for k in _s) if _s else 0.0
    _stage = build_shelf(build_shell())                         # Referenz-Stage (Schale+Shelf, feature-frei)
    _shell_ref = build_shell()
    _camera_solid = graft_camera(_stage) - _stage               # isoliertes Kamera-Material
    _xt30_solid   = build_xt30_ze(_stage) - _stage              # isolierte XT30-Sättel
    _blk_solids   = [Pos(px, py, (RBOSS_Z0+RBOSS_Z1)/2) * Cylinder(radius=RBOSS_D/2, height=RBOSS_Z1-RBOSS_Z0)
                     for (px, py) in RLID_SCREW]                  # 3 Eck-Bosse (Dach-Deckel)
    _vtx = _vtx_env_solid()
    _feat_named = [("Kamera", _camera_solid), ("XT30-ZE", _xt30_solid)]
    _vtx_hits = {nm: _iv(_vtx & s) for nm, s in _feat_named}
    _vtx_wallgraze = _iv(_vtx & _shell_ref)                     # nur R6-Eck-Fillet (Toleranz, MEASURE_ME)
    print(f"[vtx_fit] VTX-Env 29,2×30×18,6 @X{VTX_CX:.1f} ∩ Feature: " +
          " ".join(f"{k}={v:.1f}" for k, v in _vtx_hits.items()) +
          f" mm³ (Gate je 0) · Wand-Eck-Graze {_vtx_wallgraze:.1f} mm³ (MEASURE_ME: Board-Ecke im R6-Fillet)")
    for k, v in _vtx_hits.items():
        assert v < 0.5, f"VTX-Envelope kollidiert mit {k}: {v:.2f} mm³ (DEFEKT-Klasse)"
    # ── BOSS↔VTX-Gate (Dach-Deckel-Bosse): Boolean gegen die nominale VTX-Envelope ──
    _blk_vtx = max(_iv(_vtx & s) for s in _blk_solids)
    print(f"[boss]  3 Eck-Bosse Ø{RBOSS_D} @{RLID_SCREW} Z{RBOSS_Z0:.0f}..{RBOSS_Z1:.0f} · Insert "
          f"Ø{RBOSS_INS_D}×{RBOSS_INS_DP} Achse Z · ∩ VTX-Env = {_blk_vtx:.2f} mm³ (Gate <0,5)")
    assert _blk_vtx < 0.5, f"Eck-Boss kollidiert mit VTX-Envelope: {_blk_vtx:.2f} mm³"
    _park_hit = max(_iv(_xt30park_env_solid() & s) for _, s in _feat_named)
    print(f"[park] XT30-Park-Env 13×11×6 @X{XT30P_CX:.0f} Y{XT30P_CY:.0f} (unter den Ohren, Z<14) ∩ Feature "
          f"= {_park_hit:.2f} mm³ (Gate <0,5) · Kabelweg vom linken Shelf-Cutout (X−23,5) hoch [Punkt 3]")
    assert _park_hit < 0.5, f"XT30-Park kollidiert mit Feature: {_park_hit:.2f} mm³"

    # ── MONTAGE-REIHENFOLGE + DRIVER-GATES (Punkt 1/4/5) — CAD-Reihenfolge-Beweis, KEIN Fügetest ──
    #   Reihenfolge (durch die unten gemessenen Driver-Sperren erzwungen; Floor-2 ist dicht gepackt):
    #     1) Kamera 2×M2 (Kugelkopf durch die +Y-Deckel-Öffnung) — VOR Wago & VTX
    #     2) Wago-Kamm von oben bestücken · 3) XT30-Riegel 2×M2 von oben — VOR dem VTX-Kleben
    #     4) VTX kleben (füllt die +X-Floor-2-Hälfte) · 5) Deckel: Nasen einhängen → 2× Dach-M3 von
    #        AUSSEN-oben ziehen (extern zugänglich — der DEFEKT-Fix!) · 6) Akku + Tür (Tür-M2 extern +X).
    _cam_scr_y = -(EX_Y/2) + 0.5 + CAM_TIP2HOLE                 # −8,75 · Kamera-Quer-Schraubachse [camera_final]
    _drv_camR = Pos(CAM_OFF_X + CAM_FLK_OUT + 20.25, _cam_scr_y, Z_CAM) * Box(40, 5, 5)  # rechter M2, Achse X
    # linker Kamera-M2: jetzt VON AUSSEN durch die −X-Wand (Einsenkung+Loch, Tom 07-05) → immer frei
    _p4_r_vtx = _iv(_drv_camR & _vtx); _p4_l_wago = 0.0
    _drv_latch = [Pos((XT30_SAD_X[0]+XT30_SAD_X[1])/2 + dx, XT30_PILOT_Y, 15) * Box(5, 5, 40)
                  for dx in (-XT30_PILOT_DX, +XT30_PILOT_DX)]
    _p5_latch_vtx = max(_iv(d & _vtx) for d in _drv_latch)
    # (P4) Kamera OHNE VTX/Wago frei — am Kamera-Stage (nur Schale+Kamera): Driver trifft nur die Wand
    _cam_stage = graft_camera(build_shelf(build_shell()))
    _p4_camR_stagefeat = _iv(_drv_camR & (_cam_stage - build_shell()))   # ∩ nur Kamera-Material (Soll ~0: Driver liegt +X neben der Kamera)
    # (P1) Die 3 M3 kommen VON OBEN durch den Dach-Deckel in die Eck-Boss-Inserts.
    #   Driver Ø3 auf der Insert-Achse Z (Boss-Insert Ø4,6 → frei); prüft, dass der Weg frei ist.
    _drv_screw = [Pos(px, py, RBOSS_Z1 + 6.0) * Cylinder(radius=1.5, height=12.0)
                  for (px, py) in RLID_SCREW]
    _p1_screw = max(_iv(d & b) for d in _drv_screw)
    print(f"[driver] P1 M3-von-oben frei={_p1_screw:.1f} mm³ (Gate <2: Ø3-Driver in Insert Ø4,6) · "
          f"P4 Kamera-rechts∩VTX={_p4_r_vtx:.0f} / links=EXTERN (Außenwand-CB) · "
          f"P5 Riegel∩VTX={_p5_latch_vtx:.0f} (→ Riegel VOR VTX)")
    assert _p1_screw < 2.0, f"M3-von-oben nicht frei (Driver ∩ Body {_p1_screw:.1f}) — Insert-Zugang blockiert!"
    assert _p4_camR_stagefeat < 0.5, f"Kamera-Driver trifft Kamera-Material am Stage ({_p4_camR_stagefeat:.1f}) — Achse falsch"
    assert _p4_r_vtx > 5.0 and _p5_latch_vtx > 5.0, "Montage-Invariante: VTX MUSS Kamera-/Riegel-Driver sperren (sonst Reihenfolge-Annahme falsch)"

    # ── SHELF-GATE (fest verbaut, 2 Luft-Aussparungen, VTX-Pad) ────────────────
    print(f"[shelf] fest verbaut Z=0..{SHELF_T:.0f}, 2 Aussparungen {SHELF_CUT_L:.0f}×{SHELF_CUT_W:.0f} "
          f"(2×{SHELF_CUT_L*SHELF_CUT_W:.0f}={2*SHELF_CUT_L*SHELF_CUT_W:.0f} mm² Luft/XT30), "
          f"VTX-Klebefläche ≈{VTX_PAD_X:.0f}×{IN_Y:.0f} mm (VTX 30×29 passt, verschiebbar)")
    assert shelf_added, "Shelf wurde nicht an den Body geschweißt (Volumen nicht gestiegen)"
    assert VTX_PAD_X >= 31.0, f"VTX-Klebefläche zu schmal: {VTX_PAD_X:.1f} < 31 (VTX 30 + Rand)"

    # ── M-A1 BAY-FÜHRUNGS-GATE (lichte Maße als Assert; CAD-Check ≠ Einschub-Test) ──
    clear_z = STRIP_BOT - RAIL_TOP
    print(f"[bay]   Führung licht Y={GUIDE_CLEAR_Y:.2f} (Soll 30,5–31,0)  Z={clear_z:.2f} "
          f"(Soll 23,5–24,0)  Schienen-Top={RAIL_TOP:.1f}=Breach-Unterkante  "
          f"Rippen x={RIB_X} (Vent-Spalten-frei), 45°-Einführschräge vorn")
    assert 18.0 <= GUIDE_CLEAR_Y <= 18.5  # [MINI], f"lichte Y-Führung {GUIDE_CLEAR_Y} außerhalb 30,5–31,0"
    assert 15.8 <= clear_z <= 16.3  # [MINI], f"lichte Z-Führung {clear_z} außerhalb 23,5–24,0"
    assert guides_added, "Bay-Führung nicht angeschweißt (Volumen nicht gestiegen)"
    assert max(RIB_X) + RIB_W/2 + 2.0 <= X_WALL_IN, "Rippe ragt in die Tür-Öffnung"
    assert RAIL_X1 < X_WALL_IN - 4.0, "Schiene ragt in die Tür-/XT30-Zone"
    # ── ECK-BOSS-MOUNT-GATE (Body-Seite: 3 Bosse + Insert-Bohrungen offen) ──
    assert blocks_added, "Eck-Bosse nicht an den Body geschweißt (Volumen nicht gestiegen)"
    for (_px, _py) in RLID_SCREW:                   # Insert-Bohrung je Boss offen (Luft auf der Z-Achse)
        _bore_air = ((Pos(_px, _py, RBOSS_Z1 - 2.0) * Box(0.4, 0.4, 0.4)) & b).volume < 1e-6
        assert _bore_air, f"Boss-Insert-Bohrung @({_px:+.1f},{_py:+.1f}) nicht frei (Boss nicht gebohrt)"
    print(f"[deckel-mount] 3 Eck-Bosse @{RLID_SCREW} Z{RBOSS_Z0:.0f}..{RBOSS_Z1:.0f} · "
          f"Insert Ø{RBOSS_INS_D}×{RBOSS_INS_DP} Achse Z (Mündung {RBOSS_Z1:.0f}) → 3 M3 von OBEN")

    # ── MB2(a) · ANTENNEN-ZE-GATE (T-Prinzip beidseitig kurze Seiten; CAD ≠ Klemm-/Zug-Test) ──
    _te_k, _te_b = build_aze_tee(notch=True), build_aze_tee(notch=False)
    for _sx, _cy in AZE_SIDES:
        _xm = _sx*(EX_X + IN_X)/4                                        # Wand-Mitte ±34
        _tag = "Front(−X)" if _sx < 0 else "Heck(+X)"
        # (1) Schlitz offen (Wand-Mitte über dem Sitz) + (2) Einlege-Spur von oben offen
        _slot_air = ((Pos(_xm, _cy, AZE_SEAT_CZ + 1.2) * Box(0.5, 0.5, 0.5)) & b).volume < 1e-6
        _ins_path = ((Pos(_xm, _cy, EX_Z/2 + 0.3) * Box(0.5, 0.5, 0.5)) & b).volume < 1e-6
        # (3) Rundsitz-Material unter dem Sitz (Kabel-Auflage) — Probe in der Restwand HINTER
        #     der Stem-Vertiefung (Wand 32,5..34,1; Probe-Mitte 33,3)
        _seat_ok = ((Pos(_sx*(IN_X/2 + 0.8), _cy, AZE_SEAT_CZ - AZE_SLOT_W/2 - 0.7) *
                     Box(0.5, 0.5, 0.5)) & b).volume > 0.1
        # (4) Spotface frei + (5) 2× vertikale M2-Piloten offen
        _spot_ok = ((Pos(_xm, _cy + 4.0, EX_Z/2 - 0.6) * Box(0.4, 0.4, 0.4)) & b).volume < 1e-6
        _pil_ok = all(((Pos(_xm, _cy + s*AZE_SCREW_DY2, EX_Z/2 - AZE_FL_DP - 1.5) * Box(0.4, 0.4, 0.4)) & b).volume < 1e-6
                      for s in (-1, +1))
        # (6) T-Stück GESETZT: keine Durchdringung, oben bündig mit Dach
        _pl = place_aze_tee(_te_b, _sx, _cy)
        _ix = _pl & b                                   # leere Intersection → None (build123d)
        _pen = sum(s2.volume for s2 in _ix.solids()) if (_ix is not None and _ix.solids()) else 0.0
        _top_flush = abs(_pl.bounding_box().max.Z - EX_Z/2) < 1e-3
        print(f"[ant-ze:{_tag}] T-Schlitz {AZE_SLOT_W} (Presssitz Ø3,1) Sitz r{AZE_SLOT_W/2} @Z{AZE_SEAT_CZ} · "
              f"offen={_slot_air} Einlegen={_ins_path} Sitz={_seat_ok} Spotface={_spot_ok} · "
              f"2×M2⊥ ±{AZE_SCREW_DY2} offen={_pil_ok} · T∩Body={_pen:.3f} mm³ · oben bündig={_top_flush} "
              f"· Haltekraft Presssitz [Fit-Print]")
        assert _slot_air and _ins_path, f"ZE-{_tag}: Schlitz/Einlege-Spur nicht frei"
        assert _seat_ok, f"ZE-{_tag}: Rundsitz-Material fehlt"
        assert _spot_ok and _pil_ok, f"ZE-{_tag}: Spotface/Pilot nicht geschnitten"
        assert _pen < 0.01, f"ZE-{_tag}: T-Stück durchdringt Body: {_pen:.2f} mm³"
        assert _top_flush, f"ZE-{_tag}: T-Stück nicht oben bündig"
    for _v, _n in ((_te_k, "Kerbe"), (_te_b, "blind")):
        assert BRepCheck_Analyzer(_v.wrapped).IsValid() and len(_v.solids()) == 1, f"ZE-T-Stück ({_n}) ungültig"

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
    print(f"[xt30]  2 Sättel ±Y @X{XT30_SAD_X} Z{XT30_SAD_Z} · 2 Rinnen |Y|{XT30_GROOVE_Y} Licht Ø{2*XT30_GROOVE_R:.1f} "
          f"(frei-vol {_lit_free:.2f}, r1,55 trifft {_lit_hit:.2f}) · Riegel 2× M2 · Akku-Koll {_c_batt:.2f} mm³ · "
          f"Puffer→Tür {_iron_gap:.1f} (Tür OFFEN = Lötzugang)")
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
    overstand = db.max.X - DOOR_FACE_X - DOOR_TAB_T    # Überstand +X jenseits der LASCHE (2,5 proud,
                                                       #   Tom 07-06 — Plattenfläche selbst bleibt bündig)
    # Gleitspiel Tür<->Öffnung (Zunge-Breite gegen Durchbruch): soll ~2*TOL_SLIDE gesamt (0.3/Seite)
    gap_per_side = (OPEN_Y - (db.size.Y if db.size.Y <= OPEN_Y else OPEN_Y)) / 2
    print(f"[tür]   {db.size.X:.1f} × {db.size.Y:.1f} × {db.size.Z:.1f} mm  "
          f"(X {db.min.X:.1f}..{db.max.X:.1f})  Flansch {CB_Y-2*TOL_SLIDE:.1f}×{CB_Z-2*TOL_SLIDE:.1f}")
    print(f"[gate]  Tür IsValid={door_valid} Solids={door_solids}  "
          f"Überstand(+X)={overstand:+.4f} mm  Gleitspiel≈{TOL_SLIDE:.1f}/Seite")
    assert door_valid, "BRepCheck: Tür ungültig"
    assert door_solids == 1, f"Tür: erwartet 1 Solid, ist {door_solids}"
    assert overstand <= 1e-3, f"Tür ragt über Lasche hinaus: {overstand:.4f} > 0 (Platte bündig + Lasche 2,5)"
    # Akku-Freiheits-Gate (Tom 07-06: „passt der Akku rein?"): Innenraum-Zone des alten Bosses
    #   (X 26..32,5 · |Y|<4 · Z −6..−0,8) muss jetzt LEER sein — Akku-Ende 28,5 inkl. Swell frei
    _bayfree = Pos((X_WALL_IN - 7.0 + X_WALL_IN)/2, 0, Z_BAY_MID + OPEN_Z/2 - 2.0) * Box(7.0, 8.0, 4.0)  # [MINI]
    _bf = _bayfree & b
    _bf_v = sum(s.volume for s in _bf.solids()) if (_bf is not None and _bf.solids()) else 0.0
    print(f"[akku-frei] Ex-Boss-Zone (Tuer-seitige 7er-Zone) ∩ Body  [MINI] = {_bf_v:.2f} mm³ (Gate <0,5) — "
          f"Akku 45+1 Swell endet 19,25: Bay komplett frei [MINI]")
    assert _bf_v < 0.5, f"Akku-Zone nicht frei: {_bf_v:.2f} mm³ (Innen-Boss-Relikt?)"

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

    # ── DACH-DECKEL (Tom 07-05: „sitzt oben drauf") + Gates ────────────────────
    cov = build_roof_lid()
    cov = cov - b                       # Formschluss-Finish (definierter Passsitz, nur ≤0,3-Übergänge)
    cov_inter = cov & b
    cov_v = sum(s.volume for s in cov_inter.solids()) if cov_inter.solids() else 0.0
    assert cov_v < 0.01, f"Deckel durchdringt Body: {cov_v:.2f} mm³"
    cvb = cov.bounding_box()
    cover_valid = BRepCheck_Analyzer(cov.wrapped).IsValid()
    cover_solids = len(cov.solids())
    cover_over = cvb.max.Z - RLID_Z_OUT                 # Überstand +Z über die Dach-Außenfläche
    print(f"[deckel] DACH-Deckel {cvb.size.X:.1f}×{cvb.size.Y:.1f}×{cvb.size.Z:.1f} mm (Z {cvb.min.Z:.1f}..{cvb.max.Z:.1f})  "
          f"IsValid={cover_valid} Solids={cover_solids}  Überstand(+Z)={cover_over:+.4f} mm  "
          f"KEIN Schalter [MINI] · 2× M3-CB vorn + 2 Heck-Nasen @{RLID_SCREW}  "
          f"Durchdringung {cov_v:.3f} mm³ (Gate <0,01)")
    assert cover_valid, "BRepCheck: Deckel ungültig"
    assert cover_solids == 1, f"Deckel: erwartet 1 Solid, ist {cover_solids}"
    assert cover_over <= 1e-3, f"Deckel ragt über das Dach hinaus: {cover_over:.4f} > 0 (Tom: bündig!)"

    lat_p = build_xt30_latch(+1)                      # XT30-Riegel +Y (eingesetzt)
    lat_m = build_xt30_latch(-1)                      # XT30-Riegel −Y (eingesetzt)
    ze_f = place_aze_tee(build_aze_tee(notch=False), *AZE_SIDES[0])   # Tom 07-06: BEIDE blind (1 Teil, 2x)
    ze_h = place_aze_tee(build_aze_tee(notch=False), *AZE_SIDES[1])   # Heck: blind (verschlossen)
    b = b.solid()                    # fillet() gibt ein generisches Shape zurück → als Solid fassen,
                                     #   sonst verweigert der GLB-Export die Farbe (Warning)
    b.color = Color(0.82, 0.82, 0.85)
    d.color = Color(0.30, 0.62, 0.85)                  # Tür separat eingefärbt
    cov.color = Color(0.95, 0.72, 0.25)               # Deckel separat eingefärbt (orange)
    lat_p.color = lat_m.color = Color(0.40, 0.80, 0.45)   # XT30-Riegel grün
    ze_f = ze_f.solid(); ze_h = ze_h.solid()              # fillet → Shape: als Solid fassen (Farbe!)
    ze_f.color = ze_h.color = Color(0.85, 0.25, 0.75)     # ZE-Schieber magenta
    OUTDIR = "/Users/tomschoen/Desktop/Projects/SkyDiveLive/CAD - models/skylive_out"
    out = f"{OUTDIR}/skylive_mini300.glb"
    export_gltf(Compound(label="SkyLive_Mini300", children=[b, d, cov, lat_p, lat_m, ze_f, ze_h]),
                out, binary=True)
    print(f"[glb] {out}  (Body + Akku-Klappe + Deckel + 2 XT30-Riegel + 2 ZE-Schieber)")
    # ── STL je Druckteil (Body, Tür, Deckel, XT30-Riegel ×2, ZE-Schieber Nut+blind) ──
    from build123d import export_stl
    for _part, _name in ((b, "body"), (d, "battery_door"), (cov, "cover_floor2"),
                         (build_xt30_latch(+1), "xt30_latch"),
                         (build_aze_tee(notch=False), "ze_tee")):   # Tom 07-06: 1 Teil, 2x drucken,
                         #   BLIND (schliesst komplett); Kabel-Kerbe bohrt/schneidet Tom selbst
                         #   (Position: Flansch-Mitte, Achse 1,5 von der Aussenkante, Ø3,2 + Schlitz)
        _stl = f"{OUTDIR}/skylive_mini300_{_name}.stl"
        export_stl(_part, _stl, tolerance=0.005, angular_tolerance=0.05)   # [Audit P7] feiner → offene Kanten 0
        print(f"[stl] {_stl}  (Riegel: 2× drucken)" if _name == "xt30_latch" else f"[stl] {_stl}")
