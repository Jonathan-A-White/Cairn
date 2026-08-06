"""Does transcription noise ALONE destroy solvability at n=87?

This is the control that decides how to read every negative result in this
report. Take real English, encipher it with a simple substitution, then
corrupt the ciphertext at the same rate at which my own transcription is
uncertain (18/87 = 21% 'L' glyphs, 39/87 = 45% 'L or M'), by swapping the
affected symbols to a CONFUSABLE neighbour -- exactly the error mode the
image analysis showed (adjacent rotations collapsing).

If a 21% confusion rate drops the solver from ~98% recovery to chance, then
Dorabella's resistance is fully explained by transcription noise and no
cryptanalytic conclusion can be drawn from this image.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
import corpus
from solver import solve, norm

D=corpus.get(); TEXT=D['text']
RNG=np.random.default_rng(31337)
RESTARTS=20; ITERS=15000; N=87

def trial(rate, rng):
    i=rng.integers(0,len(TEXT)-N); pt=TEXT[i:i+N]
    letters=sorted(set(pt)); k=len(letters)
    perm=rng.permutation(26)[:k]
    m={c:int(perm[j]) for j,c in enumerate(letters)}
    ct=np.array([m[c] for c in pt])
    # confusion structure: each symbol has 2 'adjacent rotation' neighbours
    order=rng.permutation(k)
    nb={int(order[j]):(int(order[(j-1)%k]),int(order[(j+1)%k])) for j in range(k)}
    sym=sorted(set(ct.tolist()))
    idxmap={s:s for s in sym}
    ct2=ct.copy()
    hit=rng.random(N)<rate
    for p in np.flatnonzero(hit):
        a,b=nb.get(int(ct[p]),(int(ct[p]),int(ct[p])))
        ct2[p]= a if rng.random()<.5 else b
    best,got,_,_=solve(ct2.tolist(), restarts=RESTARTS, iters=ITERS, seed=int(rng.integers(1e6)))
    acc=sum(x==y for x,y in zip(got,pt))/N
    return norm(best,N), acc

def run():
    print("="*78)
    print("CONTROL — does transcription noise alone explain unsolvability?")
    print("="*78)
    print(f"\n{'confusion rate':>14s} {'score/gram':>11s} {'sd':>6s} {'char-accuracy':>14s} {'sd':>6s} {'frac>90%':>9s}")
    for rate in [0.0, 0.05, 0.10, 0.21, 0.35, 0.45, 0.60]:
        rng=np.random.default_rng(int(rate*1000)+7)
        res=[trial(rate,rng) for _ in range(25)]
        s=np.array([r[0] for r in res]); a=np.array([r[1] for r in res])
        tag=''
        if abs(rate-0.21)<1e-9: tag='  <- my "L" ambiguity rate'
        if abs(rate-0.45)<1e-9: tag='  <- my "L or M" rate'
        print(f"{rate:14.2f} {s.mean():11.3f} {s.std():6.3f} {a.mean():14.2f} {a.std():6.2f} {(a>0.9).mean():9.2f}{tag}")
    print("\nCompare with Dorabella's observed solver score (see solver2.log [B]).")

if __name__=='__main__':
    run()
