"""Segment the 87 Dorabella glyphs and compute orientation/arc-count features."""
from PIL import Image, ImageDraw
import numpy as np, json, math
from scipy import ndimage

SRC='/root/.claude/uploads/c5be28fe-db65-5dc7-b12c-63a97f5b8ba3/c33c55ff-9715.jpg'
BANDS={1:(1003,1083,2,1060,29),2:(1093,1152,6,1080,31),3:(1192,1249,9,1078,27)}
THR=150; MINSZ=30
COMPASS=['E','NE','N','NW','W','SW','S','SE']   # index = angle//45, math convention (y up)

def load_row(r):
    y0,y1,x0,x1,exp=BANDS[r]
    a=np.asarray(Image.open(SRC).convert('L')).astype(float)
    sub=a[y0-6:y1+6, x0:x1]
    return sub

def comps_of(r):
    sub=load_row(r)
    b=sub<THR
    lab,n=ndimage.label(b, structure=np.ones((3,3)))
    objs=ndimage.find_objects(lab)
    out=[]
    for i in range(1,n+1):
        sl=objs[i-1]
        m=(lab[sl]==i)
        size=int(m.sum())
        h=sl[0].stop-sl[0].start; w=sl[1].stop-sl[1].start
        if size<MINSZ: continue
        if h<=4 and w>200: continue        # UI bar strip
        out.append(dict(row=r,size=size,x0=int(sl[1].start),x1=int(sl[1].stop),
                        y0=int(sl[0].start),y1=int(sl[0].stop),
                        mask=m, sl=sl))
    out.sort(key=lambda d:d['x0'])
    return out, sub

def features(c):
    m=c['mask']; h,w=m.shape
    ys,xs=np.nonzero(m)
    # math coords: y up
    cy_ink = (h-1-ys).mean(); cx_ink = xs.mean()
    cy_box = (h-1)/2.0;       cx_box = (w-1)/2.0
    vx, vy = cx_box-cx_ink, cy_box-cy_ink     # points toward the OPEN side
    ang = math.degrees(math.atan2(vy,vx)) % 360
    idx = int(round(ang/45.0)) % 8
    # distance from the 45-degree decision boundary (0 = perfectly on a boundary)
    resid = abs(((ang/45.0) - round(ang/45.0)))    # 0..0.5
    mag = math.hypot(vx,vy)
    # extent along the stacking axis (perpendicular to opening dir), using the QUANTISED dir
    th = math.radians(idx*45)
    px, py = -math.sin(th), math.cos(th)          # perpendicular unit vector
    proj = (xs-cx_ink)*px + ((h-1-ys)-cy_ink)*py
    span = proj.max()-proj.min()
    # extent along opening axis
    proj2 = (xs-cx_ink)*math.cos(th) + ((h-1-ys)-cy_ink)*math.sin(th)
    span2 = proj2.max()-proj2.min()
    return dict(ang=ang, orient=COMPASS[idx], oidx=idx, resid=resid, mag=mag,
                span=span, span2=span2, w=w, h=h, size=c['size'])

def all_glyphs():
    G=[]
    for r in (1,2,3):
        cs,_=comps_of(r)
        for j,c in enumerate(cs):
            f=features(c); f['row']=r; f['col']=j; f['x0']=c['x0']; f['x1']=c['x1']
            G.append((c,f))
    return G

def sheet(row, per=10, cell=230, out=None, annotate=False):
    cs,sub=comps_of(row)
    n=len(cs); cols=per; rows=(n+per-1)//per
    img=Image.new('RGB',(cols*cell, rows*cell),(255,255,255))
    d=ImageDraw.Draw(img)
    for j,c in enumerate(cs):
        gy,gx=j//per, j%per
        pad=4
        y0=max(0,c['y0']-pad); y1=min(sub.shape[0],c['y1']+pad)
        x0=max(0,c['x0']-pad); x1=min(sub.shape[1],c['x1']+pad)
        g=Image.fromarray(np.uint8(np.clip(sub[y0:y1,x0:x1],0,255)))
        gw,gh=g.size; s=min((cell-46)/gw,(cell-46)/gh)
        g=g.resize((max(1,int(gw*s)),max(1,int(gh*s))), Image.LANCZOS).convert('RGB')
        ox=gx*cell+(cell-g.size[0])//2; oy=gy*cell+34+(cell-46-g.size[1])//2
        img.paste(g,(ox,oy))
        d.rectangle([gx*cell+2,gy*cell+2,(gx+1)*cell-2,(gy+1)*cell-2],outline=(200,200,200))
        d.text((gx*cell+8, gy*cell+8), f"r{row}.{j}", fill=(200,0,0))
        if annotate:
            f=features(c)
            d.text((gx*cell+90, gy*cell+8), f"{f['orient']}", fill=(0,0,200))
    out=out or f'out/sheet_row{row}.png'
    img.save(out); return out, n

if __name__=='__main__':
    import sys
    for r in (1,2,3):
        o,n=sheet(r)
        print(o,n)
