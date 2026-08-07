"""How far from ordinary English does documented Elgar actually sit?

Section 7.4 measured that explaining Dorabella's solver deficit by idiolect
alone would need 40-50% coined vocabulary. That was a simulation with no
empirical anchor. Buckley (1905) quotes Elgar verbatim throughout -- the
author states in his introduction that "the sayings of Elgar are recorded in
the actual words addressed directly to the writer" -- so his register can be
measured directly.

Method mirrors section 7.3 exactly: the language model is held fixed (the
modern quadgram model) and only the plaintext register varies, so any
difference is a property of the text. Scores are per-quadgram over 87-character
windows, directly comparable to every other figure in this report.
"""
import sys, os, re
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
import corpus as C, period_corpus

RAW=os.path.join(os.path.dirname(__file__),'..','data','buckley1905.txt')
N=87
QUAD=C.get()['quad']

def clean_book():
    t=open(RAW, encoding='utf-8', errors='ignore').read()
    t=re.sub(r'##+ p\..*?##+', ' ', t)          # page markers
    t=re.sub(r'-\n', '', t)                      # rejoin hyphenations
    t=t.replace('\n',' ')
    return t

def quoted_spans(t, minlen=60, maxlen=600):
    """Spans inside double quotes. OCR leaves quote marks unbalanced, so a span
    is only accepted if it is of plausible sentence length AND contains no
    page-marker debris -- otherwise the regex bridges distant quote marks and
    swallows whole chapters."""
    out=[]
    for m in re.finditer(r'["\u201c\u201d]([^"\u201c\u201d]+)["\u201c\u201d]', t):
        g=m.group(1).strip()
        if not (minlen <= len(g) <= maxlen): continue
        if re.search(r'#|\bp\.\s*\d|PAGE|ILLUSTRATION', g): continue
        if sum(ch.isalpha() or ch.isspace() for ch in g)/len(g) < 0.90: continue
        out.append(g)
    return out

def letters(s):
    return "".join(ch for ch in s.upper() if ch in C.A)

def windows(s, n=N, step=20):
    return [s[i:i+n] for i in range(0, max(1,len(s)-n+1), step) if len(s[i:i+n])==n]

def score(w):
    return C.score(w, QUAD, 4)/(N-3)

if __name__=='__main__':
    t=clean_book()
    print("="*78); print("ELGAR IDIOLECT, MEASURED"); print("="*78)
    qs=quoted_spans(t)
    eq=letters(" ".join(qs))
    print(f"\nquoted spans >=60 chars: {len(qs)};  {len(eq)} letters after cleaning")
    print(f"  sample: {eq[:110]}")
    # chapters IV-V: sustained close-paraphrase of Elgar's conversation
    i=t.find('EDWARD ELGAR AT HOME'); j=t.rfind('THE PROGRESS OF ELGAR')
    chap=letters(t[i:j]) if (i>0 and j>i) else ''
    whole=letters(t)
    bands={}
    for nm,src in (('Elgar quoted verbatim',eq),
                   ('Buckley chs IV-V (Elgar reported)',chap),
                   ('Buckley whole book (1905 prose)',whole)):
        w=windows(src)
        if len(w)<5: print(f"  {nm}: too short ({len(w)} windows)"); continue
        v=np.array([score(x) for x in w]); bands[nm]=v
        print(f"\n  {nm:36s} n={len(v):4d} windows  mean={v.mean():.3f} sd={v.std():.3f}")
    # reference bands, same model, same window length
    rng=np.random.default_rng(7)
    mod=C.get()['text']; aus=period_corpus.clean()
    for nm,src in (('modern English (reference)',mod),('Austen letters (reference)',aus)):
        v=np.array([score(src[i:i+N]) for i in rng.integers(0,len(src)-N,600)])
        bands[nm]=v
        print(f"  {nm:36s} n={len(v):4d} windows  mean={v.mean():.3f} sd={v.std():.3f}")
    print("\n" + "-"*78)
    print(f"  {'Dorabella (consensus, solved)':36s}                  = -4.680")
    print("-"*78)
    if 'Elgar quoted verbatim' in bands:
        e=bands['Elgar quoted verbatim']; m=bands['modern English (reference)']
        print(f"\n  Elgar-vs-modern register cost: {e.mean()-m.mean():+.3f}/gram")
        gap=-4.680-m.mean()
        print(f"  gap to explain (Dorabella - modern): {gap:+.3f}")
        print(f"  fraction explained by Elgar's own register: "
              f"{100*(e.mean()-m.mean())/gap:.0f}%")
