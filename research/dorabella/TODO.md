# Open work, with priors attached

Each item states what was *not* done, what I expect, and why — so the
expectation is on record before the experiment, not after. Where I give a
probability it is a genuine prior, not a hedge; hold me to it.

**Rounds 16–22 (§23–§31) closed four of the original five items and opened
four new ones.** Closed items are kept below with their outcome and their prior,
because a prior is only worth writing down if it is scored afterwards.

**Read first: §31.4.** All three mechanism-side directions §20.3 named have now
been run and none accounts for the deficit, and §29 showed the deficit replicates
across six fitness families. The open items below are therefore no longer about
finding the mechanism.

---

## Scoreboard on the original five

| item | prior | outcome | where |
|------|-------|---------|-------|
| 1. Keyword-mixed Heraldic sweep | 20% that some keyword lands materially above the null | **run.** Leg A exact and free; leg B met its z ≥ +2 threshold at +2.24 but the best member is 1.26 *worse* than an unconstrained solve. Prior roughly vindicated — something landed, and it was worth little. | §26 |
| 2. Marco arc-count test | 85% it lands | **blocked, and the blocker measured.** Neither confirmed nor refuted: the experiment could not be run at 750×400. A by-product is the project's first calibration of the arc channel on known plaintext. | §24 |
| 3. Full columnar sweep | 5% the full sweep finds anything the subset missed | **run, all 46,232 orderings.** | §27 |
| 4. Interrupted latent null | 95% the completed null confirms | **still open.** See item A below. | §12.3 |
| 5. Genre caveat on §19 | 60% his letters score below his conversation; 15% they reach the required depth | **superseded in part.** §25.5 shows the deficit survives re-basing the language model, so the register question no longer has the leverage this item assumed. See item B. | §25 |

---

## A. Interrupted latent null — §12.3 (carried over unchanged)

**What.** The matched-budget null for the 2¹³ latent labelling sweep was
interrupted by a container restart at **2 of 8 reps** (−4.841, −4.927, both
below the observed −4.686). Flagged inline as incomplete.

**Prior.** ~95% the completed null confirms the reported conclusion, since that
conclusion rests on an *absolute* comparison (best of 8192 = −4.613 against the
English band at −4.196 ± 0.168), not on the null. Finish it anyway — an
incomplete null in a report about null discipline is a bad look, and it is
~40 minutes of compute.

**Status after Round 16's audit:** unchanged. The audit re-ran the headline
solve and the mirror statistic but not the long sweeps, so this is still the
one incomplete null in the report.

---

## B. §7.4's coinage dose was priced against a fixed model — §25.5

**What.** §7.4 priced "deliberate coinage or private shorthand" at a 40–50%
dose, by scoring nonce-word-laden plaintext under the **standard, unchanged**
quadgram model. §25.5 showed that for phonetic respelling — a closely analogous
mechanism — that measurement is an artifact of the model rather than of the
text: once the solver is given a model of the mechanism, the gap to the
enciphered-English band is flat across every dose from 0 to 0.75.

**Why it matters.** Surviving hypothesis (2) in §20.2 rests entirely on §7.4's
number. If coinage behaves like respelling under an adapted model, hypothesis
(2) loses its quantitative basis and hypothesis (1) stands alone.

**Why it might not.** Coinage is not respelling. Invented words have no
generative rule to build a model from — that is what makes them invented — so
there may be no "adapted model" to re-base against, in which case §7.4's
measurement stands and the analogy fails. Establishing *which* is the
experiment.

**Prior.** ~55% that a nonce-adapted model flattens the §7.4 dose curve the way
§25.5 flattened the phonetic one. Genuinely uncertain; the disanalogy above is
real.

---

## C. Elgar's letters — narrower than item 5 was

**What changed.** The original item 5 wanted Elgar's letters as an
*idiolect corpus*, to test whether his epistolary register sits 0.3–0.4 below
ordinary English. §25 removed most of that motivation: the phonetic hypothesis
was given a solver that spoke its language, passed its positive control at 0.96
recovery, and still failed at every dose. Seasoning a corpus with his documented
spellings changes the phoneme table, not §25.5's finding that re-basing the
model does not move the gap.

**What the letters are still worth.** Two things, both narrower.

1. **Cribs.** §4.4 disposed of every obvious crib from the 1897 context —
   `PENNY`, `MISS PENNY` and `WOLVERHAMPTON` cannot be placed at all. Letters to
   Dora are the one source of *non-obvious* candidate cribs: shared jokes,
   nicknames, running references. A crib is testable at n = 87 in a way a
   register is not.
2. **Item B's corpus.** If the coinage question above is run, Elgar's letters
   are where his actual coinages are.

**Prior.** ~25% that a letters-derived crib is placeable in the consensus at
all, given that the pattern constraint killed three of the four obvious ones.

---

## D. Notebook page at 2–3× resolution — §24.3, a specification not a wish

**What.** A capture of the 1924+ notebook page at **1500–2250 px across**,
against the 750 px currently held. §24 measured why: the median key-table glyph
is ~9 px wide, giving a 3-arc glyph ~3 px per arc, at which an arc is
indistinguishable from a stroke join. Reliable separation needs ~6 px per arc.

**What it would buy.** The Marco test (item 2), the `LONDON TOMORROW` line
(§14.1), and independent corroboration of Pelling's reading of that page —
which §24.4 downgraded to a *reported reading* because this project cannot
check it. The page is held by the Elgar Birthplace Museum.

**Prior.** Unchanged from the original item 2: ~85% the test lands **if** the
capture is obtained, since the key is known, the plaintext is known, and §24.1
showed the arc channel carries real signal even at the resolution that defeats
it.

---

## F. A solver that SEARCHES under 6-gram entropy-weighted fitness — §29.5

**What.** §29 re-scored; it did not re-search. Every key in it was chosen by
quadgram hill-climbing, so the audit can say the deficit is not an artifact of
window length or of the missing entropy term, and cannot say what a solver
optimising 6-gram entropy-weighted fitness would find. AZdecrypt broke Z340 with
that estimator on a comparably short, distorted text.

**Why it matters.** It is the one remaining way the deficit could still be an
estimator artifact, and §29 explicitly could not close it. It is also the first
experiment in the project that would use the field's current best solver design
rather than this report's own.

**Cost.** A rewrite of the annealer's fitness call plus a matched-budget null;
the 6-gram table already exists in `scripts/fitness_families.py`. Comparable to
§25's budget.

**Prior.** ~20% that searching under the new fitness moves the consensus more
than 0.5 σ relative to its own null. Low: §29 found the quadgram estimator is
the *most charitable* of six to Dorabella, so a better estimator should if
anything widen the gap. But "should" is what this round exists to stop assuming.

---

## G. The phoneme point prediction — §30.1

**What.** Encipher real merged-phoneme English under a random 24-class MASC and
solve it with the report's **standard letter** quadgram model at the §4.2 budget.

**Why it matters.** It is a *point* prediction, fixed in advance, on a feature
the hypothesis was not built from: if Dorabella is phoneme-MASC, a letter-model
solve of one must land at Dorabella's own score, **≈ −4.68**. Land at −4.2 and
the text was letter-solvable anyway; land at −5.0 and it is indistinguishable
from noise. Both kill it.

**Status.** Envelope already passed (§30.1): unicity clears at 44–84 against 87,
and phoneme English separates from its shuffles at 10.2 pooled sd, three times
the letter margin. The Pitman-cognate rationale for the mirror pairs is refuted
and must be dropped — but the hypothesis does not need it.

**Cost.** About two minutes.

**Prior.** ~25% it lands within 0.1 of −4.68. The mechanism is right in kind
(a wrong unit produces exactly a model-invariant deficit), but the target is
narrow and nothing says the deficit's *size* should match.

---

## E. Pelling's provenance — §10.7, still the highest-value documentary question

Unchanged and still open: one email settles whether Pelling's 2012 reading was
independent of Hartmeier's 2006. It does not change the substantive conclusion
(§12.3 closed that), but it decides whether the three-reader triangulation has
three legs or two.

---

## What is now closed and should not be re-opened without new evidence

- **Phonetic English** (§25). Rejected on its own terms, with a passing
  positive control — not shelved, not untestable.
- **The transposition family** (§27). Exhausted; §16.2's caveat is discharged.
- **The mirror excess as evidence of design** (§26.2). Deflated: an ordinary
  keyword accounts for most of it without design intent.
- **Elgar's conversational register** (§19.2). Closed in Round 14 and not
  re-opened by anything since.
- **Local / short-scale transposition** (§31). Rejected; both pre-registered
  thresholds failed, one in the wrong direction.
- **Article III's music cipher** (§30.2). Struck: the ledger entry described a
  structure §15.1 had already shown is not in the primary source, and what
  remains is covered by §4/§8.3/§26 as substitution and by §5 as pitch mapping.
- **Mirror-pairs-as-doubles** (§30.3). Withdrawn before running, on §26.2.
