"""Segmentation + geometry on the high-resolution plate scan (3090x1280)."""
import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage
from classify import hull_diameter

SRC='/root/.claude/uploads/c5be28fe-db65-5dc7-b12c-63a97f5b8ba3/a91ae255-dorabellahires.jpg'
BANDS=[(58,263),(286,528),(583,822)]      # three cipher rows
EXPECT=[29,31,27]
COMPASS=['E','NE','N','NW','W','SW','S','SE']
THR=128

def load():
    return np.asarray(Image.open(SRC).convert('L')).astype(float)

def comps(row, thr=THR, minsz=None):
    a=load(); y0,y1=BANDS[row]
    sub=a[y0-8:y1+8]
    b=sub<thr
    lab,n=ndimage.label(b, structure=np.ones((3,3)))
    objs=ndimage.find_objects(lab)
    sizes=ndimage.sum(b,lab,range(1,n+1))
    if minsz is None: minsz=max(60, 0.06*np.median([s for s in sizes if s>60] or [200]))
    out=[]
    for i in range(1,n+1):
        if sizes[i-1]<minsz: continue
        sl=objs[i-1]
        out.append(dict(mask=(lab[sl]==i), size=int(sizes[i-1]),
                        x0=int(sl[1].start), x1=int(sl[1].stop),
                        y0=int(sl[0].start), y1=int(sl[0].stop)))
    out.sort(key=lambda d:d['x0'])
    return out, sub

def geom(c):
    m=c['mask']; h,w=m.shape
    ys,xs=np.nonzero(m)
    pts=np.stack([xs.astype(float),(h-1-ys).astype(float)],axis=1)
    A,B,diam=hull_diameter(pts)
    ax=B-A; L=np.linalg.norm(ax) or 1
    u=ax/L; p=np.array([-u[1],u[0]])
    mid=(A+B)/2; cen=pts.mean(axis=0)
    bulge=float((cen-mid)@p)
    openv=-p if bulge>0 else p
    ang=math.degrees(math.atan2(openv[1],openv[0]))%360
    return dict(diam=float(diam), ang=ang, bulge=abs(bulge),
                axis=math.degrees(math.atan2(u[1],u[0]))%180)

if __name__=='__main__':
    tot=0
    alld=[]
    for r in range(3):
        cs,sub=comps(r)
        print(f"row{r+1}: {len(cs)} components (expect {EXPECT[r]})")
        tot+=len(cs)
        for c in cs: alld.append(geom(c))
    print(f"total {tot} (expect 87)")
    ds=sorted(d['diam'] for d in alld)
    print("diameters:", " ".join(f"{d:.0f}" for d in ds))
