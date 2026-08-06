"""Reference English corpus + n-gram models.

No network access to a real text corpus, so the corpus is synthesised by
frequency-weighted sampling from wordfreq's empirical English word-frequency
table. This reproduces English letter and within-word n-gram statistics
faithfully; it does NOT reproduce cross-word syntax, which is a stated
limitation (quadgrams straddling a space are under-modelled).
"""
import numpy as np, os, pickle, re
from collections import Counter

A = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
IDX = {c:i for i,c in enumerate(A)}
CACHE = os.path.join(os.path.dirname(__file__), '..', 'data', 'corpus.pkl')

def build_corpus(n_chars=4_000_000, seed=0):
    from wordfreq import top_n_list, word_frequency
    words = [w for w in top_n_list('en', 60000) if re.fullmatch(r"[a-z']+", w)]
    freqs = np.array([word_frequency(w,'en') for w in words])
    freqs = freqs/freqs.sum()
    rng = np.random.default_rng(seed)
    out=[]; tot=0
    while tot < n_chars:
        batch = rng.choice(len(words), size=200000, p=freqs)
        chunk = "".join(words[i].replace("'","").upper() for i in batch)
        out.append(chunk); tot += len(chunk)
    return "".join(out)[:n_chars]

def ngram_logprob(text, n, floor=0.01):
    counts = np.zeros((26,)*n, dtype=np.float64)
    idx = np.array([IDX[c] for c in text if c in IDX], dtype=np.int64)
    if n==1:
        np.add.at(counts, idx, 1)
    else:
        views=[idx[i:len(idx)-n+1+i] for i in range(n)]
        np.add.at(counts, tuple(views), 1)
    tot = counts.sum()
    p = (counts+floor)/(tot+floor*counts.size)
    return np.log10(p)

def get(n_chars=4_000_000):
    if os.path.exists(CACHE):
        with open(CACHE,'rb') as f: return pickle.load(f)
    text = build_corpus(n_chars)
    d = dict(text=text,
             uni=ngram_logprob(text,1),
             bi=ngram_logprob(text,2),
             tri=ngram_logprob(text,3),
             quad=ngram_logprob(text,4))
    with open(CACHE,'wb') as f: pickle.dump(d,f,protocol=4)
    return d

def score(s, table, n):
    idx=[IDX[c] for c in s if c in IDX]
    if len(idx)<n: return -1e9
    a=np.array(idx)
    views=tuple(a[i:len(a)-n+1+i] for i in range(n))
    return float(table[views].sum())

if __name__=='__main__':
    d=get()
    print("corpus chars:", len(d['text']))
    print("sample:", d['text'][:120])
    # sanity: English vs shuffled
    import random
    s=d['text'][:87]
    sh=''.join(random.sample(s,len(s)))
    for name,t,n in [('quad',d['quad'],4),('tri',d['tri'],3)]:
        print(f"{name}: english={score(s,t,n)/ (87-n+1):.3f}  shuffled={score(sh,t,n)/(87-n+1):.3f} (per-gram)")
