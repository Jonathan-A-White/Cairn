"""Phase 5b — the musically most natural mapping: 8 orientations -> 8 scale degrees
within a single octave, arc count carrying rhythm (and so ignored for pitch)."""
import sys, os, itertools
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
import ensemble
from phase5 import tonal_melody, interval_stats, ORDER

RNG=np.random.default_rng(2024)

def ref_stats(n, reps=4000):
    sims=[interval_stats(tonal_melody(n,RNG)) for _ in range(reps)]
    return {k:(np.mean([s[k] for s in sims]), np.std([s[k] for s in sims]))
            for k in ('small','mean_abs','rev','zero')}

def score(pitches, ref):
    s=interval_stats(pitches)
    z=sum(abs(s[k]-ref[k][0])/ref[k][1] for k in ('small','mean_abs','rev'))
    return z, s

def best_over_mappings(seq, ref):
    best=(1e9,None,None)
    for rot in range(8):
        for d in (1,-1):
            base=[ORDER[(d*i+rot)%8] for i in range(8)]
            deg={o:i for i,o in enumerate(base)}
            p=[deg[x[1:]] for x in seq]
            z,s=score(p,ref)
            if z<best[0]: best=(z,(rot,d),s)
    return best

def run():
    V=ensemble.variants(); seq=V['T0_canonical']; n=len(seq)
    ref=ref_stats(n)
    print("PHASE 5b — pitch from ORIENTATION ONLY (single octave), arcs = rhythm")
    print(f"  tonal reference: step<=2={ref['small'][0]:.3f}+-{ref['small'][1]:.3f}  "
          f"mean|i|={ref['mean_abs'][0]:.2f}+-{ref['mean_abs'][1]:.2f}  "
          f"rev={ref['rev'][0]:.3f}+-{ref['rev'][1]:.3f}")
    z,rd,s=best_over_mappings(seq,ref)
    print(f"  Dorabella best-of-16: z={z:.2f} (rot,dir)={rd}  "
          f"step<=2={s['small']:.3f} mean|i|={s['mean_abs']:.2f} rev={s['rev']:.3f}")
    null=[]
    for _ in range(3000):
        t=list(seq); RNG.shuffle(t)
        null.append(best_over_mappings(t,ref)[0])
    null=np.array(null)
    print(f"  null (shuffled, best-of-16): mean={null.mean():.2f} sd={null.std():.2f} "
          f"5th={np.quantile(null,.05):.2f}")
    print(f"  p = {(null<=z).mean():.3f}")
    # circular-adjacency check: are consecutive orientations near-neighbours on the dial?
    o=[ORDER.index(x[1:]) for x in seq]
    d=np.abs(np.diff(o)); d=np.minimum(d,8-d)
    nullc=[]
    for _ in range(5000):
        t=o.copy(); RNG.shuffle(t)
        dd=np.abs(np.diff(t)); dd=np.minimum(dd,8-dd); nullc.append(dd.mean())
    nullc=np.array(nullc)
    print(f"\n  mean circular step between consecutive orientations = {d.mean():.3f}")
    print(f"  null (shuffled): mean={nullc.mean():.3f} sd={nullc.std():.3f}  "
          f"p(smaller)={(nullc<=d.mean()).mean():.3f}")
    print("  (a melody written on a rotational dial would show SMALL circular steps)")
if __name__=='__main__': run()
