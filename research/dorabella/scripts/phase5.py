"""Phase 5 — music hypothesis, and the unicity-distance analysis."""
import sys, os, math, itertools
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
from collections import Counter
import ensemble

RNG=np.random.default_rng(99)
ORDER=['N','NE','E','SE','S','SW','W','NW']       # clockwise from N

# ---------------- reference melodic statistics ----------------
def tonal_melody(n, rng):
    """Stepwise-dominated diatonic melody: the standard first-order model of
    Western tonal melody (Narmour/Huron: small intervals dominate, ~65-70%
    of intervals are <=2 scale steps)."""
    steps=np.array([-7,-5,-4,-3,-2,-1,0,1,2,3,4,5,7])
    w=np.array([.01,.02,.04,.06,.12,.22,.06,.22,.12,.06,.04,.02,.01]); w=w/w.sum()
    d=0; out=[]
    for _ in range(n):
        out.append(d); d+=rng.choice(steps,p=w); d=int(np.clip(d,-14,14))
    return out

def interval_stats(pitches):
    iv=np.diff(np.array(pitches))
    if len(iv)==0: return dict(small=0,zero=0,mean_abs=0,rev=0)
    small=float((np.abs(iv)<=2).mean())
    zero=float((iv==0).mean())
    mean_abs=float(np.abs(iv).mean())
    # contour reversal rate: fraction of direction changes (tonal melody ~0.5-0.6)
    sgn=np.sign(iv); sgn=sgn[sgn!=0]
    rev=float((np.diff(sgn)!=0).mean()) if len(sgn)>1 else 0.0
    return dict(small=small,zero=zero,mean_abs=mean_abs,rev=rev)

def mapping_score(pitches, ref):
    """Distance from reference tonal-melody statistics (lower = more melodic)."""
    s=interval_stats(pitches)
    return ( abs(s['small']-ref['small'])/ref['small_sd']
           + abs(s['mean_abs']-ref['mean_abs'])/ref['mean_abs_sd']
           + abs(s['rev']-ref['rev'])/ref['rev_sd'] ), s

def run():
    print("="*78); print("PHASE 5 — MUSIC HYPOTHESIS"); print("="*78)
    V=ensemble.variants(); seq=V['T0_canonical']; n=len(seq)

    # reference distribution from simulated tonal melodies of length 87
    sims=[interval_stats(tonal_melody(n,RNG)) for _ in range(4000)]
    ref=dict(small=np.mean([s['small'] for s in sims]),  small_sd=np.std([s['small'] for s in sims]),
             mean_abs=np.mean([s['mean_abs'] for s in sims]), mean_abs_sd=np.std([s['mean_abs'] for s in sims]),
             rev=np.mean([s['rev'] for s in sims]),       rev_sd=np.std([s['rev'] for s in sims]))
    print(f"\nSimulated tonal melody (n=87): stepwise<=2 = {ref['small']:.3f}+-{ref['small_sd']:.3f}, "
          f"mean|interval| = {ref['mean_abs']:.2f}+-{ref['mean_abs_sd']:.2f}, "
          f"contour-reversal = {ref['rev']:.3f}+-{ref['rev_sd']:.3f}")

    # Also: a random-order null (same symbols, shuffled) mapped the same way
    print("\nCandidate mappings: orientation -> scale degree, arc count -> octave.")
    print("All 8 rotational offsets x 2 directions x 3 arc-count->octave orders are enumerated;")
    print("each is scored against the tonal-melody reference, and compared with the")
    print("distribution obtained by applying the SAME mapping to shuffled text.\n")

    results=[]
    for rot in range(8):
        for direction in (1,-1):
            base=[ORDER[(direction*i+rot)%8] for i in range(8)]
            deg={o:i for i,o in enumerate(base)}
            for octmap in itertools.permutations([0,1,2]):
                om={str(i+1):octmap[i] for i in range(3)}
                pitches=[deg[s[1:]] + 7*om[s[0]] for s in seq]
                sc,st=mapping_score(pitches,ref)
                results.append((sc,rot,direction,octmap,st))
    results.sort(key=lambda x:x[0])
    print(f"{'rank':>4s} {'score':>6s} {'rot':>3s} {'dir':>4s} {'oct':>9s} {'step<=2':>8s} {'mean|i|':>8s} {'rev':>6s}")
    for r,(sc,rot,di,om,st) in enumerate(results[:6],1):
        print(f"{r:4d} {sc:6.2f} {rot:3d} {di:4d} {str(om):>9s} {st['small']:8.3f} {st['mean_abs']:8.2f} {st['rev']:6.3f}")
    print("  ...")
    for r,(sc,rot,di,om,st) in enumerate(results[-2:],len(results)-1):
        print(f"{r:4d} {sc:6.2f} {rot:3d} {di:4d} {str(om):>9s} {st['small']:8.3f} {st['mean_abs']:8.2f} {st['rev']:6.3f}")

    best=results[0][0]
    # null: best-of-48 score achievable on shuffled text
    nullbest=[]
    for _ in range(2000):
        s=list(seq); RNG.shuffle(s)
        b=1e9
        for rot in range(8):
            for direction in (1,-1):
                base=[ORDER[(direction*i+rot)%8] for i in range(8)]
                deg={o:i for i,o in enumerate(base)}
                for octmap in itertools.permutations([0,1,2]):
                    om={str(i+1):octmap[i] for i in range(3)}
                    p=[deg[x[1:]] + 7*om[x[0]] for x in s]
                    sc,_=mapping_score(p,ref)
                    b=min(b,sc)
        nullbest.append(b)
    nullbest=np.array(nullbest)
    print(f"\nBest-of-48 mapping score: Dorabella = {best:.2f}")
    print(f"  null (same symbols, shuffled order, best-of-48): mean={nullbest.mean():.2f} "
          f"sd={nullbest.std():.2f} 5th pct={np.quantile(nullbest,.05):.2f}")
    print(f"  p-value (fraction of shuffles scoring at least as melodic) = {(nullbest<=best).mean():.3f}")

    # ---------------- unicity distance ----------------
    print("\n"+"="*78); print("UNICITY DISTANCE"); print("="*78)
    H_eng=1.5   # bits/char, Shannon's estimate of the entropy rate of English
    Dred=math.log2(26)-H_eng
    print(f"English entropy rate ~{H_eng} bits/char; redundancy D = log2(26) - {H_eng} = {Dred:.2f} bits/char\n")
    def lg_fact(a,b=1):    # log2(a!/b!)
        return sum(math.log2(i) for i in range(b+1,a+1))
    models=[
        ("simple substitution, 24 symbols -> 26 letters (injective)", lg_fact(26,2)),
        ("simple substitution, bijective on 24 letters",              lg_fact(24)),
        ("homophonic, 24 symbols -> 26 letters (many-to-one)",        24*math.log2(26)),
        ("polyalphabetic, 2 alphabets",                               2*lg_fact(26,2)),
        ("polyalphabetic, 3 alphabets",                               3*lg_fact(26,2)),
    ]
    print(f"{'model':58s} {'H(K) bits':>10s} {'U = H(K)/D':>11s}")
    for nm,hk in models:
        print(f"{nm:58s} {hk:10.1f} {hk/Dred:11.1f}")
    print(f"\nCipher length available: {n} characters.")
    print(f"  -> 87 chars EXCEEDS the ~{lg_fact(26,2)/Dred:.0f}-char unicity distance of simple substitution")
    print("     by roughly 3x. A simple substitution of ordinary English at this length should")
    print("     have a unique solution, and should be well within reach of a quadgram solver.")
    # effective length under abbreviation
    print("\n  Sensitivity: if the plaintext is abbreviated/phonetic/proper-noun-heavy, its")
    print("  redundancy falls. At D = 2.0 bits/char the unicity distance rises to "
          f"{lg_fact(26,2)/2.0:.0f}; at D = 1.0 it rises to {lg_fact(26,2)/1.0:.0f} — i.e. beyond the text.")

if __name__=='__main__':
    run()
