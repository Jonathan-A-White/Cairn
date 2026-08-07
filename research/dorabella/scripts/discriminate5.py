"""Five-model discrimination, adding TRANS+MASC to the model set.

The open puzzle from Round 10 is that no model generated BOTH the mirror
excess and the solver deficit. Transposition composed with substitution is a
candidate the earlier model set did not contain: it leaves unigram statistics
untouched while destroying n-gram structure.
"""
import sys, os, itertools
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
import discriminate as d
from compare import load_all
from transposition import columnar, rowgrid_perms

def gen_trans(rng):
    """MASC-encipher English, then apply a columnar transposition."""
    base=d.emit(d.eng(rng),[d.rand_key(rng)],[])
    k=int(rng.integers(2,9))
    idx=columnar(len(base),k)
    if rng.random()<0.3:
        idx=list(rowgrid_perms(len(base)).values())[int(rng.integers(0,6))]
    return [base[i] for i in idx]

def gen5(model,rng):
    return gen_trans(rng) if model=='TRANS' else d.gen(model,rng)

if __name__=='__main__':
    models=['MASC','DIAL','MIRROR','COMPOSITE','TRANS']
    NS=40
    rng=np.random.default_rng(161803)
    d.RNG=rng
    X=[];y=[]
    for mi,m in enumerate(models):
        for _ in range(NS):
            X.append(d.feats(gen5(m,rng))); y.append(mi)
        print(f"  generated {NS} x {m}", flush=True)
    X=np.array(X); y=np.array(y)
    print("\nfeature means by model:")
    print(f"{'model':11s}"+"".join(f"{n:>11s}" for n in d.NAMES))
    for mi,m in enumerate(models):
        print(f"{m:11s}"+"".join(f"{X[y==mi,j].mean():11.3f}" for j in range(X.shape[1])))
    print(f"{'sd (pooled)':11s}"+"".join(f"{X[:,j].std():11.3f}" for j in range(X.shape[1])))
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import cross_val_score
    sc=cross_val_score(RandomForestClassifier(n_estimators=500,random_state=0),X,y,cv=5)
    print(f"\n5-way CV accuracy: {sc.mean():.3f} +- {sc.std():.3f}   (chance 0.200)")
    clf=RandomForestClassifier(n_estimators=900,random_state=0).fit(X,y)
    T=load_all(); cons=T['consensus']; ORD="ABCDEFGH"
    dora=[f"{ORD.index(s[0])}{int(s[1])-1}" for s in cons]
    fd=np.array(d.feats(dora))
    p=clf.predict_proba(fd.reshape(1,-1))[0]
    print("\nposterior over models for Dorabella:")
    for m,pp in sorted(zip(models,p),key=lambda t:-t[1]):
        print(f"  {m:11s} {pp:.3f}")
    print("\nDorabella vs each model mean (pooled sd units):")
    print(f"{'feature':11s}{'dora':>9s}"+"".join(f"{m:>11s}" for m in models))
    for j,n in enumerate(d.NAMES):
        row=f"{n:11s}{fd[j]:9.3f}"
        for mi in range(len(models)):
            row+=f"{(fd[j]-X[y==mi,j].mean())/max(X[:,j].std(),1e-9):+11.2f}"
        print(row)
