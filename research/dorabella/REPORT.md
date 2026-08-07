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

All scores are mean quadgram log-probability per gram. **Every solve —
observed, null and control — uses an identical budget of 20 restarts × 15 000
annealing iterations.** (My first pass gave the observed text 40 × 20 000
against nulls at 12 × 12 000; search budget alone raises the achievable score,
and correcting that removed most of an apparent effect.)

### 4.1 Positive control and reference bands

| band | mean | sd | note |
|------|------|----|------|
| enciphered real English, n=87 | **−4.196** | 0.168 | solver recovers 96% of characters |
| shuffled consensus (order destroyed) | −5.010 | 0.087 | max over 60 runs: −4.834 |
| uniform random, 20 symbols | −5.178 | 0.125 | max over 60 runs: −4.899 |

The positive control is the licence to interpret anything else here: at exactly
87 characters the solver recovers *known* enciphered English at 96% character
accuracy. The method has power at this length.

### 4.2 Observed

| variant | forward | reversed | percentile vs null | z vs English |
|---------|---------|----------|--------------------|--------------|
| consensus | **−4.680** | −4.707 | 1.00 | **−2.88** |
| dCode | −4.678 | −4.726 | 1.00 | −2.86 |
| consensus + dCode core | −4.678 | −4.717 | 1.00 | −2.86 |
| consensus + Schmeh core | −4.856 | −4.913 | 0.98 | −3.92 |
| Schmeh | −4.948 | −4.936 | 0.86 | −4.47 |
| consensus, core masked | −4.622 | −4.625 | 1.00 | −2.53 |

Three readings:

1. **Above the meaningless-text null.** The consensus at −4.680 beats the best
   of 120 null runs (−4.834) by 0.15, roughly 3.8 null sd above the null mean.
   Unlike my image transcription — which sat *inside* the null range once
   budgets were matched — the published transcription is genuinely more
   language-like than scrambled text.
2. **Far below real English.** −2.88 sd below the enciphered-English band, and
   below its 5th percentile (−4.513). It does not behave like a simple
   substitution of ordinary English.
3. **No support for reversal.** Reversed scores are consistently *slightly
   worse* than forward across every variant. Whatever the text is, it is not
   improved by reading backwards.

Two internal consistency checks worth noting. Schmeh's transcription — the one
that disagrees most with the other two (9.2% and 11.5%) — also solves worst,
essentially at the null. And the masked variant scores "best" of all, purely
because collapsing 20 positions to one symbol leaves 17 distinct symbols and
more repeats to overfit. Both confirm that solver score tracks transcription
quality and symbol count, not just content.

### 4.3 The corruption control — what the gap actually means

Take real English, encipher it properly, then corrupt the ciphertext by
swapping symbols to a confusable neighbour at a controlled rate — the exact
error mode transcription produces. (An earlier version of this sweep was
**wrong**: the neighbour map was keyed on `0..k−1` while ciphertext symbols
came from a permutation of `0..25`, so a `.get` default silently skipped most
corruptions. Fixed and re-run; a nominal 0.21 rate now changes 0.206 of
positions.)

| corruption rate | score/gram | char accuracy | note |
|-----------------|-----------|---------------|------|
| 0.000 | −4.216 | 0.97 | |
| 0.023 | −4.305 | 0.91 | consensus vs dCode distance |
| 0.050 | −4.479 | 0.77 | |
| **0.092** | **−4.702** | 0.66 | consensus vs Schmeh distance |
| 0.115 | −4.738 | 0.46 | Schmeh vs dCode distance |
| 0.150 | −4.834 | 0.37 | |
| 0.184 | −4.856 | 0.31 | my image transcription's measured error |
| 0.250 | −4.873 | 0.25 | |

**The observed consensus score of −4.680 interpolates to an equivalent
transcription-error rate of ≈ 8.8%.**

A side result worth recording: my image transcription has a *measured* 18.4%
error and scored −4.735, whereas this sweep predicts −4.856 for 18.4% *random*
confusion. Systematic transcription error — consistently collapsing the same
pair of rotations — is markedly less destructive than random error of the same
magnitude, because a consistent collapse is itself close to a substitution the
solver can absorb.

So the honest statement is conditional, and it hinges on a quantity nobody has
measured — the consensus transcription's *absolute* error:

- If the consensus is as accurate as its 2.3% distance from dCode suggests,
  a simple substitution of ordinary English should score ≈ −4.31. We observe
  −4.680, a shortfall of ~2.2 sd of the corruption-trial spread. **Simple
  substitution of ordinary English is disfavoured.**
- If the consensus carries ~9% absolute error, the observation is *exactly*
  what simple-substitution English predicts, and nothing is excluded.

The pairwise distances cannot settle this, because the three transcriptions
are not independent — a shared misreading of the same ambiguous glyph moves
them together. This is now the single quantity on which the whole question
turns.

### 4.4 Crib-constrained solves

Not pattern screens: the crib is pinned into the key and everything else is
annealed around it. The meaningful comparison is against the same crib forced
into *shuffled* versions of the same text, at matched budget.

| crib | fitting positions | best constrained | shuffled-text null | z | vs unconstrained (−4.680) |
|------|-------------------|------------------|--------------------|---|---------------------------|
| ALFRED | 31 | −4.883 | −5.230 ± 0.114 | 3.04 | costs 0.20 |
| JULY | 58 | −5.048 | −5.216 ± 0.057 | 2.94 | costs 0.37 |
| ELGAR | 44 | −5.036 | −5.263 ± 0.112 | 2.03 | costs 0.36 |
| MALVERN | 19 | −5.357 | −5.418 ± 0.084 | 0.72 | costs 0.68 |
| SYMPATHY | 1 (pos 69) | −5.657 | −5.763 ± 0.277 | 0.38 | costs 0.98 |
| PENNY | **0** | — | — | — | cannot be placed |
| WOLVERHAMPTON | **0** | — | — | — | cannot be placed |
| MISS PENNY | **0** | — | — | — | cannot be placed |

**PENNY cannot be placed anywhere in the consensus transcription.** It needs a
doubled symbol (the `NN`), and the text contains only four doubled symbols,
none in a compatible context. Same for WOLVERHAMPTON and MISSPENNY. That is a
clean structural negative, independent of any language model — and it disposes
of the most obvious candidate cribs from the 1897 context.

**No crib is supported.** Every one of them *costs* score relative to leaving
the solver unconstrained, meaning the solver does better when free to ignore
the crib entirely. And the apparent significances are a selection artifact:
z tracks the number of fitting positions almost monotonically (ALFRED 31 → 3.04,
JULY 58 → 2.94, ELGAR 44 → 2.03, MALVERN 19 → 0.72, SYMPATHY 1 → 0.38). A crib
with 58 placements gets 58 chances to find a lucky fit; one with a single
placement gets one. That ordering is what a null-effect-plus-selection looks
like, not what a genuine crib looks like — a real crib should show a *large* z
at a *specific* position and cost little relative to the unconstrained solve.
None does.

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

## 7. Round 2 — high-resolution plate, period corpus, invented vocabulary

Three new inputs arrived: a high-resolution scan of the 1937 book plate
(3090×1280, ~3× the linear resolution of the first image), Jane Austen's
*Letters* (Gutenberg #42078) as period corpus, and the 1886 Liszt concert
programme carrying an 18–25 glyph pencilled fragment in the same symbol set.

**Context that reframes everything: the original manuscript is lost.** Every
transcription in existence descends from the same 1937 printed halftone. There
is no ground truth to measure absolute error against, and inter-transcriber
agreement is inflated by shared-source correlation that no amount of better
imaging can break.

### 9.1 The higher resolution does not rescue the orientation estimator

Segmentation of the hi-res plate gives 29/31/27 = 87 glyphs (one speck
discarded), matching the published split. But the 8-fold quantisation test on
measured opening angles is *still* not significant:

| test | 1st image | hi-res plate | null p95 |
|------|-----------|--------------|----------|
| 2-fold order parameter | 0.659 | 0.652 | 0.183 |
| 4-fold | 0.485 | 0.395 | 0.186 |
| 8-fold | 0.207 (p=0.021) | **0.162 (p=0.104)** | 0.185 |

Tripling the resolution changed nothing. **The failure is intrinsic to the
hull-diameter estimator, not to image quality** — a useful negative, since it
means better photographs will not automatically yield better transcriptions.

### 9.2 How internally consistent is the consensus? — 86%

Absolute accuracy is unmeasurable, but *internal consistency* is not: if the
consensus is a faithful reading, glyphs sharing a label should look alike. A
leave-one-out nearest-neighbour classifier on scale-normalised glyph bitmaps
(rotation deliberately **not** normalised, since orientation is the label):

| target | LOO accuracy | chance |
|--------|--------------|--------|
| full symbol | **0.862** | 0.069 |
| arc count | **0.943** | 0.338 |
| orientation | **0.897** | 0.161 |

The consensus labels are strongly predictable from ink. The orientation
confusion matrix is near-diagonal; almost all residual error sits in the rare
class `H` (4 of 8 misassigned, confused with `A` and `G`).

Twelve positions carry a consensus label that disagrees with the
nearest-looking glyph: **0, 4, 9, 15, 21, 23, 24, 33, 36, 68, 71, 77**. These
are the concrete candidates for mis-transcription.

A surprise: they are **not** enriched among the 20 transcriber-contested
positions (3 of 20 overlap; Fisher exact p = 1.000). Where transcribers
disagree with each other is *not* where the glyphs are visually ambiguous.
That points at convention differences or transcription slips rather than
genuine illegibility — and it means contested-position lists are a poor proxy
for where the reading is actually uncertain.

**This sets a ceiling.** If glyph appearance determines the consensus label
only ~86–90% of the time, the plate supports roughly 10–14% irreducible
reading error — which is the same size as the ~8.8% equivalent error implied
by the solver score (§4.3). The crux of conclusion 6 may therefore be
**permanently unresolvable from surviving sources**.

### 9.3 Period register explains ~9% of the gap

Language model held fixed (modern synthetic), plaintext register varied, so
any difference is a property of the text:

| plaintext | plain score | solved | recovery |
|-----------|-------------|--------|----------|
| modern English | −4.233 ± 0.150 | −4.236 ± 0.175 | 0.96 |
| Austen letters (1800s epistolary) | −4.281 ± 0.147 | −4.277 ± 0.153 | 0.95 |

**Register cost: −0.041/gram — 9% of the −0.444 gap.** Period epistolary
English solves essentially as well as modern English. Dorabella remains 2.64σ
below the Austen band. *Register alone does not explain the gap.*

### 9.4 Invented vocabulary — the right idea, but it needs an implausible dose

Simulating portmanteaus directly (prefix of one word + suffix of another, the
`HYSTERIOUS` = hysterical + mysterious construction), with frequency-weighted
vocabulary so the zero-nonce baseline reproduces natural English:

| nonce-word fraction | plain score | solved | recovery |
|---------------------|-------------|--------|----------|
| 0.00 | −4.243 | −4.220 | 0.98 |
| 0.15 | −4.459 | −4.447 | 0.84 |
| 0.30 | −4.605 | −4.411 | 0.87 |
| 0.50 | −4.786 | −4.682 | 0.62 |
| 0.75 | −4.945 | −4.710 | 0.54 |

Dorabella's −4.680 corresponds to roughly **40–50% invented vocabulary**.
(The solved column is noisy at 14 reps per point; the plain column, at 400
reps, is the reliable one and puts the equivalent between 0.30 and 0.50.)

So the mechanism is real but the required dose is not plausible: explaining
the whole gap by idiolect means *half the words in the note are coinages*.
By contrast ~9% transcription error explains it entirely and sits squarely
inside the 10–14% ambiguity the plate actually exhibits. **Transcription noise
is much the more parsimonious explanation** — though the two combine, and
~5% error plus ~15% coinage would also suffice.

### 9.5 The Liszt fragment — not readable from this image

The pencilled cipher is at x≈42–58, y≈233–686 of the programme scan, written
rotated; de-rotated it resolves into recognisable Dorabella-type glyphs.
But at 26 px tall it is below the threshold for reliable segmentation:
connected-component counts swing from 5 to 20 across thresholds (140–170) and
the projection profile is fragmentary. **No transcription is offered.**

One discrepancy worth flagging: the fragment appears to carry roughly 20–24
glyphs, whereas the reported solution `GETS YOU TO JOY, AND HYSTERIOUS` is 25
letters and the accompanying description calls it an 18-character message.
Those three numbers cannot all be right, and I could not verify the 1977
decoding independently (no external network access). A higher-resolution image
of this page is worth more than anything else currently outstanding: it is the
only known-plaintext sample in this symbol system.

---

## 8. Round 3 — Elgar's own key, and an exhaustive structured-key sweep

### 8.1 Elgar's 1920 alphabet, extracted and verified

The notebook page gives Elgar's own A–Z key in his hand, and it is not an
arbitrary permutation. Twenty-four letters — **I and J share a symbol, U and V
share a symbol**, both explicitly labelled as such — laid out in **8 groups of
3**: one group per orientation, arc count giving position within the group.

That yields a closed-form key:

```
letter = ALPHA24[ orientation_index * 3 + (arc_count - 1) ]
ALPHA24 = "ABCDEFGHIKLMNOPQRSTUWXYZ"          (no J, no V)
```

Applying it to the consensus transcription reproduces **dCode's published
string at 85/87 characters**, differing only at positions 33 and 77.

### 8.2 dCode is not an independent transcription — and that moves the crux

§8.1 settles it: dCode's letter string is *the consensus transcription
deciphered under Elgar's notebook alphabet*. A fixed key application is a
relabeling, so the identity-partition and bijection analyses remain valid —
but the **independence** does not.

This retracts a load-bearing number. In §1.1 I reported consensus-vs-dCode
agreement of 97.7% and in §4.3 used the implied ~2.3% error to argue that
simple-substitution English was disfavoured. That comparison was never
measuring two independent readings; it was measuring one transcription against
a relabeled near-copy of itself. **There are two independent sources, not
three.**

The only genuinely independent estimate of transcription error is therefore
consensus-vs-Schmeh: **9.2%**. The solver score implies **8.8%**. Those agree
almost exactly. Combined with the plate's measured 10–14% appearance
ambiguity (§7.2), the evidence now points one way: **transcription noise is
sufficient to explain the entire gap**, and the "disfavoured" branch of
conclusion 6 has lost its support.

A corroboration worth recording: the two positions where consensus and dCode
genuinely differ — **33 and 77** — were both independently flagged by the
appearance classifier of §7.2 as glyphs whose label contradicts their nearest
look-alike. Probability of that under chance placement is (12/87)² ≈ 0.019.
The classifier is detecting real ambiguity.

### 8.3 Exhaustive sweep over Elgar's structural key family

Because the key family is a permutation over 8 orientation-groups × 3 arc
counts rather than an arbitrary 24!, it can be searched **exhaustively** —
483,840 keys (8! orderings of orientation groups × 3! of arc counts × 2
layouts, orientation-major and count-major). No hill climbing, so no
local-optimum excuse, and the null is exact.

| key | score/gram |
|-----|-----------|
| **Elgar's own 1920 notebook key, applied literally** | **−7.705** |
| best over all 483,840 structured keys | −6.272 |
| null: same sweep on shuffled text (30 reps) | −6.266 ± 0.083 (max −6.093) |
| reference: enciphered real English at n=87 | ≈ −4.20 |

**p = 0.500, z = −0.08.** The best structured key on the real text scores
*exactly at the mean of the shuffled null*. Elgar's documented key structure
gives no traction on the 1897 note whatsoever, and his literal notebook key is
worse than gibberish.

This is the strongest negative in the report, because it is exhaustive rather
than heuristic. Either the 1897 key was structurally unlike the 1920 one, or a
further layer intervenes, or the plaintext is not English.

(Note the two figures are different quantities: −7.705 is the *literal*
decipherment scored as-is, whereas the −4.678 of §4.2 came from letting a free
solver re-permute those symbols over all 24! keys. Both are far below English.)

### 8.4 Two corrections to the supplied material

**The Liszt fragment is not solved.** Thorley's 1977 `GETS YOU TO JOY, AND
HYSTERIOUS` is rejected by both Bauer and Pelling; Pelling transliterates the
fragment as `ABC DECFGB HID CBJKDK` — 3+6+3+6 = **18 symbols** plus a terminal
dash. That resolves the count discrepancy flagged in §7.5: 18 is correct, 25
is the discredited reading, and my 20–24 was over-segmentation at 26 px. The
fragment is a *second short ciphertext*, not a known-plaintext sample.

**The notebook's `DO YOU GO TO LONDON TOMORROW?` line is in a different cipher
system.** Examined at magnification, the marks above and below that line are
short vertical strokes with small flags — not 1–3 arc semicircles. It is
therefore **not** a calibration sample for the arc alphabet. The arc-glyph
lines elsewhere on that page are Elgar practising the alphabet in order, with
no plaintext attached.

With both of these gone, **no known-plaintext sample in the Dorabella arc
alphabet is currently in hand.**

---

## 9. Conclusions, ranked by robustness

### Well supported

**1. The text is not random, and not a melody.** It beats every
meaningless-text null on solver score (percentile 1.00) and sits at the 98th
percentile of the uniform-symbol IC null. Against music: the best of 96
pitch mappings scores *worse* than the sequence's own shuffles (p = 0.903),
and consecutive glyphs are further apart on the rotational dial than chance
(z = +2.25, p = 0.989) — replicated independently on my image transcription
(z = 1.2–2.6 across six variants). **The music hypothesis is disfavoured**
within the mapping families tested.

**2. 87 characters is *not* too short — for simple substitution.** Unicity
distance is ≈ 27 characters, so the text is ~3.2× what uniqueness requires,
and the solver empirically recovers known enciphered English at this length
with 96% accuracy. The folk explanation for the cipher's survival is wrong.

**3. The arc-count channel carries no detectable structure.** Entropy 1.576
against a 1.585 ceiling, distribution 29/33/25. Replicated across the
consensus and my independent transcription (which got arc count 97.7% right).
If loop count encodes anything systematic, it leaves no trace.

**4. No polyalphabetic period.** No Kasiski spacing divisor is enriched above
chance, and row-by-row drift is not significant in any variant (p = 0.07–0.32).

**5. PENNY, MISS PENNY and WOLVERHAMPTON cannot appear in the text.** A
structural fact about doubled symbols, independent of any language model.

### Genuinely uncertain — and now the crux

**6. Whether this is a simple substitution of ordinary English cannot be
settled from surviving sources.** The observed score corresponds to ≈ 8.8%
equivalent glyph error. Round 2 sharpened rather than resolved this:

- The manuscript is lost; all transcriptions descend from one 1937 halftone,
  so absolute error has no measurable ground truth and inter-transcriber
  agreement is inflated by shared-source correlation.
- Tripling image resolution did not improve the orientation estimator at all
  (8-fold quantisation p = 0.104, vs 0.021 before), so better photographs of
  *this* source will not fix it.
- The plate supports only ~86–90% appearance-to-label consistency, i.e.
  10–14% irreducible reading error — the same magnitude as the ~8.8% the
  solver score implies. **The measurement and the effect are the same size.**

Two mechanisms each explain the gap fully, and they are not exclusive:
~9% transcription error, or ~40–50% invented vocabulary. The former is
comfortably inside what the plate exhibits; the latter would mean half the
note is coinages. **Transcription noise is the more parsimonious explanation**,
and period register is *not* — it accounts for only 9% of the gap (§7.3).

**Round 3 removed the counter-argument.** The ~2% figure that supported the
"disfavoured" branch came from consensus-vs-dCode agreement, and dCode is now
proven to be the consensus deciphered under Elgar's own key (§8.2) — not an
independent reading. The only independent estimate is consensus-vs-Schmeh at
9.2%, against a solver-implied 8.8%. Those agree, and both sit inside the
plate's 10–14% ambiguity. The weight of evidence is now that **the gap is
transcription noise**, and that this cannot be pushed further without a
genuinely independent reading of the plate.

**7. Arc count and orientation are not independent** (χ² = 40.18,
MC p = 0.001, Cramér's V = 0.481). I discarded this in my first pass as an
artifact of my own reading — sound reasoning, wrong conclusion, since it
replicates at the same strength on a transcription I had no hand in. It is
real; its meaning is open. The four never-used symbols (`D3`, `E1`, `E2`,
`H3`) are consistent with the inventory being shaped rather than uniform.

**7a. Elgar's own key structure is exhaustively excluded.** All 483,840 keys
in the family his 1920 notebook documents (8 orientation-groups × 3 arc counts,
both layouts) score at the shuffled-text null on the 1897 note — best −6.272
against a null of −6.266 ± 0.083, p = 0.500. His literal notebook key scores
−7.705. Because the search is exhaustive there is no local-optimum escape.
Either the 1897 key was structurally unlike the 1920 one, or a further layer
intervenes, or the plaintext is not English (§8.3).

### Not supported / uninformative

**8. Reversal.** Reversed scores are consistently slightly worse. Note also
that IC, entropy, unigram frequencies and doubled-symbol counts are *exactly*
reversal-invariant, so any "reads backwards" claim resting on them is vacuous.

**9. Sukhotin vowel separation.** Precision 0.56 when calibrated on plain
English at n=87 — barely better than chance. Its output here carries no
information.

**10. All cribs tested.** ALFRED's z = 3.04 does not survive multiple-comparison
correction and still costs 0.20 relative to leaving the solver unconstrained.

### Methodological findings worth carrying forward

**10a. Where transcribers disagree is not where glyphs are ambiguous.** The
12 positions whose consensus label contradicts the nearest-looking glyph are
not enriched among the 20 transcriber-contested positions (Fisher p = 1.000).
Contested-position lists are a poor proxy for genuine illegibility.

**11. The identity-partition metric overstates transcription disagreement by
~10×.** Consensus vs dCode is "20 disputed positions" but only 2 actual glyph
differences. Anyone using disputed-position counts as an error rate will badly
misjudge how uncertain the transcriptions are.

**12. Search budget must be matched between observed and null**, and per-row
scores need *length-matched* nulls. Both errors independently produced
convincing-looking effects in my first pass that vanished on correction. A
27-character row can be forced to read `TSINSTANDASTHINGSAREASURALR` at the
44th percentile of its own null.

**13. Symbol-count proximity is not evidence of transcription accuracy.** My
18 distinct symbols against the true 20 coexisted with 16 misread glyphs.

---

## 10. The single most informative next experiment

**A genuinely independent re-transcription of the plate — by a reader who has
not seen the consensus.** Round 3 showed that what looked like three
independent transcriptions is really two, and the whole crux now rests on a
single pairwise number (consensus vs Schmeh, 9.2%). One more independent
reading would either confirm that ~9% is the plate's real noise floor — closing
the question in favour of transcription noise — or expose the consensus as
better than that, reopening it. Nothing else currently in reach moves the
central question.

Two candidates I previously ranked first have been downgraded by Round 3: the
Liszt fragment is not a known-plaintext sample (Thorley's reading is rejected;
it is an 18-symbol ciphertext), and the notebook's `LONDON TOMORROW` line is in
a different cipher system. **No known-plaintext sample in the arc alphabet is
currently known to exist**, which is itself worth stating plainly.

*Previously recommended, now superseded:*

**A high-resolution image of the 1886 Liszt programme fragment.** My earlier
answer — measure the consensus against a scan of the original — is now known to
be unfulfillable: the manuscript is lost, and Round 2 showed that better
imaging of the surviving plate does not improve orientation reading anyway.

The Liszt fragment replaces it, and is strictly better, because it is the only
**known-plaintext** sample in this symbol system. It would give: a direct read
on Elgar's key construction; ground-truth glyph geometry from ink rather than
halftone, for calibrating the confusion structure; and an independent check on
the claimed 1977 decoding. The image supplied (453×687, cipher column 26 px
tall) is far below what segmentation needs — component counts swing from 5 to
20 across thresholds. Note also that its apparent 20–24 glyphs sit awkwardly
against both the reported 25-letter solution and the "18-character" description;
that discrepancy alone is worth resolving.

Failing that, the honest position is that conclusion 6 is **permanently
conditional**, and effort is better spent on structured-key hypothesis families
(structured alphabet-to-grid layouts, still untested) than on more imaging.

The second experiment, worth building in parallel, is the latent-variable
formulation: joint inference over (glyph labels, key) with the ~20 contested
positions as the only free label variables and per-glyph geometric confidence
as the prior. That search space is small (≤ 2²⁰, far less with
transcriber-attested values only) and it yields a falsifiable output the
discrete ensemble cannot: if the posterior concentrates on one labelling that
*also* clears the null, that is evidence; if it stays flat, the cipher is
provably underdetermined by the available images — itself a publishable
negative.
