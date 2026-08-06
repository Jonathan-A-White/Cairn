"""Phase 2 (statistical characterisation) and Phase 3 (structural hypotheses)."""
import sys, os, json, math
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
from collections import Counter, defaultdict
from scipy import stats
import ensemble, corpus

RNG = np.random.default_rng(12345)
N = 87

# ---------- core statistics ----------
def ic(seq):
    n=len(seq); c=Counter(seq)
    if n<2: return float('nan')
    return sum(v*(v-1) for v in c.values())/(n*(n-1))

def entropy(seq):
    n=len(seq); c=Counter(seq)
    p=np.array([v/n for v in c.values()])
    return float(-(p*np.log2(p)).sum())

def doubles(seq):
    return sum(1 for a,b in zip(seq,seq[1:]) if a==b)

def repeats(seq, k):
    d=defaultdict(list)
    for i in range(len(seq)-k+1):
        d[tuple(seq[i:i+k])].append(i)
    return {g:pos for g,pos in d.items() if len(pos)>1}

def kasiski(seq, k=2):
    sp=[]
    for g,pos in repeats(seq,k).items():
        for a,b in zip(pos,pos[1:]): sp.append(b-a)
        if len(pos)>2: sp += [pos[-1]-pos[0]]
    return sp

# ---------- null generators (all length-87 sequences) ----------
def eng_sample(text, n=N):
    i=RNG.integers(0,len(text)-n); return list(text[i:i+n])

VOW=set('AEIOU')
def shorthand(s):
    """Crude phonetic/abbreviated English: drop most non-initial vowels."""
    out=[]
    for j,ch in enumerate(s):
        if ch in VOW and j>0 and RNG.random()<0.65: continue
        out.append(ch)
    return out

def mono_encipher(s, k=24):
    """Monoalphabetic map of 26 letters onto k symbols (surjective, 26-k merges)."""
    tgt=list(range(k))+list(RNG.integers(0,k,26-k))
    RNG.shuffle(tgt)
    m={c:tgt[i] for i,c in enumerate(corpus.A)}
    return [m[c] for c in s]

def uniform_sym(k, n=N):
    return list(RNG.integers(0,k,n))

def melody(n=N, ndeg=8, noct=3):
    """Diatonic melody as (degree, octave) pairs -> up to 24 symbols.
    Random walk with step-wise motion strongly favoured (as in tonal melody)."""
    steps=np.array([-4,-3,-2,-1,1,2,3,4]); w=np.array([.04,.07,.14,.25,.25,.14,.07,.04])
    d=RNG.integers(0,ndeg); o=noct//2; out=[]
    for _ in range(n):
        out.append(d + ndeg*o)
        d += RNG.choice(steps,p=w)
        while d<0: d+=ndeg; o-=1
        while d>=ndeg: d-=ndeg; o+=1
        o=int(np.clip(o,0,noct-1))
    return out

def null_dist(gen, reps=4000):
    I=[];H=[];D=[];R2=[]
    for _ in range(reps):
        s=gen()
        if len(s)<10: continue
        I.append(ic(s)); H.append(entropy(s)); D.append(doubles(s))
        R2.append(sum(len(p)-1 for p in repeats(s,2).values()))
    return dict(ic=np.array(I), H=np.array(H), dbl=np.array(D), rep2=np.array(R2))

def pct(arr, v):
    return float((arr<=v).mean())

# ---------- Sukhotin ----------
def sukhotin(seq):
    syms=sorted(set(seq)); idx={s:i for i,s in enumerate(syms)}; k=len(syms)
    M=np.zeros((k,k))
    for a,b in zip(seq,seq[1:]):
        if a==b: continue
        M[idx[a],idx[b]]+=1; M[idx[b],idx[a]]+=1
    rem=set(range(k)); vowels=set()
    row=M.sum(axis=1).copy()
    while True:
        cand=[i for i in rem if row[i]>0]
        if not cand: break
        i=max(cand,key=lambda j:row[j])
        if row[i]<=0: break
        vowels.add(i); rem.discard(i)
        for j in list(rem): row[j]-=2*M[i,j]
    return [syms[i] for i in sorted(vowels)], syms

# ---------- main ----------
def analyse():
    d=corpus.get(); text=d['text']
    V=ensemble.variants()
    print("="*78); print("PHASE 2 — STATISTICAL CHARACTERISATION"); print("="*78)

    # null distributions
    nulls={
      'english_plain'     : null_dist(lambda: eng_sample(text)),
      'english_shorthand' : null_dist(lambda: shorthand(eng_sample(text,140))[:N]),
      'mono_english_24'   : null_dist(lambda: mono_encipher(eng_sample(text))),
      'uniform_24'        : null_dist(lambda: uniform_sym(24)),
      'uniform_18'        : null_dist(lambda: uniform_sym(18)),
      'melody_24'         : null_dist(lambda: melody()),
    }
    print(f"\nNull distributions at n={N} (4000 reps each)")
    print(f"{'model':20s} {'IC mean':>8s} {'IC sd':>7s} {'IC 5-95%':>16s} {'H mean':>7s} {'H sd':>6s} {'dbl':>5s} {'rep2':>5s}")
    for k,v in nulls.items():
        print(f"{k:20s} {v['ic'].mean():8.4f} {v['ic'].std():7.4f} "
              f"[{np.quantile(v['ic'],.05):.4f},{np.quantile(v['ic'],.95):.4f}] "
              f"{v['H'].mean():7.3f} {v['H'].std():6.3f} {v['dbl'].mean():5.2f} {v['rep2'].mean():5.2f}")

    print(f"\nObserved, per transcription variant:")
    print(f"{'variant':16s} {'k':>3s} {'IC':>7s} {'H':>6s} {'dbl':>4s} {'rep2':>5s} {'rep3':>5s}  percentile of IC vs each null")
    obs={}
    for name,seq in V.items():
        o=dict(k=len(set(seq)), ic=ic(seq), H=entropy(seq), dbl=doubles(seq),
               rep2=sum(len(p)-1 for p in repeats(seq,2).values()),
               rep3=sum(len(p)-1 for p in repeats(seq,3).values()))
        obs[name]=o
        ps=" ".join(f"{m.split('_')[0][:4]}={pct(nulls[m]['ic'],o['ic']):.2f}" for m in nulls)
        print(f"{name:16s} {o['k']:3d} {o['ic']:7.4f} {o['H']:6.3f} {o['dbl']:4d} {o['rep2']:5d} {o['rep3']:5d}  {ps}")

    # channel decomposition on canonical
    seq=V['T0_canonical']
    for chan,f in [('arc-count',ensemble.arcs),('orientation',ensemble.orient)]:
        s=f(seq)
        print(f"\n{chan} channel: distinct={len(set(s))} IC={ic(s):.4f} H={entropy(s):.3f} "
              f"doubles={doubles(s)} (uniform H would be {math.log2(len(set(s))):.3f})")

    print("\nRepeated bigrams/trigrams (canonical T0):")
    for k in (2,3):
        rp=repeats(seq,k)
        if rp:
            for g,pos in sorted(rp.items(), key=lambda x:-len(x[1])):
                print(f"  {k}-gram {'-'.join(g):20s} x{len(pos)} at {pos} spacings {[b-a for a,b in zip(pos,pos[1:])]}")
    sp=kasiski(seq,2)
    print(f"  Kasiski bigram spacings: {sorted(sp)}")
    if sp:
        from math import gcd
        from functools import reduce
        print(f"  gcd of spacings: {reduce(gcd,sp)}")
        for p in range(2,13):
            hits=sum(1 for s_ in sp if s_%p==0)
            print(f"    period {p:2d}: {hits}/{len(sp)} spacings divisible")

    print("\n"+"="*78); print("PHASE 3 — STRUCTURAL HYPOTHESES"); print("="*78)
    # independence of arc count and orientation
    print("\n(a) Are arc-count and orientation independent?")
    for name,seq in V.items():
        a=ensemble.arcs(seq); o=ensemble.orient(seq)
        av=sorted(set(a)); ov=sorted(set(o))
        tab=np.zeros((len(av),len(ov)))
        for x,y in zip(a,o): tab[av.index(x),ov.index(y)]+=1
        chi2,p,dof,exp=stats.chi2_contingency(tab)
        cv=math.sqrt(chi2/(len(seq)*(min(tab.shape)-1)))
        low=(exp<5).mean()
        # Monte-Carlo p (expected counts are small, so asymptotic chi2 is unreliable)
        cnt=0; reps=5000
        for _ in range(reps):
            pa=np.array(a.copy()); po=np.array(o.copy()); RNG.shuffle(po)
            t2=np.zeros_like(tab)
            for x,y in zip(pa,po): t2[av.index(x),ov.index(y)]+=1
            c2=stats.chi2_contingency(t2)[0] if t2.sum(axis=0).all() and t2.sum(axis=1).all() else 0
            cnt += (c2>=chi2)
        print(f"  {name:16s} chi2={chi2:7.2f} dof={dof:3d} asymp_p={p:.3f} MC_p={cnt/reps:.3f} "
              f"CramersV={cv:.3f} frac_exp<5={low:.2f}")

    print("\n(b) Row-by-row drift (is the message homogeneous?)")
    for name,seq in V.items():
        R=ensemble.rows_of(seq)
        ics=[ic(r) for r in R]; Hs=[entropy(r) for r in R]
        syms=sorted(set(seq))
        tab=np.array([[r.count(s) for s in syms] for r in R])
        chi2,p,dof,exp=stats.chi2_contingency(tab+0.0) if tab.sum() else (0,1,0,None)
        # MC p-value by permuting positions across rows
        cnt=0; reps=3000
        flat=list(seq)
        for _ in range(reps):
            RNG.shuffle(flat)
            R2=ensemble.rows_of(flat)
            t2=np.array([[r.count(s) for s in syms] for r in R2])
            try: c2=stats.chi2_contingency(t2+0.0)[0]
            except Exception: c2=0
            cnt += (c2>=chi2)
        print(f"  {name:16s} IC/row={[f'{x:.3f}' for x in ics]} H/row={[f'{x:.2f}' for x in Hs]} "
              f"chi2={chi2:.1f} MC_p={cnt/reps:.3f}")

    print("\n(c) Reversal — which statistics can even detect it?")
    s=V['T0_canonical']; r=s[::-1]
    print(f"  IC fwd={ic(s):.4f} rev={ic(r):.4f} | H fwd={entropy(s):.3f} rev={entropy(r):.3f} "
          f"| doubles fwd={doubles(s)} rev={doubles(r)}")
    print("  -> IC, entropy, unigram freqs and doubled-symbol counts are exactly reversal-invariant;")
    print("     only directional (n-gram / solver) evidence can bear on the 'reads backwards' claim.")

    print("\n(d) Sukhotin vowel separation (canonical T0)")
    v,syms=sukhotin(V['T0_canonical'])
    print(f"  symbols: {syms}")
    print(f"  classified VOWEL: {v}  ({len(v)}/{len(syms)})")
    cnt=Counter(V['T0_canonical'])
    print(f"  vowel-class share of text: {sum(cnt[x] for x in v)/N:.3f} (English letters ~0.38-0.40)")
    # calibrate: run Sukhotin on enciphered English of same length
    hits=[]
    for _ in range(500):
        s87=eng_sample(text)
        vv,_=sukhotin(s87)
        true=set('AEIOU')
        tp=len(set(vv)&true); fp=len(set(vv)-true)
        hits.append((tp,fp,len(vv)))
    hits=np.array(hits)
    print(f"  calibration on plain English n=87: mean {hits[:,0].mean():.1f} true vowels + "
          f"{hits[:,1].mean():.1f} false, of {hits[:,2].mean():.1f} called "
          f"-> precision {hits[:,0].sum()/hits[:,2].sum():.2f}")
    return obs, nulls

if __name__=='__main__':
    analyse()
