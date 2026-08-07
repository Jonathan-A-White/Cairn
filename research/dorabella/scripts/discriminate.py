"""Can ANY statistic distinguish the surviving hypotheses at n = 87?

The thesis on the table is that Dorabella is a dial/sliding-card sectional
polyalphabetic. Before adopting it, the adversarial question must be answered:
is that reading DISTINGUISHABLE at this length from the rival survivors, or is
it merely compatible with the evidence like everything else?

Four generative models, each producing 87 symbols over a 20-symbol alphabet
laid out on the 8-orientation x 3-arc grid:
  A  MASC            - simple substitution of English, random key
  B  DIAL            - sectional polyalphabetic, 2-3 sections, key changes mid-text
  C  MIRROR-MASC     - simple substitution whose key mirrors common bigrams
  D  COMPOSITE       - part MASC English, part random 'decoration'

Statistics: IC, entropy, repeated bigrams, doubled symbols, mirror-pair count,
across-row IC spread, and best injective solver score. A classifier is then
cross-validated on these features. If it cannot beat chance, no statistic at
n=87 separates the hypotheses, and they can only be ranked by documentary
weight -- which is itself a reportable result.
"""
import sys, os, math, itertools
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
from collections import Counter
import corpus as C
from compare import load_all
from solver import solve, norm
from phase23 import ic, entropy, doubles, repeats

D=C.get(); TEXT=D['text']
N=87; ROWS=[29,31,27]
ALPHA24="ABCDEFGHIKLMNOPQRSTUWXYZ"
SLOTS=[(o,k) for o in range(8) for k in range(3)]     # 24 (orientation, arc) slots
RNG=np.random.default_rng(31415)
SOLVE_RESTARTS=10; SOLVE_ITERS=8000

def mirror_key(rng):
    """Assign letters to slots so that high-bigram-mass pairs sit 180 apart."""
    import networkx as nx
    tr=str.maketrans({'J':'I','V':'U'})
    t=TEXT[:400000].translate(tr)
    bg=Counter(t[i:i+2] for i in range(len(t)-1)); tot=sum(bg.values())
    G=nx.Graph()
    for i,a in enumerate(ALPHA24):
        for b in ALPHA24[i+1:]:
            G.add_edge(a,b,weight=(bg[a+b]+bg[b+a])/tot)
    M=list(nx.max_weight_matching(G,maxcardinality=True))
    rng.shuffle(M)
    key={}
    for g,(a,b) in enumerate(M):          # group g and g+4 are mirrors
        go, gm = g%4, (g%4)+4
        pos=g//4
        key[a]=(go,pos); key[b]=(gm,pos)
    return key

def rand_key(rng):
    sl=[SLOTS[i] for i in rng.permutation(24)]
    return {c:sl[i] for i,c in enumerate(ALPHA24)}

def eng(rng,n=N):
    i=rng.integers(0,len(TEXT)-n)
    return TEXT[i:i+n].translate(str.maketrans({'J':'I','V':'U'}))

def emit(pt, keys, bounds):
    out=[]
    for i,c in enumerate(pt):
        k=keys[sum(1 for b in bounds if i>=b)]
        o,a=k[c]; out.append(f"{o}{a}")
    return out

def gen(model, rng):
    if model=='MASC':
        return emit(eng(rng), [rand_key(rng)], [])
    if model=='DIAL':
        nsec=rng.integers(2,4)
        cuts=sorted(rng.choice(range(15,N-15), size=nsec-1, replace=False))
        return emit(eng(rng), [rand_key(rng) for _ in range(nsec)], cuts)
    if model=='MIRROR':
        return emit(eng(rng), [mirror_key(rng)], [])
    if model=='COMPOSITE':
        k=rand_key(rng); s=emit(eng(rng),[k],[])
        a,b=sorted(rng.choice(range(10,N-10),2,replace=False))
        for i in range(a,b):                       # decoration stretch
            o,kk=SLOTS[rng.integers(0,24)]; s[i]=f"{o}{kk}"
        return s
    raise ValueError(model)

def mirror_pairs(seq):
    n=0
    for x,y in zip(seq,seq[1:]):
        d=abs(int(x[0])-int(y[0])); d=min(d,8-d)
        if d==4 and x[1]==y[1]: n+=1
    return n

def rowspread(seq):
    k=0; v=[]
    for L in ROWS: v.append(ic(seq[k:k+L])); k+=L
    return float(np.std(v))

def feats(seq, with_solver=True):
    f=[ic(seq), entropy(seq), doubles(seq),
       sum(len(p)-1 for p in repeats(seq,2).values()),
       mirror_pairs(seq), rowspread(seq), len(set(seq))]
    if with_solver:
        b,_,_,_=solve(seq,restarts=SOLVE_RESTARTS,iters=SOLVE_ITERS,seed=int(RNG.integers(1e6)))
        f.append(norm(b,N))
    return f

NAMES=['IC','H','doubles','rep2','mirror','rowspread','k','solver']

if __name__=='__main__':
    models=['MASC','DIAL','MIRROR','COMPOSITE']
    NS=40
    X=[];y=[]
    for mi,m in enumerate(models):
        for _ in range(NS):
            X.append(feats(gen(m,RNG))); y.append(mi)
        print(f"  generated {NS} x {m}", flush=True)
    X=np.array(X); y=np.array(y)
    print("\nfeature means by model:")
    print(f"{'model':11s}"+"".join(f"{n:>11s}" for n in NAMES))
    for mi,m in enumerate(models):
        print(f"{m:11s}"+"".join(f"{X[y==mi,j].mean():11.3f}" for j in range(X.shape[1])))
    print(f"{'sd (pooled)':11s}"+"".join(f"{X[:,j].std():11.3f}" for j in range(X.shape[1])))

    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import cross_val_score
    clf=RandomForestClassifier(n_estimators=400, random_state=0)
    sc=cross_val_score(clf,X,y,cv=5)
    print(f"\n4-way classification accuracy (5-fold CV): {sc.mean():.3f} +- {sc.std():.3f}   (chance 0.250)")
    for a,b in itertools.combinations(range(4),2):
        m=(y==a)|(y==b)
        s2=cross_val_score(RandomForestClassifier(n_estimators=400,random_state=0),X[m],y[m],cv=5)
        print(f"  {models[a]:10s} vs {models[b]:10s}: {s2.mean():.3f}   (chance 0.500)")
    # where does Dorabella fall?
    T=load_all(); cons=T['consensus']
    ORD="ABCDEFGH"
    dora=[f"{ORD.index(s[0])}{int(s[1])-1}" for s in cons]
    fd=np.array(feats(dora))
    print("\nDorabella feature vector vs each model's mean (in pooled sd units):")
    print(f"{'feature':11s}{'dorabella':>11s}"+"".join(f"{m:>11s}" for m in models))
    for j,n in enumerate(NAMES):
        row=f"{n:11s}{fd[j]:11.3f}"
        for mi in range(4):
            z=(fd[j]-X[y==mi,j].mean())/max(X[:,j].std(),1e-9)
            row+=f"{z:+11.2f}"
        print(row)

def posterior():
    """Classifier posterior over models for the real Dorabella feature vector."""
    import numpy as np, itertools
    from sklearn.ensemble import RandomForestClassifier
    models=['MASC','DIAL','MIRROR','COMPOSITE']
    NS=40
    rng=np.random.default_rng(271828)
    global RNG; RNG=rng
    X=[];y=[]
    for mi,m in enumerate(models):
        for _ in range(NS):
            X.append(feats(gen(m,rng))); y.append(mi)
    X=np.array(X); y=np.array(y)
    clf=RandomForestClassifier(n_estimators=800,random_state=0).fit(X,y)
    T=load_all(); cons=T['consensus']; ORD="ABCDEFGH"
    dora=[f"{ORD.index(s[0])}{int(s[1])-1}" for s in cons]
    fd=np.array(feats(dora)).reshape(1,-1)
    p=clf.predict_proba(fd)[0]
    print("\nclassifier posterior over models for Dorabella (fresh 160-sample fit):")
    for m,pp in sorted(zip(models,p), key=lambda t:-t[1]):
        print(f"  {m:11s} {pp:.3f}")
    imp=clf.feature_importances_
    print("\nfeature importances:")
    for n,i in sorted(zip(NAMES,imp), key=lambda t:-t[1]):
        print(f"  {n:11s} {i:.3f}")
