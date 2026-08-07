# Dorabella Cipher — computational analysis

Skeptical cryptanalysis of Edward Elgar's 1897 Dorabella cipher (87 symbols,
3 rows). The goal is characterisation and hypothesis ranking, **not** a
claimed plaintext. See `REPORT.md` for findings.

## Layout

| path | what |
|------|------|
| `data/transcription.tsv` | 87-glyph transcription with per-glyph confidence + alternates |
| `scripts/glyphs.py`      | locates the cipher band, segments the 87 glyphs |
| `scripts/classify.py`    | arc-count / orientation geometry from the ink |
| `scripts/sheets.py`      | magnified per-glyph contact sheets for visual reading |
| `scripts/ensemble.py`    | builds the 6-variant transcription ensemble |
| `scripts/corpus.py`      | synthesised English reference corpus + n-gram models |
| `scripts/phase23.py`     | Phase 2 statistics, Phase 3 structural tests |
| `scripts/solver.py`      | Phase 4 hill-climbing solver (first run) |
| `scripts/solver2.py`     | Phase 4 corrected: matched search budget + length-matched nulls |
| `scripts/phase5.py`      | Phase 5 music hypothesis + unicity distance |
| `scripts/phase5b.py`     | Phase 5 orientation-only pitch mapping |

## Reproducing

```bash
pip install numpy scipy pillow wordfreq
python3 scripts/glyphs.py      # segmentation (writes contact sheets to out/)
python3 scripts/phase23.py     # Phase 2 + 3
python3 scripts/phase5.py      # Phase 5 + unicity distance
python3 scripts/solver2.py     # Phase 4 (slow, ~10 min)
```

The transcription is derived from the supplied image of the public-domain
scan; published transcriptions were unreachable from this environment. Its
limitations are documented in `REPORT.md` §1.
