"""Crib-CONSTRAINED solving.

A pattern screen only asks 'could these letters sit here without contradiction'.
This instead pins the crib into the key and anneals everything else around it,
then asks whether the constrained optimum is still a good decipherment. The
comparison that makes it meaningful: the same crib, pinned at the same kind of
position, in SHUFFLED text. If a crib is really present, constraining it should
cost little relative to the unconstrained solve; if it is absent, the constraint
drags the score down to the shuffled-text level.
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
import corpus, ensemble2
from solver import qscore, norm

A=corpus.A; AI={c:i for i,c in enumerate(A)}
RESTARTS=14; ITERS=12000; N=87

def anneal_fixed(cidx, k, fixed, rng, iters=ITERS):
    """fixed: dict symbol_index -> letter_index, held constant."""
    free=[s for s in range(k) if s not in fixed]
    used=set(fixed.values())
    avail=[l for l in range(26) if l not in used]
    key=np.zeros(k,dtype=int)
    for s,l in fixed.items(): key[s]=l
    pick=rng.permutation(len(avail))[:len(free)]
    for s,pi in zip(free,pick): key[s]=avail[pi]
    cur=best=qscore(key[cidx]); bkey=key.copy()
    if not free: return best,bkey
    for it in range(iters):
        T=8.0*(0.05/8.0)**(it/iters)
        nk=key.copy()
        if rng.random()<0.75 or len(avail)<=len(free):
            if len(free)<2: continue
            i,j=rng.choice(len(free),2,replace=False)
            a,b=free[i],free[j]; nk[a],nk[b]=nk[b],nk[a]
        else:
            inuse=set(nk[free].tolist())
            spare=[l for l in avail if l not in inuse]
            if not spare: continue
            a=free[rng.integers(0,len(free))]
            nk[a]=spare[rng.integers(0,len(spare))]
        s=qscore(nk[cidx])
        if s>cur or rng.random()<math.exp((s-cur)/T):
            key,cur=nk,s
            if s>best: best,bkey=s,nk.copy()
    return best,bkey

def fit_crib(seq, crib, pos):
    """Return symbol->letter dict if the crib can sit at pos, else None."""
    syms=sorted(set(seq)); idx={s:i for i,s in enumerate(syms)}
    f={}; rev={}
    for j,ch in enumerate(crib):
        s=idx[seq[pos+j]]; l=AI[ch]
        if s in f and f[s]!=l: return None
        if l in rev and rev[l]!=s: return None
        f[s]=l; rev[l]=s
    return f

def solve_with_crib(seq, crib, seed):
    syms=sorted(set(seq)); idx={s:i for i,s in enumerate(syms)}
    cidx=np.array([idx[s] for s in seq]); k=len(syms)
    rng=np.random.default_rng(seed)
    best=(-1e9,None,None)
    for pos in range(0, len(seq)-len(crib)+1):
        f=fit_crib(seq,crib,pos)
        if f is None: continue
        for _ in range(RESTARTS):
            b,key=anneal_fixed(cidx,k,f,rng)
            if b>best[0]:
                best=(b,pos,"".join(A[c] for c in key[cidx]))
    return best

def run():
    V=ensemble2.variants(); cons=V['E0_consensus']
    rng=np.random.default_rng(9)
    cribs=['MALVERN','ALFRED','PENNY','SYMPATHY','JULY','ELGAR','WOLVERHAMPTON','MISSPENNY']
    print("="*78); print("CRIB-CONSTRAINED SOLVING (consensus transcription)"); print("="*78)
    # unconstrained reference
    from solver import solve
    ub,_,_,_=solve(cons, restarts=20, iters=15000, seed=1)
    print(f"\nunconstrained best on consensus: {norm(ub,N):.3f}/gram\n")
    print(f"{'crib':14s} {'fits':>5s} {'best score':>11s} {'pos':>4s}  {'shuffled-text null':>20s}  {'z':>6s}")
    for crib in cribs:
        b,pos,pt=solve_with_crib(cons,crib,int(rng.integers(1e6)))
        nfits=sum(1 for p in range(N-len(crib)+1) if fit_crib(cons,crib,p))
        if nfits==0:
            print(f"{crib:14s} {0:5d} {'--':>11s} {'--':>4s}  {'(cannot be placed)':>20s}")
            continue
        # null: same crib forced into shuffled versions of the same text
        nl=[]
        for _ in range(12):
            s=list(cons); rng.shuffle(s)
            nb,_,_=solve_with_crib(s,crib,int(rng.integers(1e6)))
            if nb>-1e8: nl.append(norm(nb,N))
        nl=np.array(nl) if nl else np.array([np.nan])
        z=(norm(b,N)-nl.mean())/nl.std() if len(nl)>1 and nl.std()>0 else float('nan')
        print(f"{crib:14s} {nfits:5d} {norm(b,N):11.3f} {pos:4d}  {nl.mean():9.3f}+-{nl.std():.3f}  {z:6.2f}")
        print(f"{'':14s} {pt}")
if __name__=='__main__':
    run()
