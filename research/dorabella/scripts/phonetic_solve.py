"""Experiment 1 — phonetic English, run against PREREG-phonetic.md.

Four pre-registered checks, in the order the pre-registration fixes:

  P1  mechanism strength   phonetic English under the STD model must fall
                           >= 0.20/gram below ordinary English under STD
  P2  adjacency survival   phonetic English must retain >= 80% of ordinary
                           English's mirror-producing bigram mass at the
                           section 11.2 ceiling
  P3  positive control     solver recovery of known enciphered phonetic
                           English at n=87 under the PHON model, >= 0.50
                           mean character accuracy.  GATES P4.
  P4  the test             consensus solved under PHON, against identically
                           procedured nulls and against the phonetic-English
                           band.  Success = z improves by >= 1.0 sd on the
                           -2.88 of section 4.2.

Budget is 20 restarts x 15000 iters everywhere -- observed, null and control --
matching section 4.1/4.2 exactly (standing rule 1).
"""
import sys, os, itertools
sys.path.insert(0, os.path.dirname(__file__))
from collections import Counter
import numpy as np

import corpus, phonetic, ensemble2
import solver
from solver import solve, norm

RESTARTS, ITERS, N = 20, 15000, 87
RNG = np.random.default_rng(31415)
ALPHA24 = "ABCDEFGHIKLMNOPQRSTUWXYZ"

STD = corpus.get()
PHON = phonetic.get()


def banner(s):
    print("\n" + "=" * 78); print(s); print("=" * 78)


def use(model):
    """Point the solver's fitness function at a given quadgram table."""
    solver.QUAD = model['quad']


def windows(text, k, n=N):
    out = []
    for _ in range(k):
        i = int(RNG.integers(0, len(text) - n))
        out.append(text[i:i + n])
    return out


def pergram(s, table):
    return corpus.score(s, table, 4) / (N - 3)


# ---------------------------------------------------------------------------
def p1_mechanism():
    banner("P1 — MECHANISM STRENGTH (threshold: phonetic falls >= 0.20/gram under STD)")
    std_w = windows(STD['text'], 2000)
    phn_w = windows(PHON['text'], 2000)
    a = np.array([pergram(w, STD['quad']) for w in std_w])
    b = np.array([pergram(w, STD['quad']) for w in phn_w])
    drop = a.mean() - b.mean()
    print(f"\n  scored under the STANDARD quadgram model, 87-char windows:")
    print(f"    ordinary English  : {a.mean():.3f} +- {a.std():.3f}")
    print(f"    phonetic English  : {b.mean():.3f} +- {b.std():.3f}")
    print(f"    drop              : {drop:.3f}/gram")
    print(f"    deficit to explain: 0.444/gram  (section 7.3: Dorabella -4.680 vs -4.236)")
    print(f"    fraction of the deficit supplied: {drop/0.444*100:.0f}%")
    ok = drop >= 0.20
    print(f"\n  P1 {'PASS' if ok else 'FAIL'} (threshold 0.20)")
    return ok, drop, a.mean(), b.mean()


# ---------------------------------------------------------------------------
def _mirror_stats(text):
    bg = Counter(zip(text, text[1:])); tot = sum(bg.values())
    mass = {"".join(k): v / tot for k, v in bg.items()}
    def m(x): return mass.get(x, 0.0)
    elgar = sum(m(ALPHA24[i] + ALPHA24[i + 12]) + m(ALPHA24[i + 12] + ALPHA24[i])
                for i in range(12))
    import networkx as nx
    G = nx.Graph()
    for x, y in itertools.combinations(ALPHA24, 2):
        G.add_edge(x, y, weight=m(x + y) + m(y + x))
    M = nx.max_weight_matching(G, maxcardinality=True)
    ceil = sum(m(x + y) + m(y + x) for x, y in M)
    named = " ".join(sorted("".join(sorted(p)) for p in M))
    return elgar, ceil, named, m


def p2_adjacency():
    banner("P2 — ADJACENCY SURVIVAL (threshold: >= 80% of the 11.2 ceiling retained)")
    se, sc, sn, sm = _mirror_stats(STD['text'])
    pe, pc, pn, pm = _mirror_stats(PHON['text'])
    print(f"\n  mirror-producing bigram mass (section 11.2 machinery, 24-letter alphabet):")
    print(f"                              ordinary   phonetic   retained")
    print(f"    under Elgar's 1920 key    {se*100:7.2f}%  {pe*100:8.2f}%   {pe/se*100:6.0f}%")
    print(f"    best possible key (ceil)  {sc*100:7.2f}%  {pc*100:8.2f}%   {pc/sc*100:6.0f}%")
    print(f"    expected pairs / 86 slots {sc*86:7.2f}   {pc*86:8.2f}")
    print(f"\n    optimal matching, ordinary: {sn}")
    print(f"    optimal matching, phonetic: {pn}")
    print(f"\n  the three bigrams the hypothesis says must survive respelling:")
    for b in ('ER', 'AN', 'IN', 'TH', 'RE'):
        print(f"    {b}: ordinary {sm(b)*1000:5.1f} per mille   phonetic {pm(b)*1000:5.1f}"
              f"   retained {pm(b)/sm(b)*100:3.0f}%")
    ok = pc / sc >= 0.80
    print(f"\n  P2 {'PASS' if ok else 'FAIL'} (threshold 80%)")
    return ok, pc / sc


# ---------------------------------------------------------------------------
def _control(text, model, trials):
    """Encipher known plaintext from `text` under a random MASC; solve under `model`."""
    use(model)
    scores, accs = [], []
    for _ in range(trials):
        i = int(RNG.integers(0, len(text) - N)); pt = text[i:i + N]
        L = sorted(set(pt)); perm = RNG.permutation(26)[:len(L)]
        mp = {c: int(perm[j]) for j, c in enumerate(L)}
        b, got, _, _ = solve([mp[c] for c in pt], restarts=RESTARTS, iters=ITERS,
                             seed=int(RNG.integers(1e6)))
        scores.append(norm(b, N))
        accs.append(sum(x == y for x, y in zip(got, pt)) / N)
    return np.array(scores), np.array(accs)


def p3_control():
    banner("P3 — POSITIVE CONTROL (threshold: >= 0.50 recovery; GATES P4)")
    print("\n  Can the solver recover KNOWN enciphered phonetic English at n=87 when")
    print("  its fitness function is the phonetic model?  40 trials, 20x15000.")
    ps, pa = _control(PHON['text'], PHON, 40)
    print(f"\n    phonetic English under PHON : score {ps.mean():.3f} +- {ps.std():.3f}"
          f"   recovery {pa.mean():.2f}  (median {np.median(pa):.2f}, >90%: {(pa>0.9).mean():.2f})")
    print("\n  reference — the same control for ordinary English under the standard")
    print("  model, which is what licensed every interpretation in section 4:")
    ss, sa = _control(STD['text'], STD, 40)
    print(f"    ordinary English under STD  : score {ss.mean():.3f} +- {ss.std():.3f}"
          f"   recovery {sa.mean():.2f}  (section 4.1 reported -4.196 +- 0.168, 0.96)")
    ok = pa.mean() >= 0.50
    print(f"\n  P3 {'PASS' if ok else 'FAIL'} (threshold 0.50 recovery)")
    return ok, ps, pa, ss, sa


# ---------------------------------------------------------------------------
def p4_test(phon_band):
    banner("P4 — THE TEST (threshold: z improves by >= 1.0 sd on -2.88)")
    cons = ensemble2.variants()['E0_consensus']

    use(STD)
    b, pt_std, _, _ = solve(cons, restarts=RESTARTS, iters=ITERS, seed=777)
    std_obs = norm(b, N)
    print(f"\n  sanity, consensus under STD : {std_obs:.3f}  (section 4.2: -4.680)")

    use(PHON)
    b, pt_phon, _, _ = solve(cons, restarts=RESTARTS, iters=ITERS, seed=777)
    obs = norm(b, N)
    print(f"  consensus under PHON        : {obs:.3f}")
    print(f"  best plaintext under PHON   : {pt_phon}")

    print("\n  nulls, identical procedure and budget under the PHON model:")
    sh = []
    for _ in range(60):
        s = list(cons); RNG.shuffle(s)
        sh.append(norm(solve(s, restarts=RESTARTS, iters=ITERS,
                             seed=int(RNG.integers(1e6)))[0], N))
    sh = np.array(sh)
    ur = []
    k = len(set(cons))
    for _ in range(60):
        s = [str(x) for x in RNG.integers(0, k, N)]
        ur.append(norm(solve(s, restarts=RESTARTS, iters=ITERS,
                             seed=int(RNG.integers(1e6)))[0], N))
    ur = np.array(ur)
    allnull = np.concatenate([sh, ur])
    print(f"    shuffled consensus : {sh.mean():.3f} +- {sh.std():.3f}  max {sh.max():.3f}")
    print(f"    uniform random     : {ur.mean():.3f} +- {ur.std():.3f}  max {ur.max():.3f}")
    print(f"    consensus percentile vs null : {(allnull <= obs).mean():.2f}")

    z_phon = (obs - phon_band.mean()) / phon_band.std()
    print(f"\n  the comparison that matters — each text against its OWN model's")
    print(f"  enciphered-English band, in that band's sd units:")
    print(f"    STD  : -4.680 vs -4.196 +- 0.168  ->  z = -2.88   (section 4.2)")
    print(f"    PHON : {obs:.3f} vs {phon_band.mean():.3f} +- {phon_band.std():.3f}"
          f"  ->  z = {z_phon:+.2f}")
    print(f"    change: {z_phon - (-2.88):+.2f} sd")

    # the null-relative check declared in the prereg: did the model just
    # flatter everything?
    lift_obs = obs - std_obs
    lift_null = sh.mean() - (-5.010)          # section 4.1's STD shuffled mean
    print(f"\n  did the model simply flatter everything? (prereg, meaningless-result #1)")
    print(f"    consensus lift STD->PHON       : {lift_obs:+.3f}")
    print(f"    shuffled-null lift STD->PHON   : {lift_null:+.3f}")
    print(f"    net movement against its null  : {lift_obs - lift_null:+.3f}")

    ok = z_phon >= -1.9
    print(f"\n  P4 {'PASS' if ok else 'FAIL'} (threshold z >= -1.9)")
    return ok, obs, z_phon, sh, ur, pt_phon


if __name__ == '__main__':
    print("EXPERIMENT 1 — PHONETIC ENGLISH")
    print("run against PREREG-phonetic.md; thresholds fixed before the corpus was built")
    print(f"STD corpus {len(STD['text'])} chars, PHON corpus {len(PHON['text'])} chars")

    ok1, drop, std_m, phn_m = p1_mechanism()
    ok2, ret = p2_adjacency()
    ok3, ps, pa, ss, sa = p3_control()

    banner("GATE")
    if not ok3:
        print(f"""
  P3 FAILED at {pa.mean():.2f} recovery against a 0.50 threshold.

  Per the pre-registration this is recorded as a SECOND untestable-in-principle
  result, alongside section 13.2's homophonic family: the phonetic family is
  NOT rejected -- the method has no power against it at n=87. P4 is not run and
  no consensus solve under the phonetic model is reported, because an
  uncalibrated solver's output is not interpretable (standing rule 6).
""")
        sys.exit(0)

    ok4, obs, z, sh, ur, pt = p4_test(ps)

    banner("SUMMARY AGAINST THE PRE-REGISTRATION")
    print(f"""
  P1 mechanism strength   {'PASS' if ok1 else 'FAIL'}   phonetic falls {drop:.3f}/gram under STD (>= 0.20)
  P2 adjacency survival   {'PASS' if ok2 else 'FAIL'}   {ret*100:.0f}% of the ceiling retained (>= 80%)
  P3 positive control     {'PASS' if ok3 else 'FAIL'}   {pa.mean():.2f} recovery at n=87 (>= 0.50)
  P4 the test             {'PASS' if ok4 else 'FAIL'}   z = {z:+.2f} against the phonetic band (>= -1.90)
""")
