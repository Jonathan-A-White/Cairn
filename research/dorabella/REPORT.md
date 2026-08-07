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

## 7. Conclusions, ranked by robustness

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

**6. Whether this is a simple substitution of ordinary English depends
entirely on the consensus transcription's absolute error rate.** The observed
score corresponds to ≈ 8.8% equivalent glyph error. At the ~2% error implied
by consensus-vs-dCode agreement, the hypothesis is disfavoured by ~2.2 sd; at
~9% it is perfectly consistent. Pairwise transcription distances cannot
resolve this because the transcriptions are not independent.

**7. Arc count and orientation are not independent** (χ² = 40.18,
MC p = 0.001, Cramér's V = 0.481). I discarded this in my first pass as an
artifact of my own reading — sound reasoning, wrong conclusion, since it
replicates at the same strength on a transcription I had no hand in. It is
real; its meaning is open. The four never-used symbols (`D3`, `E1`, `E2`,
`H3`) are consistent with the inventory being shaped rather than uniform.

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

## 8. The single most informative next experiment

**Measure the consensus transcription's absolute error against a
high-resolution scan of the original.** Everything now turns on conclusion 6,
and that one number decides it: at ~2% error the simple-substitution-English
hypothesis is disfavoured and the interesting question becomes *what else* the
cipher is; at ~9% error nothing has been excluded and the field is back where
it started.

Every other avenue is currently rate-limited by this. More compute, more
mapping families, more cribs and better language models all sit downstream of
a quantity that a single good photograph would fix. The original is held by
the Elgar Birthplace Museum; the British Library holds related material.

The second experiment, worth building in parallel, is the latent-variable
formulation: joint inference over (glyph labels, key) with the ~20 contested
positions as the only free label variables and per-glyph geometric confidence
as the prior. That search space is small (≤ 2²⁰, far less with
transcriber-attested values only) and it yields a falsifiable output the
discrete ensemble cannot: if the posterior concentrates on one labelling that
*also* clears the null, that is evidence; if it stays flat, the cipher is
provably underdetermined by the available images — itself a publishable
negative.
