# Pre-registration — Experiment 1: phonetic English

**Written before the phonetic corpus was built and before any phonetic model
touched the consensus transcription.** Committed separately from, and ahead of,
the result. Standing rule 4.

---

## The hypothesis, and why it is the one worth running

§17.4 left a structural constraint. Dorabella's joint profile needs a mechanism
that **preserves plaintext adjacency** — so a mirroring key's bigram structure
survives into the ciphertext and the mirror excess is possible — while
**destroying quadgram fitness** by ~0.44/gram. Substitution preserves adjacency
and preserves fitness. Transposition destroys fitness and destroys adjacency.
Their composition destroys adjacency (§17.3, which is why the pre-registered
sixth model failed the feature it was built for). Each fails one half.

Phonetic respelling is the one hypothesis on the table that satisfies both
halves *by construction rather than by assembly*:

- **Adjacency-preserving.** Respelling changes which letters spell a sound, not
  which sounds sit next to which. `ER`, `AN`, `IN` survive respelling intact.
- **Fitness-destroying against a standard-corpus quadgram model.** `TION` →
  `SHUN`, `OUGH` → `OO`, silent letters and doubled letters gone, `EA`/`OU`/`AI`
  digraphs replaced. The high-mass quadgrams a standard model is built on stop
  appearing.

It has never been given a solver that speaks its language. Every solve in this
report scored candidate plaintexts against a **standard-orthography** quadgram
model, so a phonetically spelled plaintext would be penalised as gibberish even
if recovered perfectly.

**Documentary basis.** Elgar's letters are dense with jokey phonetic spellings
(`gorjus`, `skorse`, `warbling wigorously`). Sams argued phoneticization
independently in 1970. §19.2 measured Elgar's register as ordinary English —
but from Buckley's biography, i.e. his *conversational* register as filtered by
a biographer, which is the wrong genre by that section's own recorded caveat
(`TODO.md` item 5, flagged there as load-bearing). Letters are the documented
home of the phonetic spellings; nothing in §19.2 reaches them.

## Method

Corpus construction is held identical to `scripts/corpus.py` in every respect
except the respelling — same `wordfreq` frequency-weighted word sampling, same
4M characters, same no-spaces concatenation — so the respelling is the only
variable. Grapheme-to-phoneme via CMUdict, then a fixed phoneme→grapheme table
(ARPABET, stress stripped). Words absent from CMUdict keep their orthography.

Two quadgram models are then in play: **STD** (the existing `data/corpus.pkl`)
and **PHON** (the same construction over respelled text). Absolute scores under
the two are not comparable — a different model has a different scale — so every
comparison below is *within* a model: a text against that model's own English
band, in that band's sd units. This is the §7.3 discipline.

## Pre-registered predictions and thresholds

Stated as thresholds, with a genuine prior on each. Hold me to them.

**P1 — the mechanism must be strong enough.** Phonetic English, scored under
the **STD** quadgram model, must fall at least **0.20/gram** below ordinary
English scored under the same model. The deficit to explain is 0.44; a
mechanism supplying less than half of it cannot be the account even in
principle. *Prior: 80% this passes.* Run before any contact with the cipher.

**P2 — the mechanism must not destroy the other half.** Phonetic English must
retain at least **80%** of ordinary English's mirror-producing bigram mass at
the §11.2 ceiling (max-weight matching over the 24-letter alphabet). If
respelling collapses the ceiling, phonetic English fails the adjacency half of
the §17.4 constraint and is no better placed than transposition.
*Prior: 85% this passes.*

**P3 — positive control, and it gates everything after it.** Encipher known
phonetic English at n = 87 under a random MASC and solve it with the **PHON**
model, at the §4.1 budget of 20 × 15 000, 40 trials. Threshold: **mean
character accuracy ≥ 0.50**.

> If P3 fails, this is recorded as a **second untestable-in-principle result**
> alongside §13.2's homophonic family — the family is not rejected, the method
> has no power against it at this length — and the experiment **stops there**.
> No solve of the consensus under the phonetic model is reported, because an
> uncalibrated solver's output is not interpretable (standing rule 6).

*Prior: 65% this passes.* Phonetic English is still highly redundant, but it is
more regular and lower-entropy than standard orthography, which cuts both ways.

**P4 — the test itself, only if P3 passes.** Solve the consensus under the PHON
model at 20 × 15 000, with nulls run by the identical procedure: shuffled
consensus and uniform random, same budget, same model, 60 reps each. The
quantity of interest is the consensus's **z against the phonetic-English band**,
compared against its **−2.88 z against the standard English band** (§4.2).

> Success threshold: improvement of **≥ 1.0 sd**, i.e. z ≥ −1.9. Anything less
> is recorded as no rescue.

*Prior: 15% this passes.* Low. The deficit has survived four rounds of
increasingly charitable treatment, and a language model fitted to a more
regular text may simply score everything higher, which the null is there to
catch.

## What would make a positive result meaningless

Declared now, so it cannot be argued away later.

1. **A looser model flatters everything.** If PHON raises the consensus *and*
   raises the shuffled null by a similar amount, nothing has been learned. The
   consensus must move relative to its own nulls, not in absolute score.
2. **No plaintext claim without the garbage null.** Standing rule: a readable
   output is claimed only if it beats the garbage-solution null. A phonetic
   solver's output will *look* more word-like by construction, which makes this
   rule more important here, not less.
3. **No post-hoc tuning of the phoneme table.** The table is fixed before the
   corpus is built. If it is later changed for any reason, every number after
   the change is a fresh experiment with a fresh null, and the report says so.

## A validation anchor, fixed in advance

The respeller is checked against Elgar's own documented spelling before use:
CMUdict gives *gorgeous* as `G AO R JH AH S`, which the fixed table renders
`GORJUS` — the spelling Elgar actually wrote. That is a coincidence of the
table with his practice, not a fit to it, and it is recorded because it was
checked before the corpus was built rather than after the result was known.

**Elgar's own letters are not in this corpus.** Seasoning the model with his
documented spellings requires the letters themselves, which this session does
not have. If P3 and P4 show life, the letters are the correct next input — they
are simultaneously the phonetic-idiolect corpus and the crib source — and the
result below is the systematic-phonetic baseline they would be measured
against, not a measurement of Elgar.
