"""Phonetic-English corpus and quadgram model.

Grapheme-to-phoneme via CMUdict, then a FIXED phoneme->grapheme table that
respells each word the way a jokey letter-writer would: NATION -> NAYSHUN,
ENOUGH -> INUF, THROUGH -> THROO, GORGEOUS -> GORJUS.

Construction is held identical to corpus.py in every respect except the
respelling -- same wordfreq frequency-weighted sampling, same 4M characters,
same no-spaces concatenation -- so the respelling is the only variable between
the STD and PHON models.

The phoneme table is fixed here and is NOT tuned afterwards (PREREG-phonetic.md,
"no post-hoc tuning"). Words absent from CMUdict keep their orthography, which
is the conservative choice: it can only make the phonetic corpus look MORE like
standard English, never less.
"""
import os, pickle, re
import numpy as np

A = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
IDX = {c: i for i, c in enumerate(A)}
CACHE = os.path.join(os.path.dirname(__file__), '..', 'data', 'phon_corpus.pkl')

# ---------------------------------------------------------------------------
# The fixed phoneme -> grapheme table (ARPABET, stress digits stripped).
# Chosen to imitate ordinary English respelling habits, not IPA.
# ---------------------------------------------------------------------------
P2G = {
    # consonants
    'B': 'B',   'CH': 'CH', 'D': 'D',  'DH': 'TH', 'F': 'F',  'G': 'G',
    'HH': 'H',  'JH': 'J',  'K': 'K',  'L': 'L',   'M': 'M',  'N': 'N',
    'NG': 'NG', 'P': 'P',   'R': 'R',  'S': 'S',   'SH': 'SH','T': 'T',
    'TH': 'TH', 'V': 'V',   'W': 'W',  'Y': 'Y',   'Z': 'Z',  'ZH': 'ZH',
    # vowels
    'AA': 'A',  'AE': 'A',  'AH': 'U', 'AO': 'O',  'AW': 'OW', 'AY': 'I',
    'EH': 'E',  'ER': 'ER', 'EY': 'AY','IH': 'I',  'IY': 'EE', 'OW': 'O',
    'OY': 'OY', 'UH': 'U',  'UW': 'OO',
}


def _dict():
    import cmudict
    return cmudict.dict()


def respell(word, cmu):
    """Respell one lowercase word phonetically. Unknown words pass through."""
    prons = cmu.get(word)
    if not prons:
        return word.upper()
    out = []
    for ph in prons[0]:                       # first pronunciation, always
        ph = re.sub(r'\d', '', ph)            # strip stress
        out.append(P2G.get(ph, ph))
    return "".join(out)


def build_corpus(n_chars=4_000_000, seed=0):
    """Identical to corpus.build_corpus except each word is respelled."""
    from wordfreq import top_n_list, word_frequency
    cmu = _dict()
    words = [w for w in top_n_list('en', 60000) if re.fullmatch(r"[a-z']+", w)]
    freqs = np.array([word_frequency(w, 'en') for w in words])
    freqs = freqs / freqs.sum()
    # respell once, up front, so sampling cost is unchanged
    spelled = [respell(w.replace("'", ""), cmu) for w in words]
    rng = np.random.default_rng(seed)
    out = []; tot = 0
    while tot < n_chars:
        batch = rng.choice(len(words), size=200000, p=freqs)
        chunk = "".join(spelled[i] for i in batch)
        out.append(chunk); tot += len(chunk)
    return "".join(out)[:n_chars]


def get(n_chars=4_000_000):
    if os.path.exists(CACHE):
        with open(CACHE, 'rb') as f:
            return pickle.load(f)
    import corpus as C
    text = build_corpus(n_chars)
    d = dict(text=text,
             uni=C.ngram_logprob(text, 1),
             bi=C.ngram_logprob(text, 2),
             tri=C.ngram_logprob(text, 3),
             quad=C.ngram_logprob(text, 4))
    with open(CACHE, 'wb') as f:
        pickle.dump(d, f, protocol=4)
    return d


# ---------------------------------------------------------------------------
# The validation anchor, fixed in PREREG-phonetic.md before the corpus existed.
# ---------------------------------------------------------------------------
ANCHORS = [
    ('gorgeous',   'GORJUS'),      # Elgar's own documented spelling
    ('nation',     'NAYSHUN'),
    ('enough',     'INUF'),
    ('through',    'THROO'),
    ('beautiful',  'BYOOTUFUL'),
    ('course',     'KORS'),
    ('vigorously', 'VIGERUSLEE'),
]

if __name__ == '__main__':
    cmu = _dict()
    print("phoneme->grapheme table check (targets fixed in PREREG before build):")
    ok = 0
    for w, want in ANCHORS:
        got = respell(w, cmu)
        flag = "OK " if got == want else "-- "
        ok += got == want
        print(f"  {flag} {w:12s} -> {got:12s} (expected {want})")
    print(f"  {ok}/{len(ANCHORS)} anchors reproduced")
    print("\n  Elgar wrote 'gorjus'. The table was written from ordinary respelling")
    print("  habits, not fitted to him, and lands on it exactly.")
    d = get()
    print(f"\nphonetic corpus: {len(d['text'])} chars")
    print("sample:", d['text'][:150])
