from PIL import Image, ImageOps, ImageDraw
import numpy as np, sys, os
SRC='/root/.claude/uploads/c5be28fe-db65-5dc7-b12c-63a97f5b8ba3/c33c55ff-9715.jpg'
BANDS={1:(1003,1083,2,1060),2:(1093,1152,6,1080),3:(1192,1249,9,1078)}
def chunks(row, n=6, scale=8, pad=8, overlap=24):
    y0,y1,x0,x1 = BANDS[row]
    im = ImageOps.autocontrast(Image.open(SRC).convert('L'))
    W = x1-x0
    step = W//n
    outs=[]
    for k in range(n):
        cx0 = x0 + k*step - (overlap if k>0 else 0)
        cx1 = x0 + (k+1)*step + (overlap if k<n-1 else 0)
        cx1 = min(cx1, x1)
        crop = im.crop((cx0, y0-pad, cx1, y1+pad))
        w,h = crop.size
        up = crop.resize((w*scale, h*scale), Image.LANCZOS).convert('RGB')
        d = ImageDraw.Draw(up)
        # ruler: tick every 10 native px, label every 20
        for x in range(cx0, cx1):
            if x % 10 == 0:
                X=(x-cx0)*scale
                d.line([(X,0),(X, 14 if x%20 else 26)], fill=(255,0,0), width=2)
                if x % 20 == 0:
                    d.text((X+3, 26), str(x), fill=(255,0,0))
        out=f'out/r{row}_c{k}.png'
        up.save(out); outs.append((out, cx0, cx1, up.size))
    return outs
if __name__=='__main__':
    r=int(sys.argv[1]); n=int(sys.argv[2]) if len(sys.argv)>2 else 6
    for o in chunks(r,n): print(o)
