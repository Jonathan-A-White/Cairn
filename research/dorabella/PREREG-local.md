# Pre-registration — Round 22: the local / short-scale transposition family

**Written before the family touched the consensus transcription.** Standing
rules 4 and 5.

---

## Why this family, and why it is the last mechanism-side candidate

§20.3 named it and did not run it:

> "…or a transposition confined to a scale shorter than the adjacency window,
> which would preserve local pairs while disrupting longer n-grams. That last is
> untested and is the most obviously missing member of the model set."

§27 then exhausted the columnar family — all 46,232 orderings — and found the
observed text scoring *below* its own null (z = −0.85, p = 0.800). Columnar
transposition is long-range: it moves characters tens of positions, destroying
bigram adjacency wholesale, which is exactly why §17.3's composed model failed.
**A short-scale transposition is the complement**, and it is the one shape of
mechanism left that could, by construction, do what the remaining explanandum
requires:

- **preserve bigram adjacency** — a permutation whose maximum displacement is
  a few positions leaves most adjacent pairs adjacent;
- **wreck quadgram fitness** — any scrambling inside a 4-character window
  destroys quadgrams outright.

After §26.2 partly dissolved the mirror excess (an ordinary keyword accounts for
most of it), the solver deficit is the sole remaining explanandum, and this is
the only mechanism-side candidate for it that has not been swept.

## The family, defined precisely

Three components, all applied as candidate *inverse* permutations to the
ciphertext, with the residual then solved as a MASC — §16.2's and §27's
procedure exactly.

**1. Block-periodic permutations.** Partition the 87 positions into consecutive
blocks of *w* and apply the *same* permutation π ∈ S_w to every block.
Parameters: window `w ∈ {2,3,4,5,6}`, `π ∈ S_w`, block offset `o ∈ {0,…,w−1}`
(so blocks need not align with position 0; any leading partial block is left in
place).

**2. The same, restarting at each line boundary.** The note is three lines of
29 / 31 / 27. A scribe working line by line would reset the pattern at each
line, so every member of (1) is also generated with blocks restarting at
positions 0, 29 and 60.

**3. Sparse single swaps at longer period.** For `w ∈ {7,8}`, full S_w is
5,040 and 40,320 and would swamp the family with permutations that are no longer
local. Instead only the strictly-local members are taken: a single adjacent
transposition (i, i+1) within each block, `i ∈ {0,…,w−2}`, over all offsets,
whole-text and per-line. This covers "swap every 7th or 8th adjacent pair"
without admitting long-range members.

**Size, verified before pre-registering:** 10,272 generated, **9,129 distinct**
after deduplication by the resulting index permutation. Maximum displacement is
**≤ 5 for every member** (histogram: 1 member at 0, 254 at 1, 813 at 2, 2,055 at
3, 3,414 at 4, 2,592 at 5), which is the property that makes this family *local*
rather than merely small. The identity is present and is reported separately as
the baseline. **9,129 against §27's 46,232 — a fifth of the columnar sweep's
cost**, so it is run exhaustively.

**Explicitly excluded, with reasons.** Rail-fence and other zigzag routes are
*not* local — a 3-rail fence moves characters across the whole text — and
§16.2's route variants already covered that shape. Bounded-displacement
permutations in full generality are not enumerable: permutations of 87 elements
with displacement ≤ 1 alone number Fib(88) ≈ 10¹⁸, which is why the family is
structured periodically rather than defined by a displacement bound.

## Procedure

§27's two-stage protocol, unchanged: cheap scan (1 × 2500) over all 9,129, then
the top 25 re-solved at §16.2's budget (8 × 9000). **The null runs the identical
two-stage best-of-9,129 procedure on shuffled text**, 5 reps, so the selection
sits inside it (standing rule 2).

**No sieving on statistics measured on this text.** The family is defined by its
geometry alone. It is not filtered by mirror-pair count, by IoC, or by anything
else measured on the consensus — §12.1's circularity, which this report has had
to correct once already.

## Pre-registered thresholds

**Q1 — does the family beat its own null?** Threshold **z ≥ +2** for the best
member against the identical best-of-9,129 null.

**Q2 — and does it beat doing nothing?** §27.2's lesson is that a family-level z
can be carried entirely by the identity member. The quantity that speaks to the
mechanism is the **gain over identity**, and §28.4's spread rule sets the bar:
the gain must exceed the identity's own seed-to-seed spread at the same budget,
which §27.2 measured at **0.153**. A gain smaller than that is not an effect,
whatever its z.

Both must pass. If Q1 passes and Q2 fails, the finding is recorded as "the
family adds nothing beyond what §4 already established", which is what happened
to §16.2 and §26.3.

**If both pass**, the model is assembled from the feature it explains and rule 4
applies: before any claim, the winning member is tested on **held-out features
it was not selected for** — the mirror-pair count of the un-transposed sequence,
its IoC, its entropy, its doubled-symbol count and its repeated-bigram count,
each against the §15.2 model bands. Declared now so the targets cannot be chosen
afterwards.

## Prior

**~12% that the family lands (both Q1 and Q2).** Higher than §27's 5% because
§20.3 identified this shape on mechanism grounds rather than by enumeration, and
because it is the complement of the family that just failed. Low in absolute
terms because the deficit has now survived an exhausted columnar sweep, an
exhausted key geometry, an exhausted rotation family, a keyword-mixed sweep and
a rejected phonetic hypothesis, and because a 9,129-member family will find
*something* on noise — which is precisely what the matched null is for.

**~40% that Q1 passes on its own**, i.e. the same carried-by-identity result
that §16.2 and §26.3 produced. That outcome would be uninformative and is
pre-labelled as such here so it cannot be presented as a positive later.
