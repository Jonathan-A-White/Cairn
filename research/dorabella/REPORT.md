# The Dorabella Cipher: a transcription-noise decomposition and the exhaustive elimination of three key families

**Status: characterisation, not solution.** No plaintext is claimed. Every
positive-looking result is reported against a simulated null, and every solver
comparison uses a matched search budget.

---

## Abstract

The Dorabella cipher (Elgar, 14 July 1897; 87 symbols over an alphabet of
1–3 semicircular arcs in 8 rotations) is analysed with explicit attention to
two failure modes that dominate the amateur literature: hill-climbers that
always produce English-flavoured output at n = 87, and transcription
disagreement mistaken for cryptographic structure.

Four contributions. **(1) A transcription-noise decomposition.** Of the four
transcriptions in circulation, dCode is shown to be a verbatim copy of
Hartmeier and the Zenodo archive to contain only the published consensus, so
the field holds three independent readings, not five. Triangulating those
three yields per-reader error rates — Hartmeier 1.1%, Pelling 3.4%, Schmeh
10.3% — with 74/87 positions unanimous and **zero three-way splits**.
**(2) A bound on what transcription can explain.** Enumerating all 2¹³ = 8192
labellings of the reader-contested positions and solving each shows that even
maximally charitable transcription leaves the decipherment 2.4 sd short of
English. **(3) Exhaustive elimination of three key families** — Elgar's own
documented 1924 geometry (483,840 keys), constant-step additive rotation, and
the transcription-ambiguity space — each with matched-budget nulls.
**(4) One constructive constraint**: Massey's mirror-pair anomaly is
replicated (13 vs 5.15 ± 2.17, p = 0.0018), shown to be incompatible with
Elgar's own key (which predicts 5.70) but compatible with a key built to
mirror common bigrams (ceiling 10.52), which constrains the 1897 key without
condemning the plaintext.

Also reported: 87 characters *exceeds* the unicity distance of simple
substitution (≈ 27), so the cipher's survival is not explained by the text
being too short; the arc-count channel is statistically indistinguishable from
uniform; the music hypothesis is disfavoured; and Thorley's 1977 reading of
the related Liszt fragment is inconsistent with its 18-symbol length.

### Reading guide

| section | content |
|---|---|
| §0–1 | sources, provenance, and how to measure transcription disagreement |
| §2–3 | ciphertext statistics and structural tests, against n = 87 nulls |
| §4 | solving, with positive controls and matched-budget nulls |
| §5–6 | music hypothesis; unicity distance |
| §7–12 | successive rounds: imaging limits, Elgar's key, the archive, the three-reader decomposition, the mirror constraint, rotation and latent sweeps |
| §13 | conclusions ranked by robustness |
| §14 | what would actually move this |

Sections 7–12 are kept in the order the work happened, including two
conclusions that were drawn and later withdrawn (§9 → §10.4), because the
retractions are part of the method.

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

## 9. Round 4 — the Zenodo archive does not contain the raw transcriptions

The Hauer et al. code-and-data archive (DOI 10.5281/zenodo.4819086, 119 MB,
8,709 files) was reassembled and searched exhaustively. **The five source
transcriptions are not in it.**

It contains exactly one Dorabella transcription, appearing in four different
symbol labelings for four different experiments:

| file | agreement with consensus (Fig. 2) |
|------|-----------------------------------|
| `LanguageIdentification/IsDorabellaEnglish/DorabellaTranscription.txt` | **100.0%** |
| `ImpactOfPerplexityMusicVsText/dora1/dora.txt` | **100.0%** |
| `ImpactOfPerplexityMusicVsText/dora2/dora2.txt` | **100.0%** |
| `ImpactOfPerplexityMusicVsText/dora3/dora4.txt` | **100.0%** |

All four are exact relabelings of the published consensus under Hungarian
alignment — identical partitions, different names. Confirmed absent: any file
referencing Schmeh, Pelling, Hartmeier or benzedrine (the only greps that hit
are large English word-frequency tables); any file with 87 lines (per-position
votes); any file using orientation+count tokens; any consensus-building script.

**Consequence for the crux.** The reader-noise floor cannot be estimated from
ten pairwise comparisons, because only one independent reading is in hand
(Schmeh). And that single number is itself **biased low**: the consensus is a
majority vote over five readers *including Schmeh*, so Schmeh agrees with it
more than with an arbitrary independent reader. Consensus-vs-Schmeh at 9.2% is
therefore a **lower bound** on true reader-to-reader disagreement.

Against the pre-registered decision rule — floor ~8–12% favours transcription
noise, ≤4–5% reopens the deficit — the only available estimate is ≥9.2%,
already inside the upper band and able only to rise. **The rule fires for the
transcription-noise branch.** The maximum-parsimony reading of this project is:
*a simple substitution whose plaintext we cannot recover because the surviving
source cannot be read accurately enough*, with the caveat that shared-source
error (a halftone artifact fooling all readers identically) is invisible to any
such analysis and always will be, the manuscript being lost.

### 9.1 Incidental findings from the archive

- The authors' reference corpus is **Letters of Jane Austen** (`LJA.txt`,
  Gutenberg), the same text independently chosen for §7.3 here.
- `CiphertextCharacteristics/Scripts/encodeDorabella.py` encodes the alphabet
  as `1⇑ 1⇗ 1⇒ … 3⇖` — 3 arc counts × 8 directions, matching the structure
  extracted from Elgar's notebook in §8.1.
- The same script contains `isReflection` / `countReflections`, and the archive
  ships `mirroredSymbols.sh`: the authors tested whether adjacent symbols are
  **mirror reflections** of one another. That hypothesis is untested here and
  is a reasonable next probe, being cheap and structurally motivated.

---

## 10. Round 5 — three readers, per-reader error rates, and a reversal

### 10.1 Provenance: "dCode" was never a fourth reader

A screenshot of Hartmeier's benzedrine.ch page shows the letter string
`BPECAHTCKYFRQDRIRRHPPRDXYXGFS / TRTHTCKLCERREHGQTRFRHUSQDXKKXFS /
ESHUSEDUWGSERHUQSDCPGSHCDXC` — character-identical to dCode's. **dCode copied
Hartmeier.** The archive of "independent" sources shrinks again.

The same page also states outright that its letters are a *decipherment under
an "(arbitrary) key"*, not raw glyph names, and describes that key exactly as
extracted in §8.1: "the first symbol is two semi-circles with their open sides
facing east, we pick the second eastern letter, B". Since a fixed key is a
relabeling, the partition analyses are unaffected. The page also quotes Kevin
Jones on the Liszt fragment being an **18-character** code, independently
corroborating Pelling's count over Thorley's 25 (§8.4).

### 10.2 Three genuinely pre-consensus readers, triangulated

Hartmeier (2006), Schmeh (2018), Pelling (2012) all read the plate before the
2021 consensus existed. Aligned to a common labelling by Hungarian assignment:

| pair | disagreement |
|------|--------------|
| Hartmeier vs Schmeh | 10 / 87 = 11.5% |
| Hartmeier vs Pelling | 4 / 87 = 4.6% |
| Schmeh vs Pelling | 12 / 87 = 13.8% |

All three verify exactly as reported. The three-way structure is where it gets
informative: **74 of 87 positions are unanimous, and there are ZERO three-way
splits.** At every one of the 13 contested positions exactly two readers agree
and one dissents — a perfect fit to a model of independent single-reader error,
and a strong internal validation of the triangulation.

That yields per-reader error rates directly:

| reader | dissents | rate | 95% CI (Clopper–Pearson) | positions |
|--------|----------|------|--------------------------|-----------|
| Hartmeier | 1 | **1.1%** | [0.0%, 6.2%] | 33 |
| Pelling | 3 | **3.4%** | [0.7%, 9.7%] | 12, 21, 84 |
| Schmeh | 9 | **10.3%** | [4.8%, 18.7%] | 9, 22, 23, 25, 37, 50, 68, 77, 85 |

**Schmeh is the noisy reader**, by roughly an order of magnitude. This is
independently corroborated by Phase 4: Schmeh's string solved at the null
(−4.948) while the Hartmeier and consensus lineages solved at −4.68 (§4.2).

The 3-reader majority differs from Hartmeier at exactly one position (33).

### 10.3 The bitmap classifier and the human readers agree on where the plate is hard

The 13 reader-contested positions are
`9, 12, 21, 22, 23, 25, 33, 37, 50, 68, 77, 84, 85`. The 12 positions flagged
in §7.2 by a leave-one-out nearest-neighbour classifier on glyph bitmaps — a
method that knew nothing about any reader — are
`0, 4, 9, 15, 21, 23, 24, 33, 36, 68, 71, 77`.

**Six positions overlap: 9, 21, 23, 33, 68, 77. Fisher exact p = 0.0020.**

Two entirely different methods — human transcribers reading a halftone, and a
pixel classifier trained on consensus labels — independently localise the same
glyphs as the hard ones. This substantially raises confidence in both, and it
makes the error budget *position-localised* rather than diffuse. It also
retracts the §7.2 remark that contested positions do not track illegibility:
that was computed against the *transcriber-contested* list, which is now known
to have been contaminated by dCode's non-independence.

### 10.4 Round 4's conclusion does not survive

Round 4 concluded that transcription noise explained the entire solver gap. It
rested on 9.2% (consensus vs Schmeh) as the noise floor. With Schmeh now
identified as a 10.3% outlier against readers at 1.1% and 3.4%, that figure was
inflated by one reader, and the conclusion has to be withdrawn.

### 10.5 The residual deficit, recomputed

Corruption anchors at the rates the three-reader data actually supports, all at
matched solver budget (40 trials per rate). Observed consensus: **−4.680**.

| assumed error rate | expected score | sd | sem | residual deficit | source of the rate |
|--------------------|----------------|----|----|------------------|--------------------|
| 0.0% | −4.229 | 0.143 | 0.023 | **−0.451** | perfect transcription |
| 1.1% | −4.329 | 0.173 | 0.027 | **−0.351** | Hartmeier's rate (≈ consensus) |
| 3.4% | −4.412 | 0.189 | 0.030 | **−0.268** | Pelling's rate |
| 6.2% | −4.616 | 0.223 | 0.035 | **−0.064** | upper 95% CI on Hartmeier |
| 10.3% | −4.695 | 0.210 | 0.033 | **+0.015** | Schmeh's rate — the outlier |

A negative residual means Dorabella scores *worse* than a genuine simple
substitution of English read at that error rate.

If the consensus inherits the accuracy of its best readers — 1–3%, which is
what §10.2 implies — then **a deficit of roughly −0.27 to −0.35/gram
survives**. Round 4's clean "transcription noise explains everything"
conclusion was an artifact of using Schmeh's error rate as if it were the
plate's, and is withdrawn.

**But the deficit is not robust to the uncertainty in that error rate, and
this should not be overstated.** Dorabella is a single draw, so the right yardstick
is the corruption distribution's sd, not its standard error:

| assumed error | deficit | deficit / sd | one-tailed p |
|---------------|---------|--------------|--------------|
| 0.0% | −0.451 | −3.15 | ~0.001 |
| 1.1% | −0.351 | −2.03 | ~0.02 |
| 3.4% | −0.268 | −1.42 | ~0.08 |
| 6.2% | −0.064 | −0.29 | ns |
| 10.3% | +0.015 | +0.07 | ns |

Hartmeier's error rate rests on **one** dissent in 87, so its 95% interval is
[0.0%, 6.2%] — and across that interval the deficit runs from decisive to
absent. The honest statement is: *a deficit of about 2 sd at the point
estimate, decaying to nothing by 6% error.* Suggestive, not established.

### 10.6 Exhaustive latent sweep over the contested positions

With zero three-way splits, every contested position has exactly two candidate
readings — the majority value and the dissenter's — so the latent-variable
model collapses to an enumeration of 2¹³ = 8192 complete labellings. Each is
solved, and the best is compared against the identical best-of-8192 procedure
applied to shuffled text, so the selection effect sits in the null too.

*(running; result to follow)*

### 10.7 The fork this all turns on

Everything above assumes **Pelling read the plate independently of
Hartmeier**. I do not think 4 glyphs of disagreement establishes that, and the
suggestion that it "rules out copying" should be resisted — dCode copying
Hartmeier verbatim is direct proof that copying happens in this literature, and
4 corrections to an inherited transcription is an entirely ordinary amount of
editing.

The two branches diverge sharply:

- **If Pelling is independent:** three readers, errors 1.1 / 3.4 / 10.3%, the
  consensus inherits roughly 1–3% error, and a residual deficit of ~0.3–0.45
  survives. The "plain English, badly transcribed" story weakens and
  second-layer or non-English hypotheses revive.
- **If Pelling derives from Hartmeier:** there are two lineages, not three. The
  H/P agreement measures editing rather than independent reading, and the only
  true independent comparison is lineage-vs-Schmeh at 11.5–13.8% — at which the
  residual deficit vanishes entirely and Round 4 stands.

Two refinements pull in opposite directions and are worth stating rather than
silently netting off. Reader *disagreement* is a lower bound on *absolute*
error, since a glyph all three misread identically is invisible — which makes
the true error higher and the deficit smaller. But §7.4 showed systematic error
is less damaging than random error of the same rate, and transcription error is
systematic — which makes the expected score higher and the deficit larger.

**Resolving Pelling's provenance is now the single highest-value question in
the project**, and unlike every previous "next experiment" it is answerable
from documentary evidence rather than from the plate.

---

## 11. Round 6 — Massey replicated, and what the mirror excess actually implies

### 11.1 One of Massey's two observations replicates; the other does not

Massey (2017) reported two anomalies by eye. Both are testable against
permutation nulls that hold the symbol multiset fixed and randomise only order.

| statistic | observed | null | p |
|-----------|----------|------|---|
| adjacent 180°-opposed pairs, **same arc count** | **13** | 5.15 ± 2.17 | **0.0018** |
| adjacent 180°-opposed pairs, any arc count | 27 | 12.58 ± 3.13 | **0.0001** |
| longest arc-count alternation run | 13 | 10.31 ± 3.00 | 0.19 (ns) |

**The mirror-pair anomaly replicates exactly** — 13 against ~5 expected, which
is precisely Massey's "12–13 versus ~5". Two independent routes (his by eye,
mine via the dial statistic of §5, z = +2.25) find the same thing.

**The alternation-run claim does not survive.** A longest run of 13 sounds
striking against his stated control maximum of 5–6, but a proper permutation
null gives a mean of 10.3 and a maximum of 37: with three near-equal arc-count
classes, long alternation runs are ordinary. That control was wrong.

### 11.2 What the mirror excess implies — a constructive discrimination

The excess is anomalous for monoalphabetic English because plaintext bigrams do
not know the key's geometry. Unless the key was *built* so that common bigrams
land on mirrored symbols. That is quantifiable.

Under Elgar's key (§8.1), the bigrams that become same-arc opposed pairs are
`AN NA BO OB CP PC DQ QD ER RE FS SF GT TG HU UH IW WI KX XK LY YL MZ ZM`.
They carry 6.63% of English bigram mass — dominated by ER (16.1‰), AN (16.0‰)
and RE (14.3‰).

| key | mirror-producing bigram share | expected pairs in 86 slots |
|-----|-------------------------------|----------------------------|
| order-shuffled null | — | 5.15 |
| **Elgar's actual 1920 key** | 6.63% | **5.70** |
| **best possible key** (max-weight perfect matching over letter pairs) | 12.23% | **10.52** |
| share needed to expect 13 | 15.12% | 13 |

The optimal matching pairs `HT, ER, IN, AL, FO, MP, SU, CK, BY, DW, GQ, XZ` —
i.e. a key deliberately arranged so TH/HT, ER/RE and IN/NI fall opposite.

Three conclusions follow:

1. **Elgar's actual key cannot produce the excess.** It predicts 5.70; we
   observe 13, about +2.4 sd. This is independent corroboration of §8.3's
   exhaustive negative, by a completely different statistic.
2. **A bigram-optimised key can.** The best achievable expectation is 10.52,
   and observing 13 against that is +0.8 sd — entirely unremarkable. So
   Pelling's "key crafted so common bigrams mirror" hypothesis **survives the
   test that kills Elgar's own key**.
3. **Massey's hoax/nonsense reading is therefore not required.** The mirror
   excess has a live explanation that keeps the text meaningful. It is evidence
   against *this particular key*, not against language.

No key can reach 15.12% — the theoretical ceiling is 12.23% — so the observed
13 sits slightly above even the optimum's expectation, but well inside its
noise. The mirror statistic constrains the key without condemning the plaintext.

### 11.3 The notebook is 1924 or later, which reframes Round 3

Marco the spaniel was born 27 May 1924, so the "Marco Elgar" page postdates
Dorabella by ~27 years, not 23 — and Pelling reads it as Elgar *reconstructing*
a system he no longer remembered, with `A VERY OLD CYPHER` enciphered on the
same page.

That materially changes how §8.3 should be read. The exhaustive sweep killed
**the reconstructed 1924 geometry**, not the concept of a structured key. If
Elgar's own later recollection was imperfect, failure of that family on the
1897 note is expected rather than damning. §11.2 sharpens this from the other
side: whatever the 1897 key was, it put common bigrams opposite in a way the
1924 geometry does not.

It also means known plaintext in the arc alphabet **does** exist after all —
`MARCO ELGAR` and `A VERY OLD CYPHER` on that page — which retracts the flat
statement in §8.4 that no such sample is known. The arc-count channel test on
those lines remains outstanding.

---

## 12. Round 7 — the additive-rotation family, pre-registered and exhausted

### 12.1 Why this family, and why not the mirror-optimal one

The obvious follow-up to §11.2 — search keys constrained to mirror
high-frequency bigrams — is **circular as scoped**. The constraint is derived
from the observed mirror excess, on the text that exhibits it; scoring such
keys against unconstrained nulls double-counts the evidence. It is not run here.

The additive-rotation family is pre-committed on **documentary** grounds
instead. Elgar owned Schooling's four 1896 *Secrets in Cipher* articles and
solved the Nihilist cipher in the fourth — a Polybius substitution plus an
*additive keyword layer* — fifteen months before Dorabella. (The I=J / U=V
merges of `ALPHA24` are themselves the Polybius-tradition merges.) The dial
analogue, proposed by Pelling in 2009 as the "rotating pigpen", is a
substitution whose orientation and/or arc channel is shifted by a key
advancing per character.

Hypothesis: `cipher_i = plain_i` shifted by `s·i`, on the orientation channel
mod 8 and/or the arc channel mod 3. Decryption un-shifts and solves the
residual as a monoalphabetic cipher. Family size 8 × 3 = 24, enumerated
exhaustively.

### 12.2 Result: the identity is the best member

| rank | orientation step | arc step | score/gram |
|------|------------------|----------|------------|
| **1** | **0** | **0** | **−4.761  (identity — the plain monoalphabetic case)** |
| 2 | 4 | 0 | −5.082 |
| 3 | 2 | 0 | −5.111 |
| 4 | 5 | 1 | −5.175 |
| 5 | 7 | 2 | −5.235 |

**Every non-trivial rotation scores worse than no rotation at all**, by a
margin of 0.32/gram or more. The best-of-family equals the identity, so the
rotation family contributes nothing: there is no constant-step shift that
makes the text more English-like.

Note rank 2 is orientation step 4 — the mirror step, the one that would
manufacture the §11.2 anomaly. Even it is 0.32 worse than doing nothing.

Null, identical best-of-24 procedure on shuffled text, 14 reps: **−4.943 ±
0.060, max −4.855**. Observed best-of-family −4.761, **z = +3.02, p < 0.001**.
So the family-level result confirms §4 — the text beats meaningless text — but
that margin is carried entirely by the identity member. The rotation layer
itself contributes nothing.

**Constant-step rotation is dead.** This is the second documented key family
exhausted, after §8.3. Periodic (multi-character) keys remain untested, and at
n = 87 a period of 4 or more is beyond what the text can support — the unicity
distance for a 2-alphabet polyalphabetic is already 55, and 82 for three (§6).

### 12.3 Exhaustive latent sweep: resolving the contested positions does not rescue it

All 2¹³ = 8192 labellings of the 13 reader-contested positions were enumerated
and solved.

| | score/gram |
|---|---|
| majority-of-three reading | −4.680 |
| **best of all 8192 labellings** | **−4.613** |
| median of 8192 | −5.021 |
| worst of 8192 | −5.423 |
| enciphered real English (reference) | ≈ −4.20 |

Cherry-picking the single most favourable resolution of every contested glyph —
an 8192-fold selection, and far more freedom than any honest transcription
would grant — buys **0.067/gram**, and lands 2.4 sd short of the English band.
The best labelling's plaintext is still gibberish.

So the transcription ambiguity that Rounds 5–6 localised, even resolved
maximally favourably, does **not** account for the deficit. This is the
strongest available answer to "would a perfect transcription solve it?": within
the space the three readers actually disagree over, no.

Two runs were made. A thorough scan (3 restarts × 4000 iters per labelling)
found a best of **−4.613**; a cheaper matched-budget rerun (1 × 2500) found
**−4.686**, having missed the better mask — the cheap scan is noisier, so
−4.613 is the better estimate of the true best-of-8192.

The matched-budget null was interrupted by a container restart after 2 of 8
reps: **−4.841, −4.927**, both below the observed −4.686. Indicative but not a
completed null, and reported as such. The section's conclusion does not rest on
it: the comparison that matters is absolute — even the best of 8192 labellings
falls 2.4 sd short of the English band, and its plaintext is gibberish.

---

## 13. Round 8 — the homophonic family, and the limit of what a quadgram score can decide

### 13.1 Provenance note

Schooling's *Secrets in Cipher* I **is** on archive.org
(`sim_pall-mall-magazine`, vol. VIII, 1896, pp. 119–129), contrary to the
report that the series is unavailable there. Article I is a survey of
historical systems, and it documents one directly relevant construction:
"underneath each of the letters of the alphabet are written three, sometimes
four, peculiar marks … the writer made use of any one of these three marks to
represent a letter." That is **homophonic substitution**, in Elgar's
possession fifteen months before Dorabella. It is pre-registered here on the
same documentary footing as the rotation family, and it was the one documented
family thought recoverable in principle at this length — §6 puts its unicity
distance at 35.2 against 87 available, versus 55 for a 2-alphabet
polyalphabetic.

### 13.2 The family cannot be tested at n = 87

A non-injective solver (many cipher symbols may share a letter) has strictly
more freedom than the injective one, so it scores higher on everything. All
rows below use the identical solver and budget — 25 restarts × 18,000 iters.

| | score/gram |
|---|---|
| **Dorabella (consensus)** | **−3.942** |
| homophonically-enciphered English (positive control) | −4.012 ± 0.054 |
| shuffled Dorabella (null) | −4.029 ± 0.077 |
| **uniform random symbols (null)** | **−4.017 ± 0.047** |

**All four coincide.** Genuine homophonic English (−4.012) and uniform random
noise (−4.017) are indistinguishable. The solver cannot tell a real message
from nothing at all, so it certainly cannot adjudicate Dorabella. The
observed "96th percentile against the null" and "+1.28 sd above the English
control" are artifacts of that collapse and carry no information.

The homophonic hypothesis is therefore **untestable at this length, not
rejected.** Contrast the injective case, where the same machinery separates
English (−4.20) from meaningless text (−5.01) by 0.81/gram, and recovers known
plaintext at 96% accuracy.

### 13.3 What this says about unicity distance

This is the sharpest methodological result in the report, and it corrects a
natural misreading of §6. The analytic unicity distance for the homophonic
family is 35.2, comfortably under 87, which says a unique key *exists* given
unlimited computation and a perfect model of English. The empirical test shows
a quadgram score cannot *find* it at this length — the added key freedom
absorbs the text's redundancy faster than the statistic can exploit it.

**Unicity distance bounds uniqueness, not discriminability.** Every "the
cipher is long enough in principle" argument in this literature — including
the one in §6 that opens with 87 exceeding simple substitution's 27 — needs
this caveat attached. It holds for simple substitution because that was
verified empirically by positive control; it does not transfer to richer
families merely because their unicity numbers are also below 87.

### 13.4 Consequence for the surviving hypotheses

Three families are now exhausted (§8.3, §12.2, §12.3) and a fourth is shown
untestable. The probability mass that would otherwise flow to "homophonic, and
we simply have not found the key" must instead be recorded as **unresolvable
with these methods at this length** — which is a different and more honest
resting place than either acceptance or rejection.

---

## 14. Round 9 — Schooling Article II, and the notebook's second cipher identified

Article II (*Pall Mall Magazine* vol. VIII, pp. 245–256) is now in hand.
Articles III and IV remain outstanding.

### 14.1 No. 30 — Charles I's shorthand cipher — matches the notebook's stroke line

Page 256 reproduces "King Charles the First's Shorthand Cipher, written by the
King himself": the alphabet written along a horizontal rule, with **dots and
dashes placed above or below the line** denoting each letter. Schooling's text:
"the dots and dashes, placed above or below a line, which were employed to
denote the letters of the alphabet."

In §8.4 I reported that the notebook's `DO YOU GO TO LONDON TOMORROW?` line is
**not** in the arc alphabet but in a different system of "short vertical strokes
with small flags". Measuring that line now: the plaintext letters occupy
y 196–206, with marks confined to y 181–195 **above** and y 207–215 **below**,
and each position carries ink on one side or the other — almost never both.
That is No. 30's structure exactly: one mark per letter, above or below a rule.

**Qualitatively this identifies the notebook's second cipher as Charles I's
shorthand system from Schooling Article II.** The significance is the one
proposed: Elgar was copying *specific printed systems* out of Schooling into
the exercise book, which raises the prior that the arc alphabet also follows a
printed model and promotes Articles III–IV from background to primary-source
key candidates.

**But the decisive decode is not achievable from the available image.** The
known plaintext contains nine `O`s, so a correct reading must place identical
marks at all nine — a test that needs no key. It cannot be run here:
segmenting the line yields 27 blobs for 23 letters, and the marks themselves
are 1–5 pixel features. A zoomed capture of the notebook line, and of the
No. 30 strip on p. 256, would settle it either way. **Reported as a structural
match, not a confirmed decipherment.**

### 14.2 No. 19 — the sliding-card cipher — as the documented model for the dots

Article II also describes a 24-letter sliding-card system (J and U omitted)
whose card position is changed at intervals mid-message, each change signalled
**in-band by a numeral marking the new setting**. This is the only construction
encountered anywhere in this project that *predicts* Dorabella's anomalous dots
rather than explaining them away, and it mechanically produces the sectional
heterogeneity that Pelling, Massey and §3.2 have each noticed by different
routes.

It is **not swept**, and deliberately so: §6 puts a 2-alphabet polyalphabetic's
unicity distance at 55 and a 3-alphabet's at 82 against 87 available, so a
sectional system with 2–3 segments is underdetermined at this length. Sweeping
it would be fitting noise by construction — the same objection that retired the
mirror-constrained search in §12.1. It is recorded in the surviving-hypotheses
list with documentary weight, not tested.

### 14.3 The Two-Word Square eliminated on parity

Article II's 1627 Two-Word Square (OPTIMVS/DOMINVS) is digraphic: each plaintext
letter becomes two ciphertext letters, so any ciphertext it produces has even
length. Dorabella has **87** symbols. Eliminated.

### 14.4 Ledger

Families exhausted: Elgar's 1924 geometry (§8.3), constant-step rotation
(§12.2), transcription-ambiguity space (§12.3). Shown untestable at n = 87:
homophonic (§13.2). Eliminated on structure: digraphic (§14.3). Recorded but
untestable in principle: sliding-card / sectional polyalphabetic (§14.2).
Outstanding and pre-registerable: Article III's music cipher — 12 + 12 notes
over 24 letters with I/J and U/V merged, the closest printed analogue to a
two-factor 24-symbol design yet identified.

---

## 15. Round 10 — Article III, and an adversarial test of the dial thesis

### 15.1 Two documentary claims that do not survive checking

Article III (pp. 453–461) is in hand. Two specific structural claims made
about it are **not supported by the primary source**:

- The music cipher (No. 41, p. 459, George II era) is described on p. 460 only
  as "composed by substituting the specified musical notes for the letters of
  the alphabet which are written underneath the notes." There is **no 12 + 12
  quarter/eighth-note structure and no I/J or U/V merge stated.** The claim
  that this is a 24-letter two-factor design with Elgar's exact merges is not
  in the text; it may be inferable from the facsimile, which is not legible at
  the resolution available.
- The series was reported unavailable on archive.org; it is there
  (`sim_pall-mall-magazine`, vol. VIII).

Both are recorded because the documentary thread has been the strongest part
of the collaboration and its error rate matters. What *is* confirmed on p. 460
is a motive rather than a mechanism: the musical cipher's stated advantage is
"not attracting suspicion, because this cipher might very well pass for being
merely the copy of a few bars of music … sent away to a similarly gifted
friend." Suggestive for a composer writing to a young friend — but Dorabella
is not musical notation, so it bears on motive only.

Nos. 34–37 (revolving dial and ladder) and No. 31 (Foreign Office syllable
cipher) are as described. The dial device is genuinely documented, genuinely
rotating, and genuinely changes key mid-message.

### 15.2 The adversarial test: are the surviving hypotheses distinguishable?

Before adopting a dial/sectional thesis, the question is whether that reading
is *distinguishable* at n = 87 from its rivals, or merely compatible like
everything else. Four generative models were simulated, 40 samples each, over
the 8 × 3 grid:

| model | construction |
|-------|--------------|
| MASC | simple substitution of English, random key |
| DIAL | sectional polyalphabetic, 2–3 sections, key changed mid-text |
| MIRROR | simple substitution whose key mirrors common bigrams (§11.2) |
| COMPOSITE | part MASC English, part random "decoration" |

Features: IC, entropy, doubles, repeated bigrams, mirror-pair count, across-row
IC spread, distinct symbols, and best injective solver score at matched budget.

**They are distinguishable.** Random-forest, 5-fold cross-validated:

| comparison | accuracy | chance |
|---|---|---|
| 4-way | **0.669 ± 0.058** | 0.250 |
| MASC vs DIAL | 0.900 | 0.500 |
| MASC vs MIRROR | 0.938 | 0.500 |
| MASC vs COMPOSITE | 0.787 | 0.500 |
| DIAL vs MIRROR | 0.925 | 0.500 |
| DIAL vs COMPOSITE | 0.600 | 0.500 |
| MIRROR vs COMPOSITE | 0.950 | 0.500 |

So the "nothing at n = 87 can separate them, rank by documentary weight alone"
branch does **not** fire. The statistics have power here, and the only weak
pair is DIAL vs COMPOSITE (0.600) — which makes sense, since both are
heterogeneous-by-construction.

### 15.3 Where Dorabella actually falls — against the thesis

Dorabella's feature vector in pooled-sd units from each model's mean:

| feature | Dorabella | vs MASC | vs DIAL | vs MIRROR | vs COMPOSITE |
|---------|-----------|---------|---------|-----------|--------------|
| IC | 0.059 | −0.76 | +0.60 | −0.87 | +0.30 |
| entropy | 4.030 | +0.58 | −0.89 | +0.65 | −0.66 |
| repeated bigrams | 19 | −0.01 | +1.28 | +0.03 | +0.96 |
| **mirror pairs** | **13** | **+2.58** | **+2.46** | **+0.66** | **+2.78** |
| row-IC spread | 0.011 | +0.36 | +0.09 | +0.34 | −0.08 |
| solver score | −4.823 | −0.95 | +0.58 | −0.97 | +0.17 |

Classifier posterior over the four models, fresh 160-sample fit:

| model | posterior |
|-------|-----------|
| **MIRROR** | **0.851** |
| MASC | 0.070 |
| **DIAL** | **0.052** |
| COMPOSITE | 0.026 |

Feature importances: mirror 0.253, solver 0.179, entropy 0.145, IC 0.108.

**The dial thesis is the least supported of the four readings, at 5%.** The
decisive feature is the mirror count: at 13, Dorabella sits +2.5 sd above MASC,
DIAL and COMPOSITE alike, but only **+0.66 sd** above the mirror-key model.
A sectional dial does not predict adjacent-symbol rotational opposition — that
was the one anomaly the thesis claimed to explain, and it does not.

The honest complication is that no single model reproduces Dorabella's *joint*
profile. Mirror count points at MIRROR; solver score points the other way
(−0.97 sd below MIRROR's mean, but +0.58 above DIAL's). Dorabella has MIRROR's
mirror excess **and** DIAL's solver deficit, and none of the four models
generates both at once.

### 15.4 A caveat that partly rescues the thesis, stated plainly

The DIAL simulation used **independent random keys per section**. A real
revolving dial rotates a *single* alphabet, so its section keys are related by
rotation, not independent — a more constrained model that would preserve more
structure than what I simulated. The 0.052 posterior therefore applies to
sectional-polyalphabetic-with-independent-keys, and may understate a true
rotating-dial device.

Against that: §12.2 swept constant-step rotations exhaustively and found the
identity best by ≥0.32/gram, including step 4 — the very rotation that would
manufacture the mirror excess. Both routes point away from rotation as the
mechanism behind the anomaly.

### 15.5 Consequence for the write-up

The proposed organising thesis — "Dorabella is unsolved because its author
studied a cipher class that is information-theoretically unrecoverable at this
length" — is elegant and documentarily well-supported, but the ciphertext
statistics do not support it over the alternatives, and actively favour a
different one. Adopting it would mean weighting documentary evidence over
measurement in the one place where measurement turned out to have power.

The defensible framing is narrower and, I think, better: **the mirror-key
simple-substitution reading is the best-supported of the tested models
(posterior 0.851), it is the only one consistent with the strongest anomaly in
the ciphertext, and no tested model reproduces the observed profile in full.**
The dial family stays in the surviving list on documentary grounds, explicitly
flagged as favoured by provenance and disfavoured by statistics.

---

## 16. Round 11 — the transposition family, and the joint-profile puzzle survives

### 16.1 The Heraldic cipher is the printed model for the arc alphabet

Article IV, Nos. 48–49 (p. 613): a shield divided into compartments, alphabet
of 24 with J and V omitted, two or three alphabet-consecutive letters per
compartment, each letter denoted by **the angle of its compartment plus one,
two or three tick marks**.

That is the Dorabella design: orientation plus 1–3 arcs, 24 letters,
consecutive triplets per orientation. It is also exactly the structure of
Elgar's 1924 notebook key (§8.1). The design-source question is closed as
firmly as it can be.

The cryptological consequence is neutral-to-negative for new hypotheses,
however: the Heraldic cipher is a plain monoalphabetic substitution, and
§8.3 already swept all 483,840 standard-alphabet layouts of that geometry.
The one variant not covered is **keyword-mixed alphabets** laid into the
triplet geometry — small and pre-registerable, and a natural generator of the
mirror structure without Elgar designing for it. Not run here.

### 16.2 Transposition — a documented family nobody had swept

Article IV, No. 46 (Pack of Cards): message written down columns, order
restored by rhyme — columnar transposition, in Elgar's library. Neither this
report nor, as far as can be established, any published analysis has tested it.

Its predicted signature matches the observation better than anything yet
proposed: transposition leaves **single-symbol frequencies untouched** (which
is why Dorabella's look English-like) while **destroying bigram and quadgram
structure** (the solver deficit). And unlike the dial it stays inside the
unicity bound — verified here: MASC 87.4 bits → 27.3 characters; adding
columnar column-order entropy for k ≤ 8 (≤ 15.3 bits) gives a joint unicity
distance of **32.1 against 87 available**. Recoverable in principle.

**Result.** 21 permutations (columnar k = 2–8 with identity and reversed
column orders, plus route variants over the 29/31/27 line structure), each
un-transposed then MASC-solved at matched budget:

| | score/gram |
|---|---|
| identity (no transposition) | −4.838 |
| **best of family** (`reverse`) | **−4.759** |
| null: identical best-of-21 on shuffled text, 10 reps | −4.915 ± 0.050 (max −4.824) |
| enciphered real English | ≈ −4.20 |

Observed z = +3.13 against the null — **but that margin is carried by the
identity member**, which §4 already established beats meaningless text. The
gain *from transposition itself* is 0.079 over identity, from 21 tries, against
a null sd of 0.050: about 1.6 sd of pure selection. And the best member remains
0.56 below the English band.

**Transposition does not rescue the decipherment.** That the `reverse`
permutation topped the list is worth one sentence and no more — at full budget
§4.2 found reversal consistently *worse* than forward across every variant, so
this is selection noise, not support for the reads-backwards literature.

**Scope caveat, stated because this report's other sweeps were exhaustive and
this one is not.** A complete columnar sweep would enumerate all *k*! column
orderings (46,232 for k ≤ 8); I tested a documented subset of 21. §8.3 and
§12.2 were genuinely exhaustive; **§16.2 is not**, and a full sweep remains
open.

### 16.3 The fifth model: TRANS added to the classifier

The Round-10 puzzle was that no model generated both the mirror excess and the
solver deficit. TRANS+MASC was the obvious missing candidate. Adding it:

5-way CV accuracy **0.560 ± 0.012** against 0.200 chance — still discriminating.

| model | posterior for Dorabella |
|-------|-------------------------|
| **MIRROR** | **0.722** |
| MASC | 0.116 |
| TRANS | 0.056 |
| DIAL | 0.054 |
| COMPOSITE | 0.052 |

TRANS does not win, and the reason is precise. Its mirror-pair mean is 3.575 —
Dorabella sits **+2.82 sd** away — while its solver mean is −4.832, which
Dorabella matches at **+0.32 sd**. So transposition reproduces the solver
deficit and **not** the mirror excess, the mirror image of MIRROR's failure
(+0.91 sd on mirrors, −0.88 sd on solver).

**The joint-profile puzzle survives an expanded model set.** Across five
generative models, none produces both of Dorabella's distinguishing features
at once. MIRROR remains the best single account at 0.722, having now survived
a harder test — but "best of five imperfect models" is the correct description,
not "identified".

---

## 17. Round 12 — the mirror pairs are not clustered, and the puzzle turns out to be structural

### 17.1 The position test: no clustering

Pre-registered by the literature rather than by this report: Massey observed
that the mirror pairs and the alternation runs occupy disjoint stretches, and
Pelling (2020) flagged "the cluster of mirror pairs at the end of the middle
line" as candidate padding, proposing its excision before solving. Under a
mirror-key MASC the pairs should track high-mass bigrams and be roughly
uniform; under a composite/decoration reading they should cluster.

The 13 pairs sit at adjacency positions
`12, 27, 38, 40, 49, 52, 54, 56, 58, 62, 71, 73, 78` — 2 in line 1, 7 in line
2, 4 in line 3, with five of them in positions 49–58. That looks exactly like
the reported cluster.

It is not one.

| test | observed | null | p |
|------|----------|------|---|
| max pairs in any 12-wide window | 5 | uniform placement of 13 points: 4.26 ± 0.78 | **0.33** |
| max pairs in any 12-wide window | 5 | shuffled sequence, conditioned on 11–15 pairs: 3.95 ± 0.77 | **0.20** |
| KS against uniform | D = 0.294 | — | **0.17** |

**Thirteen points scattered at random across 86 slots produce a five-in-twelve
window as a matter of course.** The apparent cluster at the end of line 2 is
what randomness looks like at this density.

This is the third human visual observation in this cipher's literature to fail
a proper null, after Massey's alternation-run claim (§11.1, p = 0.19) and the
run-length control that accompanied it. The one visual observation that *has*
survived is the mirror excess itself (p = 0.0018) — which is a reminder that
the eye is good at detecting that something is unusual and unreliable at
saying what.

### 17.2 The excision experiment is declined

Pelling's proposed excision — remove the mirror-dense region, re-solve the
remainder — was the one procedure on the table that could have produced a
partial decipherment, since ~70 characters is above the empirically validated
recovery threshold of §4.1.

It is not run, for two reasons that would each be sufficient. There is no
statistically real cluster to excise (§17.1). And the excision window would be
chosen by inspecting the data, so any improvement would be the §12.1
circularity in a new costume — with the added hazard that removing 18 symbols
from 87 raises the null for *any* window, as §4.3's length-matched row nulls
already demonstrated.

### 17.3 The sixth model: pre-registered, and it fails where it was built to succeed

MIRROR + light transposition was declared in advance with falsification
targets, precisely because it is assembled from the two features it is meant
to explain. Judged on six held-out features:

| feature | Dorabella | model mean | z | verdict |
|---------|-----------|------------|---|---------|
| IC | 0.059 | 0.065 | −0.76 | pass |
| entropy | 4.030 | 3.960 | +0.51 | pass |
| doubles | 4 | 5.000 | −0.48 | pass |
| repeated bigrams | 19 | 14.625 | +0.97 | pass |
| row-IC spread | 0.011 | 0.012 | −0.12 | pass |
| distinct symbols | 20 | 19.400 | +0.37 | pass |
| *mirror pairs* | *13* | *5.775* | *+1.89* | **(assembled — FAILS)** |
| *solver* | *−4.806* | *−4.916* | *+0.30* | *(assembled — matches)* |

The automated verdict printed PASS on 6/6 held-out features. **That verdict is
wrong and is overridden here.** The model reproduces the solver deficit and
**not** the mirror excess — its mirror mean is 5.775 against Dorabella's 13,
barely above the shuffled baseline of 5.15. It fails on one of the two features
it was specifically constructed to capture.

### 17.4 Why — and this is the round's actual finding

The failure has a cause, and the cause resolves the puzzle's status.

**Mirror-pair excess and transposition make incompatible demands on
adjacency.** Mirror pairs are a property of *which symbols sit next to which*:
a mirroring key produces them only because common plaintext bigrams remain
adjacent in the ciphertext. Transposition's entire mechanism is the destruction
of that adjacency. Composing the two therefore cannot preserve both — the
transposition step scrambles away the mirror structure the key created, which
is exactly what the simulation shows.

So the Round-10 puzzle upgrades from *unexplained* to *structurally
constrained*: Dorabella's two distinguishing features pull in opposite
directions on the same underlying property. Any model that reproduces both
needs a mechanism that **preserves plaintext adjacency** (to keep the mirrors)
while **destroying n-gram fitness** (to depress the solver) — and substitution,
transposition, and their composition each fail one half by construction.

Six-way posterior: MIRROR 0.376, MIRROR_TRANS 0.368, DIAL 0.082, COMPOSITE
0.072, MASC 0.062, TRANS 0.040. MIRROR remains the best single account, now on
a near-tie with a composed model that does not actually do its job.

### 17.5 What this leaves

The surviving space is narrower and better characterised than at any earlier
point. A mechanism preserving adjacency while depressing n-gram fitness would
be: a plaintext that is not ordinary English (idiolect, coinage, abbreviation —
§7.4 measured the required dose at 40–50%, implausible but not impossible), or
a substitution key we have not guessed that both mirrors common bigrams and
maps them unfavourably for a quadgram model. Both remain untested and neither
is currently distinguishable from the other at n = 87.

*(Keyword-mixed Heraldic sweep not run. If attempted, note that `ENIGMA` must
be excluded as a candidate keyword — the Variations postdate the July 1897
note by roughly two years.)*

---

## 18. Round 13 — the edition ensemble, and what it can and cannot measure

Both memoir editions were obtained: the 1937 first edition appendix plate and
the 1947 OUP second edition, the latter carrying Dora's September 1946
addendum ("Nobody, so far as I am aware, has yet succeeded in reading it").

### 18.1 A framing limit, before any measurement

Both plates descend from the **same lost original photograph**. Differences
between them are therefore *reproduction* noise — screening, printing,
scanning — added downstream of the original. A cross-edition comparison bounds
that downstream noise; it **cannot** bound the original photograph's own
limitations, which is where §7.2's 10–14% appearance ambiguity lives. The
hoped-for clean split of "measurement noise vs reader noise" is thus narrower
than it first appears: the measurement half is only the part introduced after
1937.

### 18.2 The 1937 plate segments cleanly, and yields a dot inventory

Connected components at fixed threshold:

| line | components | expected |
|------|-----------|----------|
| 1 | 30 | 29 |
| 2 | 31 | 31 |
| 3 | 28 | 27 |
| **total** | **89** | **87** |

The two extras are isolated small marks, and they separate unambiguously by
size — line 1's smallest component is 14 px against a next-smallest of 101,
line 3's is 22 against 94:

| line | position | size | location |
|------|----------|------|----------|
| 3 | ordinal 6 | 22 px | 21% across the line |
| 1 | ordinal 24 | 14 px | 81% across the line |
| 2 | — | — | **none** |

The line-3 mark at ordinal 6 **matches the documented dot** (reported as line 3,
char 5/6). Line 2 carries **no** anomalous mark in the 1937 plate, consistent
with the second dot being a later-edition artifact rather than an original
feature.

The line-1 mark at ordinal 24 is recorded as observed but uncertain: at 14 px
it is at the scale of a print speck or scan noise. Inspected at magnification
it is a small dot sitting **below the baseline**, between glyphs.

### 18.2a Cross-edition persistence of the line-3 dot

A zoomed capture of the 1947 plate settles the more important half of this.
Although §18.3 shows the 1947 image cannot be segmented automatically, the
line-3 dot is **plainly visible by eye** in it: sitting between the fifth and
sixth glyphs, in the same dark ink tone as the glyphs themselves and clearly
distinct from the grey pencil numerals above.

This matters more than the automated count. **A print speck would not survive
independent re-screening for a new edition.** The line-3 dot appearing in both
the 1937 and 1947 plates is therefore good evidence that it is a feature of the
original note rather than a reproduction artifact — which is the first direct
support for treating it as intentional, and the strongest thing the edition
ensemble has produced.

The line-1 sub-baseline mark is **not** resolvable in the 1947 capture. That is
inconclusive rather than refuting: at 2–3 px in a blurred sepia JPEG, a mark of
that size would be lost regardless of whether it is there. Its status is
unchanged — observed in 1937, unverified elsewhere.

Summary of the dot inventory:

| mark | 1937 | 1947 | verdict |
|------|------|------|---------|
| line 3, between glyphs 5–6 | present | **present** | original feature, cross-edition |
| line 1, sub-baseline at ordinal 24 | present | not resolvable | unverified |
| line 2 | absent | absent | no support for a second dot |

### 18.3 The 1947 plate is not usable at this resolution

| | components (lines 1/2/3) | median component size |
|---|---|---|
| 1937 | 30 / 31 / 28 | ~190 px |
| 1947 | 50 / 50 / 50 | ~27 px |

The 1947 capture yields 150 components against 87 glyphs. The cause is
twofold: a previous library borrower has pencilled symbol numbers above the
cipher lines, and the fainter sepia print has fragmented the ink itself.
Critically, **no size threshold separates the two** — filtering at 40 px drops
to 32 components, at 60 px to 21, because genuine glyph strokes have broken
into pencil-scale fragments. The print and the annotation occupy the same size
regime.

**The cross-edition glyph-level comparison cannot be performed from these
captures.** It is not attempted, and no cross-edition disagreement figure is
reported. Both images are phone screenshots of a lending-library viewer, at
roughly a quarter the linear resolution of the plate scan already analysed in
§7. A direct high-resolution capture of the 1947 plate would make the
measurement possible; these do not.

*(The borrower's pencilled numbering is itself a stranger's partial
transcription attempt, in a public library copy. It does not appear to reach
87.)*

### 18.4 Textual variants, now citable from the primary source

| | 1937 first edition | 1947 second edition |
|---|---|---|
| recipient | "a letter from the Lady to my **mother**" | "to my **stepmother**" |
| cross-reference | "(see p. 9)" | "(see p. 7)" |

Dora's mother died days after her birth, so the first edition misstates the
recipient and 1947 corrects it. Cryptanalytically irrelevant, but it is direct
evidence that **the editions were actively revised**, which supports the
premise that the plates were not mechanically identical either — and makes the
1949 Methuen third screening worth obtaining if it surfaces.

Also now citable from the source rather than at second hand: "the third letter
I had from him, if indeed it is one", and Dora's statement that Elgar never
explained it and that all attempts to solve it had failed.

---

## 19. Conclusions, ranked by robustness

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

## 20. The single most informative next experiment

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
