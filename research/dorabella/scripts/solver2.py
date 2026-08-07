"""Phase 4, corrected: every score compared at an IDENTICAL search budget,
and per-row scores compared against LENGTH-MATCHED nulls.

The first run of solver.py gave the observed text 40 restarts x 20000 iters
while the nulls got 12 x 12000. Search budget alone raises the achievable
score, so that comparison was biased in favour of the observed text. Here
every solve -- observed, null and positive control -- uses the same budget.
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
import corpus, ensemble
from solver import solve, norm, to_idx

D=corpus.get(); TEXT=D['text']; QUAD=D['quad']
RESTARTS=20; ITERS=15000          # <-- the single shared budget
RNG=np.random.default_rng(2718)

def budgeted(seq, seed):
    b,pt,_,_=solve(list(seq), restarts=RESTARTS, iters=ITERS, seed=seed)
    return norm(b,len(seq)), pt

def null_band(n, k, reps, kind):
    out=[]
    for _ in range(reps):
        if kind=='shuffle_T0':
            s=list(ensemble.variants()['T0_canonical']); RNG.shuffle(s); s=s[:n]
        else:
            s=[str(x) for x in RNG.integers(0,k,n)]
        out.append(budgeted(s, int(RNG.integers(1e6)))[0])
    return np.array(out)

def eng_band(n, reps):
    """Encipher real English of length n and solve it at the same budget."""
    out=[]; acc=[]
    for _ in range(reps):
        i=RNG.integers(0,len(TEXT)-n); pt=TEXT[i:i+n]
        letters=sorted(set(pt)); perm=RNG.permutation(26)[:len(letters)]
        m={c:int(perm[j]) for j,c in enumerate(letters)}
        s,got=budgeted([m[c] for c in pt], int(RNG.integers(1e6)))
        out.append(s); acc.append(sum(a==b for a,b in zip(got,pt))/n)
    return np.array(out), np.array(acc)

def run():
    print("="*78)
    print(f"PHASE 4 (CORRECTED) — matched budget: {RESTARTS} restarts x {ITERS} iters everywhere")
    print("="*78)
    V=ensemble.variants(); T0=V['T0_canonical']; n=87; k=len(set(T0))

    print("\n[A] Reference bands at n=87, all at the shared budget")
    eb,ea=eng_band(87,40)
    sb=null_band(87,k,60,'shuffle_T0')
    ub=null_band(87,k,60,'uniform')
    print(f"    enciphered real English : mean={eb.mean():.3f} sd={eb.std():.3f} "
          f"5th={np.quantile(eb,.05):.3f}   (solver char-accuracy {ea.mean():.2f})")
    print(f"    shuffled Dorabella      : mean={sb.mean():.3f} sd={sb.std():.3f} "
          f"95th={np.quantile(sb,.95):.3f} max={sb.max():.3f}")
    print(f"    uniform random          : mean={ub.mean():.3f} sd={ub.std():.3f} "
          f"95th={np.quantile(ub,.95):.3f} max={ub.max():.3f}")

    print("\n[B] Observed, same budget")
    allnull=np.concatenate([sb,ub])
    print(f"    {'variant':16s} {'fwd':>7s} {'rev':>7s} {'pct(null)':>10s} {'z vs English':>13s}")
    for name,seq in V.items():
        f,_=budgeted(seq, 101); r,_=budgeted(seq[::-1], 102)
        print(f"    {name:16s} {f:7.3f} {r:7.3f} {(allnull<=f).mean():10.2f} "
              f"{(f-eb.mean())/eb.std():13.2f}")

    print("\n[C] Per-row scores against LENGTH-MATCHED nulls")
    R=ensemble.rows_of(T0)
    for i,row in enumerate(R):
        m=len(row)
        s,pt=budgeted(row, 200+i)
        nb=null_band(m,k,50,'shuffle_T0')
        e2,_=eng_band(m,30)
        print(f"    row{i+1} (n={m}): obs={s:.3f}  shuffle-null mean={nb.mean():.3f} "
              f"sd={nb.std():.3f} max={nb.max():.3f}  English={e2.mean():.3f}+-{e2.std():.3f}"
              f"  pct(null)={(nb<=s).mean():.2f}")
        print(f"              {pt}")
    print("\n    Note how much easier a 27-31 symbol text is to force into English-looking")
    print("    output: the null itself rises sharply as n falls. Short-row 'readings' are")
    print("    the clearest demonstration of why a raw solver score proves nothing.")

if __name__=='__main__':
    run()
