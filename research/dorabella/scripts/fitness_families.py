"""Round 21 — the fitness-family audit. Run against PREREG-fitness.md.

Every headline number in this report is mean quadgram log-probability per gram.
Section 28.2's claim that the deficit "survives re-basing the language model"
was established with a phonetic quadgram model -- still a quadgram model. This
re-scores the frozen results under five other fitness families and asks whether
the deficit is a property of the text or of the estimator.

NO NEW SEARCHES. Every key here was already chosen by quadgram hill-climbing.
solver3.py's runs are regenerated at the same seed and budget purely to recover
the plaintexts the frozen run did not save; reproduction of its published means
(-4.196 / -5.010 / -5.178) is the check that this is the frozen procedure.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from collections import Counter
import numpy as np

import corpus, ensemble2
from solver import solve, norm

RESTARTS, ITERS, N = 20, 15000, 87
A = corpus.A
IDX = corpus.IDX
D = corpus.get()
TEXT = D['text']


def banner(s):
    print("\n" + "=" * 78); print(s); print("=" * 78)


# ---------------------------------------------------------------------------
# n-gram count tables for n = 5, 6, held as sorted int64 codes + counts so the
# 26^6 dense table (2.5 GB) is never built.
# ---------------------------------------------------------------------------
class NGram:
    def __init__(self, text, n):
        self.n = n
        a = np.array([IDX[c] for c in text if c in IDX], dtype=np.int64)
        code = np.zeros(len(a) - n + 1, dtype=np.int64)
        for i in range(n):
            code = code * 26 + a[i:len(a) - n + 1 + i]
        self.keys, cnt = np.unique(code, return_counts=True)
        self.cnt = cnt.astype(np.float64)
        self.total = float(cnt.sum())
        # positive-valued table, AZdecrypt style: unseen -> 0
        self.pos = np.log10(self.cnt + 1.0)
        # log-probability table, this report's style
        self.logp = np.log10(self.cnt / self.total)
        self.floor_logp = np.log10(0.01 / self.total)

    def _codes(self, s):
        a = np.array([IDX[c] for c in s], dtype=np.int64)
        code = np.zeros(len(a) - self.n + 1, dtype=np.int64)
        for i in range(self.n):
            code = code * 26 + a[i:len(a) - self.n + 1 + i]
        return code

    def _lookup(self, s, table, miss):
        code = self._codes(s)
        j = np.searchsorted(self.keys, code)
        j[j >= len(self.keys)] = 0
        hit = self.keys[j] == code
        out = np.full(len(code), miss, dtype=np.float64)
        out[hit] = table[j[hit]]
        return out

    def mean_logp(self, s):
        return float(self._lookup(s, self.logp, self.floor_logp).mean())

    def mean_pos(self, s):
        return float(self._lookup(s, self.pos, 0.0).mean())


def entropy(s):
    c = np.array(list(Counter(s).values()), dtype=np.float64)
    p = c / c.sum()
    return float(-(p * np.log2(p)).sum())


def ioc(s):
    c = np.array(list(Counter(s).values()), dtype=np.float64)
    n = len(s)
    return float((c * (c - 1)).sum() / (n * (n - 1)))


ENG_FREQ = None


def chi2(s):
    c = np.zeros(26)
    for ch in s:
        c[IDX[ch]] += 1
    exp = ENG_FREQ * len(s)
    return float((((c - exp) ** 2) / np.maximum(exp, 1e-9)).sum())


# ---------------------------------------------------------------------------
def regenerate():
    """solver3.py's [A] and [B], reproduced exactly, keeping the plaintexts."""
    rng = np.random.default_rng(4242)          # solver3.py's RNG
    cons = ensemble2.variants()['E0_consensus']
    k = len(set(cons))

    eng = []
    for _ in range(40):
        i = rng.integers(0, len(TEXT) - N); pt = TEXT[i:i + N]
        L = sorted(set(pt)); perm = rng.permutation(26)[:len(L)]
        m = {c: int(perm[j]) for j, c in enumerate(L)}
        b, got, _, _ = solve([m[c] for c in pt], restarts=RESTARTS, iters=ITERS,
                             seed=int(rng.integers(1e6)))
        eng.append((norm(b, N), got))
    sh = []
    for _ in range(60):
        s = list(cons); rng.shuffle(s)
        b, got, _, _ = solve(s, restarts=RESTARTS, iters=ITERS,
                             seed=int(rng.integers(1e6)))
        sh.append((norm(b, N), got))
    ur = []
    for _ in range(60):
        s = [str(x) for x in rng.integers(0, k, N)]
        b, got, _, _ = solve(s, restarts=RESTARTS, iters=ITERS,
                             seed=int(rng.integers(1e6)))
        ur.append((norm(b, N), got))
    return eng, sh, ur, cons


def consensus_seeds(cons, nseed=10):
    """Section 28.4's spread rule: the consensus solve is not a point estimate."""
    out = []
    for s in range(nseed):
        b, got, _, _ = solve(cons, restarts=RESTARTS, iters=ITERS, seed=777 + 1000 * s)
        out.append((norm(b, N), got))
    return out


# ---------------------------------------------------------------------------
def main():
    global ENG_FREQ
    cnt = np.zeros(26)
    for ch in TEXT:
        cnt[IDX[ch]] += 1
    ENG_FREQ = cnt / cnt.sum()

    print("=" * 78)
    print("ROUND 21 — FITNESS-FAMILY AUDIT")
    print("=" * 78)
    print("run against PREREG-fitness.md; thresholds fixed before any table was built")

    print("\nbuilding 5-gram and 6-gram tables (sparse; the dense 26^6 is 2.5 GB)...")
    G5 = NGram(TEXT, 5); G6 = NGram(TEXT, 6)
    print(f"  distinct 5-grams {len(G5.keys):,}   distinct 6-grams {len(G6.keys):,}")

    banner("REGENERATION CHECK — is this the frozen procedure?")
    eng, sh, ur, cons = regenerate()
    e0 = np.array([x[0] for x in eng])
    s0 = np.array([x[0] for x in sh])
    u0 = np.array([x[0] for x in ur])
    print(f"\n  {'band':26s} {'regenerated':>22s}   {'section 4.1 published':>22s}")
    print(f"  {'enciphered real English':26s} {e0.mean():10.3f} +- {e0.std():6.3f}"
          f"   {-4.196:10.3f} +- {0.168:6.3f}")
    print(f"  {'shuffled consensus':26s} {s0.mean():10.3f} +- {s0.std():6.3f}"
          f"   {-5.010:10.3f} +- {0.087:6.3f}")
    print(f"  {'uniform random':26s} {u0.mean():10.3f} +- {u0.std():6.3f}"
          f"   {-5.178:10.3f} +- {0.125:6.3f}")

    banner("SECTION 28.4's SPREAD RULE — the consensus solve is not a point estimate")
    cs = consensus_seeds(cons)
    cq = np.array([x[0] for x in cs])
    print(f"\n  consensus re-solved at 10 seeds, same 20x15000 budget:")
    print(f"    {np.round(cq, 3).tolist()}")
    print(f"    mean {cq.mean():.3f}  sd {cq.std():.3f}"
          f"  min {cq.min():.3f}  max {cq.max():.3f}")
    print(f"    section 4.2 published the single value -4.680")

    # -----------------------------------------------------------------
    families = [
        ("F1 quadgram logprob (frozen)", lambda s: corpus.score(s, D['quad'], 4) / (N - 3)),
        ("F2 5-gram logprob",            lambda s: G5.mean_logp(s)),
        ("F3 6-gram logprob",            lambda s: G6.mean_logp(s)),
        ("F4 5-gram x entropy (AZ)",     lambda s: G5.mean_pos(s) * entropy(s)),
        ("F5 6-gram x entropy (AZ)",     lambda s: G6.mean_pos(s) * entropy(s)),
    ]

    # F6 needs the English band's own IoC / chi2 spread first
    eng_txt = [x[1] for x in eng]
    ioc_m, ioc_s = np.mean([ioc(t) for t in eng_txt]), np.std([ioc(t) for t in eng_txt])
    chi_m, chi_s = np.mean([chi2(t) for t in eng_txt]), np.std([chi2(t) for t in eng_txt])

    def f6_lam(lam):
        def f(s):
            q = corpus.score(s, D['quad'], 4) / (N - 3)
            return (q - lam * abs((ioc(s) - ioc_m) / ioc_s)
                      - lam * abs((chi2(s) - chi_m) / chi_s))
        return f
    families.append(("F6 quadgram + IoC/chi2", f6_lam(0.5)))

    banner("THE AUDIT — the consensus against each family's own English band")
    print(f"\n  IoC/chi2 reference from the English band: IoC {ioc_m:.4f} +- {ioc_s:.4f},"
          f" chi2 {chi_m:.1f} +- {chi_s:.1f}")
    print(f"\n  {'family':30s} {'Eng band':>18s} {'consensus':>20s} {'z':>7s} {'pct null':>9s}")
    rows = []
    for name, fn in families:
        eb = np.array([fn(t) for t in eng_txt])
        nl = np.array([fn(x[1]) for x in sh] + [fn(x[1]) for x in ur])
        ob = np.array([fn(x[1]) for x in cs])          # all 10 seeds
        z = (ob.mean() - eb.mean()) / eb.std()
        zlo = (ob.max() - eb.mean()) / eb.std()        # most favourable seed
        pct = (nl <= ob.mean()).mean()
        rows.append((name, eb, nl, ob, z, zlo, pct))
        print(f"  {name:30s} {eb.mean():9.3f}+-{eb.std():<7.3f}"
              f" {ob.mean():11.3f}+-{ob.std():<7.3f} {z:7.2f} {pct:9.2f}")

    banner("VERDICT AGAINST THE PRE-REGISTRATION")
    f1z = rows[0][4]
    print(f"\n  threshold: |z| >= 2.0 in every one of F2-F6, and none more than")
    print(f"  1.5 sigma from F1's z.\n")
    print(f"  {'family':30s} {'z':>8s} {'best seed':>10s} {'|z|>=2':>8s} {'|dz| vs F1':>11s}")
    ok = True
    for name, eb, nl, ob, z, zlo, pct in rows:
        d = abs(z - f1z)
        good = abs(z) >= 2.0
        if name != rows[0][0]:
            ok &= good and d <= 1.5
        print(f"  {name:30s} {z:8.2f} {zlo:10.2f} {'yes' if good else 'NO':>8s}"
              f" {d:11.2f}")
    zs = np.array([r[4] for r in rows[1:]])
    print(f"\n  between-family spread of z (F2-F6): {zs.min():.2f} to {zs.max():.2f}"
          f"  (range {zs.max()-zs.min():.2f})")
    print(f"  within-family spread from seed alone, F1: "
          f"{(rows[0][3].max()-rows[0][3].min())/rows[0][1].std():.2f} sigma")
    print(f"\n  PRE-REGISTERED PREDICTION {'HOLDS' if ok else 'FAILS'}")

    # -----------------------------------------------------------------
    banner("DIAGNOSTIC 1 — z is a ratio; which part of it moved?")
    print("""
  z = (band mean - consensus) / band sd. A family can lose z by closing the
  GAP (the deficit is estimator-dependent, which is the finding the threshold
  was written to detect) or by inflating the BAND SD (the estimator is just
  noisier, which is a statement about power, not about the text). These are
  different results and the threshold cannot tell them apart. Separated here.
""")
    print(f"  {'family':30s} {'gap':>9s} {'band sd':>9s} {'gap/sd = z':>11s}"
          f" {'normalised deficit':>19s}")
    for name, eb, nl, ob, z, zlo, pct in rows:
        gap = eb.mean() - ob.mean()
        span = eb.mean() - nl.mean()            # English down to meaningless
        print(f"  {name:30s} {gap:9.3f} {eb.std():9.3f} {z:11.2f} {gap/span*100:18.0f}%")
    print("""
  'normalised deficit' = how far the consensus falls from that family's English
  band towards its own meaningless-text null, as a percentage of that span. It
  is scale-free and does not divide by the band sd, so it is the statistic that
  survives a change of estimator. This is the number to read across families.
""")

    # -----------------------------------------------------------------
    banner("DIAGNOSTIC 2 — F6 has a free parameter I chose; how much does it matter?")
    print("""
  F6's penalty weight lambda was set to 0.5 by me, with no principle behind it.
  If z moves materially with lambda then F6 is not a well-specified family and
  its failure is a fact about my parameterisation, not about the deficit.
""")
    print(f"  {'lambda':>8s} {'Eng band':>18s} {'consensus':>18s} {'z':>8s}"
          f" {'norm deficit':>13s}")
    for lam in (0.0, 0.1, 0.25, 0.5, 1.0, 2.0):
        fn = f6_lam(lam)
        eb = np.array([fn(t) for t in eng_txt])
        nl = np.array([fn(x[1]) for x in sh] + [fn(x[1]) for x in ur])
        ob = np.array([fn(x[1]) for x in cs])
        z = (ob.mean() - eb.mean()) / eb.std()
        nd = (eb.mean() - ob.mean()) / (eb.mean() - nl.mean())
        print(f"  {lam:8.2f} {eb.mean():10.3f}+-{eb.std():<6.3f}"
              f" {ob.mean():10.3f}+-{ob.std():<6.3f} {z:8.2f} {nd*100:12.0f}%")

    # save the recovered plaintexts so any re-analysis is free
    np.savez(os.path.join(os.path.dirname(__file__), '..', 'out', 'fitness_texts.npz'),
             eng=np.array(eng_txt), sh=np.array([x[1] for x in sh]),
             ur=np.array([x[1] for x in ur]), cons=np.array([x[1] for x in cs]),
             cons_q=cq)
    return rows


if __name__ == '__main__':
    main()
