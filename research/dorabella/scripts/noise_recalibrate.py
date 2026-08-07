"""Recalibrated corruption control.

Now that inter-transcriber disagreement is measured (2.3% consensus-vs-dCode,
9.2% consensus-vs-Schmeh, 11.5% Schmeh-vs-dCode), the corruption sweep is
re-run densely across THAT range rather than across my own error rate. The
question this answers: if Dorabella really were a simple substitution of
ordinary English, how well should the published transcriptions solve it?
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
import corpus
from solver import solve, norm
D=corpus.get(); TEXT=D['text']
RESTARTS=20; ITERS=15000; N=87

def trial(rate, rng):
    i=rng.integers(0,len(TEXT)-N); pt=TEXT[i:i+N]
    L=sorted(set(pt)); k=len(L); perm=rng.permutation(26)[:k]
    m={c:int(perm[j]) for j,c in enumerate(L)}
    ct=np.array([m[c] for c in pt])
    vals=sorted(set(ct.tolist())); m=len(vals)
    ring=[vals[i] for i in rng.permutation(m)]
    nb={ring[j]:(ring[(j-1)%m], ring[(j+1)%m]) for j in range(m)}
    ct2=ct.copy()
    for p in np.flatnonzero(rng.random(N)<rate):
        a,b=nb[int(ct[p])]; ct2[p]= a if rng.random()<.5 else b
    best,got,_,_=solve(ct2.tolist(), restarts=RESTARTS, iters=ITERS, seed=int(rng.integers(1e6)))
    return norm(best,N), sum(x==y for x,y in zip(got,pt))/N

if __name__=='__main__':
    print("recalibrated corruption sweep over the measured inter-transcriber range")
    print(f"{'rate':>6s} {'score/gram':>11s} {'sd':>6s} {'acc':>6s} {'frac>90%':>9s}  note")
    notes={0.023:'consensus vs dCode', 0.092:'consensus vs Schmeh',
           0.115:'Schmeh vs dCode', 0.184:'my image transcription'}
    for rate in [0.0,0.023,0.05,0.092,0.115,0.15,0.184,0.25]:
        rng=np.random.default_rng(int(rate*10000)+3)
        r=[trial(rate,rng) for _ in range(30)]
        s=np.array([x[0] for x in r]); a=np.array([x[1] for x in r])
        print(f"{rate:6.3f} {s.mean():11.3f} {s.std():6.3f} {a.mean():6.2f} {(a>0.9).mean():9.2f}  {notes.get(rate,'')}")
