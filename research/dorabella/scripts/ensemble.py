"""Transcription ensemble: canonical reading plus variants over ambiguous glyphs."""
import os, numpy as np
from collections import Counter
HERE=os.path.dirname(__file__)
TSV=os.path.join(HERE,'..','data','transcription.tsv')

def load():
    rows=[]
    for l in open(TSV):
        if l.startswith('#') or not l.strip(): continue
        i,r,c,lab,conf,alts=l.rstrip('\n').split('\t')
        rows.append(dict(i=int(i),row=int(r),col=int(c),lab=lab,conf=conf,
                         alts=[] if alts=='-' else alts.split(',')))
    return rows

ROWLEN=[29,31,27]

def variants():
    rows=load()
    base=[r['lab'] for r in rows]
    V={}
    V['T0_canonical']=list(base)
    # T1/T2: push ambiguous (L) glyphs onto their 1st / 2nd alternative
    for k,pick in [('T1_L_alt1',0),('T2_L_alt2',1)]:
        v=list(base)
        for j,r in enumerate(rows):
            if r['conf']=='L' and len(r['alts'])>pick: v[j]=r['alts'][pick]
        V[k]=v
    # T3: push BOTH L and M glyphs onto their first alternative (maximal perturbation)
    v=list(base)
    for j,r in enumerate(rows):
        if r['conf'] in ('L','M') and r['alts']: v[j]=r['alts'][0]
    V['T3_LM_alt1']=v
    # T4/T5: random draws over the plausible set, seeded
    for seed in (1,2):
        rng=np.random.default_rng(seed); v=list(base)
        for j,r in enumerate(rows):
            if r['conf']=='H' or not r['alts']: continue
            pool=[r['lab']]+r['alts']
            w=[0.6]+[0.4/len(r['alts'])]*len(r['alts']) if r['conf']=='M' else [0.4]+[0.6/len(r['alts'])]*len(r['alts'])
            v[j]=pool[rng.choice(len(pool),p=np.array(w)/sum(w))]
        V[f'T{3+seed}_random{seed}']=v
    return V

def rows_of(seq):
    out=[];k=0
    for L in ROWLEN: out.append(seq[k:k+L]); k+=L
    return out

def arcs(seq):  return [s[0] for s in seq]
def orient(seq):return [s[1:] for s in seq]

if __name__=='__main__':
    V=variants()
    for k,v in V.items():
        c=Counter(v)
        diff=sum(1 for a,b in zip(v,V['T0_canonical']) if a!=b)
        print(f"{k:16s} distinct={len(c):2d}  differs from T0 at {diff:2d}/87 positions")
