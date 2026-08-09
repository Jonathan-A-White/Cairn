"""Round 22 — the local / short-scale transposition family. Run against
PREREG-local.md.

Section 20.3 named this family and never ran it: "a transposition confined to a
scale shorter than the adjacency window, which would preserve local pairs while
disrupting longer n-grams. That last is untested and is the most obviously
missing member of the model set."

Section 27 exhausted the COLUMNAR family, which is long-range. This is its
complement: 9,129 distinct permutations, every one with maximum displacement
<= 5, so bigram adjacency largely survives while any quadgram spanning a block
boundary is destroyed.

Procedure is section 27's, unchanged: cheap scan over the whole family, top 25
re-solved at section 16.2's budget, and the null runs the IDENTICAL two-stage
best-of-9,129 on shuffled text so the selection sits inside it.
"""
import sys, os, itertools, time
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
from multiprocessing import Pool

import corpus
from compare import load_all
from solver import solve, norm

N = 87
LINES = [(0, 29), (29, 60), (60, 87)]
SCAN_R, SCAN_I = 1, 2500          # stage 1, matches section 27
FULL_R, FULL_I = 8, 9000          # stage 2, matches section 16.2
TOP = 25
NULL_REPS = 5
IDENT_SEEDS = 10                  # section 28.4's spread rule
RNG = np.random.default_rng(1897)


def block_perm(n, w, pi, off, segs=None):
    """apply pi to every consecutive block of w starting at `off`;
    segs restricts the blocking to given spans (the three lines)."""
    idx = list(range(n))
    out = idx[:]
    for (a, b) in ([(0, n)] if segs is None else segs):
        s = a + off
        while s + w <= b:
            blk = idx[s:s + w]
            for j, p in enumerate(pi):
                out[s + j] = blk[p]
            s += w
    return tuple(out)


def build_family():
    """PREREG-local.md's three components, deduplicated by index permutation."""
    seen = {}
    def add(perm, label):
        if perm not in seen:
            seen[perm] = label
    # 1 & 2: block-periodic, whole-text and per-line
    for w in range(2, 7):
        for pi in itertools.permutations(range(w)):
            for off in range(w):
                for segs, tag in ((None, 'all'), (LINES, 'line')):
                    add(block_perm(N, w, pi, off, segs), f"w{w} {pi} off{off} {tag}")
    # 3: strictly-local single adjacent swaps at w = 7, 8
    for w in (7, 8):
        for i in range(w - 1):
            pi = list(range(w)); pi[i], pi[i + 1] = pi[i + 1], pi[i]
            for off in range(w):
                for segs, tag in ((None, 'all'), (LINES, 'line')):
                    add(block_perm(N, w, tuple(pi), off, segs),
                        f"w{w} swap({i},{i+1}) off{off} {tag}")
    perms = list(seen.keys())
    return perms, [seen[p] for p in perms]


PERMS, LABELS = build_family()
IDENTITY = tuple(range(N))
IDENT_J = PERMS.index(IDENTITY)


def _scan_chunk(args):
    seq, lo, hi, seed0 = args
    out = []
    for j in range(lo, hi):
        s = [seq[i] for i in PERMS[j]]
        b, _, _, _ = solve(s, restarts=SCAN_R, iters=SCAN_I, seed=seed0 + j)
        out.append(norm(b, len(seq)))
    return lo, out


def sweep(seq, seed0, pool, nchunk=64):
    n = len(PERMS)
    edges = np.linspace(0, n, nchunk + 1).astype(int)
    args = [(seq, int(a), int(b), seed0) for a, b in zip(edges, edges[1:])]
    scores = np.empty(n)
    for lo, vals in pool.imap_unordered(_scan_chunk, args):
        scores[lo:lo + len(vals)] = vals
    top = np.argsort(-scores)[:TOP]
    refined = []
    for j in top:
        s = [seq[i] for i in PERMS[j]]
        b, pt, _, _ = solve(s, restarts=FULL_R, iters=FULL_I, seed=seed0 + 7 * int(j))
        refined.append((norm(b, len(seq)), int(j), pt))
    refined.sort(key=lambda t: -t[0])
    return refined, scores


if __name__ == '__main__':
    cons = load_all()['consensus']
    print("=" * 78)
    print("ROUND 22 — LOCAL / SHORT-SCALE TRANSPOSITION")
    print("=" * 78)
    print("run against PREREG-local.md; family fixed and counted before the run\n")
    md = [max(abs(p - i) for i, p in enumerate(t)) for t in PERMS]
    print(f"  family: {len(PERMS)} distinct permutations"
          f"   (section 27's columnar family: 46,232)")
    print(f"  maximum displacement: {min(md)} to {max(md)} positions"
          f"  -- this is what makes the family local")
    print(f"  stage 1 scan {SCAN_R}x{SCAN_I}; stage 2 {FULL_R}x{FULL_I} on top {TOP}")
    print(f"  null: identical two-stage best-of-{len(PERMS)} on shuffled text,"
          f" {NULL_REPS} reps\n")

    t0 = time.time()
    with Pool(4) as pool:
        res, scores = sweep(cons, 500, pool)
        print(f"  scan complete in {time.time()-t0:.0f}s")

        # section 28.4: the identity baseline gets its spread, not a point estimate
        ident = np.array([norm(solve(list(cons), restarts=FULL_R, iters=FULL_I,
                                     seed=4242 + 1000 * s)[0], N)
                          for s in range(IDENT_SEEDS)])
        print(f"\n  identity (no transposition), {IDENT_SEEDS} seeds at {FULL_R}x{FULL_I}:")
        print(f"    mean {ident.mean():.3f}  sd {ident.std():.3f}"
              f"  min {ident.min():.3f}  max {ident.max():.3f}")
        print(f"    section 27.2 measured this spread at 0.153; here it is"
              f" {ident.max()-ident.min():.3f}")

        print(f"\n  scan distribution over all {len(PERMS)}:")
        print(f"    mean {scores.mean():.3f}  sd {scores.std():.3f}"
              f"  max {scores.max():.3f}  min {scores.min():.3f}")
        print(f"    identity's rank in the scan: "
              f"{int((scores > scores[IDENT_J]).sum()) + 1} of {len(PERMS)}")

        print(f"\n  top 10 after full-budget re-solve:")
        print(f"  {'rank':>4s} {'member':>34s} {'score':>8s}   plaintext")
        for r, (sc, j, pt) in enumerate(res[:10], 1):
            print(f"  {r:4d} {LABELS[j]:>34s} {sc:8.3f}   {pt}")

        best = res[0][0]
        gain = best - ident.max()          # against the identity's BEST seed
        print(f"\n  best of family     : {best:.3f}  ({LABELS[res[0][1]]})")
        print(f"  identity best seed : {ident.max():.3f}")
        print(f"  gain over identity : {gain:+.3f}   (Q2 bar: > 0.153)")

        print(f"\n  null — identical two-stage best-of-{len(PERMS)} on shuffled text:")
        nulls = []
        for t in range(NULL_REPS):
            s = list(cons); RNG.shuffle(s)
            nres, _ = sweep(s, 9000 + 137 * t, pool)
            nulls.append(nres[0][0])
            print(f"    rep {t+1}: {nulls[-1]:.3f}", flush=True)

    nulls = np.array(nulls)
    z = (best - nulls.mean()) / nulls.std()
    print(f"\n    null mean={nulls.mean():.3f} sd={nulls.std():.3f} max={nulls.max():.3f}")
    print(f"    observed={best:.3f}  z={z:+.2f}  p={(nulls >= best).mean():.3f}")

    q1 = z >= 2.0
    q2 = gain > 0.153
    print(f"""
  VERDICT AGAINST THE PRE-REGISTRATION
    Q1  family beats its own null (z >= +2)        : {'PASS' if q1 else 'FAIL'}  (z = {z:+.2f})
    Q2  gain over identity exceeds its seed spread : {'PASS' if q2 else 'FAIL'}  ({gain:+.3f} vs 0.153)

  Both were required. {'Held-out falsification targets now apply (PREREG-local.md).'
      if (q1 and q2) else
      'Q1 alone was pre-labelled uninformative: a family-level z carried by the'
      + chr(10) + '  identity member restates section 4 and says nothing about the mechanism.'}

  Reference: enciphered real English at n=87 is about -4.20/gram.
  Total runtime {time.time()-t0:.0f}s.
""")
