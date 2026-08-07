# Dorabella Cipher — computational analysis

Sceptical cryptanalysis of Edward Elgar's cipher of 14 July 1897 (87 symbols in
3 lines, over an alphabet of 1–3 semicircular arcs in 8 rotations).

**No plaintext is claimed and none is believed.** The deliverable is a
characterisation: which hypotheses the evidence supports, which it excludes,
and which cannot be decided at this length. `REPORT.md` is the findings
document; start at its Abstract, then §20 (Conclusions) if you want the
outcome before the derivation.

If you are here to **audit** rather than read, §20.1 lists every headline claim
with its section, and the table below maps sections to the script that produced
them. Everything is re-runnable.

---

## The standing rules

These were adopted after each was violated at least once, and the violations
are documented in the report rather than quietly corrected. Any new experiment
should follow them.

1. **Matched search budget.** Observed text and nulls get *identical* restarts
   and iterations. A bigger budget raises the score on anything; the first
   Phase-4 run gave the observed text 40×20,000 against nulls at 12×12,000 and
   manufactured an effect that vanished on correction (§4).
2. **Identical-procedure nulls.** If the observed result is a best-of-N
   selection, the null must be the same best-of-N on shuffled text, so the
   selection effect is inside the null (§8.3, §12.2, §16.2).
3. **Length-matched nulls.** Shorter texts are easier to overfit. A 27-symbol
   row can be forced to read `TSINSTANDASTHINGSAREASURALR` at the 44th
   percentile of its own null (§4.3).
4. **Pre-registration for assembled models.** A model built from the features
   it is meant to explain must declare falsification targets on *held-out*
   features before running. §17.3's sixth model passed 6/6 held-out features
   and still failed the feature it was assembled for — which is only visible
   because the targets were fixed in advance.
5. **No constraint derived from the data it is then tested on.** A key family
   defined by an anomaly, searched on the text exhibiting that anomaly, scored
   against unconstrained nulls, triple-counts the evidence (§12.1, §17.2).
6. **Positive controls before interpretation.** Recovery of *known* enciphered
   English at n=87 (96%) is what licenses interpreting any solver output at all
   (§4.1). Where the control fails, the family is untestable, not rejected
   (§13.2).
7. **Documentary claims get primary-source checks.** Three failed (§20.1).

---

## Where each headline number comes from

| section | claim | script |
|---------|-------|--------|
| §1.1 | inter-transcriber disagreement (Hungarian alignment) | `scripts/compare.py` |
| §1.2 | image transcription scored vs consensus | `scripts/glyph_classifier.py` |
| §2, §3 | IC / entropy / Kasiski / Sukhotin, with nulls | `scripts/phase23.py`, `phase235_consensus.py` |
| §4.1 | positive control, 96% recovery at n=87 | `scripts/solver2.py` |
| §4.2 | matched-budget solving, all variants | `scripts/solver3.py` |
| §4.3 | corruption curve (error rate → expected score) | `scripts/noise_recalibrate.py` |
| §4.4 | crib-constrained solves | `scripts/cribs.py` |
| §5 | music mappings + dial test | `scripts/phase5.py`, `phase5b.py` |
| §6 | unicity distances | `scripts/phase5.py` |
| §7.2 | bitmap classifier, consensus consistency | `scripts/glyph_classifier.py` |
| §7.3 | register cost (Austen vs modern) | `scripts/register_cost.py` |
| §7.4 | invented-vocabulary dose | `scripts/nonce_words.py` |
| §8.1 | Elgar's key → dCode reproduction (85/87) | `scripts/three_readers.py` + inline |
| §8.3 | exhaustive 483,840-key sweep | `scripts/structured_keys.py` |
| §10.2 | three-reader triangulation | `scripts/three_readers.py` |
| §10.5 | residual deficit table | `scripts/crux_rerun.py` |
| §11.1 | Massey replication (mirror pairs, runs) | `scripts/massey.py` |
| §12.2 | additive-rotation sweep | `scripts/rotation_sweep.py` |
| §12.3 | 2¹³ latent labelling sweep | `scripts/latent_sweep.py` |
| §13.2 | homophonic family | `scripts/homophonic.py` |
| §15.2 | 4-model discrimination + posterior | `scripts/discriminate.py` |
| §16.2 | transposition sweep | `scripts/transposition.py` |
| §16.3 | 5-model discrimination | `scripts/discriminate5.py` |
| §17.1 | mirror-position clustering test | `scripts/mirror_positions.py` |
| §17.3 | pre-registered sixth model | `scripts/model6.py` |
| §18 | edition segmentation | `scripts/editions.py` |
| §19.2 | Elgar's measured register | `scripts/idiolect.py` |

Run outputs are committed under `out/*.log` — every number in the report can be
checked against the log that produced it without re-running anything.

---

## Data

| path | what | provenance |
|------|------|------------|
| `data/consensus.txt` | HistoCrypt majority consensus, 87 tokens (orientation A–H × arcs 1–3) | Hauer et al. 2025, Fig. 2 |
| `data/schmeh.txt` | Schmeh transcription, 87 chars | MysteryTwister |
| `data/dcode.txt` | dCode string — **not independent**, = Hartmeier 2006 (§10.1) | benzedrine.ch via dCode |
| `data/pelling.txt` | Pelling 2012 reading, 87 chars | ciphermysteries.com |
| `data/transcription.tsv` | my image-derived reading, with per-glyph confidence + alternates | this work; 81.6% correct vs consensus |
| `data/austen_letters.txt` | Austen's *Letters* | Gutenberg #42078 |
| `data/buckley1905.txt` | Buckley, *Sir Edward Elgar* (1905) | HathiTrust, Harvard scan (`hvd.ml19th`) |
| `data/dorabella_part_a*` | Hauer et al. code+data archive, split | Zenodo 10.5281/zenodo.4819086 |
| `sources/` | plate and article captures, with a manifest | see `sources/PROVENANCE.md` |

Reassemble the Zenodo archive with `cat data/dorabella_part_* > archive.tar.gz`.
It contains only the consensus transcription in four relabelings (§9) — no raw
reader transcriptions.

---

## Reproducing

```bash
pip install numpy scipy pillow scikit-learn networkx wordfreq matplotlib
cd research/dorabella

python3 scripts/phase235_consensus.py   # statistics + structural tests (~10 min)
python3 scripts/solver3.py              # matched-budget solving (~25 min)
python3 scripts/structured_keys.py      # exhaustive key sweep (~10 min)
python3 scripts/massey.py               # mirror-pair replication (~1 min)
python3 scripts/mirror_positions.py     # clustering test (~2 min)
python3 scripts/discriminate5.py        # model discrimination (~30 min)
```

The English corpus (`data/corpus.pkl`) is built on first use and cached; it is
gitignored because it is large and deterministic from `scripts/corpus.py`.

**Solver budget** is set per script as `RESTARTS × ITERS`. To compare anything
new against a published number here, use the same values as the script that
produced it — mixing budgets is rule 1, and it is the error this project most
often had to correct.

---

## Freeze point

This analysis was frozen after 15 rounds at commit **`3822b25`**
("Round 15: freeze — conclusion, reader-facing docs, TODOs, source artifacts")
on branch `claude/dorabella-cipher-analysis-xtnnsr`.

A local tag `dorabella-v1.0` marks it, but **the tag could not be pushed** —
the session's credentials returned HTTP 403 on tag creation. Use the commit SHA
to identify the freeze; anything after it is follow-up work.

---

## Open work

See `TODO.md`. Five items, each with the prior attached, so the next reader
inherits open questions rather than rediscovering them. The genre caveat in
TODO item 5 is load-bearing for anything built on §19.
