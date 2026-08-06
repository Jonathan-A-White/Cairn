from PIL import Image, ImageDraw
import numpy as np, json
from scipy import ndimage
SRC='/root/.claude/uploads/c5be28fe-db65-5dc7-b12c-63a97f5b8ba3/c33c55ff-9715.jpg'
BANDS={1:(1003,1083,2,1060,29),2:(1093,1152,6,1080,31),3:(1192,1249,9,1078,27)}
THR=150; MINSZ=30

def components(r):
    y0,y1,x0,x1,exp=BANDS[r]
    a=np.asarray(Image.open(SRC).convert('L')).astype(float)
    sub=a[y0-6:y1+6, x0:x1]
    b=sub<THR
    lab,n=ndimage.label(b, structure=np.ones((3,3)))
    objs=ndimage.find_objects(lab)
    out=[]
    for i in range(1,n+1):
        sl=objs[i-1]
        size=int((lab[sl]==i).sum())
        if size<MINSZ: continue
        out.append(dict(id=i,size=size,
                        xs=int(sl[1].start),xe=int(sl[1].stop),
                        ys=int(sl[0].start),ye=int(sl[0].stop)))
    out.sort(key=lambda d:d['xs'])
    return out, sub, lab

if __name__=='__main__':
    for r in (1,2,3):
        comps,sub,lab=components(r)
        print(f"--- row{r}: {len(comps)} comps (expect {BANDS[r][4]})")
        for j,c in enumerate(comps):
            print(f"  {j:2d} x[{c['xs']:4d},{c['xe']:4d}] w={c['xe']-c['xs']:3d} y[{c['ys']:3d},{c['ye']:3d}] h={c['ye']-c['ys']:3d} size={c['size']:4d}")
