"""Majority-of-three reconstruction over the genuinely pre-consensus readers.

Hartmeier (2006), Schmeh (2018), Pelling (2012). All three read the 1937 plate
before the 2021 consensus existed. Their letter strings use different symbol
names, so each is aligned to a common labelling by Hungarian assignment before
comparison. At each position where they do not all agree, the reader who
differs from the other two is the presumptive error.
"""
import sys, os, itertools
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
from scipy.optimize import linear_sum_assignment
from compare import load_all

def align(src, ref):
    """Relabel src into ref's symbol names by best one-to-one assignment."""
    A=sorted(set(src)); B=sorted(set(ref))
    M=np.zeros((len(A),len(B)))
    for x,y in zip(src,ref): M[A.index(x),B.index(y)]+=1
    r,c=linear_sum_assignment(-M)
    m={A[i]:B[j] for i,j in zip(r,c)}
    spare=iter([s for s in "0123456789#@$%&*" ])
    return [m.get(x) or next(spare) for x in src]

def load():
    T=load_all(); T.pop('_conf')
    pel=list(open(os.path.join('data','pelling.txt')).read().strip())
    H=T['dcode']                      # == Hartmeier (dCode copied it)
    return {'hartmeier':list(H), 'schmeh':align(T['schmeh'],H), 'pelling':align(pel,H)}, T['consensus']

if __name__=='__main__':
    R,cons=load()
    names=['hartmeier','schmeh','pelling']
    n=87
    odd={k:[] for k in names}; unan=0; three_way=[]
    for i in range(n):
        v=[R[k][i] for k in names]
        if v[0]==v[1]==v[2]: unan+=1; continue
        # who is the odd one out?
        counts={x:v.count(x) for x in set(v)}
        if len(set(v))==3: three_way.append(i); continue
        maj=[x for x,c in counts.items() if c==2][0]
        odd[[k for k,x in zip(names,v) if x!=maj][0]].append(i)
    print(f"unanimous positions: {unan}/87 ({unan/n:.1%})")
    print(f"three-way splits   : {len(three_way)} {three_way}")
    print("\nper-reader error count (reader differs from the other two):")
    tot=0
    for k in names:
        print(f"  {k:10s} {len(odd[k]):2d}/87 = {len(odd[k])/n:5.1%}   positions {odd[k]}")
        tot+=len(odd[k])
    print(f"  total {tot}  (union of all pairwise disagreements should equal this)")
    # binomial CIs
    from scipy import stats
    print("\n  95% CI on each reader's error rate (Clopper-Pearson):")
    for k in names:
        lo,hi=stats.beta.ppf(0.025,len(odd[k]),n-len(odd[k])+1) if len(odd[k])>0 else 0.0, \
              stats.beta.ppf(0.975,len(odd[k])+1,n-len(odd[k]))
        lo=0.0 if len(odd[k])==0 else float(stats.beta.ppf(0.025,len(odd[k]),n-len(odd[k])+1))
        print(f"  {k:10s} {len(odd[k])/n:5.1%}  [{lo:.1%}, {float(hi):.1%}]")
    # majority string vs consensus
    maj=[]
    for i in range(n):
        v=[R[k][i] for k in names]
        c={x:v.count(x) for x in set(v)}
        maj.append(max(c,key=c.get))
    d=[i for i in range(n) if maj[i]!=R['hartmeier'][i]]
    print(f"\n3-reader majority vs Hartmeier: differs at {len(d)} positions {d}")
    # overlap with classifier flags
    flagged=[0,4,9,15,21,23,24,33,36,68,71,77]
    allbad=sorted(set(sum(odd.values(),[]))|set(three_way))
    ov=sorted(set(allbad)&set(flagged))
    print(f"\nall contested positions ({len(allbad)}): {allbad}")
    print(f"classifier-flagged   ({len(flagged)}): {flagged}")
    print(f"overlap ({len(ov)}): {ov}")
    tab=[[len(ov), len(flagged)-len(ov)],[len(allbad)-len(ov), 87-len(flagged)-(len(allbad)-len(ov))]]
    print(f"Fisher exact p = {stats.fisher_exact(tab)[1]:.4f}")
