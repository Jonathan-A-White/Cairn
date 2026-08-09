# The Dorabella Cipher: a transcription-noise decomposition and the exhaustive elimination of two key families

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
English. **(3) Exhaustive elimination of two key families** — Elgar's own
documented 1924 geometry (483,840 keys) and constant-step additive rotation —
each with matched-budget nulls, plus a homophonic family shown *untestable*
rather than rejected, a digraphic family eliminated on parity, and a
transposition family swept only in part (21 of 46,232 orderings, flagged).
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
| §23–28 | the fresh-eyes phase: audit, then four experiments — see §28 for the revised ledger |

Sections 7–19 are kept in the order the work happened, including two
conclusions that were drawn and later withdrawn (§9 → §10.4), because the
retractions are part of the method.

**Reading this repository:** `README.md` maps every headline number to the
script that produced it and states the seven standing methodological rules.
`TODO.md` carries five open items with priors attached — item 5 is a caveat on
§19 that is load-bearing and easy to misread. `sources/PROVENANCE.md` documents
the image captures and their resolution limits.

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

**Result reported in §12.3** (it completed after Round 7). In brief: best of
8192 = −4.613, against −4.680 for the majority reading — a gain of 0.067 from
an 8192-fold selection, still 2.4 sd short of English. The matched-budget null
was interrupted at 2 of 8 reps and is flagged there as incomplete.

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

*(Audit note, §23: this table was computed inline in Round 6 and had no
committed script. Re-derived in `scripts/audit_phase0.py`, every entry
reproduces exactly except the ceiling, which comes back at **12.19% → 10.48**
rather than 12.23% → 10.52. The optimal matching is identical letter-for-letter,
so the 0.045pp gap is in the bigram normalisation of a computation that no
longer exists to be inspected. It does not move the conclusion below: 13
against 10.48 is +0.83 sd where 13 against 10.52 is +0.82.)*

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

Two **key families** are now exhausted (§8.3 Elgar's 1924 geometry, §12.2
constant-step rotation), the **transcription-labelling space** has been
enumerated (§12.3, though its null was interrupted), and a third family is
shown untestable. The probability mass that would otherwise flow to "homophonic, and
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

Key families exhausted: Elgar's 1924 geometry (§8.3), constant-step rotation
(§12.2). Labelling space enumerated (not a key family): transcription
ambiguity (§12.3). Shown untestable at n = 87:
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

**The line-1 sub-baseline mark is absent from the 1947 plate.** A
high-magnification capture of the right-hand portion of the lines resolves this
properly. The comparison is anchored to content rather than coordinates: the
visible glyph run `3 3 w a v ᶶ ᶜ` is the same sequence in which the 1937 mark
appears, so the same stretch of the line is being inspected in both. The line-1
glyph band ends cleanly at its baseline with **zero ink below it**, and at a
magnification where the pencil numerals are legible and the glyph strokes crisp,
a 2–3 px mark would be conspicuous.

So the two anomalous marks behave oppositely across editions, and that is what
makes the ensemble useful:

| mark | 1937 | 1947 | verdict |
|------|------|------|---------|
| line 3, between glyphs 5–6 | present | **present** | **original feature** |
| line 1, sub-baseline at ordinal 24 | present | **absent** | **1937 print artifact** |
| line 2 | absent | absent | no support for a second dot |

The full glyph-level cross-edition comparison was not achievable (§18.3), but
the ensemble adjudicates individual marks cleanly, because the logic is
asymmetric and does not need segmentation: **a mark surviving an independent
re-screening is on the original; a mark appearing in one screening only is an
artifact of that screening.** That disposes of the line-1 mark I raised last
round — it was a print speck, exactly as its 14 px size suggested — and
promotes the line-3 dot from "documented" to "physically corroborated".

By the same argument, the reported second dot in the 1949 Methuen plate, absent
from both editions examined here, is more likely a 1949 screening artifact than
a recovered original feature. The line-2 region is the specific thing to
inspect if that edition surfaces.

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

## 19. Round 14 — the primary source, and Elgar's measured register

### 19.1 Source inflation: the Schooling story is one sentence

Buckley's *Sir Edward Elgar* (1905) is the primary source for Elgar's
cryptographic interests, cited throughout the secondary literature. An
exhaustive search of the full 3,869-line text for `cipher | cryptogram |
Schooling | puzzle | enigma | secret | anagram` returns exactly **one** passage
on the subject, at p. 41:

> "During railway journeys amuses himself with cryptograms; solved one by John
> Holt Schooling who defied the world to unravel his mystery."

That is the complete content. **No index cards, no wooden box, no "working in
the dark", no 1896 date, no identification of which cipher.** Every one of
those details entered the record through later authors and museum artifacts,
not through the biography they are attributed to.

What the primary source establishes: Elgar solved a Schooling challenge, and
was proud enough of it to tell his biographer. What it does not establish:
method, date, or which of the four articles' challenges. The report's earlier
sections should be read with that distinction in place — §12.1's documentary
motivation for the rotation family survives (Elgar demonstrably engaged with
Schooling), but the specific "Nihilist cipher, 1896" framing does not come from
Buckley.

**This is the third secondary claim in this project to fail a primary check**,
after the music cipher's "12 + 12 notes with I/J and U/V merges" (§15.1, not in
the text) and Thorley's Liszt solution (§8.4, 25 letters against 18 symbols).
The pattern is consistent: a modest primary fact accretes specificity as it
passes through hands that do not cite pages. Given that this report has spent
fourteen rounds applying null distributions to statistical claims, applying the
same scepticism to documentary ones is not optional — **source inflation in the
Dorabella literature is a finding, not a footnote.**

*(One incidental primary fact worth keeping, p. 40: Elgar's house name "Craeg
Lea … conceals an anagram". Documented wordplay in his own hand, contemporary,
and relevant to §7.4 — it establishes that Elgar played this kind of game,
without saying anything about how far he played it.)*

### 19.2 Elgar's register, measured — and the idiolect branch closes

§7.4 established that explaining Dorabella's solver deficit by unusual language
alone would require 40–50% coined vocabulary, but that was a simulation with no
empirical anchor. Buckley supplies one: his introduction states that "the
sayings of Elgar are recorded in the actual words addressed directly to the
writer", and the book quotes him verbatim throughout.

Method identical to §7.3 — language model held fixed (modern quadgram), only
the register varied, scored per-quadgram over 87-character windows:

| text | windows | mean | sd |
|------|---------|------|-----|
| **Elgar, quoted verbatim** | 238 | **−4.219** | 0.151 |
| Buckley chs. IV–V (Elgar's conversation, reported) | 3225 | −4.249 | 0.167 |
| Buckley, whole book (1905 prose) | 4936 | −4.277 | 0.228 |
| modern English (reference) | 600 | −4.240 | 0.135 |
| Austen letters (reference) | 600 | −4.271 | 0.161 |
| **Dorabella (consensus, solved)** | — | **−4.680** | — |

**Elgar's documented register is statistically indistinguishable from ordinary
English — and if anything marginally *more* ordinary, at +0.021 above the
modern reference.** The register cost is not merely too small to explain the
gap; it has the wrong sign. Edwardian prose generally (−4.277) also sits on the
reference band, alongside Austen (−4.271).

So the branch that needed Elgar's natural register to sit 0.3–0.4 below
ordinary English is **closed**. What survives of the non-English reading is
only the narrower claim that this specific note was *deliberately* written in
coinage or private shorthand — which §7.4 priced at 40–50% nonce words, an
implausible but not impossible dose, and which the Craeg Lea anagram shows is
at least the kind of game he played.

*(Caveat: this measures conversational and reported register as filtered
through a biographer, not a deliberately cryptic private note to a young
friend, which is a different genre. The measurement constrains "Elgar wrote
unusually" and not "Elgar wrote a deliberately playful nonsense note".
The quoted-span set also includes two epigraph poems and one quoted critic,
about 300 of 4,838 characters, which is too small to move the mean.)*

### 19.3 State of the surviving hypotheses

With the register branch closed, what remains is what §17.5 identified, now
with one leg shortened:

1. **A substitution key we have not guessed**, mirroring common bigrams while
   mapping them unfavourably for a quadgram model — best-supported by the
   classifier at 0.722–0.851 across model sets, and the only reading consistent
   with the strongest replicated anomaly.
2. **Deliberate coinage or private shorthand** at ~40–50% density — not
   excluded, but now with no support from Elgar's measured ordinary register.
3. **Sectional/sliding-card polyalphabetic** — best documentary support of any
   reading, the only one predicting the (now cross-edition-confirmed) line-3
   dot, and provably underdetermined at n = 87.

No experiment available at this length distinguishes (1) from (2), and (3) is
untestable by construction.

---

## 20. Conclusions

> **This section is the Round-15 conclusion and it is not the last word.**
> Rounds 16–20 (§23–§28) postdate it, and §28 carries the revised ledger. Three
> things below have moved: §20.1's family table gains two rows and loses its
> one "not exhausted" entry (§26, §27); §20.2's hypothesis (2) has had the
> measurement it rests on called into question (§25.6); and §20.3's open
> problem has been narrowed but not solved (§25.6, §28). One figure in §20.3
> was corrected by audit (§23.1). Read §28 alongside this.

### 20.1 What this report establishes

**The transcription-noise decomposition** (§1, §10, §18). Of the four
transcriptions in circulation, dCode is a verbatim copy of Hartmeier (§10.1,
proven: applying Elgar's own key to the consensus reproduces dCode's string at
85/87) and the Zenodo archive contains only the published consensus in four
relabelings (§9). The field therefore holds **three** independent readings, not
five. Triangulating them: 74/87 positions unanimous, **zero three-way splits**,
giving per-reader error rates of Hartmeier 1.1%, Pelling 3.4%, Schmeh 10.3%.
Six of the 13 contested positions were independently flagged by a bitmap
classifier that knew nothing of any reader (Fisher p = 0.0020).

**The family ledger**, every entry with matched-budget nulls:

| family | status | evidence |
|--------|--------|----------|
| Elgar's 1924 notebook geometry | **exhausted** (483,840 keys) | best −6.272 vs null −6.266 ± 0.083, p = 0.500 (§8.3) |
| constant-step additive rotation | **exhausted** (24 keys) | identity is the best member; all rotations ≥0.32 worse (§12.2) |
| homophonic | **untestable at n = 87** | solver cannot separate real homophonic English (−4.012) from uniform noise (−4.017) (§13.2) |
| digraphic (Two-Word Square) | **eliminated on parity** | even-length output; 87 is odd (§14.3) |
| transposition + substitution | **not exhausted** — 21 of 46,232 tested | best −4.759 vs identity −4.838; gain 0.079 ≈ 1.6 sd of selection (§16.2) |
| sectional / sliding-card polyalphabetic | **underdetermined in principle** | unicity 55 (k=2) and 82 (k=3) against 87 available (§6, §14.2) |
| transcription-labelling space | enumerated (2¹³), null incomplete | best of 8192 = −4.613, still 2.4 sd short of English (§12.3) |

**Two methodological results.** First: **unicity distance bounds uniqueness,
not discriminability** (§13.3). The homophonic family's unicity distance is
35.2 against 87 available, yet a quadgram score cannot find its key — added key
freedom absorbs redundancy faster than the statistic exploits it. Every "long
enough in principle" argument needs this caveat, including this report's own
headline that 87 exceeds simple substitution's 27, which survives only because
a positive control verified it empirically (96% recovery of known plaintext).

Second: **claims must be specific enough to test.** Four human visual
observations met proper nulls, with one survivor — the mirror-pair excess
(13 vs 5.15 ± 2.17, p = 0.0018) replicated; the alternation-run claim (p = 0.19),
the mirror-clustering claim (p = 0.20), and the disjointness claim all failed.
Three documentary claims met primary-source checks, with **no** survivors: the
music cipher's "12+12 notes, I/J and U/V merged" (not in the text, §15.1),
Thorley's Liszt solution (25 letters against 18 symbols, §8.4), and the
Schooling story's index cards, wooden box, 1896 date and Nihilist
identification (none in Buckley, §19.1). The distinction that separates the
survivor from the failures is not eye-versus-machine but whether the claim is
**specific enough to test**: "there is a dot here" is; "these regions look
disjoint" is not.

**Subsidiary findings.** 87 characters exceeds simple substitution's unicity
distance (~27) by ~3.2×, so the cipher's survival is not explained by length
(§6). The arc-count channel is statistically indistinguishable from uniform —
entropy 1.576 against a 1.585 ceiling (§2.3). The music hypothesis is
disfavoured: best of 96 pitch mappings scores worse than the sequence's own
shuffles, p = 0.903 (§5). No polyalphabetic period (§2.4), no significant row
drift (§3.2), Sukhotin uninformative at this length (§3.4). PENNY, MISS PENNY
and WOLVERHAMPTON cannot be placed at all (§4.4). The line-3 dot appears in
both the 1937 and 1947 plates and is therefore an original feature; the line-1
mark appears in 1937 only and is a print artifact (§18.2a). Elgar's documented
register is indistinguishable from ordinary English, marginally *more* ordinary
at +0.021 (§19.2).

### 20.2 What survives

Three readings, none excluded and none demonstrated:

1. **An unguessed substitution key** that mirrors common bigrams while mapping
   them unfavourably for a quadgram model. Best-supported by the classifier
   (posterior 0.722–0.851 across model sets), and the only reading consistent
   with the strongest replicated anomaly.
2. **Deliberate coinage or private shorthand** at ~40–50% density (§7.4). Not
   excluded, but with no support from Elgar's measured ordinary register — see
   the genre caveat in `TODO.md`, which is load-bearing.
3. **Sectional / sliding-card polyalphabetic.** The best documentary support of
   any reading, and the only one predicting the now cross-edition-confirmed
   line-3 dot — but provably underdetermined at n = 87, and the classifier
   ranks it last (0.052–0.082).

No experiment available at this length distinguishes (1) from (2); (3) is
untestable by construction. **Favoured by provenance, disfavoured by
statistics** is the honest description of (3), and the disagreement between the
two evidence streams is itself a result.

### 20.3 The closing open problem, stated precisely

Dorabella has two distinguishing statistical features. It carries an **excess
of adjacent 180°-opposed glyph pairs** (13 observed against 5.15 ± 2.17,
p = 0.0018), and its **best decipherment falls short of English** (−4.680
against −4.196 ± 0.168 for enciphered real English at matched budget).

Across six generative models — plain substitution, sectional polyalphabetic,
mirror-key substitution, composite text, transposition+substitution, and
mirror-key+transposition — **no model reproduces both features at once.**
Mirror-key substitution matches the mirror excess (+0.91 sd) and misses the
deficit (−0.88 sd). Transposition matches the deficit (+0.32 sd) and misses the
mirror excess (+2.82 sd). Their composition, pre-registered with falsification
targets, passed all six held-out features and still failed the mirror count it
was built to capture (model mean 5.775 against 13).

The failure has a cause, and it is structural:

> **Mirror-pair excess and transposition make incompatible demands on
> adjacency.** Mirror pairs exist only because common plaintext bigrams remain
> adjacent in the ciphertext; transposition's mechanism is the destruction of
> that adjacency.

So the open problem is precise:

> **Find a mechanism that preserves plaintext adjacency — so that a mirroring
> key's bigram structure survives into the ciphertext — while simultaneously
> destroying quadgram fitness by ~0.5/gram. Substitution, transposition, and
> their composition each fail one half by construction.**

Candidate directions not tested here: a substitution key that is
adjacency-preserving by definition but maps high-frequency bigrams onto
low-frequency quadgram contexts (the §16.1 keyword-mixed Heraldic sweep is the
cheapest probe); a plaintext whose own quadgram statistics are depressed
without disturbing bigram adjacency (coinage at the §7.4 dose does this, and is
the only tested mechanism that could); or a transposition confined to a scale
shorter than the adjacency window, which would preserve local pairs while
disrupting longer n-grams. That last is untested and is the most obviously
missing member of the model set.

---

## 21. What would actually move this

Ranked, with the reasoning that survived fourteen rounds of revision.

**1. A genuinely independent re-transcription of the plate**, by a reader who
has not seen the consensus. The transcription-noise decomposition rests on
three readings, one of which (Schmeh) is a 10.3% outlier. A fourth independent
reading would either confirm ~9% as the plate's noise floor or expose the
consensus as better than that. This remains first because §12.3 showed the
*labelling* space cannot rescue the decipherment, so the question is whether
the consensus is right, not which labelling to prefer.

**2. Pelling's provenance** — one email settles whether his 2012 reading was
independent of Hartmeier's 2006 (§10.7). It does not change the substantive
conclusion (§12.3 closed that), but it decides whether the three-reader
triangulation has three legs or two.

**3. The keyword-mixed Heraldic sweep** (§16.1, never run). The only
pre-registerable family that could generate the mirror structure as a
*byproduct* rather than by design — which would dissolve the one thing about
the best-supported reading that strains credulity.

Explicitly **not** recommended, with reasons: better imaging of the surviving
plate (§7.1 showed 3× resolution changed nothing), the Liszt fragment (not
known plaintext, §8.4), a sliding-card sweep (underdetermined by unicity,
§14.2), and any search constrained by a statistic measured on this text
(circular, §12.1).

---

## 22. Limitations

**Capture resolution, not the cipher, blocked three measurements**: the Liszt
fragment (§8.4), the notebook's `LONDON TOMORROW` line (§14.1), and the
cross-edition glyph comparison (§18.3). This is the most consistent obstacle in
the project and the one a better-resourced follow-up could actually remove. It
separates "we could not" from "nobody can" — a distinction this report has
otherwise been careful to maintain.

**The English reference model** is synthesised by frequency-weighted sampling
from `wordfreq`'s empirical table, not drawn from a real corpus. It reproduces
letter and within-word n-gram statistics but under-models cross-word structure.
Austen's *Letters* and Buckley's *Elgar* provide period anchors (§7.3, §19.2)
but the quadgram model itself remains modern.

**Every plate descends from one lost photograph.** Shared-source error — a
halftone artifact fooling all readers identically — is invisible to every
analysis here and always will be. All reader-disagreement figures are lower
bounds on absolute error.

**The transposition family is not exhausted** (§16.2): 21 of 46,232 column
orderings. Unlike §8.3 and §12.2, "exhausted" would be an overstatement there.

**One null run is incomplete** (§12.3): the matched-budget latent null was
interrupted by a container restart at 2 of 8 reps. Its section's conclusion
rests on an absolute comparison to the English band, not on that null.

---

## 23. Round 16 — Phase 0 audit, by a reader with no stake in the result

The analysis was frozen at `3822b25` after fifteen rounds. Before extending it,
its headline numbers were re-derived from the committed scripts in a fresh
container, by a reader instructed to treat any discrepancy as a finding.

**The environment reproduces.** `data/corpus.pkl` is gitignored and rebuilt on
first use from `wordfreq`; the rebuild here used `wordfreq` 3.1.1, `numpy`
2.4.6. This matters more than it looks — every quadgram score in the report is
computed against that regenerated table, so a corpus that drifted with the
library version would silently invalidate the whole score column. It did not.

| claim | section | reported | re-derived | verdict |
|-------|---------|----------|------------|---------|
| consensus solve, forward | §4.2 | −4.680 | **−4.680** | exact, plaintext identical |
| consensus solve, reversed | §4.2 | −4.707 | **−4.707** | exact |
| mirror-pair count | §11.1 | 13 | **13** | exact, same 13 positions |
| mirror-pair null | §11.1 | 5.15 ± 2.17 | **5.174 ± 2.179** | exact |
| mirror-pair p | §11.1 | 0.0018 | **0.0017** | exact (MC noise) |
| Elgar-key mirror share | §11.2 | 6.63% → 5.70 | **6.63% → 5.70** | exact |
| optimal matching | §11.2 | 12 named pairs | **identical** | exact |
| best-possible-key ceiling | §11.2 | 12.23% → 10.52 | **12.19% → 10.48** | **0.045pp low** |

The solve was re-run at the published budget (20 × 15 000, seeds 777/778) and
returns the reported score *and* the reported gibberish plaintext character for
character. The mirror statistic was deliberately **not** re-run from
`massey.py`: it was reimplemented from the definition, given a closed-form
expectation (E = 86 × P(slot is a mirror pair) = 5.1724, no simulation), and
nulled with a different RNG at ten times the reps. All three routes agree.

### 23.1 Two discrepancies, neither load-bearing

**(a) §11.2's ceiling is 0.045pp high.** The max-weight matching reproduces
letter-for-letter, so the difference is in the bigram normalisation of a
Round-6 computation that was never committed and cannot now be inspected.
13 observed against a 10.48 expectation is +0.83 sd; against 10.52 it is +0.82.
The section's conclusion — that a bigram-optimised key makes 13 unremarkable,
and therefore survives the test that kills Elgar's own key — is unchanged.
Annotated inline rather than overwritten.

**(b) §20.3 spliced two runs in one sentence.** It gave mirror-key
substitution's mirror-pair z as **+0.66** and its solver z as **−0.88**. Those
are from different model sets: +0.66 is the four-model run
(`out/discriminate.log`), −0.88 the five-model run (`out/disc5.log`), whose own
mirror z is +0.91. §16.3 quotes the consistent five-model pair. §20.3 is
corrected to **+0.91**, matching the run its other number comes from. The
statement it supports — MIRROR reproduces the mirror excess and not the solver
deficit — holds under either figure, and the structural constraint that follows
from it is untouched.

### 23.2 A gap in the reproducibility claim, now closed

The README says every headline number maps to a committed script. **§11.2 did
not.** Its constructive discrimination — the calculation that rules out Elgar's
own key by a route independent of §8.3, and that supplies the ceiling every
later mirror argument is measured against — was computed inline in Round 6 and
left uncommitted. It is the single most consequential number in the report
without a script behind it, and it is also the one that failed to reproduce
exactly. That ordering is not a coincidence and is worth stating plainly:
**the uncommitted computation is the one that drifted.**

`scripts/audit_phase0.py` now regenerates all three checks, and the README's
script map has rows for §11.2 and for the audit itself.

### 23.3 What the audit does not cover

Re-derived: two headline numbers plus the §11.2 table. Cross-checked by reading
`out/*.log` against the prose: §4.2, §4.3, §4.4, §8.3, §10.5, §12.2, §12.3,
§13.2, §15.2, §16.2, §16.3, §17.3, §19.2 — all consistent with their logs.
**Not** re-run: the long sweeps (§8.3's 483,840 keys, §12.3's 8192 labellings,
the model-discrimination fits), which are checked against their committed logs
only. The interrupted latent null of §12.3 remains interrupted.

The report's conclusions stand as written, with §20.3's one figure corrected.

---

## 24. Round 17 — the Marco test, and the arc channel calibrated for the first time

`TODO.md` item 2 proposed the one **positive** experiment left on the table.
Pelling reads the 1924+ notebook page as carrying `MARCO ELGAR` and `A VERY OLD
CYPHER` in the arc alphabet (§11.3); the arc-count channel is the one this
project reads at 94–98%; so extract the arc counts from those lines and check
them against what the known plaintext predicts under Elgar's key. Prior 85%
that it lands. Blocker: capture resolution.

**The blocker was asserted, never measured.** It is measured here, and the
measurement needed no new material, because of one fact nobody had used:

> **The same page carries Elgar's own key table.** Twenty-four glyphs, same
> hand, same photograph, same resolution, each with its letter written
> underneath. Under his key the arc count of `ALPHA24[i]` is `i mod 3 + 1`, so
> the table's true arc counts are 1, 2, 3 repeating — **ground truth, free,
> drawn from the very image the test must read.**

That makes the key table a known-plaintext sample in the arc alphabet in its
own right, and it is the one this project can actually use.

### 24.1 The arc channel is detectable at this resolution — the project's first positive calibration

Glyphs segmented by column profile; two per-glyph features scored against the
key table's known arc counts.

| feature | Spearman ρ | permutation p | rank assignment |
|---------|-----------|---------------|-----------------|
| glyph width | +0.611 | 0.049 | 5/9 |
| **ink mass** | **+0.949** | **0.0006** | **9/9** |

Ink mass was *chosen* on row 1, so row 1 cannot also test it. Row 2
(`KLMNOPQRS`) is the other row the segmenter recovers exactly and was not used
to pick the feature:

| held-out row 2 | value |
|---|---|
| Spearman ρ | **+0.896** |
| permutation p | **0.0016** |
| rank assignment | 7/9 |
| threshold transferred from row 1, no renormalisation | 6/9 |

**The arc-count channel carries real signal at 750 × 400**, and this is the
first time in the project that the channel has been calibrated against known
plaintext in the arc alphabet rather than assumed from the cipher plate.

### 24.2 And it is not good enough, which is the finding

Detectable is not reliable. Two failures, either sufficient on its own.

**The channel classifies at 67–78% on held-out data** — 7/9 by rank, 6/9 by
transferred threshold — against the **94–98%** at which §2.3 and §7.2 read the
arc channel on the cipher plate. A 70% channel cannot adjudicate a 10-glyph
prediction: `MARCO ELGAR` predicts arc counts `3,1,2,3,2 / 2,2,1,1,2`, and at
70% per-glyph accuracy the expected number of matches under the true reading
(7) overlaps the null for a wrong reading almost completely.

**Glyph segmentation fails upstream of that.** Against the key table's known
glyph counts:

| row | true glyphs | column profile | connected components |
|-----|-------------|----------------|----------------------|
| `ABCDEFGHI` | 9 | 9 | 10 |
| `KLMNOPQRS` | 9 | 9 | 9 |
| `TUWXYZ` | 6 | 9 | 9 |

Two of three rows for one segmenter, one of three for the other. On the three
practice lines the two segmenters return 7/10, 11/16 and 11/17 — **disagreeing
with each other by more than the four-glyph difference between `MARCO ELGAR`
(10 glyphs) and `A VERY OLD CYPHER` (14).** The lines cannot be assigned to the
claimed plaintexts on glyph count, let alone read.

### 24.3 What would unblock it, stated as a specification

The median key-table glyph is ~9 px wide, so a 3-arc glyph gets ~3 px per arc —
at which an arc is not distinguishable from a stroke join. Reliable separation
needs ~6 px per arc, hence ~18 px per glyph: **a capture of the notebook page
at 2–3× linear resolution, 1500–2250 px across.** The page is held by the Elgar
Birthplace Museum. This is the same class of obstacle as §22's other three, and
the same remedy.

### 24.4 Consequences for the ledger

**TODO item 2's 85% prior is neither confirmed nor refuted.** The experiment
could not be run, and the honest ledger entry is *blocked by capture*, not
*tested and failed* — the distinction §22 exists to preserve.

**One claim is downgraded.** §11.3 records, from Pelling, that the notebook
page carries known plaintext in the arc alphabet, and §11.3 used that to
retract §8.4's flat statement that no such sample exists. That retraction
stands on Pelling's reading, which **this project has not corroborated and
cannot corroborate at this resolution.** It should be carried as a *reported
reading*, not as a measurement — the same standard §19.1 applied to the
Schooling story. What this round establishes independently is narrower and
firmer: the key table is a known-plaintext sample in the arc alphabet, and the
arc channel reads it at 67–78%.

**One methodological point generalises.** The 94–98% arc-channel reliability
quoted throughout this report was measured on the cipher plate and then carried
to the notebook without re-derivation. It does not transfer: the same channel
on the same alphabet in the same hand reads at 67–78% on a different capture.
**Channel reliability is a property of the photograph, not of the alphabet**,
and any future use of the arc channel on new material must re-calibrate on that
material rather than inherit the figure.

---

## 25. Round 18 — phonetic English, given a solver that speaks it

§17.4 left a structural constraint: Dorabella needs a mechanism that
**preserves plaintext adjacency** (so a mirroring key's bigram structure
survives, permitting the mirror excess) while **destroying quadgram fitness**
by ~0.44/gram. Substitution keeps both. Transposition destroys both. Their
composition destroys adjacency, which is why §17.3's pre-registered sixth model
failed the feature it was built for.

Phonetic respelling is the one hypothesis that satisfies both halves **by
construction rather than by assembly**, and it had never been given a solver
that speaks its language: every solve in this report scored candidates against
a standard-orthography quadgram model, which penalises a phonetically spelled
plaintext as gibberish even when it is recovered perfectly. Documentary basis:
Elgar's letters are dense with jokey phonetic spellings, Sams argued
phoneticization independently in 1970, and §19.2's contrary measurement used
his *conversational* register — the wrong genre by its own recorded caveat.

Pre-registered in `PREREG-phonetic.md`, committed ahead of the result, with
four thresholds and priors fixed before the corpus was built.

### 25.1 Construction

Grapheme-to-phoneme via CMUdict, then a fixed phoneme→grapheme table (ARPABET,
stress stripped) chosen from ordinary respelling habits: `NATION` → `NAYSHUN`,
`ENOUGH` → `INUF`, `THROUGH` → `THROO`, `BEAUTIFUL` → `BYOOTUFUL`. Corpus
construction is held identical to `scripts/corpus.py` in every other respect —
same `wordfreq` sampling, same 4M characters — so respelling is the only
variable. Words absent from CMUdict keep their orthography, which can only make
the phonetic corpus look *more* like standard English.

**A validation anchor, fixed in the pre-registration before the corpus existed:**
CMUdict gives *gorgeous* as `G AO R JH AH S`, which the table renders
**`GORJUS`** — the spelling Elgar actually wrote. The table was written from
general respelling habits, not fitted to him, and lands on his own spelling
exactly. Seven of seven anchors reproduce.

### 25.2 The mechanism does exactly what §17.4 asked for

| pre-registered check | threshold | result | |
|---|---|---|---|
| **P1** fitness destruction | ≥ 0.20/gram | **1.395/gram** | PASS |
| **P2** adjacency survival | ≥ 80% of the §11.2 ceiling | **109%** | PASS |

Phonetic English scored under the **standard** quadgram model falls to
−5.631 ± 0.304 against ordinary English's −4.236 ± 0.136 — a drop of
**1.395/gram**, which is **314% of the 0.444 deficit to be explained**. And it
does so while *increasing* mirror-producing bigram mass:

| | ordinary | phonetic |
|---|---|---|
| mirror share under Elgar's 1920 key | 6.63% | **8.00%** |
| best-possible-key ceiling (§11.2 machinery) | 12.19% | **13.22%** |
| expected mirror pairs in 86 slots, at ceiling | 10.48 | **11.37** |

`ER` gains mass (16.1 → 25.1‰, because `ER` is a phoneme), `IN` and `TH` are
unchanged (97%, 103%). `AN` and `RE` lose ground (57%, 61%) — the
pre-registration's specific claim that "ER, AN, IN survive" is **half wrong on
AN**, and is recorded as such; the aggregate it was standing in for passes.

**This is the first mechanism in the project to satisfy both halves of the
§17.4 constraint at once.** It is adjacency-preserving and fitness-destroying,
which no substitution, transposition, or composition of the two can be.

### 25.3 The positive control passes, which is what makes the result a result

| **P3** positive control | threshold ≥ 0.50 | **0.96** | PASS |
|---|---|---|---|

Known phonetic English, enciphered under a random MASC at n = 87 and solved
with the phonetic model at the §4.1 budget, is recovered at **0.96 character
accuracy** — identical to the 0.96 that licensed every interpretation in §4,
and reproduced here at 0.94 for ordinary English under the standard model as a
same-run reference.

So this is **not** a second §13.2. The homophonic family was untestable because
the solver could not separate real homophonic English from noise; here the
solver has full power. Whatever comes next is a genuine test.

### 25.4 And the test fails, decisively

| **P4** the test | threshold z ≥ −1.90 | **z = −5.68** | FAIL |
|---|---|---|---|

| | consensus | that model's own English band | z |
|---|---|---|---|
| standard model | −4.680 | −4.196 ± 0.168 | **−2.88** |
| phonetic model | −4.872 | −4.197 ± 0.119 | **−5.68** |

Giving the solver a language model that speaks phonetic English does not shrink
the deficit. **It nearly doubles it**, moving the consensus 2.80 sd *further*
from English, and the phonetic solve's best plaintext is no more readable than
the standard one.

The pre-registration's first "meaningless result" check clears it of the
obvious artifact: this is not a looser model flattering everything. Against the
PHON model the consensus falls 0.191 while its own shuffled null falls only
0.109, so the consensus moved **−0.083 against its own null** — down, not up.

### 25.5 The dose curve — declared post-hoc, and it closes the escape route

P1's overshoot (314% of the deficit) means P4 tested the *wrong dose* by
construction: full respelling is far too destructive, and the deficit
corresponds to a partial dose. That objection is real, so the dose curve was
run — the same move §7.4 made for invented vocabulary, scored the same way, and
therefore directly comparable.

**Declared post-hoc.** It was not in the pre-registration. Its motivation was
established before P4 ran, but the decision to run it was taken after seeing P4
fail, and that is what counts. Reported as a diagnostic, with its own null.

Each word respelled with probability *d*; each dose gets its own model, its own
enciphered-English band, and its own shuffled null.

| dose | band | recovery | consensus | **gap to band** | z |
|------|------|----------|-----------|-----------------|---|
| 0.00 | −4.245 | 0.98 | −4.682 | **−0.437** | −3.52 |
| 0.15 | −4.298 | 0.95 | −4.717 | **−0.419** | −3.42 |
| 0.30 | −4.335 | 0.94 | −4.741 | **−0.406** | −2.33 |
| 0.50 | −4.308 | 0.94 | −4.711 | **−0.403** | −3.18 |
| 0.75 | −4.280 | 0.94 | −4.738 | **−0.458** | −4.12 |
| 1.00 | −4.214 | 0.96 | −4.916 | **−0.702** | −4.91 |

Read the **gap** column, not the z column: z divides by a band sd estimated
from 20 trials and is the noisier statistic (its apparent optimum at d = 0.30
is a 0.03 movement in the gap dressed up by a small sd estimate).

**The gap is flat.** It sits at −0.40 to −0.46 across doses 0 through 0.75 and
then worsens to −0.70 at full respelling. The best dose buys **0.034/gram**
against a standard-orthography baseline of −0.437. Recovery stays at 0.94–0.98
throughout, so the solver has power at every dose.

The reason is worth stating because it generalises: **the model adapts.** A
dose-*d* model scores dose-*d* English at about −4.3 whatever *d* is, so
respelling the plaintext and the reference together moves both and leaves
Dorabella exactly as far below. Phonetic spelling is only fitness-destroying
against a model that does not know about it — and a solver that does not know
about it is a solver we have already been told not to trust.

### 25.6 What this closes

**Phonetic English is rejected, not shelved.** This is the first family in the
project to be (a) shown testable at n = 87 by a passing positive control and
(b) rejected on its own terms. §8.3 and §12.2 were exhausted at the null;
§13.2 was untestable; this is a different and stronger ledger entry.

**And the §17.4 constraint survives its best candidate.** Phonetic respelling
satisfied the constraint on paper — adjacency-preserving *and* fitness-
destroying, the only mechanism yet found that is both — and still failed to
account for Dorabella. That sharpens the open problem rather than solving it:

> Satisfying the adjacency/fitness constraint is **necessary and not
> sufficient.** A mechanism can preserve bigram adjacency and depress
> standard-model quadgram fitness by three times the required amount, and still
> leave the deficit untouched once the solver is given a model of that
> mechanism. The deficit is not merely a mismatch between Dorabella and
> *standard* English; it survives re-basing the language model.

**One consequence for §20.2's surviving hypothesis (2).** "Deliberate coinage or
private shorthand at 40–50% density" (§7.4) is the closest surviving relative of
what was tested here, and it now inherits a specific liability: §7.4 priced its
dose against a *fixed standard* model, exactly the condition under which §25.5
shows the effect is an artifact of the model rather than of the text. Hypothesis
(2) is not refuted — coinage is not respelling, and invented words have no
phoneme table to re-base against — but the measurement it rests on has been
shown to be model-relative in a closely analogous case, and should be re-run
against an adapted model before being carried further.

**The letters were not needed and are not yet warranted.** The pre-registration
committed to requesting photographs of Elgar's letters to Dora if the phonetic
hypothesis showed life. It did not: the mechanism works and the hypothesis
fails, at every dose, with the solver at full power. Seasoning the corpus with
Elgar's own spellings would change the phoneme table, not the finding of §25.5
that re-basing the model does not move the gap. The letters remain the right
source for the *crib* question and for the §19 genre caveat; they are not the
right next step for this branch.

---

## 26. Round 19 — the keyword-mixed Heraldic sweep

§16.1 identified this gap and named it the cheapest remaining probe; §21 ranked
it third of the things that would move the analysis; `TODO.md` item 1 carried it
with a 20% prior. It had never been run.

§8.3 exhausted 483,840 **standard-alphabet** layouts of the Heraldic geometry.
That sweep permutes **where each triplet sits**; it cannot change **which
letters form a triplet**, which alphabetical order fixes as `(A,B,C)`,
`(D,E,F)`, … A keyword-mixed alphabet changes exactly that: `MALVERN` gives
`(M,A,L)`, `(U,E,R)`, `(N,B,C)`, … Pre-registered in `PREREG-keyword.md`.

**`ENIGMA` is excluded as anachronistic.** The *Variations* were composed in
1898–99 and first performed in June 1899; the note is dated 14 July 1897. It is
excluded on those grounds and not scored at all.

### 26.1 Leg A is exhaustive and free, because the arc permutation cancels

Under layout A a mirror pair is `MIXED[g[o]*3+t]` against `MIXED[g[o+4]*3+t]`.
As *t* runs over all three arc counts the arc permutation *h* cancels, so the
set of 12 mirror-producing letter pairs depends **only on how the eight triplets
pair up across the dial** — 105 partitions, and 105 again for layout B, whose
triples are the columns. **210 evaluations therefore cover the entire
483,840-key family exactly**, which makes a dictionary pass affordable.

| | mirror share | expected pairs / 86 |
|---|---|---|
| Elgar's actual 1920 key | 6.63% | 5.70 |
| **best of the standard alphabet, all 483,840 keys** | **7.46%** | **6.41** |
| period keywords, range over the ten | 7.13% – 9.26% | 6.13 – 7.96 |
| best period keyword (`ALICE`) | **9.26%** | **7.96** |
| best of 35,817 dictionary words (`SOUTHEASTERN`) | **11.33%** | **9.74** |
| unconstrained ceiling, no geometry (§11.2/§23) | 12.19% | 10.48 |

**A new and stronger form of §11.2's first conclusion.** §11.2 showed *Elgar's
actual key* cannot produce the mirror excess. Leg A shows **no key in §8.3's
entire swept family can**: the best of all 483,840 standard-alphabet layouts
reaches 6.41 expected pairs against 13 observed. The exhaustive negative of §8.3
and the mirror constraint of §11.2 now agree by construction, not merely by
coincidence of two statistics.

**Q1, the pre-registered 10% threshold: period keywords FAIL (best 9.26%),
the dictionary pass PASSES (11.33%; 267 of 35,817 words reach 10%).** Both
outcomes matched their stated priors (10% and 35%).

### 26.2 What that does to the anomaly

The observed 13 pairs, against each achievable expectation, in that
expectation's own binomial sd:

| expectation is set by | expect | z of 13 |
|---|---|---|
| order-shuffled null (§11.1) | 5.15 | **+3.57** |
| Elgar's actual key | 5.70 | +3.17 |
| best standard-alphabet key — all of §8.3's family | 6.41 | +2.70 |
| best period keyword (`ALICE`) | 7.96 | **+1.87** |
| best dictionary keyword | 9.74 | +1.11 |
| unconstrained ceiling | 10.48 | +0.83 |

**Keyword mixing deflates the anomaly without dissolving it.** This is the
question `TODO.md` item 1 was asked to settle — whether the mirror structure
could arise as a *byproduct* of an ordinary period key-making habit rather than
by design — and the answer is *partly*. A keyword no more exotic than Elgar's
wife's name takes 13 pairs from +2.70 sd (the best §8.3 could offer) to
+1.87 sd, which is not anomalous at any conventional threshold. It does not
need Elgar to have intended mirrors; it needs him to have used a keyword.

Two things keep this from being more than a deflation. `ALICE` is the best of
ten pre-registered keywords, so +1.87 is a best-of-ten selection; the *worst*
period keyword (`FORLI`, 7.13%) sits at +2.88, barely better than no keyword at
all. And the geometry still cannot reach the free-matching ceiling: the triplet
structure forces the 12 mirror pairs to be three consecutive mixed-alphabet
letters against three others, which costs about a percentage point of share
even for the best dictionary word.

### 26.3 Leg B passes its stated threshold, and the pass is worth very little

Full 483,840-key sweep per keyword — 4,838,400 keys — nulled by the identical
best-of-family procedure on shuffled text, 15 reps.

| | score/gram |
|---|---|
| best of the keyword family (`FORLI`) | **−5.940** |
| null: identical best-of-10×483,840 on shuffled text | −6.137 ± 0.088 (max −5.987) |
| observed z | **+2.24** |
| §8.3, standard alphabet, same geometry | −6.272 vs −6.266 ± 0.083, p = 0.500 |
| plain unconstrained MASC solve (§4.2) | −4.680 |
| enciphered real English | ≈ −4.20 |

**Q2's pre-registered threshold was z ≥ +2, and it is met.** The threshold is
not moved after the fact. But what it certifies is thin, and three things say
so. The best member is **1.26 worse than simply solving the text as an
unconstrained substitution** — the family is a constraint that costs score, not
a key that buys it, and it remains 1.74 below English. The observed exceeds the
null *maximum* by 0.047 against a null sd of 0.088, so a handful more null reps
could plausibly overturn it. And the effect the z measures is the one §4 already
established — that Dorabella's symbol order is not random — now visible through
a family in which it was invisible before (§8.3's p = 0.500), which is a
statement about the family's sensitivity, not about the key.

### 26.4 The two legs disagree with each other, and that is the finding

| keyword | leg A share | z of 13 | leg B score | leg B rank |
|---|---|---|---|---|
| `ALICE` | **9.26%** | +1.87 | −6.099 | 5 |
| `CALICE` | 9.10% | +1.94 | −6.339 | 10 |
| `CRAEGLEA` | 8.81% | +2.06 | −6.264 | 7 |
| `MALVERN` | 8.79% | +2.07 | −6.274 | 8 |
| `EDWARDELGAR` | 8.63% | +2.14 | −6.207 | 6 |
| `BRAUT` | 8.55% | +2.18 | −6.293 | 9 |
| `CAROLINE` | 7.91% | +2.47 | −6.044 | 2 |
| `CAROLINEALICE` | 7.91% | +2.47 | −6.044 | 3 |
| `WORCESTER` | 7.37% | +2.75 | −6.091 | 4 |
| `FORLI` | **7.13%** | +2.88 | **−5.940** | **1** |

**No keyword wins both legs.** Leg A's winner (`ALICE`) is leg B's fifth; leg
B's winner (`FORLI`) is leg A's **worst**. If any of these were the 1897 key it
would have to explain both of Dorabella's features, and none comes close to
doing so.

The ranks are in fact *anti*-correlated (Spearman −0.695). **Declared post-hoc**
— it was computed after seeing both legs, on ten points, and is reported as an
observation rather than a test. It has a mechanical reading worth recording:
both legs are functions of the same triplet partition, and an arrangement that
seats high-mass bigrams opposite is thereby committed to placements that the
solver cannot exploit. If that is what it is, then **§17.4's constraint has
reappeared inside a single key family** — the same trade-off between preserving
bigram adjacency and achieving quadgram fitness, now visible across ten
keywords rather than across six generative models.

`CAROLINEALICE` and `CAROLINE` produce the identical mixed alphabet, because
`ALICE` adds no new letters after `CAROLINE`; both are kept in the table so the
pre-registered list is reported as pre-registered.

### 26.5 Ledger

**The family is exhausted on leg A and swept on leg B.** Leg A is exact over
the whole 483,840-key family for every keyword tested, by the cancellation
argument. Leg B is exhaustive within the ten pre-registered keywords and, like
any keyword search, not exhaustive over keywords.

**The one implausibility of §20.2's leading hypothesis is reduced, not
removed.** A mirroring key no longer requires design intent — an ordinary
keyword gets most of the way there — but the leading hypothesis gains no
positive support from this round, and the keyword that best supplies the mirror
structure is the one that solves worst.

---

## 27. Round 20 — the full columnar sweep: 46,232 of 46,232

§16.2 tested 21 permutations and flagged the gap inline. §20.1's family ledger
carries the only row in that table reading **not exhausted**, and §22 lists it
as a limitation. Both are discharged here.

> sum of *k*! for *k* = 2…8 = 2 + 6 + 24 + 120 + 720 + 5040 + 40320 = **46,232**

Procedure follows §12.3's precedent for a family too large to solve at full
budget everywhere: a cheap scan (1 × 2500) over the whole family, then the top
25 re-solved at §16.2's own budget (8 × 9000). **The null runs the identical
two-stage procedure on shuffled text**, so the 46,232-fold selection sits inside
it — which is the whole point, because a family this size will find something on
noise alone.

### 27.1 Result

| | score/gram |
|---|---|
| identity (no transposition), same budget | **−4.685** |
| scan over all 46,232, distribution | −5.374 ± 0.125 (max −4.932, min −5.889) |
| **best of family** after full-budget re-solve, k=8 order (4,3,6,1,0,5,2,7) | **−4.874** |
| null: identical two-stage best-of-46,232 on shuffled text, 5 reps | **−4.815 ± 0.070** (max −4.705) |
| observed z | **−0.85**, p = **0.800** |
| enciphered real English | ≈ −4.20 |

**The observed sits below its own null mean.** Exhaustively, over every columnar
column ordering for every column count up to 8, transposition does not merely
fail to help — the best rearrangement of the real text scores no better than the
best rearrangement of noise, and **0.189 worse than not transposing at all**.

That is the expected result once stated plainly: transposition destroys
adjacency, the real text has adjacency structure to destroy, and shuffled text
does not. The 46,232-fold selection then finds an equally good overfit on both.

**Columnar transposition is exhausted and dead.** §20.1's ledger loses its one
non-exhaustive row, and §22 loses one of its five limitations.

### 27.2 A correction to how §16.2 should be read

§16.2 reported identity at **−4.838** and its best of 21 at −4.759, calling the
0.079 difference "about 1.6 sd of pure selection". This run puts identity at
**−4.685** at the same nominal 8 × 9000 budget, differing only in seed.

**The identity's seed-to-seed spread at that budget is 0.153 — about twice the
0.079 "gain" §16.2 attributed to transposition.** So the gain was not merely a
selection artifact, as §16.2 cautiously said; it was inside the run-to-run noise
of its own baseline, which is a stronger statement than the one that section
made about itself. §16.2's conclusion was right and its reasoning was too
generous to the effect.

This is standing rule 1 biting in an unexpected place. Matched *budgets* are not
sufficient when the budget is small enough that a single solve is high-variance:
matched budgets with unmatched seeds still mislead, and a baseline quoted from
one seed is a point estimate presented as a constant.

### 27.3 Scope, stated precisely

The 46,232 are the **columnar** orderings, which is what §16.2's caveat counted
and what "not exhausted — 21 of 46,232" meant. §16.2's family also contained six
route variants (`reverse`, boustrophedon, row reorderings) that are not columnar
orderings and are outside this count; they were tested there and are not re-swept
here. Within the family the report itself defined, the sweep is complete.

---

## 28. What the fresh-eyes phase changed

Five rounds: an audit and four experiments, each pre-registered where it was a
test and each nulled by its own procedure.

### 28.1 The revised family ledger

| family | status | evidence |
|--------|--------|----------|
| Elgar's 1924 notebook geometry | exhausted (483,840 keys) | §8.3 |
| constant-step additive rotation | exhausted (24 keys) | §12.2 |
| **columnar transposition** | **exhausted (46,232 of 46,232)** | best −4.874, below identity −4.685 **and below its own null**, p = 0.800 (§27) |
| **keyword-mixed Heraldic** | **leg A exact over the full family; leg B swept over 10 pre-registered keywords** | best −5.940 vs null −6.137 ± 0.088; 1.26 worse than an unconstrained solve (§26) |
| **phonetic English, any dose** | **rejected, with a passing positive control** | z = −5.68 against its own band; gap flat across doses 0–0.75 (§25) |
| homophonic | untestable at n = 87 | §13.2 |
| digraphic (Two-Word Square) | eliminated on parity | §14.3 |
| sectional / sliding-card polyalphabetic | underdetermined in principle | §6, §14.2 |
| transcription-labelling space | enumerated (2¹³), null still incomplete | §12.3 |

Phonetic English is a **new kind of entry**: the first family shown *testable*
at n = 87 by a passing positive control (0.96 recovery) and then *rejected on
its own terms*. Everything above it was exhausted at the null; §13.2 was
untestable. This is neither.

### 28.2 The open problem has changed shape

§20.3 stated it as: *find a mechanism that preserves plaintext adjacency while
destroying quadgram fitness by ~0.5/gram; substitution, transposition, and their
composition each fail one half.*

**Such a mechanism was found, and it did not help.** Phonetic respelling
preserves adjacency (it *raises* the mirror ceiling, 12.19% → 13.22%) and
destroys standard-model fitness by 1.395/gram, three times what is required —
and Dorabella scores 5.68 sd below it, worse than under the standard model, at
every dose. So:

> **Satisfying the adjacency/fitness constraint is necessary and not
> sufficient.** The deficit is not a mismatch between Dorabella and *standard
> English*. It survives re-basing the language model: under a model in which
> phonetic English is perfectly ordinary — and which recovers known phonetic
> plaintext at n = 87 at 0.96 — Dorabella is further from English, not closer.

**And one of the two features that made the problem a puzzle has partly
dissolved.** §20.3's puzzle was that no model reproduces both the mirror excess
and the solver deficit. §26.2 shows the mirror excess largely stops being
anomalous once the key is allowed an ordinary keyword: 13 pairs run from +3.57 sd
against a shuffled null, to +2.70 against the best key §8.3's family can offer,
to **+1.87 against a key mixed on `ALICE`**. It does not need a designed
mirroring key; it needs Elgar to have used a keyword, which is an unremarkable
period habit.

So the joint-profile puzzle reduces. What has to be explained is no longer *two*
features pulling against each other, but **one**: the solver deficit, now known
to survive both transposition (exhausted) and language-model re-basing.

### 28.3 What that leaves, ranked

1. **The plaintext is not a substitution of any modelable language-like text.**
   The strongest reading after §25. It covers deliberate nonsense, heavy
   abbreviation, and text whose statistics no corpus supplies — and it is
   consistent with every negative in the ledger.
2. **A substitution key not yet guessed.** Still live, but §26 removed its one
   piece of positive support: the mirror excess it was invoked to explain is
   mostly accounted for by keyword mixing, and the keyword that best supplies the
   mirror structure is the one that solves worst (§26.4).
3. **Shared transcription error.** §22's standing caveat — a halftone artifact
   fooling all three readers identically is invisible to every analysis here.
   §12.3 bounded the *reader-contested* space and found no rescue; it cannot
   bound errors on which all readers agree.
4. **Sectional / sliding-card polyalphabetic.** Unchanged: best documentary
   support, provably underdetermined at n = 87.

### 28.4 On method

Three things this phase is worth citing for, independent of the cipher.

**An uncommitted number is the one that drifts.** §11.2 was the single headline
calculation without a committed script, and it was the only one that failed to
reproduce (§23.2). The correlation has an obvious cause and is worth stating
anyway.

**Channel reliability is a property of the photograph, not of the alphabet.**
The arc channel reads at 94–98% on the cipher plate and 67–78% on the notebook —
same alphabet, same hand, different capture (§24.4). Any figure carried across
images without re-derivation is an assumption wearing a measurement's clothes.

**Matched budgets are not enough when the budget is small.** §16.2's baseline
moved 0.153 between seeds at a budget where it reported a 0.079 effect (§27.2).
Standing rule 1 needs a companion: a baseline quoted from a single solve is a
point estimate, and at low budget it must be reported with its spread.

---

## 29. Round 21 — the fitness-family audit

§28.2 claimed the deficit "survives re-basing the language model". That claim
rests on §25, where a *phonetic quadgram* model — still a quadgram model — put
Dorabella 5.68 σ below its own band. **Every headline number in this report is
mean quadgram log-probability per gram**: §4.1's bands, §4.2's −4.680, and every
null in §8.3, §12.2, §16.2, §26 and §27. If that estimator is what produces the
deficit, the report has measured one statistic's behaviour and called it a
property of the text. Pre-registered in `PREREG-fitness.md`.

**External anchor.** AZdecrypt (Van Eycke), the solver used in the 2020 break of
Z340, sums n-gram log frequencies, divides by the count, and **multiplies by the
plaintext's entropy**; its documentation gives the reason explicitly — to stop
convergence on solutions using only a few common letters — and records that it
moved from an index-of-coincidence term to an entropy term. That is a different
estimator in three ways: longer window, a degeneracy penalty this report has no
analogue of, and constraints on the candidate plaintext rather than on n-grams
alone.

*(Sign convention, declared in the pre-registration rather than defended
afterwards: log probabilities are negative, so multiplying by entropy would
reward degenerate solutions — the opposite of the stated purpose. AZdecrypt
reports positive scores, so its table holds a positive quantity. Implemented
here as `mean(log10(count+1)) × H`, with the unweighted term reported alongside
so the entropy factor is separable.)*

### 29.1 A measurement audit, and the regeneration check passes exactly

**No new searches.** Every key was already chosen by quadgram hill-climbing;
`solver3.py`'s runs were regenerated at the same seed and budget only to recover
the plaintexts the frozen run did not save.

| band | regenerated | §4.1 published |
|---|---|---|
| enciphered real English | **−4.196 ± 0.168** | −4.196 ± 0.168 |
| shuffled consensus | **−5.010 ± 0.087** | −5.010 ± 0.087 |
| uniform random | **−5.178 ± 0.125** | −5.178 ± 0.125 |

Exact on all three. This is the frozen procedure.

### 29.2 §28.4's own rule, applied to §4.2's headline number

The consensus solve re-run at 10 seeds, same 20 × 15 000 budget:

> −4.680, −4.680, −4.708, −4.680, −4.750, −4.680, −4.731, −4.765, −4.680, −4.680
> — **mean −4.704 ± 0.032, range −4.680 to −4.765**

§4.2 published **−4.680**, which is the *best* of the ten, not the typical one.
The effect is small (0.024 on the mean, 0.13 σ of the English band) and changes
no conclusion, but the direction is worth recording: **the report's single most
quoted number is the most favourable seed of its own distribution.** Every z
below is therefore computed from the 10-seed mean, which is why F1 reads −3.01
rather than the published −2.88.

### 29.3 The audit

| family | English band | consensus | z | percentile vs null |
|---|---|---|---|---|
| **F1** quadgram log-prob *(frozen)* | −4.196 ± 0.168 | −4.704 ± 0.032 | **−3.01** | 1.00 |
| **F2** 5-gram log-prob | −5.021 ± 0.342 | −6.339 ± 0.037 | **−3.86** | 0.97 |
| **F3** 6-gram log-prob | −5.736 ± 0.506 | −7.526 ± 0.163 | **−3.54** | 0.99 |
| **F4** 5-gram × entropy (AZ form) | 6.590 ± 0.889 | 3.633 ± 0.294 | **−3.33** | 1.00 |
| **F5** 6-gram × entropy (AZ form) | 4.328 ± 0.965 | 1.447 ± 0.373 | **−2.98** | 1.00 |
| **F6** quadgram + IoC/χ² penalties | −4.974 ± 0.414 | −5.554 ± 0.112 | **−1.40** | 0.90 |

**The pre-registered prediction fails.** It required |z| ≥ 2.0 in every one of
F2–F6 and no family more than 1.5 σ from F1. F6 returns −1.40 and sits 1.62 σ
away. Recorded as a failure before it is diagnosed.

I had put 20% on exactly this outcome and named the wrong family: I expected the
entropy-weighted families to break, and F5 lands within **0.03 σ** of F1. The
degeneracy penalty this report lacks turns out not to matter here at all.

### 29.4 The diagnosis — and my threshold was the wrong statistic

`z = (band mean − consensus) / band sd`. A family can lose z two ways: by
**closing the gap** (the deficit is estimator-dependent — the finding the
threshold was written to catch), or by **inflating the band sd** (the estimator
is merely noisier — a statement about power, not about the text). The threshold
cannot tell them apart. Separating them:

| family | gap | band sd | z | **normalised deficit** |
|---|---|---|---|---|
| F1 quadgram | 0.507 | 0.168 | −3.01 | **57%** |
| F2 5-gram | 1.319 | 0.342 | −3.86 | **77%** |
| F3 6-gram | 1.790 | 0.506 | −3.54 | **81%** |
| F4 5-gram × H | 2.956 | 0.889 | −3.33 | **76%** |
| F5 6-gram × H | 2.881 | 0.965 | −2.98 | **80%** |
| F6 quad + IoC/χ² | 0.579 | 0.414 | −1.40 | **49%** |

*Normalised deficit* = how far the consensus falls from that family's English
band **towards that family's own meaningless-text null**, as a percentage of
that span. It is scale-free, does not divide by the band sd, and is therefore
the statistic that actually survives a change of estimator. **It is the column
to read.**

And F6 has a free parameter I chose. λ was set to 0.5 on no principle:

| λ | English band | consensus | z | normalised deficit |
|---|---|---|---|---|
| 0.00 | −4.196 ± 0.168 | −4.704 ± 0.032 | −3.01 | 57% |
| 0.10 | −4.352 ± 0.173 | −4.874 ± 0.033 | −3.02 | 55% |
| 0.25 | −4.585 ± 0.240 | −5.129 ± 0.058 | −2.26 | 52% |
| 0.50 | −4.974 ± 0.414 | −5.554 ± 0.112 | **−1.40** | 49% |
| 1.00 | −5.752 ± 0.809 | −6.404 ± 0.226 | −0.81 | 45% |
| 2.00 | −7.307 ± 1.623 | −8.104 ± 0.457 | −0.49 | 39% |

z runs from −3.01 to −0.49 as λ goes from 0 to 2, while the band sd inflates
tenfold. **F6's failure is dominated by variance I injected, not by the deficit
closing** — the gap itself *widens* slightly (0.507 → 0.579) at λ = 0.5.

So the honest statement has two parts and both are reported:

1. **My pre-registered test failed, and it failed because I chose the wrong
   statistic.** A z-threshold across estimators with different noise levels
   tests power, not the quantity of interest. That is a design error in the
   pre-registration, not a finding about the cipher, and it is exactly the kind
   of thing pre-registration is supposed to expose rather than hide.
2. **On the scale-free statistic the deficit replicates in all six families**,
   at 39–81% of the English-to-noise span, and is **larger** under every
   longer-window and entropy-weighted family than under the frozen one.

### 29.5 What this does and does not establish

**§28.2's claim survives, and in a stronger form than it was made.** The deficit
is not an artifact of window length (5- and 6-gram families put it at 77–81%,
against the quadgram family's 57%), and it is not an artifact of the missing
degeneracy penalty (F5 lands 0.03 σ from F1). The estimator every number in this
report shares is, if anything, the *most charitable* of the six to Dorabella.

**One direction does narrow it.** Constraints on the candidate plaintext's own
distribution — IoC and χ² — move the consensus from 57% to 49% (λ = 0.5) or 39%
(λ = 2) of the span. The deficit does not close, but this is the first family in
which it shrinks rather than grows, and the reason is interpretable: the
consensus's decipherment already has more English-like letter statistics than
the nulls' do, so rewarding that helps it more than it helps them. It is a real
if partial effect and the only lead this round produces.

**Between-family variation dominates seed noise, which vindicates the round's
premise.** The z spread across F2–F6 is 2.46 σ; the spread from solver seed
alone within F1 is 0.50 σ. §28.4 asked whether the seed spread would rival the
between-family spread. It does not — it is a fifth of it, so the choice of
fitness family is a real degree of freedom that the report had never varied.

**The limitation is structural and was declared in advance.** Re-scoring is not
re-searching. Every key here was chosen to maximise *quadgram* fitness, so a
gibberish string optimised for quadgrams has no reason to score well on 6-grams;
F3 and F5 may widen the deficit mechanically. That is why the English band and
both nulls are re-scored by the identical route — the comparison is fair even
where the absolute numbers are not — and it is why **a widening is not reported
as evidence for the deficit.** The conclusion available here is the weaker
"not an artifact of window length or of the entropy term", not "the deficit is
real". What a solver that *searched* under 6-gram entropy-weighted fitness would
find is a different experiment, and after this round it is the obvious one.
