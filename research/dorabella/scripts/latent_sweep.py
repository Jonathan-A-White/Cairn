"""Exhaustive latent sweep over the 13 reader-contested positions.

With three readers and zero three-way splits, every contested position has
exactly two candidate readings: the majority value and the dissenting reader's
value. That is 2^13 = 8192 complete labellings -- small enough to enumerate,
so the latent-variable model collapses to an exhaustive search. Each labelling
is solved; the best is compared against the SAME procedure applied to shuffled
text, so the best-of-8192 selection effect is in the null too.
"""
import sys, os, itertools
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
import corpus as C
from solver import solve, norm
from three_readers import load

N=87
SCAN_RESTARTS=1; SCAN_ITERS=2500       # cheap, but IDENTICAL for observed and null
FINE_RESTARTS=20; FINE_ITERS=15000
RNG=np.random.default_rng(4242)

def contested(R):
    names=['hartmeier','schmeh','pelling']
    pos=[]; alts=[]
    for i in range(N):
        v=[R[k][i] for k in names]
        if v[0]==v[1]==v[2]: continue
        c={x:v.count(x) for x in set(v)}
        maj=max(c,key=c.get); dis=[x for x in v if x!=maj][0]
        pos.append(i); alts.append((maj,dis))
    return pos, alts

def build(base, pos, alts, mask):
    s=list(base)
    for j,(i,(maj,dis)) in enumerate(zip(pos,alts)):
        s[i]= dis if (mask>>j)&1 else maj
    return s

def scan(base,pos,alts,seed0):
    out=[]
    for mask in range(1<<len(pos)):
        s=build(base,pos,alts,mask)
        b,_,_,_=solve(s,restarts=SCAN_RESTARTS,iters=SCAN_ITERS,seed=seed0+mask)
        out.append(norm(b,N))
    return np.array(out)

if __name__=='__main__':
    R,cons=load()
    pos,alts=contested(R)
    print("="*78); print("EXHAUSTIVE LATENT SWEEP OVER READER-CONTESTED POSITIONS"); print("="*78)
    print(f"\ncontested positions ({len(pos)}): {pos}")
    print(f"labellings to enumerate: 2^{len(pos)} = {1<<len(pos)}\n")
    # majority reading as the base
    base=[max({x:[R[k][i] for k in R].count(x) for x in set(R[k][i] for k in R)}.items(),
              key=lambda t:t[1])[0] for i in range(N)]
    base=[]
    for i in range(N):
        v=[R[k][i] for k in ('hartmeier','schmeh','pelling')]
        c={x:v.count(x) for x in set(v)}
        base.append(max(c,key=c.get))
    sc=scan(base,pos,alts,1000)
    print(f"scan over all {len(sc)} labellings (cheap budget):")
    print(f"  best={sc.max():.3f}  median={np.median(sc):.3f}  worst={sc.min():.3f}")
    top=np.argsort(-sc)[:15]
    print(f"\nre-solving top 25 at full budget...")
    fine=[]
    for m in top:
        s=build(base,pos,alts,int(m))
        b,pt,_,_=solve(s,restarts=FINE_RESTARTS,iters=FINE_ITERS,seed=7000+int(m))
        fine.append((norm(b,N),int(m),pt))
    fine.sort(key=lambda t:-t[0])
    print(f"  best labelling: score={fine[0][0]:.3f} mask={fine[0][1]:013b}")
    print(f"  plaintext: {fine[0][2]}")
    # NULL: same best-of-8192 procedure on shuffled text
    print(f"\nnull: identical best-of-{1<<len(pos)} procedure on shuffled text (12 reps)")
    nulls=[]
    for t in range(8):
        b2=list(base); RNG.shuffle(b2)
        s2=scan(b2,pos,alts,50000+t*10000)
        idx=int(s2.argmax())
        s3=build(b2,pos,alts,idx)
        bb,_,_,_=solve(s3,restarts=FINE_RESTARTS,iters=FINE_ITERS,seed=90000+t)
        nulls.append(norm(bb,N))
        print(f"    rep {t+1}: {nulls[-1]:.3f}")
    nulls=np.array(nulls)
    print(f"\n  null mean={nulls.mean():.3f} sd={nulls.std():.3f} max={nulls.max():.3f}")
    print(f"  observed best={fine[0][0]:.3f}   z={(fine[0][0]-nulls.mean())/nulls.std():+.2f}"
          f"   p={(nulls>=fine[0][0]).mean():.3f}")
    print(f"\n  Reference: enciphered real English at n=87 scores about -4.20/gram.")
