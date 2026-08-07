# Computational analysis of the Dorabella Cipher (Elgar, 14 July 1897)

**Status: characterisation, not solution.** No plaintext is claimed. Every
positive-looking result is reported against a simulated null.

This report has two layers. The **primary analysis** runs on the published
transcriptions (HistoCrypt majority consensus, Schmeh, dCode). A **secondary
strand** documents an independent transcription I derived from the manuscript
image before the published ones were available, and measures it against the
consensus — that comparison turns out to be one of the more useful results
here, because it calibrates how much transcription error actually costs.

---

## 0. Sources and provenance

Three transcriptions, all verified on receipt:

| source | tokens | distinct symbols |
|--------|--------|------------------|
| HistoCrypt majority consensus (Hauer et al. 2025, Fig. 2) | 87 | 20 |
| Schmeh (MysteryTwister) | 87 | 21 |
| dCode | 87 | 20 |

The consensus uses structured labels (orientation A–H × semicircle count 1–3)
and contains exactly 20 of the 24 possible symbols — `D3`, `E1`, `E2`, `H3`
never appear. **"24 symbols" is the alphabet's design size, not an observed
count.** Schmeh's and dCode's are opaque letter labels, so only the consensus
supports the arc-count/orientation channel decomposition.

The English reference model is synthesised by frequency-weighted sampling from
`wordfreq`'s empirical English table (4 M characters). It reproduces letter and
within-word n-gram statistics but under-models cross-word structure, and is
modern rather than period English. This is the main outstanding limitation.

---

## 1. Phase 1 — Transcription, and how to measure transcription error

### 1.1 A metric correction that matters

Transcriptions use different symbol names, so only the **partition** they
induce on the 87 positions is comparable. The obvious relabeling-invariant
metric — "position *i* is disputed iff the set of positions sharing *i*'s
symbol differs" — is what produced the disputed-position lists (36 between
consensus and Schmeh, 20 between consensus and dCode, with the latter a
perfect subset of the former; both verified exactly).

**But that metric overstates disagreement by roughly an order of magnitude.**
One differing symbol class reassigns *every* position in that class. Measured
instead under the best one-to-one alignment of symbol sets (Hungarian
assignment on the confusion matrix), the real picture is:

| pair | disagreement, best bijection | "disputed positions" |
|------|------------------------------|----------------------|
| consensus vs dCode | **2.3%** (2 glyphs) | 20/87 = 23% |
| consensus vs Schmeh | **9.2%** (8 glyphs) | 36/87 = 41% |
| Schmeh vs dCode | **11.5%** (10 glyphs) | 36/87 = 41% |
| consensus vs my image read | **18.4%** (16 glyphs) | 58/87 = 67% |

Consensus and dCode are near-identical documents that the partition metric
makes look 23% apart. Anyone using disputed-position counts as an error rate —
including my own first pass — will badly overestimate transcription
uncertainty. **Residual uncertainty among published transcriptions is
2–12%, not 23–41%.**

### 1.2 The image-derived transcription, scored

Segmentation of the supplied image (connected components, threshold 150) found
exactly 29/31/27 = 87 glyphs after discarding one UI-bar artifact. Those row
lengths were not inputs, and they match the published split at indices
0–28 / 29–59 / 60–86.

Scored against the consensus under best bijection:

| channel | accuracy | chance |
|---------|----------|--------|
| whole symbol | 81.6% | ~5% |
| arc count | **97.7%** | 33% |
| orientation | 78.2% | 12.5% |

The arc-count claim from my first pass held up almost exactly: the convex-hull
diameter is cleanly trimodal and reads arc count essentially perfectly. The
orientation channel is where the error concentrates, as predicted, but at 78%
rather than the near-chance level I had feared. The recovered orientation
correspondence is coherent and near-monotone — NW→F (20/21), S→C (14/19),
E→A (9/11), NE→H (3/4), W→E (4/5) — i.e. a consistent rotational alignment
between my compass frame and the consensus letter frame, not random confusion.

I was also wrong to treat my 18 distinct symbols as evidence of a 6-class
collapse: the true count is 20, so I was 2 short, not 6. But the converse
inference is equally unsafe — **symbol-count proximity is not evidence of
positional accuracy.** My 18-vs-20 near-miss coexists with 16 genuinely
misread glyphs.

### 1.3 Confidence calibration

Scored with the fair (bijection) metric, my per-glyph H/M/L confidence labels
were **directionally right but not statistically established**:

| my confidence | glyphs | wrong | error rate |
|---------------|--------|-------|------------|
| H | 30 | 4 | 13.3% |
| M | 39 | 7 | 17.9% |
| L | 18 | 5 | 27.8% |

Monotone, and the overall 18.4% error rate is close to the 21% I had
self-assessed — better aggregate calibration than I expected. But the
L-minus-H gap of +14.4 points does not reach significance (permutation
p = 0.123) at this sample size. Self-assessed confidence on ambiguous
handwriting is usable as a weak prior, not as a reliable one.

---

## 2. Phase 2 — Statistical characterisation (consensus)

### 2.1 Nulls at n = 87

| model | IC mean | IC sd | H mean | doubles | rep. bigrams |
|-------|---------|-------|--------|---------|--------------|
| English, plain | 0.0637 | 0.0066 | 3.993 | 2.77 | 18.3 |
| English, abbreviated | 0.0618 | 0.0076 | 4.043 | 3.85 | 15.3 |
| Monoalphabetic English → 20 symbols | ~0.070 | ~0.010 | ~3.89 | ~3.4 | ~20 |
| Uniform random, 20 symbols | ~0.053 | ~0.004 | ~4.10 | ~4.4 | ~9 |
| Diatonic melody | 0.0623 | 0.0144 | 3.981 | 0.00 | 28.1 |

**IC and entropy are exactly invariant under an injective monoalphabetic
substitution.** The gap between plain English and "enciphered into 20 symbols"
comes entirely from the forced merging of letter pairs, not from encipherment.

The decisive feature of this table is that English, abbreviated English,
enciphered English and melody all overlap heavily at this length. IC has power
against uniform randomness and against essentially nothing else that matters.

### 2.2 Observed

| variant | k | IC | H | doubles | rep2 | rep3 | pct vs English | pct vs uniform |
|---------|---|-----|---|---------|------|------|----------------|----------------|
| consensus | 20 | 0.0585 | 4.030 | 4 | 19 | 2 | 0.23 | 0.98 |
| Schmeh | 21 | 0.0567 | 4.088 | 5 | 14 | 0 | 0.14 | 0.96 |
| dCode | 20 | 0.0585 | 4.030 | 4 | 20 | 4 | 0.23 | 0.98 |
| consensus + dCode core | 20 | 0.0585 | 4.030 | 4 | 20 | 4 | 0.23 | 0.98 |
| consensus + Schmeh core | 21 | 0.0580 | 4.064 | 4 | 16 | 2 | 0.20 | 0.98 |

(A sixth variant masking the 20 contested positions to a single symbol is
excluded — masking mechanically inflates IC to 0.098 and is an artifact, not a
reading.)

The text is **not uniform random** (98th percentile against that null, 19
repeated bigrams against ~9 expected). It sits at the low end of the English
band (23rd percentile) — consistent with English, and equally consistent with
several other things.

### 2.3 The arc-count channel — a robust negative

| channel | distinct | IC | H | max H | distribution |
|---------|----------|-----|---|-------|--------------|
| arc count | 3 | 0.3299 | **1.576** | 1.585 | 29 / 33 / 25 |
| orientation | 8 | 0.1510 | 2.804 | 3.000 | A9 B15 C14 D5 E4 F23 G9 H8 |

The arc-count channel is **statistically indistinguishable from uniform** —
entropy 1.576 against a 1.585 ceiling, and a near-perfect three-way split.
This replicates the finding from my independent transcription (which got arc
count 97.7% right), so it is not an artifact of either reading.

If Elgar's alphabet encoded one property of the plaintext in the loop count
and another in the rotation, the loop count carries no detectable trace of it.
The orientation channel does carry structure (H 2.804 vs 3.000, with F used
26% of the time).

### 2.4 Repeats and Kasiski

19 repeated bigrams, 2 repeated trigrams. Longest repeats: `F2-C2-G2` at
positions 48 and 72 (spacing 24), `C2-G2-F3` at 49 and 62 (spacing 13).
Notable: `B1-H1` occurs three times at 22, 53, 84 — **evenly spaced at 31 and
31**.

Bigram spacings: 5, 6, 11, 11, 11, 13, 13, 16, 20, 23, 24, 24, 27, 31, 31, 31,
31, 33, 37, 40, 52, 55, 62.

| period | divisible |
|--------|-----------|
| 2 | 8/23 |
| 3 | 5/23 |
| 4 | 6/23 |
| 5 | 4/23 |
| 6 | 3/23 |
| 7 | 0/23 |
| 8 | 4/23 |
| 11 | 5/23 |

No period is enriched above chance (a period *p* captures ~1/*p* by
coincidence). **No evidence of a polyalphabetic period.** The four spacings of
31 are the one feature worth a second look, driven largely by the evenly
spaced `B1-H1`.

---

## 3. Phase 3 — Structural hypotheses (consensus)

### 3.1 Arc count × orientation are **not** independent — *and this now replicates*

χ² = 40.18, Monte-Carlo p = 0.001 (5000 permutations), Cramér's V = 0.481.

In my first pass I saw this effect and **discarded it as a transcription
artifact**, reasoning that my visual cues for orientation correlated with arc
count. That reasoning was sound but the conclusion was wrong: the effect is
present at the same strength in the consensus transcription, which I had no
hand in producing. It is a real property of the cipher text.

Interpretation is open. It is consistent with the two channels not being
independent carriers — e.g. the symbol inventory being shaped by which
(orientation, count) pairs Elgar actually assigned, which is corroborated by
the four never-used symbols (`D3`, `E1`, `E2`, `H3`).

### 3.2 Row drift — no significant evidence

| variant | IC by row | MC p |
|---------|-----------|------|
| consensus | 0.047 / 0.058 / 0.074 | 0.318 |
| Schmeh | 0.052 / 0.056 / 0.083 | 0.067 |
| dCode | 0.047 / 0.060 / 0.074 | 0.286 |
| consensus + Schmeh core | 0.052 / 0.058 / 0.074 | 0.153 |

Every variant shows IC rising monotonically from row 1 to row 3, and Schmeh's
approaches significance (p = 0.067). Suggestive of the symbol repertoire
narrowing as Elgar wrote, but not established. **No support for a mid-message
key change.**

### 3.3 Reversal

IC, entropy, unigram frequencies and doubled-symbol counts are **exactly
invariant** under reversal. Any "it reads backwards" argument resting on such
statistics is vacuous. Only directional evidence can bear on it — see §4.

### 3.4 Sukhotin — uninformative at this length

On the consensus, Sukhotin calls 6 of 20 symbols vowels (`A3, E3, F2, F3, G2,
H1`), covering 46% of the text against English's 38–40%.

Calibrated on 500 samples of plain English at exactly n=87, Sukhotin achieves
**precision 0.56** — barely better than chance. Neither the vowel set nor the
46% share carries usable information. **No conclusion drawn.**

---

## 4. Phase 4 — Constrained solving

*(pending: `scripts/solver3.py` and `scripts/noise_recalibrate.py` in flight)*

---

## 5. Phase 5 — Music hypothesis (consensus)

Reference: simulated stepwise-dominated diatonic melodies at n=87, giving
stepwise motion (|interval| ≤ 2) = 0.767, mean |interval| = 1.79,
contour-reversal = 0.529.

**Mapping family: orientation → scale degree, arc count → octave.** All 96
mappings (8 rotations × 2 directions × 6 octave assignments) enumerated.
Best consensus mapping: z = 46.23, with stepwise motion of just **0.151**
against 0.767 for real melody. Null (same symbols, shuffled order,
best-of-48): 41.94 ± 3.43. **p = 0.903** — the real sequence is *less*
melodic than its own shuffles.

**The dial test.** If a melody were written on a rotational dial, successive
symbols should be near neighbours on it. On the consensus, the mean circular
step is 2.326 against a shuffled null of 2.012 ± 0.139 — **z = +2.25,
p(smaller) = 0.989.** Consecutive glyphs are *further* apart on the dial than
chance.

This replicates my independent transcription's result (z = 1.2–2.6 across six
variants, same direction), so it is not a reading artifact. The sequence is
mildly **anti**-melodic — which is what a substitution cipher over language
looks like, and the opposite of a transcribed tune.

**Verdict: the music hypothesis is disfavoured** within the mapping families
tested. Mappings outside them (arc count as pitch, orientation as duration,
symbols as intervals rather than absolute degrees) remain untested.

---

## 6. Unicity distance

With English entropy rate ≈ 1.5 bits/char, redundancy D = log₂26 − 1.5 = 3.20:

| model | H(K) bits | unicity distance |
|-------|-----------|------------------|
| simple substitution, 20–24 symbols → 26 letters | 87.4 | **27.3** |
| simple substitution, bijective on 24 letters | 79.0 | 24.7 |
| homophonic | 112.8 | 35.2 |
| polyalphabetic, 2 alphabets | 174.8 | 54.6 |
| polyalphabetic, 3 alphabets | 262.1 | 81.9 |

**87 characters is ~3.2× the unicity distance of simple substitution.** The
folk claim that the text is too short to ever solve is false for that
hypothesis: at this length a simple substitution of ordinary English is
uniquely determined in principle and should be within reach of a quadgram
solver.

Escape routes: polyalphabetic with 3+ alphabets pushes the unicity distance to
~82, right at the text length. And if the plaintext is abbreviated, phonetic or
proper-noun-heavy, redundancy falls — at D = 2.0 the unicity distance rises to
44, at D = 1.0 to 87, i.e. to the whole text, beyond which no unique solution
exists even in principle.

---

## 7. Conclusions

*(completed after Phase 4)*
