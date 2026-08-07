"""Pre-registered sweep over the ADDITIVE-ROTATION family (Pelling's
'rotating pigpen'), motivated on documentary rather than statistical grounds.

Elgar owned and worked through Schooling's 1896 'Secrets in Cipher' articles
fifteen months before Dorabella, and solved the Nihilist cipher in the fourth
-- a Polybius substitution PLUS an additive keyword layer. The dial analogue is
a substitution whose orientation (and/or arc) channel is shifted by a key that
advances per character.

Hypothesis: ciphertext_i = plaintext_i shifted by (s * i), on the orientation
channel mod 8 and/or the arc channel mod 3. Decryption un-shifts, leaving a
residual monoalphabetic cipher solved with the existing quadgram solver.

The family is enumerated EXHAUSTIVELY. The null runs the identical
best-of-family procedure on shuffled text, so the best-of-24 selection effect
is inside the null. This is pre-registered: the family was fixed before any
score was computed, and is NOT derived from the mirror statistic (which would
be circular, since that statistic was measured on this text).
"""
import sys, os, itertools
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
from compare import load_all
from solver import solve, norm
ORD="ABCDEFGH"
N=87
RESTARTS=20; ITERS=15000
RNG=np.random.default_rng(1896)

def encode(seq):
    o=np.array([ORD.index(s[0]) for s in seq])
    a=np.array([int(s[1])-1 for s in seq])
    return o,a

def unshift(o,a,so,sa):
    i=np.arange(len(o))
    o2=(o - so*i) % 8
    a2=(a - sa*i) % 3
    return [f"{ORD[x]}{y+1}" for x,y in zip(o2,a2)]

FAMILY=[(so,sa) for so in range(8) for sa in range(3)]     # 24, incl. identity

def best_of_family(o,a,seed0, ret_all=False):
    out=[]
    for j,(so,sa) in enumerate(FAMILY):
        s=unshift(o,a,so,sa)
        b,pt,_,_=solve(s,restarts=RESTARTS,iters=ITERS,seed=seed0+j)
        out.append((norm(b,len(o)),so,sa,pt))
    out.sort(key=lambda t:-t[0])
    return out if ret_all else out[0][0]

if __name__=='__main__':
    T=load_all(); cons=T['consensus']
    o,a=encode(cons)
    print("="*78)
    print("ADDITIVE-ROTATION SWEEP (pre-registered; Schooling/Nihilist analogue)")
    print("="*78)
    print(f"\nfamily size: {len(FAMILY)} (orientation step 0-7 mod 8 x arc step 0-2 mod 3)")
    print("identity (0,0) reproduces the plain monoalphabetic result of section 4.\n")
    res=best_of_family(o,a,100,ret_all=True)
    print(f"{'rank':>4s} {'o-step':>7s} {'a-step':>7s} {'score/gram':>11s}   plaintext")
    for r,(sc,so,sa,pt) in enumerate(res[:8],1):
        tag='  <- identity' if (so,sa)==(0,0) else ''
        print(f"{r:4d} {so:7d} {sa:7d} {sc:11.3f}   {pt}{tag}")
    ident=[t for t in res if (t[1],t[2])==(0,0)][0][0]
    print(f"\nidentity (0,0) score: {ident:.3f}   best-of-family: {res[0][0]:.3f}")

    print(f"\nnull: identical best-of-{len(FAMILY)} procedure on shuffled text (14 reps)")
    nulls=[]
    idx=np.arange(N)
    for t in range(14):
        p=RNG.permutation(idx)
        nulls.append(best_of_family(o[p],a[p],20000+t*100))
        print(f"  rep {t+1:2d}: {nulls[-1]:.3f}")
    nulls=np.array(nulls)
    print(f"\n  null mean={nulls.mean():.3f} sd={nulls.std():.3f} max={nulls.max():.3f}")
    print(f"  observed best-of-family={res[0][0]:.3f}")
    print(f"  z={(res[0][0]-nulls.mean())/nulls.std():+.2f}   p={(nulls>=res[0][0]).mean():.3f}")
    print(f"\n  Reference: enciphered real English at n=87 scores about -4.20/gram.")
