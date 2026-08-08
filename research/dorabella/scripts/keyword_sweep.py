"""Experiment 2 — keyword-mixed alphabets in the Heraldic triplet geometry.

Run against PREREG-keyword.md.

Leg A (exhaustive, closed form).  Under layout A a mirror pair is two glyphs of
the same arc count whose orientations are 180 degrees apart, so the letter pair
is MIXED[g[o]*3+t] against MIXED[g[o+4]*3+t].  As t runs over all three arc
counts the arc permutation h cancels, so the set of 12 mirror-producing letter
pairs depends ONLY on how the eight triplets pair up across the dial.  There
are 105 such pairings, and 105 again for layout B (whose triples are the
columns MIXED[k], MIXED[8+k], MIXED[16+k]).  210 evaluations therefore cover
the entire 483,840-key family for a given keyword, exactly.

Leg B (solver).  The score depends on the full key, so this is the full
483,840-key sweep per keyword, matched to section 8.3, nulled by the identical
best-of-family procedure on shuffled text.

ENIGMA is excluded as anachronistic; see PREREG-keyword.md.
"""
import sys, os, itertools
sys.path.insert(0, os.path.dirname(__file__))
from collections import Counter
import numpy as np
import corpus
from compare import load_all

ALPHA24 = "ABCDEFGHIKLMNOPQRSTUWXYZ"        # Elgar's 24: no J, no V
A24 = {c: i for i, c in enumerate(ALPHA24)}
ORD = "ABCDEFGH"

# Pre-registered keyword list. ENIGMA deliberately absent.
KEYWORDS = ['MALVERN', 'FORLI', 'CAROLINE', 'ALICE', 'CAROLINEALICE', 'CALICE',
            'CRAEGLEA', 'WORCESTER', 'EDWARDELGAR', 'BRAUT']


def mixed_alphabet(keyword):
    """Keyword mixing over the 24-letter alphabet. Elgar's own merges: J->I, V->U."""
    kw = keyword.upper().replace('J', 'I').replace('V', 'U')
    seen, out = set(), []
    for c in kw:
        if c in A24 and c not in seen:
            seen.add(c); out.append(c)
    for c in ALPHA24:
        if c not in seen:
            out.append(c)
    return "".join(out)


def pairings_of_8():
    """All 105 partitions of {0..7} into four unordered pairs."""
    def rec(rest):
        if not rest:
            yield []
            return
        a = rest[0]
        for i in range(1, len(rest)):
            b = rest[i]
            sub = rest[1:i] + rest[i + 1:]
            for tail in rec(sub):
                yield [(a, b)] + tail
    return np.array(list(rec(list(range(8)))))          # (105,4,2)


PAIRINGS = pairings_of_8()


def bigram_matrix(text):
    """W[i,j] = combined mass of bigram (letter i, letter j) in both orders,
    indexed over the 24-letter alphabet."""
    bg = Counter(zip(text, text[1:])); tot = sum(bg.values())
    W = np.zeros((24, 24))
    for (a, b), v in bg.items():
        if a in A24 and b in A24:
            W[A24[a], A24[b]] += v / tot
    return W + W.T


def leg_a_scores(mixed, W):
    """Exhaustive mirror-producing bigram share over both layouts, per pairing."""
    idx = np.array([A24[c] for c in mixed])
    triA = idx.reshape(8, 3)                              # layout A: consecutive triplets
    triB = idx.reshape(3, 8).T                            # layout B: columns
    out = {}
    for name, tri in (('A', triA), ('B', triB)):
        a = tri[PAIRINGS[:, :, 0]]                        # (105,4,3)
        b = tri[PAIRINGS[:, :, 1]]
        out[name] = W[a, b].sum(axis=(1, 2))              # (105,)
    return out


def leg_a(W, keywords, label, ceiling, verbose=True):
    rows = []
    for kw in keywords:
        mixed = mixed_alphabet(kw)
        sc = leg_a_scores(mixed, W)
        best, lay = max((sc['A'].max(), 'A'), (sc['B'].max(), 'B'))
        j = int(sc[lay].argmax())
        rows.append((best, kw, mixed, lay, PAIRINGS[j]))
    rows.sort(reverse=True, key=lambda r: r[0])
    if verbose:
        print(f"\n  {label}  (exhaustive over all 483,840 keys per keyword)")
        print(f"    {'keyword':16s} {'share':>7s} {'pairs/86':>9s} {'lay':>4s}  mixed alphabet")
        for best, kw, mixed, lay, pr in rows:
            print(f"    {kw:16s} {best*100:6.2f}% {best*86:9.2f} {lay:>4s}  {mixed}")
    return rows


def main():
    D = corpus.get()
    W = bigram_matrix(D['text'])

    print("=" * 78)
    print("EXPERIMENT 2 — KEYWORD-MIXED HERALDIC SWEEP")
    print("=" * 78)
    print("run against PREREG-keyword.md; thresholds fixed before any alphabet was built")

    # --- reference points, computed the same way -------------------------
    std = leg_a_scores(ALPHA24, W)
    elgar_pairing = np.array([[0, 4], [1, 5], [2, 6], [3, 7]])
    ji = [i for i, p in enumerate(PAIRINGS)
          if sorted(map(tuple, map(sorted, p))) == sorted(map(tuple, elgar_pairing))]
    elgar_share = float(std['A'][ji[0]])
    print("\n" + "-" * 78)
    print("LEG A — can the geometry seat common bigrams opposite?")
    print("-" * 78)
    print(f"\n  reference points:")
    print(f"    Elgar's actual 1920 key (standard alphabet, pairing o<->o+4) : "
          f"{elgar_share*100:5.2f}%  ({elgar_share*86:.2f} pairs)   [section 11.2: 6.63%]")
    print(f"    best of the standard alphabet over all 483,840 keys          : "
          f"{max(std['A'].max(), std['B'].max())*100:5.2f}%  "
          f"({max(std['A'].max(), std['B'].max())*86:.2f} pairs)   [what 8.3's family can do]")
    # unconstrained ceiling, section 11.2 / section 23
    import networkx as nx
    G = nx.Graph()
    for i, j in itertools.combinations(range(24), 2):
        G.add_edge(i, j, weight=W[i, j])
    M = nx.max_weight_matching(G, maxcardinality=True)
    ceiling = sum(W[i, j] for i, j in M)
    print(f"    unconstrained ceiling (free matching, no geometry)            : "
          f"{ceiling*100:5.2f}%  ({ceiling*86:.2f} pairs)   [section 23: 12.19%]")
    print(f"    share needed to expect 13 pairs                               : "
          f"{13/86*100:5.2f}%")

    rows = leg_a(W, KEYWORDS, "pre-registered period keywords", ceiling)
    best_period = rows[0]
    print(f"\n    threshold Q1 = 10.00% share (>= 8.6 expected pairs)")
    print(f"    best period keyword: {best_period[1]} at {best_period[0]*100:.2f}%"
          f"  -> Q1 {'PASS' if best_period[0] >= 0.10 else 'FAIL'}")

    # --- dictionary pass (free, because leg A is closed form) ------------
    from wordfreq import top_n_list
    import re
    words = [w.upper() for w in top_n_list('en', 40000)
             if re.fullmatch(r"[a-z]{4,}", w)]
    print(f"\n  dictionary pass over {len(words)} English words >= 4 letters:")
    best = []
    for kw in words:
        mixed = mixed_alphabet(kw)
        sc = leg_a_scores(mixed, W)
        b = max(sc['A'].max(), sc['B'].max())
        best.append(b)
    best = np.array(best)
    order = np.argsort(-best)[:12]
    print(f"    {'word':16s} {'share':>7s} {'pairs/86':>9s}")
    for i in order:
        print(f"    {words[i]:16s} {best[i]*100:6.2f}% {best[i]*86:9.2f}")
    print(f"\n    dictionary max = {best.max()*100:.2f}%  ({best.max()*86:.2f} pairs)"
          f"  -> Q1(dictionary) {'PASS' if best.max() >= 0.10 else 'FAIL'}")
    print(f"    distribution: mean {best.mean()*100:.2f}%  sd {best.std()*100:.2f}%"
          f"  95th {np.quantile(best, .95)*100:.2f}%")
    print(f"    words reaching the 10% threshold: {(best >= 0.10).sum()} / {len(words)}")

    # what the observed 13 looks like against each achievable expectation
    print("\n  what the observed 13 mirror pairs look like against each expectation")
    print("  (binomial sd over 86 slots at that share):")
    for lbl, sh in (("order-shuffled null (section 11.1)", 5.15 / 86),
                    ("Elgar's actual key", elgar_share),
                    ("best standard-alphabet key (8.3's family)",
                     max(std['A'].max(), std['B'].max())),
                    (f"best period keyword ({best_period[1]})", best_period[0]),
                    ("best dictionary keyword", float(best.max())),
                    ("unconstrained ceiling (no geometry)", ceiling)):
        exp = sh * 86
        sd = (86 * sh * (1 - sh)) ** 0.5
        print(f"    {lbl:42s} expect {exp:5.2f}   z = {(13-exp)/sd:+.2f}")

    return dict(elgar=elgar_share, ceiling=ceiling, rows=rows,
                dict_best=float(best.max()), dict_all=best, words=words)


# ===========================================================================
# Leg B — the solver sweep, matched to section 8.3
# ===========================================================================
def leg_b():
    """Full 483,840-key sweep per keyword, nulled by the identical
    best-of-family procedure on shuffled text (standing rule 2)."""
    import structured_keys as SK
    cons = load_all()['consensus']
    o, kk = SK.encode(cons)

    def sweep_alpha(o, kk, mixed):
        """section 8.3's exhaustive sweep, with the alphabet swapped out"""
        SK.AIDX = np.array([ord(c) - 65 for c in mixed])
        return SK.sweep(o, kk)

    print("\n" + "-" * 78)
    print("LEG B — the solver, over the same family")
    print("-" * 78)
    print(f"\n  section 8.3's exhaustive 483,840-key sweep, re-run once per keyword")
    print(f"  with the alphabet keyword-mixed. {len(KEYWORDS)} keywords ->"
          f" {len(KEYWORDS)*483840:,} keys.\n")

    obs = []
    for kw in KEYWORDS:
        mixed = mixed_alphabet(kw)
        s = sweep_alpha(o, kk, mixed)
        obs.append((s, kw))
        print(f"    {kw:16s} best = {s:.3f}")
    obs.sort(reverse=True)
    best_obs = obs[0]
    print(f"\n  best of the keyword family: {best_obs[0]:.3f}  ({best_obs[1]})")
    print(f"  section 8.3, standard alphabet, same geometry: -6.272")

    # null: identical best-over-all-keywords procedure on shuffled text
    reps = 15
    print(f"\n  null: identical best-of-{len(KEYWORDS)}x483,840 on shuffled text,"
          f" {reps} reps")
    rng = np.random.default_rng(1897)
    idx = np.arange(len(o))
    nulls = []
    for t in range(reps):
        p = rng.permutation(idx)
        nulls.append(max(sweep_alpha(o[p], kk[p], mixed_alphabet(kw))
                         for kw in KEYWORDS))
        print(f"    rep {t+1:2d}: {nulls[-1]:.3f}", flush=True)
    nulls = np.array(nulls)
    z = (best_obs[0] - nulls.mean()) / nulls.std()
    print(f"\n    null mean={nulls.mean():.3f} sd={nulls.std():.3f}"
          f" max={nulls.max():.3f}")
    print(f"    observed={best_obs[0]:.3f}  z={z:+.2f}"
          f"  p={(nulls >= best_obs[0]).mean():.3f}")
    print(f"\n  Q2 threshold was z >= +2  ->  {'PASS' if z >= 2 else 'FAIL'}")
    print(f"  Reference: enciphered real English at n=87 is about -4.20/gram.")
    return best_obs, nulls


if __name__ == '__main__':
    main()
    leg_b()
