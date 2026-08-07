"""Cross-edition comparison: 1937 first edition vs 1947 OUP second edition.

Both plates descend from the same lost original photograph, so differences
between them are REPRODUCTION noise (screening, printing, scanning), not
independent observation. This therefore bounds measurement noise added
downstream of the original; it cannot bound the original photograph's own
limitations.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
from PIL import Image
from scipy import ndimage
U='/root/.claude/uploads/c5be28fe-db65-5dc7-b12c-63a97f5b8ba3'
CFG={'1937':dict(f='854ea36e-9799.jpg',bands=[(658,708),(721,777),(805,865)],x=(110,980),thr=150),
     '1947':dict(f='398f6c96-9801.jpg',bands=[(1050,1099),(1118,1153),(1192,1235)],x=(80,950),thr=140)}
EXPECT=[29,31,27]

def comps(tag, bi, minsz=12):
    c=CFG[tag]
    a=np.asarray(Image.open(U+'/'+c['f']).convert('L')).astype(float)
    y0,y1=c['bands'][bi]; x0,x1=c['x']
    sub=a[y0-3:y1+3, x0:x1]
    b=sub<c['thr']
    lab,n=ndimage.label(b, structure=np.ones((3,3)))
    sizes=ndimage.sum(b,lab,range(1,n+1))
    objs=ndimage.find_objects(lab)
    out=[]
    for i in range(1,n+1):
        if sizes[i-1]<minsz: continue
        sl=objs[i-1]
        out.append(dict(x0=int(sl[1].start),x1=int(sl[1].stop),
                        y0=int(sl[0].start),y1=int(sl[0].stop),size=int(sizes[i-1])))
    out.sort(key=lambda d:d['x0'])
    return out, sub

if __name__=='__main__':
    for tag in ('1937','1947'):
        print(f"=== {tag}")
        tot=0
        for bi in range(3):
            cs,_=comps(tag,bi)
            tot+=len(cs)
            w=[c['x1']-c['x0'] for c in cs]
            print(f"  line{bi+1}: {len(cs):3d} components (expect {EXPECT[bi]})  "
                  f"median width {int(np.median(w)) if w else 0}  "
                  f"median size {int(np.median([c['size'] for c in cs])) if cs else 0}")
        print(f"  total {tot} (expect 87)")
