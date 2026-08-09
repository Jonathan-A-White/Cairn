"""Back-of-the-envelope for the phoneme-unit proposal (design review, not the
experiment).

Two questions were asked of it:
  Q1  does phoneme-MASC at 87 tokens over ~24 classes clear unicity, with a
      positive control that could pass at the section 25.3 standard?
  Q2  does enciphered phoneme-English separate from its shuffled null at n=87?

Both reduce to measurable properties of English phoneme sequences, so they are
measured here rather than asserted. Nothing is solved and no cipher is
searched: this is arithmetic to decide whether the experiment is worth running.

A third quantity is computed because the proposal's own structural claim turns
on it: if 180-degree rotation encodes the Pitman voiced/unvoiced cognate
relation, then Dorabella's 13 adjacent mirror pairs are 13 adjacent cognate
phoneme pairs, and the rate of those in English is checkable.
"""
import sys, os, re, math
sys.path.insert(0, os.path.dirname(__file__))
from collections import Counter
import numpy as np

# Pitman pairs voiced/unvoiced cognates as light/heavy strokes of one shape.
COGNATES = [('P', 'B'), ('T', 'D'), ('K', 'G'), ('F', 'V'),
            ('TH', 'DH'), ('S', 'Z'), ('SH', 'ZH'), ('CH', 'JH')]
UNPAIRED = ['HH', 'L', 'M', 'N', 'NG', 'R', 'W', 'Y']
# eight vowel classes on Pitman's long/short pairing; ER folded into R (it is
# an r-coloured syllabic, and Pitman writes it as the R stroke)
VOWEL_CLASSES = [('AA', 'AO'), ('AE', 'EH'), ('AH', 'UH'), ('IY', 'IH'),
                 ('EY',), ('OW',), ('UW',), ('AY', 'AW', 'OY')]


def build_maps():
    merged = {}                       # phoneme -> 24-class label (reading (a))
    for a, b in COGNATES:
        merged[a] = merged[b] = a + '/' + b
    for c in UNPAIRED:
        merged[c] = c
    for grp in VOWEL_CLASSES:
        for v in grp:
            merged[v] = '|'.join(grp)
    merged['ER'] = 'R'
    return merged


def phoneme_stream(n_target=4_000_000, seed=0):
    """Same construction as corpus.py -- wordfreq-weighted sampling -- but the
    unit is the phoneme, not the letter."""
    import cmudict
    from wordfreq import top_n_list, word_frequency
    cmu = cmudict.dict()
    words = [w for w in top_n_list('en', 60000) if re.fullmatch(r"[a-z']+", w)]
    freqs = np.array([word_frequency(w, 'en') for w in words]); freqs /= freqs.sum()
    prons = []
    keep = []
    for i, w in enumerate(words):
        p = cmu.get(w.replace("'", ""))
        if p:
            prons.append([re.sub(r'\d', '', ph) for ph in p[0]])
            keep.append(i)
    keep = np.array(keep)
    fk = freqs[keep] / freqs[keep].sum()
    rng = np.random.default_rng(seed)
    out = []
    tot = 0
    while tot < n_target:
        batch = rng.choice(len(prons), size=200000, p=fk)
        for i in batch:
            out.extend(prons[i])
        tot = len(out)
    return out[:n_target]


def cond_entropy(seq_idx, k, nsym):
    """H(X_n | previous k-1) by plug-in, in bits per symbol."""
    if k == 1:
        c = np.bincount(seq_idx, minlength=nsym).astype(float)
        p = c / c.sum()
        p = p[p > 0]
        return float(-(p * np.log2(p)).sum())
    code = np.zeros(len(seq_idx) - k + 1, dtype=np.int64)
    for i in range(k):
        code = code * nsym + seq_idx[i:len(seq_idx) - k + 1 + i]
    _, cnt = np.unique(code, return_counts=True)
    cnt = cnt.astype(float)
    Hk = -(cnt / cnt.sum() * np.log2(cnt / cnt.sum())).sum()
    code1 = code // nsym
    _, c1 = np.unique(code1, return_counts=True)
    c1 = c1.astype(float)
    Hk1 = -(c1 / c1.sum() * np.log2(c1 / c1.sum())).sum()
    return float(Hk - Hk1)


def main():
    print("=" * 78)
    print("PHONEME-UNIT PROPOSAL — BACK-OF-THE-ENVELOPE (no cipher is searched)")
    print("=" * 78)

    merged = build_maps()
    classes = sorted(set(merged.values()))
    print(f"\n  Pitman-style merged inventory: {len(classes)} classes")
    print(f"    {classes}")
    if len(classes) != 24:
        print(f"    NOTE: {len(classes)} classes, not 24 — arithmetic below uses the actual count")

    print("\n  building a phoneme corpus (wordfreq sampling, CMUdict pronunciations)...")
    ph = phoneme_stream()
    print(f"    {len(ph):,} phonemes, {len(set(ph))} distinct CMUdict phones")

    lab = [merged[p] for p in ph]
    idx_of = {c: i for i, c in enumerate(classes)}
    a = np.array([idx_of[c] for c in lab], dtype=np.int64)
    nsym = len(classes)

    # ---------------- Q1: unicity -------------------------------------
    print("\n" + "-" * 78)
    print("Q1 — UNICITY")
    print("-" * 78)
    Hs = [cond_entropy(a, k, nsym) for k in (1, 2, 3, 4)]
    print(f"\n  conditional entropy of the merged phoneme stream, bits/symbol:")
    for k, h in zip((1, 2, 3, 4), Hs):
        print(f"    H{k} (order {k-1}) = {h:.3f}")
    print(f"    log2({nsym}) = {math.log2(nsym):.3f}  (maximum)")

    HK = sum(math.log2(i) for i in range(1, nsym + 1))     # log2(nsym!)
    print(f"\n  key entropy of a phoneme-MASC over {nsym} classes:"
          f" log2({nsym}!) = {HK:.1f} bits")
    print(f"\n  {'entropy rate assumed':28s} {'D = log2(k) - H':>16s} {'unicity':>9s} {'vs 87':>8s}")
    for lbl, h in [("H2 (order-1)", Hs[1]), ("H3 (order-2)", Hs[2]),
                   ("H4 (order-3)", Hs[3]), ("H4 - 0.3 (optimistic limit)", Hs[3] - 0.3)]:
        Dred = math.log2(nsym) - h
        U = HK / Dred if Dred > 0 else float('inf')
        print(f"  {lbl:28s} {Dred:16.3f} {U:9.1f} {'CLEARS' if U < 87 else 'FAILS':>8s}")

    print(f"\n  for comparison, section 6's letter MASC: H(K)=87.4 bits,"
          f" D=3.20, unicity 27.3")

    # ---------------- Q2: separation at n=87 ---------------------------
    print("\n" + "-" * 78)
    print("Q2 — DOES PHONEME-ENGLISH SEPARATE FROM ITS SHUFFLED NULL AT n=87?")
    print("-" * 78)
    # quadgram log-prob per gram, real vs order-shuffled, 87-symbol windows
    k = 4
    code = np.zeros(len(a) - k + 1, dtype=np.int64)
    for i in range(k):
        code = code * nsym + a[i:len(a) - k + 1 + i]
    keys, cnt = np.unique(code, return_counts=True)
    logp = np.log10(cnt / cnt.sum())
    floor = math.log10(0.01 / cnt.sum())

    def score(seq):
        c = np.zeros(len(seq) - k + 1, dtype=np.int64)
        for i in range(k):
            c = c * nsym + seq[i:len(seq) - k + 1 + i]
        j = np.searchsorted(keys, c); j[j >= len(keys)] = 0
        hit = keys[j] == c
        out = np.full(len(c), floor)
        out[hit] = logp[j[hit]]
        return float(out.mean())

    rng = np.random.default_rng(7)
    real, shuf = [], []
    for _ in range(600):
        i = int(rng.integers(0, len(a) - 87))
        w = a[i:i + 87]
        real.append(score(w))
        s = w.copy(); rng.shuffle(s)
        shuf.append(score(s))
    real = np.array(real); shuf = np.array(shuf)
    sep = (real.mean() - shuf.mean()) / np.sqrt((real.std() ** 2 + shuf.std() ** 2) / 2)
    print(f"\n  87-symbol windows, quadgram log-prob per gram, merged phonemes:")
    print(f"    real phoneme English : {real.mean():.3f} +- {real.std():.3f}")
    print(f"    order-shuffled       : {shuf.mean():.3f} +- {shuf.std():.3f}")
    print(f"    separation           : {real.mean()-shuf.mean():.3f}/gram"
          f"   = {sep:.2f} pooled sd")
    print(f"\n  the same quantity for LETTERS (section 4.1, what makes the letter")
    print(f"  positive control work): English -4.196 vs shuffled-consensus -5.010,")
    print(f"  a gap of 0.814/gram.")

    # ---------------- the structural claim -----------------------------
    print("\n" + "-" * 78)
    print("THE 180-DEGREE = COGNATE CLAIM, CHECKED AGAINST ENGLISH")
    print("-" * 78)
    cog = {}
    for x, y in COGNATES:
        cog[x] = y; cog[y] = x
    n_adj = len(ph) - 1
    n_cog = sum(1 for p, q in zip(ph, ph[1:]) if cog.get(p) == q)
    rate = n_cog / n_adj
    print(f"""
  If 180-degree rotation encodes the voiced/unvoiced cognate relation, then
  Dorabella's 13 adjacent mirror pairs are 13 adjacent cognate phoneme pairs.

    adjacent cognate pairs in the phoneme corpus : {n_cog:,} of {n_adj:,}
    rate                                         : {rate*100:.3f}%
    expected in 86 adjacencies                   : {rate*86:.2f}
    observed mirror pairs                        : 13
""")
    if rate * 86 > 0:
        sd = math.sqrt(86 * rate * (1 - rate))
        print(f"    z of 13 against that expectation             : "
              f"{(13 - rate*86)/sd:+.1f}")


if __name__ == '__main__':
    main()
