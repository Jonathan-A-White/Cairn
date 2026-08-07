"""How much of the Dorabella gap does period register / idiolect explain?

Clean design: hold the LANGUAGE MODEL fixed (the modern synthetic corpus) and
vary only the plaintext register. Any difference between the bands is a
property of the text, not of the model. Training a model on Austen and testing
on held-out Austen would inflate the period band through same-author phrase
overlap (-1.357/gram, vs -4.2 for genuinely unseen text), so that route is
avoided entirely.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
import corpus as C, period_corpus, ensemble2
from solver import solve, norm

D=C.get(); MODERN=D['text']; QUAD=D['quad']
AUST=period_corpus.clean()
RESTARTS=20; ITERS=15000; N=87
RNG=np.random.default_rng(808)

def band(text, reps, label, quad=QUAD):
    sc=[]; acc=[]; raw=[]
    for _ in range(reps):
        i=RNG.integers(0,len(text)-N); pt=text[i:i+N]
        raw.append(C.score(pt,quad,4)/(N-3))
        L=sorted(set(pt)); perm=RNG.permutation(26)[:len(L)]
        m={c:int(perm[j]) for j,c in enumerate(L)}
        b,got,_,_=solve([m[c] for c in pt], restarts=RESTARTS, iters=ITERS,
                        seed=int(RNG.integers(1e6)))
        sc.append(norm(b,N)); acc.append(sum(x==y for x,y in zip(got,pt))/N)
    sc=np.array(sc); acc=np.array(acc); raw=np.array(raw)
    print(f"  {label:34s} plain={raw.mean():.3f}+-{raw.std():.3f}  "
          f"solved={sc.mean():.3f}+-{sc.std():.3f}  recovery={acc.mean():.2f}")
    return sc, raw

if __name__=='__main__':
    print("="*78)
    print("REGISTER COST — same model, different plaintext register")
    print("="*78)
    print("\nAll scored/solved under the unchanged modern quadgram model:")
    m_sc,m_raw = band(MODERN, 40, "modern English (synthetic)")
    a_sc,a_raw = band(AUST,   40, "Austen letters, 1800s epistolary")
    print(f"\n  register cost, plain text : {a_raw.mean()-m_raw.mean():+.3f}/gram")
    print(f"  register cost, after solve: {a_sc.mean()-m_sc.mean():+.3f}/gram")
    cons=ensemble2.variants()['E0_consensus']
    b,_,_,_=solve(cons, restarts=RESTARTS, iters=ITERS, seed=5150)
    obs=norm(b,N)
    gap=obs-m_sc.mean()
    reg=a_sc.mean()-m_sc.mean()
    print(f"\n  Dorabella (consensus)     : {obs:.3f}")
    print(f"  gap to modern English     : {gap:+.3f}")
    print(f"  explained by register      : {reg:+.3f}  ({100*reg/gap:.0f}% of the gap)" if gap<0 else "")
    print(f"  z of Dorabella vs Austen band: {(obs-a_sc.mean())/a_sc.std():+.2f}")
