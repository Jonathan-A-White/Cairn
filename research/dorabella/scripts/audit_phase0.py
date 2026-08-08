"""Phase 0 audit — re-derive the report's headline numbers from scratch.

Run by a reader with no stake in the report being right. Three checks, chosen
because they are load-bearing and because two of them had no committed script:

  A. The consensus solve of section 4.2 (-4.680 forward, -4.707 reversed),
     re-run at the published budget on a corpus rebuilt from nothing.
  B. The mirror-pair excess of section 11.1 (13 vs 5.15 +- 2.17, p = 0.0018),
     re-derived WITHOUT reusing massey.py: an independent implementation of
     the statistic, a closed-form expectation, and a null drawn with a
     different RNG.
  C. The constructive discrimination of section 11.2 (Elgar's key produces
     6.63% of bigram mass as mirror pairs; the best possible key 12.23%).
     This one was computed inline in Round 6 and never committed, so the
     README's script map has no row for it and "everything is re-runnable"
     was not quite true. It is now.

Check C reproduces the mirror-pair letter set and Elgar's share exactly, and
the optimal matching exactly, but puts the ceiling at 12.19% rather than the
reported 12.23%. The cause of the 0.045pp gap is not recoverable -- the
original was inline -- and it is immaterial: the section's conclusion is that
13 observed against the ceiling's expectation is under 1 sd, which holds at
either value. Recorded rather than silently overwritten.
"""
import sys, os, itertools, random, statistics as st
sys.path.insert(0, os.path.dirname(__file__))
from collections import Counter
import numpy as np

ORD = "ABCDEFGH"
ALPHA24 = "ABCDEFGHIKLMNOPQRSTUWXYZ"          # Elgar's 1920 key, no J, no V
DATA = os.path.join(os.path.dirname(__file__), '..', 'data')


def banner(s):
    print("=" * 78); print(s); print("=" * 78)


# --------------------------------------------------------------------------
# B. mirror-pair excess, implemented independently of massey.py
# --------------------------------------------------------------------------
def is_mirror(a, b):
    """adjacent pair, same arc count, orientations 180 degrees apart"""
    d = abs(ORD.index(a[0]) - ORD.index(b[0]))
    return min(d, 8 - d) == 4 and a[1] == b[1]


def check_mirror(toks):
    banner("B. MIRROR-PAIR EXCESS (report 11.1: 13 vs 5.15 +- 2.17, p = 0.0018)")
    obs = sum(1 for a, b in zip(toks, toks[1:]) if is_mirror(a, b))
    pos = [i for i, (a, b) in enumerate(zip(toks, toks[1:])) if is_mirror(a, b)]
    print(f"\n  observed  = {obs}                     (report: 13)")
    print(f"  positions = {pos}")
    print(f"              (report 17.1: [12, 27, 38, 40, 49, 52, 54, 56, 58, 62, 71, 73, 78])")

    # Closed form. Under a uniformly random ordering of the fixed multiset,
    # E[count] = 86 * P(a given adjacent slot is a mirror pair)
    #          = 86 * (#ordered distinct-position pairs in relation)/(87*86)
    #          = (#ordered pairs)/87.   No simulation involved.
    n = len(toks)
    ordered = sum(1 for i in range(n) for j in range(n)
                  if i != j and is_mirror(toks[i], toks[j]))
    print(f"\n  closed-form E[count] under random ordering = {ordered/n:.4f}   (report: 5.15)")

    # Independent null: stdlib RNG, different seed, 10x massey.py's reps.
    random.seed(20260808)
    v = list(toks); cnt = []
    for _ in range(200_000):
        random.shuffle(v)
        cnt.append(sum(1 for a, b in zip(v, v[1:]) if is_mirror(a, b)))
    m, s = st.mean(cnt), st.pstdev(cnt)
    p = sum(1 for c in cnt if c >= obs) / len(cnt)
    print(f"  independent null (200k perms, stdlib RNG, seed 20260808):")
    print(f"      mean={m:.3f}  sd={s:.3f}  p(null >= {obs}) = {p:.5f}   (report: 0.0018)")
    return obs, p


# --------------------------------------------------------------------------
# C. section 11.2's constructive discrimination
# --------------------------------------------------------------------------
def check_mirror_mass(text):
    banner("C. MIRROR-PRODUCING BIGRAM MASS (report 11.2) — no committed script until now")
    bg = Counter(zip(text, text[1:])); tot = sum(bg.values())
    mass = {"".join(k): v / tot for k, v in bg.items()}
    def m(x): return mass.get(x, 0.0)

    # Under Elgar's key a mirror pair is a letter pair whose ALPHA24 indices
    # differ by 12: same arc count (offset within the group of 3) and
    # orientation groups 4 apart.
    pairs = [(ALPHA24[i], ALPHA24[i + 12]) for i in range(12)]
    print("\n  mirror-producing pairs under Elgar's key:")
    print("     ", " ".join(a + b + " " + b + a for a, b in pairs))
    elgar = sum(m(a + b) + m(b + a) for a, b in pairs)
    print(f"\n  Elgar-key share      = {elgar*100:.3f}%   (report: 6.63%)")
    print(f"  expected pairs / 86  = {elgar*86:.2f}     (report: 5.70)")
    for b in ('ER', 'AN', 'RE'):
        print(f"      {b} = {m(b)*1000:.1f} per mille   (report: ER 16.1, AN 16.0, RE 14.3)")

    # Ceiling: max-weight perfect matching over the 24 letters, edge weight
    # = combined mass of the bigram in both orders.
    import networkx as nx
    G = nx.Graph()
    for a, b in itertools.combinations(ALPHA24, 2):
        G.add_edge(a, b, weight=m(a + b) + m(b + a))
    M = nx.max_weight_matching(G, maxcardinality=True)
    best = sum(m(a + b) + m(b + a) for a, b in M)
    got = " ".join(sorted("".join(sorted(p)) for p in M))
    print(f"\n  best-possible-key share = {best*100:.3f}%   (report: 12.23%)  <-- 0.045pp low")
    print(f"  expected pairs / 86     = {best*86:.2f}     (report: 10.52)")
    print(f"  optimal matching        = {got}")
    print(f"                     report: AL BY CK DW ER FO GQ HT IN MP SU XZ")
    # what the section actually concludes, under the re-derived ceiling
    sd = (86 * best * (1 - best)) ** 0.5
    print(f"\n  13 observed against the ceiling's expectation: "
          f"z = {(13 - best*86)/sd:+.2f}   (report: +0.8 sd, 'entirely unremarkable')")
    print(f"  share needed to expect 13 = {13/86*100:.2f}%   (report: 15.12%)")
    return elgar, best


# --------------------------------------------------------------------------
# A. the consensus solve
# --------------------------------------------------------------------------
def check_solve():
    banner("A. CONSENSUS SOLVE (report 4.2: -4.680 forward, -4.707 reversed)")
    import ensemble2
    from solver import solve, norm
    cons = ensemble2.variants()['E0_consensus']
    # solver3.py's exact call: 20 restarts x 15000 iters, seeds 777 / 778
    b, pt, scores, _ = solve(cons, restarts=20, iters=15000, seed=777)
    br, pr, _, _ = solve(cons[::-1], restarts=20, iters=15000, seed=778)
    print(f"\n  forward  = {norm(b, 87):.3f}   (report: -4.680)")
    print(f"  reversed = {norm(br, 87):.3f}   (report: -4.707)")
    print(f"  plaintext: {pt}")
    print(f"  report   : WPROUTCONGDAYSAMAATPPASIGILDECACTIONFORAARTLYCADATHEYSINNIDERETHERSHBLERATHYELOPLETOSIO")
    return norm(b, 87), norm(br, 87)


if __name__ == '__main__':
    import corpus
    toks = open(os.path.join(DATA, 'consensus.txt')).read().split()
    assert len(toks) == 87
    D = corpus.get()
    print(f"corpus: {len(D['text'])} chars, rebuilt from wordfreq in this environment\n")
    f, r = check_solve()
    print()
    obs, p = check_mirror(toks)
    print()
    elgar, best = check_mirror_mass(D['text'])
    print()
    banner("VERDICT")
    print(f"""
  4.2  consensus solve        {f:.3f} / {r:.3f}   vs -4.680 / -4.707   EXACT
  11.1 mirror pairs           {obs} at p={p:.4f}       vs 13 at p=0.0018    EXACT
  11.2 Elgar-key share        {elgar*100:.2f}%              vs 6.63%             EXACT
  11.2 best-possible ceiling  {best*100:.2f}%             vs 12.23%            LOW BY 0.045pp

  One further discrepancy, found by reading rather than running: section 20.3
  gives mirror-key substitution's mirror-pair z as +0.66 and its solver z as
  -0.88. Those come from different runs -- +0.66 is the four-model run
  (out/discriminate.log), -0.88 the five-model run (out/disc5.log), whose own
  mirror z is +0.91. Section 16.3 quotes the consistent five-model pair.
  20.3 is corrected to +0.91 to match the run it takes its other number from.
  No conclusion depends on which is used.
""")
