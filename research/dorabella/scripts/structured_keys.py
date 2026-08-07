"""Exhaustive sweep over STRUCTURED keys of Elgar's own construction.

The 1920 notebook alphabet is not an arbitrary permutation: 24 letters
(no J, no V) laid out in 8 groups of 3, one group per orientation, arc count
giving position within the group. That reduces the key space from 24! to a
handful of permutations, which can be searched EXHAUSTIVELY -- no hill
climbing, so no local-optimum excuse and an exact null.

Two layouts are covered:
  A (orientation-major): letter_index = g[orient]*3 + h[count]
  B (count-major)      : letter_index = h[count]*8 + g[orient]
g ranges over all 8! orderings of the orientation groups, h over all 3!
orderings of arc counts. 40320 * 6 * 2 = 483,840 keys.
"""
import sys, os, itertools
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
import corpus as C
from compare import load_all

QUAD=C.get()['quad']
ALPHA24="ABCDEFGHIKLMNOPQRSTUWXYZ"
AIDX=np.array([ord(c)-65 for c in ALPHA24])
ORD="ABCDEFGH"
GPERMS=np.array(list(itertools.permutations(range(8))), dtype=np.int64)   # 40320 x 8
HPERMS=list(itertools.permutations(range(3)))

def encode(seq):
    o=np.array([ORD.index(s[0]) for s in seq])
    k=np.array([int(s[1])-1 for s in seq])
    return o,k

def sweep(o,k,chunk=8000, want_best=False):
    best=-1e18; bestinfo=None
    n=len(o)
    for layout in ('A','B'):
        for h in HPERMS:
            hk=np.array(h)[k]                       # (87,)
            for s in range(0,len(GPERMS),chunk):
                G=GPERMS[s:s+chunk]                 # (m,8)
                go=G[:,o]                           # (m,87)
                pos = go*3 + hk[None,:] if layout=='A' else hk[None,:]*8 + go
                L=AIDX[pos]                         # (m,87)
                sc=QUAD[L[:,:-3],L[:,1:-2],L[:,2:-1],L[:,3:]].sum(axis=1)/(n-3)
                i=int(sc.argmax())
                if sc[i]>best:
                    best=float(sc[i])
                    if want_best:
                        bestinfo=(layout,h,tuple(G[i]),"".join(chr(65+c) for c in L[i]))
    return (best,bestinfo) if want_best else best

if __name__=='__main__':
    T=load_all(); cons=T['consensus']
    o,k=encode(cons)
    print("="*78)
    print("EXHAUSTIVE STRUCTURED-KEY SWEEP (483,840 keys of Elgar's own family)")
    print("="*78)
    # Elgar's actual notebook key = identity g, identity h, layout A
    hk=np.array([0,1,2])[k]
    L=AIDX[np.arange(8)[o]*3+hk]
    elg=float(QUAD[L[:-3],L[1:-2],L[2:-1],L[3:]].sum())/(len(o)-3)
    print(f"\nElgar's own 1920 notebook key applied to the 1897 note: {elg:.3f}/gram")
    print(f"  plaintext: {''.join(chr(65+c) for c in L)}")
    best,info=sweep(o,k,want_best=True)
    print(f"\nBest over ALL structured keys: {best:.3f}/gram")
    print(f"  layout={info[0]} count-order={info[1]} orientation-order={info[2]}")
    print(f"  plaintext: {info[3]}")
    # exact null: same sweep on shuffled text
    rng=np.random.default_rng(17)
    idx=np.arange(len(o)); nulls=[]
    for t in range(30):
        p=rng.permutation(idx)
        nulls.append(sweep(o[p],k[p]))
    nulls=np.array(nulls)
    print(f"\nNull (same symbols, shuffled order, best-of-483840): "
          f"mean={nulls.mean():.3f} sd={nulls.std():.3f} max={nulls.max():.3f}")
    print(f"  p = {(nulls>=best).mean():.3f}")
    print(f"  z = {(best-nulls.mean())/nulls.std():+.2f}")
    print(f"\nReference: enciphered real English at n=87 scores about -4.20/gram.")
