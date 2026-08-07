# Open work, with priors attached

Five items. Each states what was *not* done, what I expect, and why — so the
expectation is on record before the experiment, not after. Where I give a
probability it is a genuine prior, not a hedge; hold me to it.

---

## 1. Keyword-mixed Heraldic sweep — never run

**What.** §8.3 exhausted all 483,840 *standard-alphabet* layouts of the
Heraldic/notebook geometry (24 letters, no J or V, orientation × 1–3 ticks).
It did **not** cover keyword-mixed alphabets laid into the same triplet
geometry: mix the alphabet on a keyword, then group in threes.

**Why it matters.** It is the only untested family that could produce the
mirror structure of §11.2 as a **byproduct** rather than by design — a keyword
mixing that happens to seat ER/AN/IN opposite gives a mirror-structured
substitution without Elgar intending mirrors at all. That would dissolve the
one implausible-feeling feature of the best-supported reading.

**Prior.** ~20% that some keyword lands materially above the null. Low, because
§8.3 and §12.2 both came back at null on the same geometry — but this is the
cheapest remaining shot and it targets the §20.3 open problem directly.

**Candidate keywords.** Period-anchored: `MALVERN`, `FORLI`, `WORCESTER`,
`CRAEGLEA`, `EDWARDELGAR`, `CAROLINE`, `ALICE`, `CAROLINEALICE`, `CALICE`.
**Exclude `ENIGMA`** — the Variations postdate the July 1897 note by ~2 years.
Note the exclusion in any write-up so a reviewer does not catch it first.

**Discipline.** Exhaustive within the keyword list, identical best-of-family
procedure on shuffled nulls (rule 2), pre-registered keyword list before
scoring (rule 5).

---

## 2. Marco arc-count known-plaintext test — never run

**What.** The 1924+ notebook page carries `MARCO ELGAR` and `A VERY OLD CYPHER`
enciphered in the arc alphabet (§8.4 retraction). The arc-count channel is the
one this project reads at 94–98% accuracy. Extract arc counts from those lines
and check them against the arc counts the known plaintext predicts under
Elgar's key.

**Why it matters.** It is the only **positive** experiment left on the table,
and the only known-plaintext sample in the arc alphabet known to exist. A
confirmed calibration line strengthens the transcription chapter regardless of
outcome.

**Prior.** ~85% it lands — the key is known (§8.1), the plaintext is known, and
the arc channel is the reliable one. If it *fails*, that is far more
interesting than if it succeeds: it would mean the 1924 key does not encipher
its own page, which would put §8.1 in question.

**Blocker.** Needs a higher-resolution capture of the notebook page than the
750×400 GIF used so far.

---

## 3. Full columnar sweep — §16.2 is not exhaustive

**What.** The transposition sweep tested **21** permutations (columnar k=2–8
with identity and reversed column orders, plus route variants). A complete
sweep is all *k*! column orderings: **46,232** for k ≤ 8.

**Why it matters.** §16.2 is the only place this report says a family was
swept without meaning exhausted, and it says so inline. In a report whose
other two sweeps are genuinely exhaustive, that asymmetry should not survive.

**Prior.** ~5% that the full sweep finds anything the subset missed. The
best member (`reverse`) beat identity by 0.079 from 21 tries against a null sd
of 0.050 — pure selection. But cheap compute makes "exhausted" mean exhausted.

---

## 4. Interrupted latent null — §12.3

**What.** The matched-budget null for the 2¹³ latent labelling sweep was
interrupted by a container restart at **2 of 8 reps** (−4.841, −4.927, both
below the observed −4.686). Flagged inline as incomplete.

**Prior.** ~95% the completed null confirms the reported conclusion, since that
conclusion rests on an *absolute* comparison (best of 8192 = −4.613 against the
English band at −4.196 ± 0.168), not on the null. Finish it anyway — an
incomplete null in a report about null discipline is a bad look, and it is
~40 minutes of compute.

---

## 5. The genre caveat on §19 — load-bearing, read before building on it

**This is the item most likely to be misread, so it is stated at length.**

§19.2 measured Elgar's register from Buckley (1905) and found it
**indistinguishable from ordinary English** — marginally *more* ordinary, at
+0.021 above the modern reference. That closed the idiolect-as-register branch.

**What was actually measured:** Elgar's *conversational* register, as recorded
and filtered by a biographer, plus quoted speech in a published book.

**What was not measured:** Elgar's *epistolary-playful* register. His letters —
not his conversation — are the documented home of his phonetic spellings,
coinages and private jokes. `warbling wigorously` is the register in question,
and none of it is in Buckley.

**So the finding constrains** "Elgar spoke and was quoted in ordinary English",
**and does not constrain** "Elgar wrote a deliberately playful, phonetically
spelled, coinage-dense note to a young friend". Those are different genres and
§19.2 only reaches the first.

**Consequence.** Surviving hypothesis (2) in §20.2 — deliberate coinage at the
40–50% dose priced in §7.4 — is **not** closed by §19.2, and any reading of the
report that treats it as closed is wrong.

**The measurement that would close it:** run `scripts/idiolect.py` over a
corpus of Elgar's actual letters. Dora Penny's memoir reproduces several; the
published *Letters of Edward Elgar* (ed. Young) has many more. If his
epistolary register lands at −4.3 to −4.4, hypothesis (2) gains its first
empirical support. If it sits on the reference band with his conversation, (2)
loses its last escape route and (1) stands alone.

**Prior.** ~60% that his letters score measurably below his conversation, but
~15% that they reach the −0.3 to −0.4 depth hypothesis (2) requires. The
playfulness is real and documented; the *dose* is what is in question, and §7.4
priced that dose at half the words in the note.
