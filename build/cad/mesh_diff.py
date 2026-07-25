"""mesh_diff — Beweis, dass ein CAD-Fix NUR die Zielzone geändert hat.

Nutzung:
  python mesh_diff.py alt.stl neu.stl [--tol 0.6] [--expect x0 x1 y0 y1 z0 z1 [--expect ...]]

ACHTUNG Auflösung: Default-Toleranz 0,6 (muss über dem Sample-Abstand liegen) —
das Werkzeug beweist FEATURE-Änderungen ≥ ~1 mm, keine Sub-0,6-Drifts.

Vergleicht beide Oberflächen per Punktwolken-Abstand (beidseitig):
  * ADD  = Punkte der neuen Fläche, die von der alten > tol entfernt sind (Material dazu)
  * DEL  = Punkte der alten Fläche, die von der neuen > tol entfernt sind (Material weg)
Cluster werden als Bounding-Boxen gemeldet. Mit --expect-Boxen wird HART geprüft,
dass jede Änderung in einer der erwarteten Zonen liegt (sonst Exit 1).

Workflow-Doktrin 2026-07-25 (Fix-Zyklus nach dem XT30/Shelf-Vorfall):
kein „fertig" ohne (1) Diff ≠ leer, (2) Diff NUR in der Zielzone, (3) Render gesichtet.
"""
import argparse
import sys

import numpy as np
import trimesh
from scipy.spatial import cKDTree


def sample(mesh, n=150_000):
    pts, _ = trimesh.sample.sample_surface(mesh, n)
    return pts


def clusters(points, cell=2.0, min_pts=8):
    """Grobe Cluster über Belegungsgitter + Nachbarschafts-Flutung; liefert BBoxen."""
    if len(points) == 0:
        return []
    keys = np.floor(points / cell).astype(np.int64)
    uniq, inv = np.unique(keys, axis=0, return_inverse=True)
    kset = {tuple(k): i for i, k in enumerate(uniq)}
    parent = list(range(len(uniq)))

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    for i, k in enumerate(uniq):
        for d in ((1, 0, 0), (0, 1, 0), (0, 0, 1),
                  (1, 1, 0), (1, 0, 1), (0, 1, 1), (1, 1, 1),
                  (1, -1, 0), (1, 0, -1), (0, 1, -1)):
            j = kset.get((k[0] + d[0], k[1] + d[1], k[2] + d[2]))
            if j is not None:
                ra, rb = find(i), find(j)
                if ra != rb:
                    parent[rb] = ra
    root = np.array([find(i) for i in range(len(uniq))])[inv]
    out = []
    for r in np.unique(root):
        p = points[root == r]
        if len(p) >= min_pts:
            out.append((len(p), p.min(axis=0), p.max(axis=0)))
    return sorted(out, reverse=True, key=lambda t: t[0])


def in_boxes(points, boxes, margin=0.15):
    ok = np.zeros(len(points), dtype=bool)
    for b in boxes:
        x0, x1, y0, y1, z0, z1 = b
        ok |= ((points[:, 0] >= x0 - margin) & (points[:, 0] <= x1 + margin) &
               (points[:, 1] >= y0 - margin) & (points[:, 1] <= y1 + margin) &
               (points[:, 2] >= z0 - margin) & (points[:, 2] <= z1 + margin))
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("old"); ap.add_argument("new")
    ap.add_argument("--tol", type=float, default=0.6)
    ap.add_argument("--expect", type=float, nargs=6, action="append", default=None,
                    metavar=("x0", "x1", "y0", "y1", "z0", "z1"))
    a = ap.parse_args()

    mo, mn = trimesh.load(a.old), trimesh.load(a.new)
    # Dichte Punktwolken beider Flächen; „geändert" = weiter als tol vom nächsten
    # Punkt der Gegenseite. tol muss ÜBER dem Sample-Abstand liegen (~0,3 bei n=400k
    # auf dieser Body-Größe) — Ziel sind Feature-Änderungen ≥1 mm, kein Mikrometer-Drift.
    po, pn = sample(mo, 400_000), sample(mn, 400_000)
    to, tn = cKDTree(po), cKDTree(pn)
    add = pn[to.query(pn, workers=-1)[0] > a.tol]     # neue Fläche, weit weg von alter
    rem = po[tn.query(po, workers=-1)[0] > a.tol]     # alte Fläche, weit weg von neuer

    print(f"[mesh_diff] tol={a.tol}  ADD-Punkte={len(add)}  DEL-Punkte={len(rem)}")
    for tag, pts in (("ADD", add), ("DEL", rem)):
        for n, lo, hi in clusters(pts)[:8]:
            print(f"  [{tag}] {n:6d} Pt  X {lo[0]:7.2f}..{hi[0]:7.2f}  "
                  f"Y {lo[1]:7.2f}..{hi[1]:7.2f}  Z {lo[2]:7.2f}..{hi[2]:7.2f}")

    if len(add) == 0 and len(rem) == 0:
        print("[mesh_diff] WARNUNG: kein Unterschied — No-Op-Fix? (Shelf-Vorfall 07-14!)")

    if a.expect:
        stray = 0
        for tag, pts in (("ADD", add), ("DEL", rem)):
            if len(pts):
                out = pts[~in_boxes(pts, a.expect)]
                for n, lo, hi in clusters(out)[:6]:
                    print(f"  [STRAY-{tag}] {n:6d} Pt  X {lo[0]:7.2f}..{hi[0]:7.2f}  "
                          f"Y {lo[1]:7.2f}..{hi[1]:7.2f}  Z {lo[2]:7.2f}..{hi[2]:7.2f}")
                stray += int((~in_boxes(pts, a.expect)).sum())
        # Toleranz: einzelne Streupunkte durch Tessellations-Rauschen, keine Cluster
        if stray > 40:
            print(f"[mesh_diff] FAIL — {stray} Änderungspunkte AUSSERHALB der Zielzonen!")
            sys.exit(1)
        print(f"[mesh_diff] PASS — Änderungen nur in den Zielzonen (Streurauschen: {stray} Pt)")


if __name__ == "__main__":
    main()
