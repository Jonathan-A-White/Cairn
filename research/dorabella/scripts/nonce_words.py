"""Does invented vocabulary explain the gap?

'HYSTERIOUS' (hysterical + mysterious) is evidence Elgar's plaintexts contain
portmanteaus. This simulates that directly: replace a fraction of words with
portmanteaus (prefix of one real word + suffix of another) and measure the
cost, both in plain quadgram score and after enciphering and solving.
"""
import sys, os, re
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
import corpus as C, period_corpus, ensemble2
from solver import solve, norm
from wordfreq import top_n_list, word_frequency

D=C.get(); QUAD=D['quad']
# Frequency-weighted vocabulary, so that the frac=0 baseline reproduces natural
# English (~-4.23). Sampling words uniformly instead drops the baseline to
# -4.56 purely by excluding the commonest short words, which would make the
# whole curve uninterpretable.
_W=[w for w in top_n_list('en',60000) if re.fullmatch(r"[a-z]+",w)]
_F=np.array([word_frequency(w,'en') for w in _W]); _F=_F/_F.sum()
WORDS=[w.upper() for w in _W]
_L=[w.upper() for w in _W if len(w)>=4]      # portmanteau sources: content words
RNG=np.random.default_rng(1234)
N=87

def draw(rng):
    return WORDS[rng.choice(len(WORDS), p=_F)]

def portmanteau(rng):
    a=_L[rng.integers(0,len(_L))]; b=_L[rng.integers(0,len(_L))]
    i=rng.integers(2,max(3,len(a)-1)); j=rng.integers(1,max(2,len(b)-1))
    return a[:i]+b[j:]

def make(frac, rng):
    out=[]
    while sum(len(w) for w in out) < N+20:
        if rng.random()<frac: out.append(portmanteau(rng))
        else: out.append(draw(rng))
    return "".join(out)[:N]

if __name__=='__main__':
    print("="*78); print("INVENTED-VOCABULARY COST"); print("="*78)
    print(f"\n  sample portmanteaus: {[portmanteau(RNG) for _ in range(6)]}\n")
    print(f"{'nonce-word frac':>16s} {'plain':>8s} {'sd':>6s} {'solved':>8s} {'recovery':>9s}")
    for frac in (0.0,0.15,0.3,0.5,0.75,1.0):
        rng=np.random.default_rng(int(frac*100)+11)
        plain=[]; 
        for _ in range(400):
            s=make(frac,rng); plain.append(C.score(s,QUAD,4)/(N-3))
        sol=[];acc=[]
        for _ in range(14):
            pt=make(frac,rng)
            L=sorted(set(pt)); perm=rng.permutation(26)[:len(L)]
            m={c:int(perm[j]) for j,c in enumerate(L)}
            b,got,_,_=solve([m[c] for c in pt],restarts=20,iters=15000,seed=int(rng.integers(1e6)))
            sol.append(norm(b,N)); acc.append(sum(x==y for x,y in zip(got,pt))/N)
        print(f"{frac:16.2f} {np.mean(plain):8.3f} {np.std(plain):6.3f} "
              f"{np.mean(sol):8.3f} {np.mean(acc):9.2f}")
    print("\n  Dorabella (consensus) solved score: -4.680")
