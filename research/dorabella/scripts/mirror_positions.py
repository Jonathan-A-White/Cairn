"""Are the 13 mirror pairs uniformly spread, or clustered?

Pre-registered by the literature, not by us: Massey reported the mirror pairs
and the alternation runs occupy disjoint stretches, and Pelling (2020) flagged
"the cluster of mirror pairs at the end of the middle line" as candidate
padding. Under MIRROR (mirroring as a key property) the pairs should follow
high-mass bigrams, i.e. be roughly uniform. Under COMPOSITE (mirroring as
decoration) they cluster.

Two nulls: (a) uniform placement of the same number of points, and
(b) a permutation null on the symbol sequence CONDITIONED on producing a
comparable number of mirror pairs, so that clustering is tested independently
of the excess itself.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
from scipy import stats
from compare import load_all
ORD="ABCDEFGH"; N=87
RNG=np.random.default_rng(20200)

def mirror_pos(seq):
    out=[]
    for i,(a,b) in enumerate(zip(seq,seq[1:])):
        d=abs(ORD.index(a[0])-ORD.index(b[0])); d=min(d,8-d)
        if d==4 and a[1]==b[1]: out.append(i)
    return out

def maxwin(pos, w=12, n=86):
    """largest count inside any window of width w"""
    p=np.array(sorted(pos)); best=0
    for s in range(0, n-w+1):
        best=max(best, int(((p>=s)&(p<s+w)).sum()))
    return best

if __name__=='__main__':
    T=load_all(); cons=T['consensus']
    pos=mirror_pos(cons); m=len(pos)
    print("="*78); print("MIRROR-PAIR POSITION TEST"); print("="*78)
    print(f"\n{m} mirror pairs at adjacency positions: {pos}")
    rows=[(0,29),(29,60),(60,87)]
    for r,(s,e) in enumerate(rows,1):
        k=[p for p in pos if s<=p<e]
        print(f"  line {r} (adjacencies {s}-{e-1}): {len(k)}  {k}")
    obs_w=maxwin(pos)
    ks=stats.kstest((np.array(pos)+0.5)/86.0, 'uniform')
    print(f"\nmax pairs in any 12-wide window: {obs_w}")
    print(f"KS test against uniform: D={ks.statistic:.3f}, p={ks.pvalue:.3f}")

    # null (a): uniform placement of m points
    nu=[maxwin(RNG.choice(86,size=m,replace=False)) for _ in range(20000)]
    nu=np.array(nu)
    print(f"\nnull (a) uniform placement of {m} points:")
    print(f"  maxwin mean={nu.mean():.2f} sd={nu.std():.2f} 95th={np.quantile(nu,.95):.0f}")
    print(f"  p(null >= observed) = {(nu>=obs_w).mean():.4f}")

    # null (b): permutation of the symbol sequence, conditioned on count
    keep=[]
    v=list(cons)
    for _ in range(200000):
        RNG.shuffle(v)
        p=mirror_pos(v)
        if abs(len(p)-m)<=2: keep.append(maxwin(p))
        if len(keep)>=8000: break
    keep=np.array(keep)
    print(f"\nnull (b) shuffled sequence, conditioned on {m-2}-{m+2} mirror pairs "
          f"({len(keep)} accepted):")
    print(f"  maxwin mean={keep.mean():.2f} sd={keep.std():.2f} 95th={np.quantile(keep,.95):.0f}")
    print(f"  p(null >= observed) = {(keep>=obs_w).mean():.4f}")
