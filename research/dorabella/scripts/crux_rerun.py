"""Residual deficit under the three-reader error model.

Round 4 concluded transcription noise explained the whole gap, using 9.2%
(consensus vs Schmeh). The three-reader triangulation shows Schmeh is the
outlier (10.3% vs Hartmeier 1.1%, Pelling 3.4%), so that figure was inflated
by one noisy reader. This recomputes the deficit with corruption anchors at
the rates the reader data actually supports.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
import corpus as C
from solver import solve, norm
D=C.get(); TEXT=D['text']
RNG=np.random.default_rng(606); N=87
RESTARTS=20; ITERS=15000

def trial(rate, rng):
    i=rng.integers(0,len(TEXT)-N); pt=TEXT[i:i+N]
    L=sorted(set(pt)); k=len(L); perm=rng.permutation(26)[:k]
    m={c:int(perm[j]) for j,c in enumerate(L)}
    ct=np.array([m[c] for c in pt])
    vals=sorted(set(ct.tolist())); mm=len(vals)
    ring=[vals[i2] for i2 in rng.permutation(mm)]
    nb={ring[j]:(ring[(j-1)%mm], ring[(j+1)%mm]) for j in range(mm)}
    ct2=ct.copy()
    for p in np.flatnonzero(rng.random(N)<rate):
        a,b=nb[int(ct[p])]; ct2[p]= a if rng.random()<.5 else b
    best,got,_,_=solve(ct2.tolist(),restarts=RESTARTS,iters=ITERS,seed=int(rng.integers(1e6)))
    return norm(best,N)

if __name__=='__main__':
    OBS=-4.680
    print("="*78); print("RESIDUAL DEFICIT UNDER THE THREE-READER ERROR MODEL"); print("="*78)
    print(f"\nObserved (consensus, matched budget): {OBS:.3f}/gram\n")
    print(f"{'rate':>7s} {'n':>4s} {'expected':>9s} {'sd':>6s} {'sem':>6s} {'residual deficit':>18s} {'note'}")
    notes={0.011:'Hartmeier error (=~consensus)', 0.034:'Pelling error',
           0.062:'upper 95% CI, Hartmeier', 0.103:'Schmeh error (the outlier)'}
    for rate in (0.0, 0.011, 0.034, 0.062, 0.103):
        rng=np.random.default_rng(int(rate*10000)+5)
        v=np.array([trial(rate,rng) for _ in range(40)])
        sem=v.std()/np.sqrt(len(v))
        resid=OBS-v.mean()
        print(f"{rate:7.3f} {len(v):4d} {v.mean():9.3f} {v.std():6.3f} {sem:6.3f} "
              f"{resid:+18.3f} {notes.get(rate,'')}")
    print("\n  A negative residual means Dorabella scores WORSE than a genuine simple")
    print("  substitution of English read at that error rate -- i.e. unexplained deficit.")
