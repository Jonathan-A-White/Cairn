from PIL import Image, ImageDraw, ImageFont
import numpy as np, sys
sys.path.insert(0,'scripts')
from glyphs import comps_of
from classify import classify, arcs_from_diam

def all_items():
    items=[]
    for r in (1,2,3):
        cs,sub=comps_of(r)
        for j,c in enumerate(cs):
            items.append((r,j,c,sub))
    return items

def make_sheets(per_row=6, nrow=2, cell=380):
    items=all_items()
    per=per_row*nrow
    paths=[]
    for s in range((len(items)+per-1)//per):
        chunk=items[s*per:(s+1)*per]
        img=Image.new('RGB',(per_row*cell, nrow*cell),(255,255,255))
        d=ImageDraw.Draw(img)
        for t,(r,j,c,sub) in enumerate(chunk):
            gy,gx=t//per_row, t%per_row
            pad=5
            y0=max(0,c['y0']-pad); y1=min(sub.shape[0],c['y1']+pad)
            x0=max(0,c['x0']-pad); x1=min(sub.shape[1],c['x1']+pad)
            g=Image.fromarray(np.uint8(np.clip(sub[y0:y1,x0:x1],0,255)))
            gw,gh=g.size; sc=min((cell-70)/gw,(cell-70)/gh)
            g=g.resize((max(1,int(gw*sc)),max(1,int(gh*sc))), Image.LANCZOS).convert('RGB')
            ox=gx*cell+(cell-g.size[0])//2; oy=gy*cell+52+(cell-70-g.size[1])//2
            img.paste(g,(ox,oy))
            d.rectangle([gx*cell+2,gy*cell+2,(gx+1)*cell-2,(gy+1)*cell-2],outline=(180,180,180),width=2)
            gi=s*per+t
            f=classify(c); k=arcs_from_diam(f['diam'])
            d.text((gx*cell+10, gy*cell+10), f"#{gi}  r{r}.{j}   arcs={k}", fill=(200,0,0))
            # draw the stacking-axis crosshair reference: N arrow
            d.line([(gx*cell+cell-40, gy*cell+34),(gx*cell+cell-40, gy*cell+14)], fill=(0,150,0), width=3)
            d.text((gx*cell+cell-36, gy*cell+14), "N", fill=(0,150,0))
        p=f'out/big_{s:02d}.png'; img.save(p); paths.append(p)
    return paths
if __name__=='__main__':
    for p in make_sheets(): print(p)
