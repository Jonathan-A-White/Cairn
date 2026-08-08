"""Experiment 4 — the FULL columnar sweep: all 46,232 column orderings.

Section 16.2 tested 21 permutations (columnar k=2-8 with identity and reversed
column orders, plus route variants) and flagged the gap inline: a complete
sweep is all k! column orderings, 46,232 for k <= 8. Section 22 carries it as a
limitation and section 20.1's family ledger is the only row in that table
reading "not exhausted". This closes it.

  sum_{k=2..8} k!  =  2 + 6 + 24 + 120 + 720 + 5040 + 40320  =  46,232

Procedure follows section 12.3's precedent for a sweep too large to solve at
full budget everywhere: a cheap scan over the whole family, then the top
candidates re-solved at section 16.2's budget. The null runs the IDENTICAL
two-stage procedure on shuffled text, so the 46,232-fold selection sits inside
the null (standing rule 2) -- which is the entire point, since a family this
large will find something on noise alone.
"""
import sys, os, itertools, time
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
from multiprocessing import Pool

import corpus
from compare import load_all
from solver import solve, norm

N = 87
SCAN_R, SCAN_I = 1, 2500          # stage 1, whole family
FULL_R, FULL_I = 8, 9000          # stage 2, matches section 16.2
TOP = 25
NULL_REPS = 5
KMAX = 8
RNG = np.random.default_rng(1897)


def columnar(n, k, order):
    """indices read out column-by-column from a k-column row-wise fill"""
    rows = (n + k - 1) // k
    idx = []
    for c in order:
        for r in range(rows):
            p = r * k + c
            if p < n:
                idx.append(p)
    return idx


def all_orderings(kmax=KMAX):
    """every column ordering for every k -- the complete family"""
    fam = []
    for k in range(2, kmax + 1):
        for order in itertools.permutations(range(k)):
            fam.append((k, order))
    return fam


FAMILY = all_orderings()
PERMS = [columnar(N, k, o) for k, o in FAMILY]


def _scan_chunk(args):
    seq, lo, hi, seed0 = args
    out = []
    for j in range(lo, hi):
        s = [seq[i] for i in PERMS[j]]
        b, _, _, _ = solve(s, restarts=SCAN_R, iters=SCAN_I, seed=seed0 + j)
        out.append(norm(b, len(seq)))
    return lo, out


def sweep(seq, seed0, pool, nchunk=64):
    """stage 1 over the whole family, then stage 2 on the top TOP"""
    n = len(PERMS)
    edges = np.linspace(0, n, nchunk + 1).astype(int)
    args = [(seq, int(a), int(b), seed0) for a, b in zip(edges, edges[1:])]
    scores = np.empty(n)
    for lo, vals in pool.imap_unordered(_scan_chunk, args):
        scores[lo:lo + len(vals)] = vals
    best_idx = np.argsort(-scores)[:TOP]
    refined = []
    for j in best_idx:
        s = [seq[i] for i in PERMS[j]]
        b, pt, _, _ = solve(s, restarts=FULL_R, iters=FULL_I, seed=seed0 + 7 * int(j))
        refined.append((norm(b, len(seq)), int(j), pt))
    refined.sort(key=lambda t: -t[0])
    return refined, scores


def identity_score(seq, seed0):
    b, pt, _, _ = solve(list(seq), restarts=FULL_R, iters=FULL_I, seed=seed0)
    return norm(b, len(seq)), pt


if __name__ == '__main__':
    cons = load_all()['consensus']
    print("=" * 78)
    print("FULL COLUMNAR SWEEP — ALL 46,232 COLUMN ORDERINGS")
    print("=" * 78)
    print(f"\nfamily: sum k! for k=2..{KMAX} = {len(FAMILY)} orderings"
          f"   (section 16.2 tested 21)")
    print(f"stage 1 scan {SCAN_R}x{SCAN_I} over the whole family;"
          f" stage 2 {FULL_R}x{FULL_I} on the top {TOP}")
    print(f"null: the IDENTICAL two-stage procedure on shuffled text,"
          f" {NULL_REPS} reps\n")

    t0 = time.time()
    with Pool(4) as pool:
        res, scores = sweep(cons, 500, pool)
        print(f"  scan complete in {time.time()-t0:.0f}s")
        ident, ipt = identity_score(cons, 4242)
        print(f"\n  identity (no transposition), {FULL_R}x{FULL_I}: {ident:.3f}")
        print(f"    {ipt}")
        print(f"\n  scan distribution over all {len(FAMILY)} orderings:")
        print(f"    mean {scores.mean():.3f}  sd {scores.std():.3f}"
              f"  max {scores.max():.3f}  min {scores.min():.3f}")
        print(f"\n  top {min(10, TOP)} after full-budget re-solve:")
        print(f"  {'rank':>4s} {'k':>3s} {'column order':>22s} {'score':>8s}   plaintext")
        for r, (sc, j, pt) in enumerate(res[:10], 1):
            k, o = FAMILY[j]
            print(f"  {r:4d} {k:3d} {str(o):>22s} {sc:8.3f}   {pt}")

        best = res[0][0]
        print(f"\n  best of family : {best:.3f}"
              f"   (section 16.2's best of 21: -4.759)")
        print(f"  gain over identity: {best - ident:+.3f}")

        print(f"\n  null — identical two-stage best-of-{len(FAMILY)} on shuffled text:")
        nulls = []
        for t in range(NULL_REPS):
            s = list(cons); RNG.shuffle(s)
            nres, _ = sweep(s, 9000 + 137 * t, pool)
            nulls.append(nres[0][0])
            print(f"    rep {t+1}: {nulls[-1]:.3f}", flush=True)
    nulls = np.array(nulls)
    print(f"\n    null mean={nulls.mean():.3f} sd={nulls.std():.3f} max={nulls.max():.3f}")
    z = (best - nulls.mean()) / nulls.std()
    print(f"    observed={best:.3f}  z={z:+.2f}  p={(nulls >= best).mean():.3f}")
    print(f"""
  Read this the way section 16.2 read its own z: the margin is carried by the
  identity member, which section 4 already established beats meaningless text.
  The quantity that speaks to transposition is the gain OVER identity,
  {best - ident:+.3f}, taken from {len(FAMILY)} tries.

  Reference: enciphered real English at n=87 is about -4.20/gram.
  Total runtime {time.time()-t0:.0f}s.
""")
