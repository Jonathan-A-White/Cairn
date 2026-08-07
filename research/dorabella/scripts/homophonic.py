"""Homophonic family: many cipher symbols may map to the SAME letter.

Pre-registered on documentary grounds, like the rotation family. Schooling's
first article -- which Elgar owned -- describes exactly this: "underneath each
of the letters of the alphabet are written three, sometimes four, peculiar
marks ... the writer made use of any one of these three marks to represent a
letter." It is the one documented family that is also recoverable in principle
at this length: unicity distance 35.2 against 87 available (section 6),
against 55 for a 2-alphabet polyalphabetic.

A non-injective solver has strictly more freedom than the injective one, so it
scores higher on EVERYTHING. The nulls therefore use the identical solver, and
a homophonically-enciphered-English positive control fixes the scale.
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
import corpus as C
from compare import load_all
from solver import qscore
A=C.A; D=C.get(); TEXT=D['text']
N=87; RESTARTS=25; ITERS=18000
RNG=np.random.default_rng(1896)

def to_idx(seq):
    syms=sorted(set(seq)); m={s:i for i,s in enumerate(syms)}
    return np.array([m[s] for s in seq]), len(syms)

def anneal_homo(cidx,k,rng,iters=ITERS):
    key=rng.integers(0,26,k)
    cur=best=qscore(key[cidx]); bkey=key.copy()
    for it in range(iters):
        T=8.0*(0.05/8.0)**(it/iters)
        nk=key.copy()
        if rng.random()<0.5:
            nk[rng.integers(0,k)]=rng.integers(0,26)     # retarget one symbol
        else:
            i,j=rng.integers(0,k,2)
            nk[i],nk[j]=nk[j],nk[i]
        s=qscore(nk[cidx])
        if s>cur or rng.random()<math.exp((s-cur)/T):
            key,cur=nk,s
            if s>best: best,bkey=s,nk.copy()
    return best,bkey

def solve_homo(seq,seed):
    cidx,k=to_idx(seq); rng=np.random.default_rng(seed)
    best=-1e18; bk=None
    for r in range(RESTARTS):
        b,kk=anneal_homo(cidx,k,rng)
        if b>best: best,bk=b,kk
    return best/(len(seq)-3), "".join(A[c] for c in bk[cidx])

def homo_encipher_english(rng,k=20):
    """Encipher English into k symbols, allotting symbols in proportion to
    letter frequency -- the classic homophonic construction."""
    i=rng.integers(0,len(TEXT)-N); pt=TEXT[i:i+N]
    from collections import Counter
    f=Counter(TEXT[:200000]); letters=sorted(f)
    w=np.array([f[c] for c in letters],float); w/=w.sum()
    alloc={c:max(1,int(round(x*k))) for c,x in zip(letters,w)}
    pool={}; nxt=0
    for c in letters:
        pool[c]=[(nxt+j)%k for j in range(alloc[c])]; nxt=(nxt+alloc[c])%k
    ct=[pool[c][rng.integers(0,len(pool[c]))] for c in pt]
    return ct,pt

if __name__=='__main__':
    T=load_all(); cons=T['consensus']
    print("="*78); print("HOMOPHONIC FAMILY (pre-registered; Schooling article I)"); print("="*78)
    print(f"\nbudget: {RESTARTS} restarts x {ITERS} iters, identical for all rows\n")
    obs,pt=solve_homo(cons,11)
    print(f"Dorabella (consensus)          : {obs:.3f}   {pt}")
    # positive control
    pc=[]
    for t in range(12):
        ct,plain=homo_encipher_english(RNG)
        s,got=solve_homo(ct,int(RNG.integers(1e6)))
        pc.append(s)
    pc=np.array(pc)
    print(f"homophonic English (control)   : {pc.mean():.3f} +- {pc.std():.3f}")
    # nulls with the SAME over-powered solver
    sh=[]
    for t in range(14):
        s_=list(cons); RNG.shuffle(s_)
        sh.append(solve_homo(s_,int(RNG.integers(1e6)))[0])
    sh=np.array(sh)
    ur=[]
    for t in range(14):
        s_=[str(x) for x in RNG.integers(0,len(set(cons)),N)]
        ur.append(solve_homo(s_,int(RNG.integers(1e6)))[0])
    ur=np.array(ur)
    print(f"shuffled Dorabella (null)      : {sh.mean():.3f} +- {sh.std():.3f}  max {sh.max():.3f}")
    print(f"uniform random (null)          : {ur.mean():.3f} +- {ur.std():.3f}  max {ur.max():.3f}")
    allnull=np.concatenate([sh,ur])
    print(f"\n  observed percentile vs null : {(allnull<=obs).mean():.2f}")
    print(f"  z vs homophonic-English     : {(obs-pc.mean())/pc.std():+.2f}")
