"""Phase 4 — constrained solving with proper null and positive-control discipline."""
import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
from collections import Counter
import corpus, ensemble

A=corpus.A
D=corpus.get()
QUAD=D['quad']; TEXT=D['text']

def to_idx(seq):
    syms=sorted(set(seq)); m={s:i for i,s in enumerate(syms)}
    return np.array([m[s] for s in seq]), syms

def qscore(p):
    return float(QUAD[p[:-3],p[1:-2],p[2:-1],p[3:]].sum())

def anneal(cidx, k, rng, iters=20000, t0=8.0, t1=0.05):
    key=rng.permutation(26)[:k]
    p=key[cidx]; best=cur=qscore(p); bkey=key.copy()
    used=np.zeros(26,bool); used[key]=True
    for it in range(iters):
        T=t0*(t1/t0)**(it/iters)
        nk=key.copy()
        if rng.random()<0.75 or k>=26:
            i,j=rng.integers(0,k,2)
            if i==j: continue
            nk[i],nk[j]=nk[j],nk[i]
        else:
            free=np.flatnonzero(~used)
            if len(free)==0: continue
            i=rng.integers(0,k); nk[i]=free[rng.integers(0,len(free))]
        s=qscore(nk[cidx])
        if s>cur or rng.random()<math.exp((s-cur)/T):
            used=np.zeros(26,bool); used[nk]=True
            key, cur = nk, s
            if s>best: best, bkey = s, nk.copy()
    return best, bkey

def solve(seq, restarts=40, iters=20000, seed=0):
    cidx,syms=to_idx(seq); k=len(syms)
    rng=np.random.default_rng(seed)
    out=[]
    for r in range(restarts):
        b,key=anneal(cidx,k,rng,iters)
        out.append((b,key))
    out.sort(key=lambda x:-x[0])
    best,key=out[0]
    pt="".join(A[c] for c in key[cidx])
    return best, pt, np.array([o[0] for o in out]), syms

def norm(s, n): return s/(n-3)          # per-quadgram

def run():
    print("="*78); print("PHASE 4 — CONSTRAINED SOLVING, WITH NULLS AND POSITIVE CONTROLS"); print("="*78)
    n=87
    RNG=np.random.default_rng(7)

    # ---- POSITIVE CONTROL: can the solver recover KNOWN plaintext at n=87? ----
    print("\n[A] Positive control: encipher real 87-char English, then solve it.")
    print("    If the solver cannot recover known plaintext at this length, no result on")
    print("    Dorabella can be interpreted at all.")
    rec=[]
    for t in range(12):
        i=RNG.integers(0,len(TEXT)-n); pt=TEXT[i:i+n]
        letters=sorted(set(pt)); k=len(letters)
        perm=RNG.permutation(26)[:k]
        m={c:int(perm[j]) for j,c in enumerate(letters)}
        ct=[m[c] for c in pt]
        best,got,scores,syms=solve(ct, restarts=25, iters=15000, seed=int(RNG.integers(1e6)))
        acc=sum(a==b for a,b in zip(got,pt))/n
        rec.append(acc)
        if t<5:
            print(f"    true : {pt}")
            print(f"    got  : {got}   char-accuracy={acc:.2f}  score/gram={norm(best,n):.3f}")
    rec=np.array(rec)
    print(f"    -> recovery accuracy over {len(rec)} trials: mean={rec.mean():.2f} "
          f"median={np.median(rec):.2f} max={rec.max():.2f}  (fraction >90% correct: {(rec>0.9).mean():.2f})")

    # ---- NULL: solve texts that contain no message ----
    print("\n[B] Null distribution: best score the solver reaches on meaningless 87-symbol texts.")
    T0=ensemble.variants()['T0_canonical']
    k_obs=len(set(T0))
    nulls={}
    # (i) shuffles of Dorabella itself: identical unigram profile, order destroyed
    sh=[]
    for _ in range(60):
        s=list(T0); RNG.shuffle(s)
        b,_,_,_=solve(s, restarts=12, iters=12000, seed=int(RNG.integers(1e6)))
        sh.append(norm(b,n))
    nulls['shuffled_dorabella']=np.array(sh)
    # (ii) uniform random over the same number of symbols
    ur=[]
    for _ in range(60):
        s=[str(x) for x in RNG.integers(0,k_obs,n)]
        b,_,_,_=solve(s, restarts=12, iters=12000, seed=int(RNG.integers(1e6)))
        ur.append(norm(b,n))
    nulls['uniform_random']=np.array(ur)
    for kk,v in nulls.items():
        print(f"    {kk:20s} mean={v.mean():.3f} sd={v.std():.3f} "
              f"95th={np.quantile(v,.95):.3f} max={v.max():.3f}")
    # reference points
    eng=[norm(corpus.score(TEXT[RNG.integers(0,len(TEXT)-n):][:n],QUAD,4),n) for _ in range(2000)]
    eng=np.array(eng)
    print(f"    {'real English (n=87)':20s} mean={eng.mean():.3f} sd={eng.std():.3f} "
          f"5th={np.quantile(eng,.05):.3f}")

    # ---- OBSERVED ----
    print("\n[C] Dorabella: best solver score per transcription variant, vs the nulls.")
    V=ensemble.variants()
    allnull=np.concatenate([nulls['shuffled_dorabella'],nulls['uniform_random']])
    print(f"    {'variant':16s} {'fwd':>7s} {'rev':>7s} {'pctile(null)':>13s}  best plaintext (fwd)")
    res={}
    for name,seq in V.items():
        bf,pf,_,_=solve(seq, restarts=40, iters=20000, seed=11)
        br,pr,_,_=solve(seq[::-1], restarts=40, iters=20000, seed=12)
        nf,nr=norm(bf,n),norm(br,n)
        pc=(allnull<=nf).mean()
        res[name]=(nf,nr,pf,pr)
        print(f"    {name:16s} {nf:7.3f} {nr:7.3f} {pc:13.2f}  {pf}")
    print(f"\n    {'':16s} reversed readings:")
    for name,(nf,nr,pf,pr) in res.items():
        print(f"    {name:16s} {'':7s} {'':7s} {'':13s}  {pr}")

    # ---- rows independent / reordered ----
    print("\n[D] Rows solved independently, and row orders permuted (T0).")
    import itertools
    R=ensemble.rows_of(T0)
    for i,r in enumerate(R):
        b,p,_,_=solve(r, restarts=25, iters=15000, seed=20+i)
        print(f"    row{i+1} (n={len(r)}): score/gram={norm(b,len(r)):.3f}  {p}")
    best=None
    for perm in itertools.permutations(range(3)):
        s=sum([R[i] for i in perm],[])
        b,p,_,_=solve(s, restarts=15, iters=12000, seed=30)
        if best is None or norm(b,n)>best[0]: best=(norm(b,n),perm,p)
    print(f"    best row order {best[1]}: score/gram={best[0]:.3f}  {best[2]}")

    # ---- cribs ----
    print("\n[E] Crib-seeded solving: is any plausible crib placeable?")
    cribs=['DORA','PENNY','MISS','MALVERN','SYMPATHY','JULY','ELGAR','DORABELLA','WORCESTER']
    cidx,syms=to_idx(T0)
    for crib in cribs:
        okpos=[]
        for pos in range(0,n-len(crib)+1):
            win=cidx[pos:pos+len(crib)]
            # a crib fits iff the symbol-repetition pattern matches the crib's letter pattern
            pat_c=[list(crib).index(c) for c in crib]
            pat_s=[list(win).index(x) for x in win]
            if pat_c==pat_s: okpos.append(pos)
        print(f"    {crib:10s} pattern-compatible positions: {len(okpos)}"
              + (f"  e.g. {okpos[:8]}" if okpos else ""))
    return res, nulls, rec

if __name__=='__main__':
    run()
