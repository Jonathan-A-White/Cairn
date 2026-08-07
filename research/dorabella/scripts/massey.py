"""Replication of Massey's (2017) observations, with proper nulls.

(a) adjacent 180-degree-opposed glyph pairs -- claimed 12-13 vs ~5 expected;
(b) runs of consecutive glyphs whose adjacent arc-counts always differ --
    claimed runs of 12, 9, 8 against a control max of 5-6.
Both are computed on the consensus with permutation nulls that hold the
symbol multiset fixed, so only ORDER is randomised.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
from compare import load_all
ORD="ABCDEFGH"
RNG=np.random.default_rng(2718)

def opposed(seq, same_arcs=True):
    n=0
    for a,b in zip(seq,seq[1:]):
        d=abs(ORD.index(a[0])-ORD.index(b[0])); d=min(d,8-d)
        if d==4 and (not same_arcs or a[1]==b[1]): n+=1
    return n

def alt_runs(seq):
    """longest run over which consecutive arc counts always differ"""
    best=cur=1
    for a,b in zip(seq,seq[1:]):
        if a[1]!=b[1]: cur+=1; best=max(best,cur)
        else: cur=1
    return best

def perm_null(seq, fn, reps=20000):
    v=list(seq); out=np.empty(reps)
    for i in range(reps):
        RNG.shuffle(v); out[i]=fn(v)
    return out

if __name__=='__main__':
    T=load_all(); cons=T['consensus']
    print("="*78); print("MASSEY REPLICATION (consensus transcription)"); print("="*78)
    for name,fn in (("180-opposed adjacent pairs, SAME arc count", lambda s: opposed(s,True)),
                    ("180-opposed adjacent pairs, ANY arc count",  lambda s: opposed(s,False)),
                    ("longest arc-count alternation run",          alt_runs)):
        obs=fn(cons); nul=perm_null(cons,fn)
        p=(nul>=obs).mean()
        print(f"\n{name}")
        print(f"  observed = {obs}")
        print(f"  null: mean={nul.mean():.2f} sd={nul.std():.2f} "
              f"95th={np.quantile(nul,.95):.0f} max={nul.max():.0f}")
        print(f"  p(null >= observed) = {p:.4f}"
              + ("   <-- significant" if p<0.05 else ""))
    # where are the opposed pairs? regional test
    pos=[i for i,(a,b) in enumerate(zip(cons,cons[1:]))
         if min(abs(ORD.index(a[0])-ORD.index(b[0])),8-abs(ORD.index(a[0])-ORD.index(b[0])))==4
         and a[1]==b[1]]
    print(f"\npositions of same-arc opposed pairs: {pos}")
    rows=[(0,29),(29,60),(60,87)]
    for r,(s,e) in enumerate(rows,1):
        k=sum(1 for p_ in pos if s<=p_<e)
        print(f"  row{r} ({e-s} glyphs): {k} opposed pairs")
