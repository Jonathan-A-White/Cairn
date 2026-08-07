"""Relabeling-invariant comparison of transcriptions via identity partitions.

Two transcriptions may use different symbol names, so only the PARTITION they
induce on the 87 positions is comparable. Position i is 'disputed' between s
and t iff the set of positions sharing i's symbol differs between them.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from collections import Counter

def load_all():
    T={}
    T['consensus']=open(os.path.join('data','consensus.txt')).read().split()
    T['schmeh']=list(open(os.path.join('data','schmeh.txt')).read().strip())
    T['dcode']=list(open(os.path.join('data','dcode.txt')).read().strip())
    rows=[l.split('\t') for l in open(os.path.join('data','transcription.tsv'))
          if not l.startswith('#') and l.strip()]
    T['mine_T0']=[r[3] for r in rows]
    T['_conf']=[r[4] for r in rows]
    return T

def classes(seq):
    d={}
    for i,s in enumerate(seq): d.setdefault(s,set()).add(i)
    return [frozenset(d[s]) for s in seq]

def disputed(a,b):
    ca,cb=classes(a),classes(b)
    return [i for i in range(len(a)) if ca[i]!=cb[i]]

if __name__=='__main__':
    T=load_all(); conf=T.pop('_conf')
    names=list(T)
    print("pairwise disputed-position counts (identity partition):")
    print(f"{'':12s}"+"".join(f"{n:>12s}" for n in names))
    for x in names:
        print(f"{x:12s}"+"".join(f"{len(disputed(T[x],T[y])):12d}" for y in names))
    print()
    d_s=disputed(T['consensus'],T['schmeh'])
    d_d=disputed(T['consensus'],T['dcode'])
    print(f"consensus vs schmeh : {len(d_s)} -> {d_s}")
    print(f"consensus vs dcode  : {len(d_d)} -> {d_d}")
    print(f"dcode list subset of schmeh list? {set(d_d)<=set(d_s)}  "
          f"(overlap {len(set(d_d)&set(d_s))}/{len(d_d)})")
    core=sorted(set(d_d)&set(d_s))
    print(f"core contested positions (both comparisons): {len(core)} -> {core}")
    print()
    d_m=disputed(T['consensus'],T['mine_T0'])
    print(f"MY transcription vs consensus: {len(d_m)}/87 disputed = {len(d_m)/87:.1%}")
    print(f"  positions: {d_m}")
    agree=[i for i in range(87) if i not in set(d_m)]
    print(f"  agreement rate = {len(agree)/87:.1%}")
    print("\n  my disagreement broken down by the confidence I had assigned:")
    for c in 'HML':
        idx=[i for i in range(87) if conf[i]==c]
        bad=[i for i in idx if i in set(d_m)]
        print(f"    conf={c}: {len(bad)}/{len(idx)} disputed ({len(bad)/max(1,len(idx)):.0%})")
    print("\n  how much of my error is ORIENTATION vs ARC COUNT:")
    cons=T['consensus']; mine=T['mine_T0']
    # my labels are '<count><ORIENT>', consensus is '<ORIENT-letter><count>'
    my_k=[m[0] for m in mine]; cons_k=[c[1] for c in cons]
    same_k=sum(1 for a,b in zip(my_k,cons_k) if a==b)
    print(f"    arc count agrees at {same_k}/87 = {same_k/87:.1%} of positions")
