# Pre-registration — Experiment 2: keyword-mixed Heraldic sweep

**Written before any keyword alphabet was built and before any of them touched
the consensus transcription.** Standing rules 4 and 5.

---

## What is being swept, and why it is not already covered

§8.3 exhausted **483,840 standard-alphabet layouts** of the Heraldic/notebook
geometry: 24 letters (no J, no V) in 8 orientation-groups of 3, swept over all
8! group orderings × 3! arc orderings × 2 layouts (orientation-major and
count-major). It came back at the null (best −6.272 against −6.266 ± 0.083,
p = 0.500).

That sweep permutes **where each triplet sits**. It does not change **which
letters form a triplet** — those are fixed by alphabetical order: `(A,B,C)`,
`(D,E,F)`, … A keyword-mixed alphabet changes exactly that. `MALVERN` over the
24-letter alphabet gives `M,A,L,E,R,N,B,C,D,F,G,H,I,K,O,P,Q,S,T,U,W,X,Y,Z`, so
the triplets become `(M,A,L)`, `(E,R,N)`, `(B,C,D)`, … §8.3 cannot reach these.
§16.1 identified the gap and named it as the cheapest remaining probe;
`TODO.md` item 1 and §21 item 3 both carry it. It has never been run.

## Why it targets the §17.4 open problem specifically

The best-supported reading (§20.2 item 1) is a substitution key that *mirrors
common bigrams*. Its one implausible feature is that it requires Elgar to have
**designed** the key that way. A keyword mixing that happens to seat `ER`, `AN`
or `IN` on opposite orientations produces the same mirror structure as a
**byproduct of an ordinary period key-making habit**, with no design intent.
That would dissolve the implausibility without adding any machinery.

## The two legs, and why the first is exhaustive and free

**Leg A — the mirror geometry, solved in closed form.** Under layout A a mirror
pair is two glyphs of the same arc count whose orientations are 180° apart, so
the letter pair is `MIXED[g[o]*3 + t]` against `MIXED[g[o+4]*3 + t]`. As `t`
runs over all three arc counts the arc permutation `h` cancels: the set of 12
mirror-producing letter pairs depends **only on how the eight triplets pair up**
across the dial. There are 105 such pairings, and 105 again for layout B. So
the mirror-producing bigram share over the whole 483,840-key family collapses
to **210 evaluations per keyword** — exhaustive, exact, and instant. This also
means a dictionary pass over thousands of keywords is affordable, and it will
be run.

**Leg B — the solver.** The score does depend on the full key, so this is the
full 483,840-key sweep per keyword, matched to §8.3's procedure and nulled by
the identical best-of-family procedure on shuffled text (standing rule 2).

## Keywords, fixed now

Period-anchored, from `TODO.md` item 1 and the 1897 context:
`MALVERN`, `FORLI`, `CAROLINE`, `ALICE`, `CAROLINEALICE`, `CALICE`,
`CRAEGLEA`, `WORCESTER`, `EDWARDELGAR`, `BRAUT`.

Plus an unrestricted **dictionary pass** on leg A, since leg A is free.

**`ENIGMA` is excluded, and the exclusion is stated so a reviewer does not catch
it first.** The *Enigma Variations* were composed in 1898–99 and first performed
in June 1899; the Dorabella note is dated 14 July 1897. Using `ENIGMA` as a
keyword would be an anachronism of roughly two years — the cipher predates the
word's association with Elgar entirely. It is excluded on those grounds and not
because it scores badly; it is not scored at all.

## Pre-registered thresholds and priors

**Q1 — can the geometry seat common bigrams opposite at all?** A keyword passes
leg A if its best layout reaches a mirror-producing bigram share of **≥ 10%**
(expected ≥ 8.6 pairs in 86 slots, which puts the observed 13 within about
1.5 sd and therefore unremarkable). The unconstrained ceiling is 12.19% (§11.2,
as re-derived in §23); Elgar's own key is 6.63%.

*Prior: 10% that any period keyword reaches 10%, and 35% that some dictionary
word does.* Low, because the triplet geometry is rigid: the 12 mirror pairs are
forced to be three consecutive-in-mixed-alphabet letters against three others,
which is a far harsher constraint than the free matching that produces 12.19%.

**Q2 — does any keyword beat the null on the solver?** Best-of-family against
the identical best-of-family procedure on shuffled text, matched budget.
Threshold: **z ≥ +2** against that null.

*Prior: 20%*, carried over unchanged from `TODO.md` item 1. Low because §8.3
and §12.2 both returned null on the same geometry, but this is the cheapest
remaining shot.

## What a positive result on leg A would and would not mean

If a keyword reaches 10%, it shows the mirror excess **could** arise without
design. It would **not** identify the key: leg A scores a geometric property of
the alphabet, not a decipherment, and a key that mirrors well can still fail to
produce English. Only leg B can speak to that, and only against its own null.

If leg A succeeds and leg B fails — which is the outcome I most expect — the
honest statement is that the mirror excess loses its implausibility while the
decipherment gains nothing, and the §17.4 constraint is untouched. That
statement is written here, before the run, so it cannot be dressed up later.
