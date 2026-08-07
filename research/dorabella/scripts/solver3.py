"""Phase 4 on the PUBLISHED transcriptions, matched budget throughout."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
import corpus, ensemble2
from solver import solve, norm

D=corpus.get(); TEXT=D['text']
RESTARTS=20; ITERS=15000; N=87
RNG=np.random.default_rng(4242)

def budgeted(seq, seed):
    b,pt,_,_=solve(list(seq), restarts=RESTARTS, iters=ITERS, seed=seed)
    return norm(b,len(seq)), pt

def run():
    V=ensemble2.variants(); cons=V['E0_consensus']; k=len(set(cons))
    print("="*78)
    print(f"PHASE 4 ON PUBLISHED TRANSCRIPTIONS — {RESTARTS}x{ITERS} budget everywhere")
    print("="*78)
    print("\n[A] Reference bands at n=87")
    eb=[];ea=[]
    for _ in range(40):
        i=RNG.integers(0,len(TEXT)-N); pt=TEXT[i:i+N]
        L=sorted(set(pt)); perm=RNG.permutation(26)[:len(L)]
        m={c:int(perm[j]) for j,c in enumerate(L)}
        s,got=budgeted([m[c] for c in pt], int(RNG.integers(1e6)))
        eb.append(s); ea.append(sum(a==b for a,b in zip(got,pt))/N)
    eb=np.array(eb); ea=np.array(ea)
    sh=[]
    for _ in range(60):
        s=list(cons); RNG.shuffle(s)
        sh.append(budgeted(s,int(RNG.integers(1e6)))[0])
    sh=np.array(sh)
    ur=[]
    for _ in range(60):
        s=[str(x) for x in RNG.integers(0,k,N)]
        ur.append(budgeted(s,int(RNG.integers(1e6)))[0])
    ur=np.array(ur)
    print(f"    enciphered real English : mean={eb.mean():.3f} sd={eb.std():.3f} "
          f"5th={np.quantile(eb,.05):.3f}  (recovery acc {ea.mean():.2f})")
    print(f"    shuffled consensus      : mean={sh.mean():.3f} sd={sh.std():.3f} "
          f"95th={np.quantile(sh,.95):.3f} max={sh.max():.3f}")
    print(f"    uniform random          : mean={ur.mean():.3f} sd={ur.std():.3f} "
          f"max={ur.max():.3f}")
    allnull=np.concatenate([sh,ur])

    print("\n[B] Observed")
    print(f"    {'variant':20s} {'fwd':>7s} {'rev':>7s} {'pct(null)':>10s} {'z vs Eng':>9s}")
    out={}
    for nm,seq in V.items():
        f,pf=budgeted(seq,777); r,pr=budgeted(seq[::-1],778)
        out[nm]=(f,r,pf,pr)
        print(f"    {nm:20s} {f:7.3f} {r:7.3f} {(allnull<=f).mean():10.2f} "
              f"{(f-eb.mean())/eb.std():9.2f}")
    print("\n    best plaintexts (forward):")
    for nm,(f,r,pf,pr) in out.items():
        print(f"    {nm:20s} {pf}")
    print("\n    best plaintexts (reversed):")
    for nm,(f,r,pf,pr) in out.items():
        print(f"    {nm:20s} {pr}")

    print("\n[C] Crib-constrained solves on the consensus transcription")
    cribs=['MALVERN','WOLVERHAMPTON','ALFRED','MISSPENNY','PENNY','SYMPATHY','JULY','ELGAR']
    syms=sorted(set(cons)); idx={s:i for i,s in enumerate(syms)}
    ci=[idx[s] for s in cons]
    for crib in cribs:
        ok=[]
        for pos in range(0,N-len(crib)+1):
            w=ci[pos:pos+len(crib)]
            if [list(crib).index(c) for c in crib]==[list(w).index(x) for x in w]:
                ok.append(pos)
        print(f"    {crib:14s} pattern-compatible at {len(ok):3d} positions"
              + (f": {ok[:10]}" if ok else ""))
if __name__=='__main__':
    run()
