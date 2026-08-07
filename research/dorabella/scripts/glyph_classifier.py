"""Are the consensus labels predictable from the ink?

No independent ground truth for the Dorabella glyphs exists (the manuscript is
lost; every transcription descends from the same 1937 plate). But internal
consistency IS testable: if the consensus is a faithful reading, glyphs sharing
a label should look alike, and a classifier trained on consensus labels should
cross-validate well. Where it fails, either the glyph is genuinely ambiguous or
the consensus mis-labelled it -- and those positions are named.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
from PIL import Image
from hires import comps, geom
from compare import load_all

SZ=28

def glyphs():
    out=[]
    for r in range(3):
        cs,sub=comps(r)
        for c in cs:
            g=geom(c)
            if g['diam']<25: continue          # the speck
            out.append((c,sub,g))
    return out

def feat(c):
    """Scale/translation-normalised binary bitmap. Rotation is NOT normalised --
    orientation is exactly what we are trying to read."""
    m=c['mask'].astype(float)
    im=Image.fromarray((m*255).astype(np.uint8))
    h,w=m.shape; s=max(h,w)
    canv=Image.new('L',(s,s),0)
    canv.paste(im,((s-w)//2,(s-h)//2))
    v=np.asarray(canv.resize((SZ,SZ), Image.BILINEAR)).astype(float)/255.
    v=v-v.mean()
    n=np.linalg.norm(v)
    return (v/n).ravel() if n>0 else v.ravel()

def run():
    G=glyphs()
    print(f"glyphs extracted: {len(G)}")
    T=load_all(); cons=T['consensus']
    assert len(G)==len(cons)==87
    X=np.stack([feat(c) for c,_,_ in G])
    y=np.array(cons)
    yk=np.array([s[1] for s in cons])     # arc count
    yo=np.array([s[0] for s in cons])     # orientation
    S=X@X.T; np.fill_diagonal(S,-np.inf)  # leave-one-out 1-NN by cosine
    nn=S.argmax(axis=1)
    for name,lab in (('full symbol',y),('arc count',yk),('orientation',yo)):
        acc=(lab[nn]==lab).mean()
        # chance = sum of squared class frequencies
        _,cnt=np.unique(lab,return_counts=True); ch=((cnt/len(lab))**2).sum()
        print(f"  LOO 1-NN accuracy, {name:12s}: {acc:.3f}   (chance {ch:.3f})")
    print("\n  orientation confusion (consensus label -> nearest-neighbour label):")
    letters=sorted(set(yo))
    M=np.zeros((len(letters),len(letters)),int)
    for t,p in zip(yo,yo[nn]): M[letters.index(t),letters.index(p)]+=1
    print("      "+" ".join(f"{l:>3s}" for l in letters))
    for i,l in enumerate(letters):
        print(f"    {l} "+" ".join(f"{M[i,j]:3d}" for j in range(len(letters))))
    print("\n  positions where the consensus label disagrees with the nearest-looking glyph")
    print("  (candidate transcription errors, or genuinely ambiguous glyphs):")
    bad=[i for i in range(87) if y[nn][i]!=y[i]]
    print(f"    {len(bad)}/87 -> {bad}")
    core=[6,13,22,23,25,26,29,31,33,43,45,53,54,57,66,69,77,80,84,85]
    ov=sorted(set(bad)&set(core))
    print(f"    of which in the 20 transcriber-contested positions: {len(ov)} -> {ov}")
    import scipy.stats as st
    tab=[[len(ov), len(core)-len(ov)],[len(bad)-len(ov), 87-len(core)-(len(bad)-len(ov))]]
    print(f"    Fisher exact p = {st.fisher_exact(tab)[1]:.3f} "
          f"(are classifier-flagged positions enriched among contested ones?)")
if __name__=='__main__':
    run()
