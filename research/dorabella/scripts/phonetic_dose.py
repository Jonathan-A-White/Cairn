"""Experiment 1, follow-up — the phonetic DOSE curve.

P1 established, before the consensus was touched, that FULL phonetic respelling
costs 1.395/gram against the standard quadgram model, which is 314% of the
0.444 deficit to be explained. So the pre-registered P4 test -- consensus
solved under a fully phonetic model -- tests the wrong dose by construction,
and its failure leaves the partial-dose question open.

This is the same move section 7.4 made for invented vocabulary, and it is
scored the same way, so the two are directly comparable: 7.4 priced the coinage
dose at 40-50%; this prices the phonetic dose.

DECLARED POST-HOC. It was not in PREREG-phonetic.md. Its motivation (P1's 3x
overshoot) was established before P4 ran and is in out/phonetic.log above the
P4 block, but the decision to run this sweep was taken after seeing P4 fail,
and that is what matters for the standing rules. It is therefore reported as a
diagnostic, not as a test, and it carries its own null.
"""
import sys, os, re
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
import corpus, phonetic, ensemble2
import solver
from solver import solve, norm

RESTARTS, ITERS, N = 20, 15000, 87
DOSES = [0.0, 0.15, 0.30, 0.50, 0.75, 1.0]
RNG = np.random.default_rng(2718)
CACHE = os.path.join(os.path.dirname(__file__), '..', 'data', 'dose_corpora.npz')


def build_mixed(dose, n_chars=2_000_000, seed=0):
    """Corpus in which each sampled word is respelled with probability `dose`."""
    from wordfreq import top_n_list, word_frequency
    cmu = phonetic._dict()
    words = [w for w in top_n_list('en', 60000) if re.fullmatch(r"[a-z']+", w)]
    freqs = np.array([word_frequency(w, 'en') for w in words]); freqs /= freqs.sum()
    plain = [w.replace("'", "").upper() for w in words]
    spelled = [phonetic.respell(w.replace("'", ""), cmu) for w in words]
    rng = np.random.default_rng(seed)
    out, tot = [], 0
    while tot < n_chars:
        batch = rng.choice(len(words), size=200000, p=freqs)
        pick = rng.random(len(batch)) < dose
        chunk = "".join((spelled if p else plain)[i] for i, p in zip(batch, pick))
        out.append(chunk); tot += len(chunk)
    return "".join(out)[:n_chars]


def model_for(text):
    return dict(text=text, quad=corpus.ngram_logprob(text, 4))


def band(text, model, trials=20):
    """Enciphered-English band for this dose: encipher known plaintext, solve."""
    solver.QUAD = model['quad']
    sc, ac = [], []
    for _ in range(trials):
        i = int(RNG.integers(0, len(text) - N)); pt = text[i:i + N]
        L = sorted(set(pt)); perm = RNG.permutation(26)[:len(L)]
        mp = {c: int(perm[j]) for j, c in enumerate(L)}
        b, got, _, _ = solve([mp[c] for c in pt], restarts=RESTARTS, iters=ITERS,
                             seed=int(RNG.integers(1e6)))
        sc.append(norm(b, N)); ac.append(sum(x == y for x, y in zip(got, pt)) / N)
    return np.array(sc), np.array(ac)


def main():
    cons = ensemble2.variants()['E0_consensus']
    STD = corpus.get()
    print("=" * 78)
    print("EXPERIMENT 1 FOLLOW-UP — PHONETIC DOSE CURVE  (declared post-hoc)")
    print("=" * 78)
    print("""
  P1 showed full respelling costs 1.395/gram, 314% of the 0.444 deficit. So
  the pre-registered P4 tested the wrong dose. This finds the dose that would
  fit, the way section 7.4 did for coined vocabulary -- and then asks whether
  the consensus is actually recoverable at that dose.
""")
    print(f"  {'dose':>5s} {'control':>9s} {'recov':>6s} {'consensus':>10s} "
          f"{'z vs band':>10s} {'null(shuf)':>11s} {'vs null':>8s}")
    rows = []
    for d in DOSES:
        text = build_mixed(d)
        M = model_for(text)
        bs, ba = band(text, M)
        solver.QUAD = M['quad']
        obs = norm(solve(cons, restarts=RESTARTS, iters=ITERS, seed=777)[0], N)
        sh = []
        for _ in range(20):
            s = list(cons); RNG.shuffle(s)
            sh.append(norm(solve(s, restarts=RESTARTS, iters=ITERS,
                                 seed=int(RNG.integers(1e6)))[0], N))
        sh = np.array(sh)
        z = (obs - bs.mean()) / bs.std()
        zn = (obs - sh.mean()) / sh.std()
        rows.append((d, bs.mean(), bs.std(), ba.mean(), obs, z, sh.mean(), sh.std(), zn))
        print(f"  {d:5.2f} {bs.mean():9.3f} {ba.mean():6.2f} {obs:10.3f} "
              f"{z:+10.2f} {sh.mean():11.3f} {zn:+8.2f}")

    print("""
  'control'  = enciphered known plaintext at that dose, solved under that
               dose's own model (the section 4.1 band, recomputed per dose)
  'z vs band'= how far the consensus falls below that band, in its sd units.
               The section 4.2 figure to beat is -2.88.
  'vs null'  = consensus against shuffled consensus under the same model,
               which is the check that a looser model has not simply flattered
               everything.
""")
    best = max(rows, key=lambda r: r[5])
    print(f"  best dose = {best[0]:.2f} at z = {best[5]:+.2f}"
          f"   (standard-orthography baseline: {rows[0][5]:+.2f})")
    if best[5] <= rows[0][5] + 0.5:
        print("""
  No dose materially improves on plain orthography. The phonetic mechanism
  does not close the deficit at ANY dose, so the result is not an artifact of
  P4 having tested full respelling.""")
    np.save(os.path.join(os.path.dirname(__file__), '..', 'out', 'dose_rows.npy'),
            np.array(rows))


if __name__ == '__main__':
    main()
