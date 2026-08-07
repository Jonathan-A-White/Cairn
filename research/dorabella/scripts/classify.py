"""Orientation/arc-count classifier.

A Dorabella glyph is k in-phase semicircular arcs strung along a 'stacking axis'.
The convex-hull DIAMETER of the ink runs along that axis: its length gives k,
its direction gives the axis (mod 180 deg). The arcs all bulge to one side of
that axis, so the sign of the perpendicular centroid displacement resolves the
remaining 180 deg ambiguity: the opening faces AWAY from the bulge.
"""
import numpy as np, math, sys
sys.path.insert(0,'scripts')
from glyphs import comps_of, COMPASS

def hull_diameter(pts):
    from scipy.spatial import ConvexHull
    if len(pts) < 3: 
        i,j = 0, len(pts)-1
        return i,j,np.linalg.norm(pts[i]-pts[j])
    try:
        h = ConvexHull(pts); P = pts[h.vertices]
    except Exception:
        P = pts
    best=(0,0,-1)
    for i in range(len(P)):
        d = np.linalg.norm(P - P[i], axis=1)
        j = int(d.argmax())
        if d[j] > best[2]: best = (i, j, float(d[j]))
    return P[best[0]], P[best[1]], best[2]

def classify(c):
    m = c['mask']; h,w = m.shape
    ys,xs = np.nonzero(m)
    pts = np.stack([xs.astype(float), (h-1-ys).astype(float)], axis=1)   # math coords
    A,B,diam = hull_diameter(pts)
    axis = B-A; L=np.linalg.norm(axis)
    if L==0: axis=np.array([1.0,0.0]); L=1
    u = axis/L                       # stacking axis unit vector
    p = np.array([-u[1], u[0]])      # perpendicular
    mid = (A+B)/2.0
    cen = pts.mean(axis=0)
    bulge = float((cen-mid) @ p)     # signed: ink bulges this way along p
    openv = -p if bulge>0 else p     # opening faces away from the bulge
    ang = math.degrees(math.atan2(openv[1], openv[0])) % 360
    oidx = int(round(ang/45.0)) % 8
    resid = abs((ang/45.0) - round(ang/45.0))     # 0=dead centre, .5=on boundary
    return dict(diam=diam, ang=ang, oidx=oidx, orient=COMPASS[oidx],
                resid=resid, bulge=abs(bulge), axis_ang=math.degrees(math.atan2(u[1],u[0]))%180)

def arcs_from_diam(d):
    # thresholds calibrated on the trimodal diameter distribution
    if d < 24.5: return 1
    if d < 39.0: return 2
    return 3

if __name__=='__main__':
    rows={}
    alld=[]
    for r in (1,2,3):
        cs,_=comps_of(r); rows[r]=cs
        for j,c in enumerate(cs):
            f=classify(c); f['k']=arcs_from_diam(f['diam'])
            alld.append((r,j,f))
    ds=sorted(f['diam'] for _,_,f in alld)
    print("diameter distribution (sorted):")
    print("  "+" ".join(f"{d:.0f}" for d in ds))
    from collections import Counter
    print("arc-count counts:", Counter(f['k'] for _,_,f in alld))
    print("orientation counts:", Counter(f['orient'] for _,_,f in alld))
    print()
    print(f"{'id':8s} {'diam':>5s} {'k':>1s} {'ang':>6s} {'or':>3s} {'resid':>5s} {'bulge':>5s}")
    for r,j,f in alld:
        flag = ' <-- boundary' if f['resid']>0.35 else ''
        print(f"r{r}.{j:<5d} {f['diam']:5.1f} {f['k']:1d} {f['ang']:6.1f} {f['orient']:>3s} {f['resid']:5.2f} {f['bulge']:5.2f}{flag}")
