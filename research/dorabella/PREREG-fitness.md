# Pre-registration — Round 21: the fitness-family audit

**Written before any alternative fitness function was built and before any of
them touched the frozen results.** Standing rule 4.

---

## The problem with §28.2

§28.2 claims the deficit "survives re-basing the language model", on the
strength of §25: a phonetic quadgram model, under which phonetic English is
ordinary and known phonetic plaintext is recovered at 0.96, still puts Dorabella
5.68 σ below its own band.

**That is re-basing within one fitness family.** A phonetic quadgram model is
still a quadgram model. Every headline number in this report — §4.1's bands,
§4.2's −4.680, every null in §8.3, §12.2, §16.2, §26, §27 — is mean quadgram
log-probability per gram. If that statistic is the thing producing the deficit,
the entire report has measured one estimator's behaviour and called it a
property of the text.

The claim is therefore stronger than the evidence, and this round tests it.

## External anchor

AZdecrypt (Van Eycke) — the solver used in the 2020 break of Zodiac Z340 —
scores by summing n-gram log frequencies over the candidate plaintext, dividing
by the n-gram count, and **multiplying by the plaintext's entropy**. Its own
documentation gives the reason for the entropy factor explicitly: to stop the
solver converging on solutions that use only a few common letters ("n-gram
spaghetti"). Internally it moved from an index-of-coincidence term to an entropy
term. Forum practice around it adds IoC and χ² constraints.

That is a materially different estimator from this report's, in three ways: a
longer window (6 rather than 4), a degeneracy penalty this report has none of,
and distributional constraints on the candidate plaintext rather than on n-grams
alone. It is the natural second family, and it is the one that broke a
comparable short, distorted ciphertext.

**A sign convention has to be reconstructed, and this is declared now rather
than defended later.** Log *probabilities* are negative, so multiplying by
entropy would reward degenerate low-entropy solutions — the opposite of the
stated purpose. AZdecrypt reports positive scores in the thousands. The
consistent reading is that its table holds a positive quantity (log of the
n-gram count, not its probability), so higher entropy raises the score and
degenerate solutions are penalised. This round implements
`mean(log10(count + 1)) × H(plaintext)`, which has that behaviour, and reports
the unweighted `mean(log10(count + 1))` alongside so the entropy factor's
contribution is separable. Any conclusion that depends on the exact constant is
not a conclusion this round is entitled to draw.

## Method — a measurement audit, not a search

**No new searches.** Every key was already chosen by quadgram hill-climbing.
This round re-scores the *outputs* under other fitness families and asks whether
the deficit is a property of the text or of the estimator.

Regenerated exactly as `solver3.py` produced them — same RNG seed (4242), same
20 × 15 000 budget, same order — and this time the recovered plaintexts are
kept, which the frozen run did not save:

- 40 enciphered-real-English solves (the §4.1 band)
- 60 shuffled-consensus solves (null)
- 60 uniform-random solves (null)
- the consensus solve

Reproduction of §4.1's published means (−4.196 / −5.010 / −5.178) is the check
that the regeneration is the frozen procedure and not a new one.

Fitness families applied to every recovered plaintext:

| | family |
|---|---|
| F1 | mean quadgram log-probability — **the frozen family** |
| F2 | mean 5-gram log-probability |
| F3 | mean 6-gram log-probability |
| F4 | entropy-weighted 5-gram, AZdecrypt form |
| F5 | entropy-weighted 6-gram, AZdecrypt form |
| F6 | quadgram with IoC and χ² penalties, in each statistic's own English σ |

The quantity compared across families is **the consensus's z against that
family's own enciphered-English band**, because absolute scores are not
comparable between estimators. F1 must return −2.88.

## Pre-registered prediction and threshold

> **A real deficit replicates across fitness families at comparable σ.**

Passing: **|z| ≥ 2.0 in every one of F2–F6**, and no family more than **1.5 σ**
away from F1's −2.88.

Failing: any family in which the deficit falls below 2 σ. That would mean the
0.44/gram shortfall is substantially an artifact of the quadgram estimator, and
§28.2, §20.3 and the whole "deficit" framing would need rewriting rather than
amending.

*Prior: 70% the deficit replicates in all five.* The deficit is large and has
survived a great deal, but it has never been asked this question, and the
honest position is that a fitness family shared by every number in the report
is exactly the kind of common-mode assumption an audit exists to find. I put
20% on a partial failure (one or two families below 2 σ, most likely the
entropy-weighted ones, since the entropy factor is the term this report has no
analogue of) and 10% on a general collapse.

## §28.4's spread rule applies to every baseline here

§28.4 recorded that §16.2 quoted a baseline from one solve at a budget where
that solve varied by 0.153 between seeds. The rule that follows is applied
throughout this round: **the consensus solve is itself re-run at 10 seeds** and
reported with its spread under every family, not as the point estimate −4.680.
If the seed spread is comparable to the between-family spread, that is the
finding, and it outranks any individual family's z.

## What would make a pass meaningless

1. **Re-scoring is not re-searching, and it is conservative in a known
   direction.** These keys were chosen to maximise quadgram fitness. A gibberish
   string optimised for quadgrams has no reason to score well on 6-grams, so
   F3/F5 may *widen* the deficit mechanically. That is why the English band and
   the nulls are re-scored by the identical route: all three groups had their
   keys chosen the same way, so the comparison is fair even where the absolute
   numbers are not. A widening is therefore not evidence *for* the deficit, and
   will not be reported as such.
2. **Only a narrowing is informative.** If a family shrinks the deficit below
   2 σ, that is a real finding about the estimator. If every family widens it,
   the correct conclusion is "not an artifact of window length", which is
   weaker than "the deficit is real".
3. **The unanswered question stays open.** This round cannot say what a solver
   that *searched* under 6-gram entropy-weighted fitness would find. That is a
   new search, it is out of scope here, and if F3/F5 behave interestingly it is
   the obvious next round.
