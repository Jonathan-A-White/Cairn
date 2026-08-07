"""Sixth model: MIRROR-key MASC composed with light transposition.

PRE-REGISTERED FALSIFICATION TARGETS, fixed before the run.
This model is assembled from the two features it is meant to explain -- the
mirror excess (from MIRROR) and the solver deficit (from TRANS) -- so a fit on
THOSE two is a designed outcome and proves nothing. It must therefore be
judged on features it was NOT built from. Declared in advance:

  doubles     Dorabella = 4
  rep2        Dorabella = 19
  rowspread   Dorabella = 0.011
  k           Dorabella = 20
  IC          Dorabella = 0.059
  H           Dorabella = 4.030

The model PASSES only if it lands within +-1.5 pooled sd of Dorabella on at
least 5 of these 6 held-out features, while also matching mirror and solver.
Anything less and it is a model grown toward the data, and is reported as
rejected.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
import discriminate as d
from discriminate5 import gen5
from transposition import columnar, rowgrid_perms
from compare import load_all

HELD_OUT=['doubles','rep2','rowspread','k','IC','H']
ASSEMBLED=['mirror','solver']

def gen_mirror_trans(rng):
    base=d.emit(d.eng(rng),[d.mirror_key(rng)],[])
    if rng.random()<0.75:
        k=int(rng.integers(2,9)); idx=columnar(len(base),k)
    else:
        idx=list(rowgrid_perms(len(base)).values())[int(rng.integers(0,6))]
    return [base[i] for i in idx]

if __name__=='__main__':
    models=['MASC','DIAL','MIRROR','COMPOSITE','TRANS','MIRROR_TRANS']
    NS=40; rng=np.random.default_rng(112358); d.RNG=rng
    X=[];y=[]
    for mi,m in enumerate(models):
        for _ in range(NS):
            f=d.feats(gen_mirror_trans(rng)) if m=='MIRROR_TRANS' else d.feats(gen5(m,rng))
            X.append(f); y.append(mi)
        print(f"  generated {NS} x {m}", flush=True)
    X=np.array(X); y=np.array(y)
    T=load_all(); cons=T['consensus']; ORD="ABCDEFGH"
    dora=np.array(d.feats([f"{ORD.index(s[0])}{int(s[1])-1}" for s in cons]))
    sd=X.std(axis=0)
    mi6=models.index('MIRROR_TRANS')
    print("\nPRE-REGISTERED TEST of MIRROR_TRANS on held-out features")
    print(f"{'feature':11s}{'dorabella':>10s}{'model mean':>12s}{'z':>8s}  verdict")
    npass=0
    for j,n in enumerate(d.NAMES):
        z=(dora[j]-X[y==mi6,j].mean())/max(sd[j],1e-9)
        tag='(assembled)' if n in ASSEMBLED else ('PASS' if abs(z)<=1.5 else 'FAIL')
        if n in HELD_OUT and abs(z)<=1.5: npass+=1
        print(f"{n:11s}{dora[j]:10.3f}{X[y==mi6,j].mean():12.3f}{z:+8.2f}  {tag}")
    print(f"\nheld-out features passed: {npass}/6   (threshold 5)")
    print("VERDICT:", "PASS -- model survives its own falsification test" if npass>=5
          else "REJECTED -- grown toward the data, fails held-out features")
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import cross_val_score
    sc=cross_val_score(RandomForestClassifier(n_estimators=500,random_state=0),X,y,cv=5)
    print(f"\n6-way CV accuracy: {sc.mean():.3f} +- {sc.std():.3f}  (chance {1/6:.3f})")
    clf=RandomForestClassifier(n_estimators=900,random_state=0).fit(X,y)
    p=clf.predict_proba(dora.reshape(1,-1))[0]
    print("\nposterior over six models:")
    for m,pp in sorted(zip(models,p),key=lambda t:-t[1]): print(f"  {m:13s} {pp:.3f}")
