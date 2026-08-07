"""Period-English reference model from Jane Austen's Letters (Gutenberg #42078).

Epistolary register, ~1800. Held-out split so the language model is never
evaluated on its own training text. Austen alone is far too small for dense
quadgram estimates (26^4 = 457k cells), so the model is a linear interpolation
of Austen counts with the large synthetic-modern corpus acting as a smoothed
prior; the mixing weight is tuned on held-out Austen.
"""
import sys, os, re, pickle
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
import corpus as C

HERE=os.path.dirname(__file__)
RAW=os.path.join(HERE,'..','data','austen_letters.txt')
CACHE=os.path.join(HERE,'..','data','period.pkl')

def clean():
    t=open(RAW, encoding='utf-8', errors='ignore').read()
    # strip Gutenberg boilerplate
    m=re.search(r'\*\*\* ?START OF (THE|THIS) PROJECT GUTENBERG.*?\*\*\*', t, re.S)
    if m: t=t[m.end():]
    m=re.search(r'\*\*\* ?END OF (THE|THIS) PROJECT GUTENBERG', t)
    if m: t=t[:m.start()]
    t=t.upper()
    return "".join(ch for ch in t if ch in C.A)

def build():
    txt=clean()
    n=len(txt); cut=int(n*0.8)
    train, held = txt[:cut], txt[cut:]
    def counts(s, k):
        idx=np.array([C.IDX[c] for c in s], dtype=np.int64)
        arr=np.zeros((26,)*k)
        views=tuple(idx[i:len(idx)-k+1+i] for i in range(k))
        np.add.at(arr, views, 1)
        return arr
    ca=counts(train,4)
    syn=C.get()['text']
    cs=counts(syn[:2_000_000],4)
    pa=ca/ca.sum(); ps=cs/cs.sum()
    best=None
    for lam in [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]:
        p=lam*pa+(1-lam)*ps
        p=np.maximum(p,1e-12)
        lp=np.log10(p)
        s=C.score(held[:200000], lp, 4)/ (200000-3)
        if best is None or s>best[0]: best=(s,lam,lp)
    print(f"  best interpolation weight lambda={best[1]} (held-out {best[0]:.3f}/gram)")
    return dict(train=train, held=held, quad=best[2], lam=best[1])

def get():
    if os.path.exists(CACHE):
        with open(CACHE,'rb') as f: return pickle.load(f)
    d=build()
    with open(CACHE,'wb') as f: pickle.dump(d,f,protocol=4)
    return d

if __name__=='__main__':
    txt=clean()
    print(f"Austen letters: {len(txt)} letters after cleaning")
    print(f"  sample: {txt[3000:3120]}")
    d=get()
    print(f"  train={len(d['train'])} held-out={len(d['held'])}")
