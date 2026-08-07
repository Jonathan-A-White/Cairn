"""Phases 2, 3 and 5 re-run on the published transcriptions."""
import sys, os, math, itertools
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
from collections import Counter
from scipy import stats
import ensemble2, corpus
from phase23 import (ic, entropy, doubles, repeats, kasiski, null_dist, eng_sample,
                     shorthand, mono_encipher, uniform_sym, melody, sukhotin, pct)
from phase5 import tonal_melody, interval_stats

RNG=np.random.default_rng(555)
ROWLEN=[29,31,27]
def rows_of(s):
    o=[];k=0
    for L in ROWLEN: o.append(s[k:k+L]); k+=L
    return o
def arcs(s):   return [x[1] if x[0].isalpha() and len(x)>1 and x[1].isdigit() else '?' for x in s]
def orient(s): return [x[0] for x in s]

def run():
    V=ensemble2.variants(); cons=V['E0_consensus']
    d=corpus.get(); text=d['text']
    print("="*78); print("PHASE 2 — on published transcriptions"); print("="*78)
    nulls={'english_plain': null_dist(lambda: eng_sample(text)),
           'mono_english_20': null_dist(lambda: mono_encipher(eng_sample(text),20)),
           'uniform_20': null_dist(lambda: uniform_sym(20)),
           'melody_24': null_dist(lambda: melody())}
    print(f"\n{'model':18s} {'IC mean':>8s} {'IC sd':>7s} {'H mean':>7s} {'dbl':>5s} {'rep2':>6s}")
    for k,v in nulls.items():
        print(f"{k:18s} {v['ic'].mean():8.4f} {v['ic'].std():7.4f} {v['H'].mean():7.3f} "
              f"{v['dbl'].mean():5.2f} {v['rep2'].mean():6.2f}")
    print(f"\n{'variant':20s} {'k':>3s} {'IC':>7s} {'H':>6s} {'dbl':>4s} {'rep2':>5s} {'rep3':>5s} {'pct(Eng)':>9s} {'pct(unif)':>10s}")
    for nm,s in V.items():
        o=dict(k=len(set(s)), ic=ic(s), H=entropy(s), dbl=doubles(s),
               rep2=sum(len(p)-1 for p in repeats(s,2).values()),
               rep3=sum(len(p)-1 for p in repeats(s,3).values()))
        print(f"{nm:20s} {o['k']:3d} {o['ic']:7.4f} {o['H']:6.3f} {o['dbl']:4d} {o['rep2']:5d} "
              f"{o['rep3']:5d} {pct(nulls['english_plain']['ic'],o['ic']):9.2f} "
              f"{pct(nulls['uniform_20']['ic'],o['ic']):10.2f}")

    print("\nchannels (consensus):")
    for nm,f in (('arc count',arcs),('orientation',orient)):
        c=f(cons)
        print(f"  {nm:12s} distinct={len(set(c))} IC={ic(c):.4f} H={entropy(c):.3f} "
              f"(uniform H={math.log2(len(set(c))):.3f}) doubles={doubles(c)}  dist={dict(Counter(c))}")

    print("\nrepeats (consensus):")
    for k in (2,3,4):
        rp=repeats(cons,k)
        for g,pos in sorted(rp.items(), key=lambda x:-len(x[1])):
            print(f"  {k}-gram {'-'.join(g):18s} x{len(pos)} at {pos} spacings {[b-a for a,b in zip(pos,pos[1:])]}")
    sp=kasiski(cons,2)
    print(f"  bigram spacings: {sorted(sp)}")
    for p in range(2,13):
        print(f"    period {p:2d}: {sum(1 for x in sp if x%p==0)}/{len(sp)}")

    print("\n"+"="*78); print("PHASE 3 — on published transcriptions"); print("="*78)
    print("\n(a) arc-count x orientation independence")
    for nm,s in V.items():
        a=arcs(s); o=orient(s)
        if '?' in a: print(f"  {nm:20s} skipped (masked symbols)"); continue
        av=sorted(set(a)); ov=sorted(set(o))
        tab=np.zeros((len(av),len(ov)))
        for x,y in zip(a,o): tab[av.index(x),ov.index(y)]+=1
        keep=tab.sum(axis=1)>0; tab=tab[keep]
        chi2=stats.chi2_contingency(tab)[0]
        cnt=0; reps=5000
        for _ in range(reps):
            po=o.copy(); RNG.shuffle(po)
            t2=np.zeros_like(tab)
            for x,y in zip(a,po): t2[av.index(x),ov.index(y)]+=1
            try: cnt += (stats.chi2_contingency(t2)[0]>=chi2)
            except Exception: pass
        v=math.sqrt(chi2/(len(s)*(min(tab.shape)-1)))
        print(f"  {nm:20s} chi2={chi2:6.2f} MC_p={cnt/reps:.3f} CramersV={v:.3f}")

    print("\n(b) row drift")
    for nm,s in V.items():
        R=rows_of(s); syms=sorted(set(s))
        tab=np.array([[r.count(x) for x in syms] for r in R], dtype=float)
        chi2=stats.chi2_contingency(tab)[0]
        cnt=0; reps=3000; flat=list(s)
        for _ in range(reps):
            RNG.shuffle(flat)
            t2=np.array([[r.count(x) for x in syms] for r in rows_of(flat)],dtype=float)
            try: cnt+=(stats.chi2_contingency(t2)[0]>=chi2)
            except Exception: pass
        print(f"  {nm:20s} IC/row={[f'{ic(r):.3f}' for r in R]} MC_p={cnt/reps:.3f}")

    print("\n(d) Sukhotin (consensus)")
    vw,syms=sukhotin(cons)
    c=Counter(cons)
    print(f"  called vowels: {vw} ({len(vw)}/{len(syms)}), share of text "
          f"{sum(c[x] for x in vw)/87:.3f} (English 0.38-0.40)")

    print("\n"+"="*78); print("PHASE 5 — music, on published transcriptions"); print("="*78)
    sims=[interval_stats(tonal_melody(87,RNG)) for _ in range(4000)]
    ref={k:(np.mean([x[k] for x in sims]), np.std([x[k] for x in sims])) for k in ('small','mean_abs','rev')}
    print(f"  tonal reference: step<=2={ref['small'][0]:.3f} mean|i|={ref['mean_abs'][0]:.2f} rev={ref['rev'][0]:.3f}")
    LET='ABCDEFGH'
    def zscore(p):
        s=interval_stats(p)
        return sum(abs(s[k]-ref[k][0])/ref[k][1] for k in ref), s
    for nm,s in V.items():
        if any(x[0] not in LET for x in s): continue
        best=(1e9,None)
        for rot in range(8):
            for dirn in (1,-1):
                deg={LET[(dirn*i+rot)%8]:i for i in range(8)}
                for om in itertools.permutations([0,1,2]):
                    try: p=[deg[x[0]]+8*om[int(x[1])-1] for x in s]
                    except Exception: continue
                    z,st=zscore(p)
                    if z<best[0]: best=(z,st)
        nullb=[]
        for _ in range(600):
            t=list(s); RNG.shuffle(t)
            b=1e9
            for rot in range(8):
                for dirn in (1,-1):
                    deg={LET[(dirn*i+rot)%8]:i for i in range(8)}
                    for om in itertools.permutations([0,1,2]):
                        p=[deg[x[0]]+8*om[int(x[1])-1] for x in t]
                        b=min(b,zscore(p)[0])
            nullb.append(b)
        nullb=np.array(nullb)
        print(f"  {nm:20s} best z={best[0]:6.2f} step<=2={best[1]['small']:.3f}  "
              f"null={nullb.mean():.2f}+-{nullb.std():.2f}  p={(nullb<=best[0]).mean():.3f}")
    # dial-adjacency
    print("\n  circular-step test (orientation dial):")
    for nm,s in V.items():
        if any(x[0] not in LET for x in s): continue
        o=[LET.index(x[0]) for x in s]
        dd=np.abs(np.diff(o)); dd=np.minimum(dd,8-dd); obs=dd.mean()
        nl=[]
        for _ in range(4000):
            t=o.copy(); RNG.shuffle(t)
            e=np.abs(np.diff(t)); e=np.minimum(e,8-e); nl.append(e.mean())
        nl=np.array(nl)
        print(f"  {nm:20s} obs={obs:.3f} null={nl.mean():.3f}+-{nl.std():.3f} "
              f"z={(obs-nl.mean())/nl.std():+.2f} p(smaller)={(nl<=obs).mean():.3f}")
if __name__=='__main__':
    run()
