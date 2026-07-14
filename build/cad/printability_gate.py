#!/usr/bin/env python3
"""
printability_gate.py — Mesh-basiertes Druckbarkeits-Gate für SkyLive-Teile.

Fängt genau die Fehlerklasse, die der Kollege am 2026-07-13 per Auge fand und die der
CAD-interne Boolean-Gate (watertight/wall_min auf dem Solid) NICHT sieht, weil sie erst
im ausgelaufenen Fillet / im Mirror-Sliver / in der nach-unten-Absenkung entsteht:

  1. KNIFE-EDGE  — lokale Wandstärke -> 0 (auslaufende Radien). Ray-Cast-Sampling.
  2. OVERHANG    — Flächen > MAX_DEG nach unten (Support-Fallen), Cluster-Report.
  3. VOID        — vollständig eingeschlossener Hohlraum (shells > 1).
  4. SLIVER      — entartete Nadeldreiecke (Mirror/Boolean-Artefakte).

Nutzung:
    python printability_gate.py pfad/zu/body.stl [--min-wall 0.8] [--overhang-deg 45]
    # oder ganzen Ordner:
    python printability_gate.py "/Users/tomschoen/Desktop/SkyLiveDruck/850er/Druck"

Als Gate in den CAD-Skripten (skylive_sender.py / deploy_gespiegelt.py) direkt vor
export_stl() aufrufen:  from printability_gate import gate; gate(stl_path)  # raises on FAIL

Benötigt: trimesh, numpy, rtree   (pip install trimesh numpy rtree)
"""
from __future__ import annotations
import sys, glob, os
import numpy as np

try:
    import trimesh
except ImportError:
    sys.exit("pip install trimesh numpy rtree")

# ── Schwellen (an spec.py-Doktrin angelehnt) ────────────────────────────────
MIN_WALL     = 0.8    # mm  p1-Wandstärke muss darüber liegen (1 Perimeter = 0.5; Ziel eher >=WALL)
OVERHANG_DEG = 45.0   # °   PRINT_OVERHANG_MAX_DEG
OVERHANG_MAX_AREA = 400.0  # mm² pro 5-mm-Cluster, ab dann WARN (Support-Falle)
SLIVER_EDGE  = 0.05   # mm  kürzeste Dreieckskante darunter = entartet
N_SAMPLES    = 2500   # Wandstärke-Stichproben


def _thickness_percentiles(m, n=N_SAMPLES, seed=0):
    """FLÄCHENGEWICHTETES Wandstärke-Sampling.

    WICHTIG (Lehre aus dem 2026-07-13 Review): naives flächen-UNIFORMES Sampling
    (jede Dreiecksfläche gleich wahrscheinlich) überzeichnet dünne Zonen massiv, weil
    fein tessellierte Fillet-Ränder viele winzige Dreiecke haben -> False-Positive-FAIL
    (der Deckel schlug fälschlich an: uniform p1=0,22mm, flächengewichtet p1=1,02mm = ok).
    Deshalb: Sampling-Wahrscheinlichkeit ∝ Dreiecksfläche -> repräsentiert die reale
    Oberfläche statt die Mesh-Dichte."""
    # Zufallspunkte AUF den Dreiecken (barycentrisch), nicht Dreiecks-Zentren: bei grob
    # tessellierten Flächen kollabieren Zentren auf wenige Punkte -> die Cluster-Form-
    # Klassifikation unten sähe Kanten statt Flächen (im Membran-Selbsttest aufgefallen).
    pts, fidx = trimesh.sample.sample_surface(m, n, seed=seed)   # flächengewichtet
    nrm = m.face_normals[fidx]
    origins = pts - nrm * 0.05
    dirs = -nrm
    loc, ray_idx, _ = m.ray.intersects_location(origins, dirs, multiple_hits=False)
    if len(loc) == 0:
        return None, None
    d = np.linalg.norm(loc - origins[ray_idx], axis=1)
    keep = d > 0.02
    return d[keep], origins[ray_idx][keep]


def _cluster_points(pts, r=1.5):
    """Greedy-Verkettung: Punkte mit Abstand < r landen im selben Cluster (O(n²), n klein)."""
    used = np.zeros(len(pts), bool)
    clusters = []
    for i in range(len(pts)):
        if used[i]:
            continue
        stack, mem = [i], [i]
        used[i] = True
        while stack:
            j = stack.pop()
            nb = np.where((np.linalg.norm(pts - pts[j], axis=1) < r) & ~used)[0]
            used[nb] = True
            stack.extend(nb.tolist())
            mem.extend(nb.tolist())
        clusters.append(np.array(mem))
    return clusters


def _classify_thin_clusters(pts, d, wall_width_min=2.0, min_pts=6):
    """Junction-Kante vs. echte Dünnwand — per Form des Thin-Clusters.

    Lehre aus der visuellen Verifikation 2026-07-14 (Schnitt-Renders an den 6 dünnsten
    Body-Spots): ALLE Sub-min_wall-Stellen waren Tangenten-Cusps an Feature-Übergängen
    (Shelf-Oberkante↔Fillet, Vent-Lamellen-Spitze↔Wand, Falz↔Eckenradius) — Kanten, an
    denen ein Materialkeil geometrisch auf 0 ausläuft. Der Slicer verschmilzt die mit dem
    Nachbar-Solid (Teil wurde real erfolgreich gedruckt); sie sind kosmetisch, kein FAIL.

    Geometrische Signatur, ZWEI Kriterien (beide nötig für FAIL):
      1. FLÄCHE statt KURVE/STEG — Junction-Kanten liegen 1D aufgereiht, Membranen haben
         2D-Ausdehnung. PCA: zweitgrößte Ausdehnung >= wall_width_min (2,0: darunter liegen
         auch die 45°-Vent-Lamellen-Stege ~0,7×1,6, die FDM als 1-2-Perimeter-Band druckt —
         am schwarzen 850er-Druck real bewiesen; erst BREITERE Plateaus sind echte Membranen.
         Kalibrier-Anker: Lamellen-Steg 1,6 breit ⇒ WARN · ze_tee_flush-Ringboden Ø4,4 ⇒ FAIL).
      2. PLATEAU statt RAMPE — eine Membran hat ~konstante Dicke (IQR klein), ein Keil/
         Fillet-Auslauf rampt von ~0 bis min_wall (IQR groß). Rampen druckt FDM durch
         progressives Verschmelzen (wie jede Fase); Plateaus unter min_wall nicht.
    Winzige Cluster (< min_pts Samples) sind statistisch nicht klassifizierbar → Kante."""
    walls, edges = [], []
    for mem in _cluster_points(pts):
        cp, dm = pts[mem], d[mem]
        info = (cp.mean(0), float(np.median(dm)), len(mem))
        if len(mem) < min_pts:
            edges.append(info)
            continue
        q = cp - cp.mean(0)
        ev = np.linalg.eigvalsh(q.T @ q / len(mem))          # aufsteigend
        second_extent = 2.0 * np.sqrt(max(ev[1], 0.0))       # ~2σ quer zur Hauptrichtung
        iqr = np.percentile(dm, 75) - np.percentile(dm, 25)
        plateau = iqr < 0.35 * max(float(np.median(dm)), 0.2)
        (walls if (second_extent >= wall_width_min and plateau) else edges).append(info)
    return walls, edges


def gate(path, min_wall=MIN_WALL, overhang_deg=OVERHANG_DEG, verbose=True, raise_on_fail=False):
    m = trimesh.load(path)
    name = os.path.basename(path)
    fails, warns = [], []

    # 1 · KNIFE-EDGE / DÜNNWAND (Kurve-vs-Fläche-Klassifikation, s. _classify_thin_clusters)
    d, spts = _thickness_percentiles(m)
    if d is not None:
        p1 = np.percentile(d, 1)
        pct_thin = 100 * (d < 1.5).mean()
        thin_mask = d < min_wall
        if thin_mask.any():
            walls, edges = _classify_thin_clusters(spts[thin_mask], d[thin_mask])
            if walls:
                fails.append(f"DÜNNWAND: {len(walls)} flächige Zone(n) < {min_wall}mm "
                             f"(p1={p1:.2f}mm, {pct_thin:.1f}% der Fläche <1.5mm) — Zentren (x,y,z | median t):")
                for ctr, med, npts in sorted(walls, key=lambda w: w[1])[:6]:
                    fails.append(f"    ({ctr[0]:6.1f},{ctr[1]:6.1f},{ctr[2]:6.1f})  t≈{med:.2f}mm  ({npts} Samples)")
            if edges:
                warns.append(f"KNIFE-EDGE: {len(edges)} Junction-Kante(n) mit auslaufendem Keil "
                             f"(kosmetisch, Slicer verschmilzt; sichtbar/fühlbar als feine Kante) — Zentren:")
                for ctr, med, _ in sorted(edges, key=lambda w: w[1])[:6]:
                    warns.append(f"    ({ctr[0]:6.1f},{ctr[1]:6.1f},{ctr[2]:6.1f})  t≈{med:.2f}mm")
    else:
        warns.append("KNIFE-EDGE: keine Ray-Treffer (offenes Mesh?)")

    # 2 · OVERHANG
    n = m.face_normals; c = m.triangles_center; area = m.area_faces
    thr = -np.cos(np.radians(overhang_deg))
    zbot = m.bounds[0][2]
    down = (n[:, 2] < thr) & (c[:, 2] > zbot + 0.6)
    total = area[down].sum()
    if down.any():
        from collections import defaultdict
        cl = defaultdict(float)
        for p, a in zip(c[down], area[down]):
            cl[(round(p[0]/5)*5, round(p[1]/5)*5, round(p[2]/5)*5)] += a
        big = [(k, a) for k, a in cl.items() if a > OVERHANG_MAX_AREA]
        msg = f"OVERHANG: {total:.0f}mm² Fläche >{overhang_deg:.0f}° nach unten"
        if big:
            warns.append(msg + f"; {len(big)} große Cluster (Support-Falle):")
            for k, a in sorted(big, key=lambda x: -x[1])[:6]:
                warns.append(f"    x={k[0]} y={k[1]} z={k[2]}  {a:.0f}mm²")
        else:
            warns.append(msg + " (verteilt, ok)")

    # 3 · VOID
    shells = len(m.split(only_watertight=False))
    if m.is_watertight and shells > 1:
        fails.append(f"VOID: {shells} getrennte Shells -> eingeschlossener Hohlraum")

    # 4 · SLIVER
    tri = m.triangles
    emin = np.minimum.reduce([
        np.linalg.norm(tri[:, 1]-tri[:, 0], axis=1),
        np.linalg.norm(tri[:, 2]-tri[:, 1], axis=1),
        np.linalg.norm(tri[:, 0]-tri[:, 2], axis=1)])
    slivers = (emin < SLIVER_EDGE).sum()
    if slivers:
        warns.append(f"SLIVER: {slivers} Dreiecke mit Kante <{SLIVER_EDGE}mm (Mirror/Boolean-Artefakt)")

    ok = not fails
    if verbose:
        tag = "✅ PASS" if ok else "❌ FAIL"
        print(f"\n{tag}  {name}  (watertight={m.is_watertight}, shells={shells})")
        for f in fails: print("  ❌ " + f)
        for w in warns: print("  ⚠  " + w)
    if raise_on_fail and not ok:
        raise AssertionError(f"printability_gate FAIL: {name}\n" + "\n".join(fails))
    return ok, fails, warns


def _main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--min-wall", type=float, default=MIN_WALL)
    ap.add_argument("--overhang-deg", type=float, default=OVERHANG_DEG)
    a = ap.parse_args()
    paths = ([a.path] if a.path.lower().endswith((".stl", ".obj", ".ply"))
             else sorted(glob.glob(os.path.join(a.path, "*.stl"))))
    if not paths:
        sys.exit(f"keine Meshes unter {a.path}")
    allok = True
    for p in paths:
        ok, _, _ = gate(p, a.min_wall, a.overhang_deg)
        allok &= ok
    sys.exit(0 if allok else 1)


if __name__ == "__main__":
    _main()
