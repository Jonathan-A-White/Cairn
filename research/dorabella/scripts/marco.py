"""Experiment 3 — the Marco arc-count known-plaintext test (TODO item 2).

Pelling reads the 1924+ notebook page as carrying `MARCO ELGAR` and
`A VERY OLD CYPHER` in the arc alphabet. Section 11.3 records this as the only
known-plaintext sample in the Dorabella alphabet known to exist; TODO item 2
proposed testing it through the arc-count channel -- the channel this project
reads most reliably -- and listed the blocker as capture resolution, with a
prior of 85% that the test would land.

The blocker was asserted, never measured. It is measured here, using a control
that costs nothing:

    THE SAME PAGE CARRIES ELGAR'S OWN KEY TABLE.

Twenty-four glyphs, same hand, same photograph, same resolution, each labelled
with its letter underneath. Under Elgar's key (section 8.1) the arc count of
ALPHA24[i] is i mod 3 + 1, so the table's true arc counts are 1,2,3 repeating
-- ground truth, free, drawn from the very image the test must read. An
extractor that cannot recover the key table's arc counts cannot be trusted on
the Marco line, and the family is blocked by capture rather than by cipher.

This is section 18.3's move (the 1947 plate) applied to the notebook: establish
what the image can support before reporting anything read from it.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
from PIL import Image
from scipy import ndimage
from scipy.stats import spearmanr

SRC = os.path.join(os.path.dirname(__file__), '..', 'sources', 'notebook_1924.gif')
ALPHA24 = "ABCDEFGHIKLMNOPQRSTUWXYZ"
RNG = np.random.default_rng(1924)

# Key-table rows on the page, with the letters each carries. Bands located by
# ink profile (see locate() below); the letter content is read off the plate.
KEY_ROWS = [((30, 45), "ABCDEFGHI"),
            ((56, 72), "KLMNOPQRS"),
            ((76, 94), "TUWXYZ")]
CAND_LINES = [(147, 167), (183, 203), (219, 239)]

CLAIMS = {'MARCO ELGAR':       ['MARCO', 'ELGAR'],
          'A VERY OLD CYPHER': ['A', 'UERY', 'OLD', 'CYPHER']}   # V->U, Elgar's merge


def arcs_of(word):
    return [ALPHA24.index(c) % 3 + 1 for c in word]


def banner(s):
    print("\n" + "=" * 78); print(s); print("=" * 78)


def load():
    a = np.asarray(Image.open(SRC).convert('L'), dtype=np.float64)
    ink = 255.0 - a
    ink[:4, :] = 0; ink[384:, :] = 0; ink[:, :4] = 0; ink[:, 741:] = 0   # frame
    return ink


def locate(ink, x0, x1, t=0.12):
    p = ink[:, x0:x1].sum(axis=1); p = p / p.max()
    on = p > t; runs, s = [], None
    for y, v in enumerate(on):
        if v and s is None: s = y
        elif not v and s is not None: runs.append((s, y)); s = None
    if s is not None: runs.append((s, len(on)))
    return [r for r in runs if r[1] - r[0] >= 3]


def seg_profile(ink, y0, y1, x0=20, x1=340, gap=2, t=0.10):
    """Column-profile segmentation."""
    p = ink[y0:y1, x0:x1].sum(axis=0); p = p / (p.max() + 1e-9)
    on = p > t; runs, s, off = [], None, 0
    for x, v in enumerate(on):
        if v:
            if s is None: s = x
            off = 0
        elif s is not None:
            off += 1
            if off > gap:
                runs.append((s + x0, x - off + 1 + x0)); s = None; off = 0
    if s is not None: runs.append((s + x0, x1))
    return [r for r in runs if r[1] - r[0] >= 2]


def seg_cc(ink, y0, y1, x0=20, x1=340, t=60, minpx=4):
    """Connected-component segmentation, merged by horizontal overlap."""
    b = ink[y0:y1, x0:x1] > t
    L, n = ndimage.label(b, structure=np.ones((3, 3)))
    out = []
    for i in range(1, n + 1):
        ys, xs = np.where(L == i)
        if len(xs) >= minpx:
            out.append((xs.min() + x0, xs.max() + 1 + x0))
    return sorted(out)


def main():
    ink = load()
    print(f"capture: 750 x 400 (sources/PROVENANCE.md flags this as too low for")
    print(f"the Marco test; that flag is now measured rather than asserted)")

    # ------------------------------------------------------------------
    banner("CONTROL 1 — can glyphs even be COUNTED at this resolution?")
    print("""
  Ground truth from Elgar's own key table on the same page. If segmentation
  cannot recover the number of glyphs in a row whose letters are printed
  underneath it, nothing read from the practice lines is interpretable.
""")
    print(f"  {'row':12s} {'true':>5s} {'profile':>8s} {'components':>11s}")
    hits_p = hits_c = 0
    for (y0, y1), letters in KEY_ROWS:
        tp = len(seg_profile(ink, y0, y1))
        tc = len(seg_cc(ink, y0, y1))
        hits_p += tp == len(letters); hits_c += tc == len(letters)
        print(f"  {letters:12s} {len(letters):5d} {tp:8d} {tc:11d}")
    print(f"\n  rows recovered exactly: profile {hits_p}/3, components {hits_c}/3")

    # ------------------------------------------------------------------
    banner("CONTROL 2 — does any feature carry ARC COUNT on known glyphs?")
    (y0, y1), letters = KEY_ROWS[0]
    runs = seg_profile(ink, y0, y1)
    truth = np.array(arcs_of(letters))
    print(f"""
  Key-table row 1 is the one row both methods segment consistently, so it is
  the only row on which a per-glyph feature can be scored at all.
  Letters {letters} -> true arc counts {list(truth)}.
""")
    if len(runs) != len(truth):
        print(f"  segmentation gives {len(runs)} glyphs for {len(truth)} letters — "
              f"cannot align; CONTROL 2 not evaluable.")
        return False

    width = np.array([b - a for a, b in runs], float)
    mass = np.array([ink[y0:y1, a:b].sum() / 255.0 for a, b in runs])
    print(f"  {'letter':7s} {'true':>5s} {'width':>7s} {'ink mass':>9s}")
    for L, t, w, m in zip(letters, truth, width, mass):
        print(f"  {L:7s} {t:5d} {w:7.0f} {m:9.1f}")

    def rank_assign(feat):
        order = np.argsort(feat)
        pred = np.empty(len(feat), int)
        pred[order] = np.repeat([1, 2, 3], len(feat) // 3)
        return pred

    for name, feat in (('glyph width', width), ('ink mass', mass)):
        rho, _ = spearmanr(feat, truth)
        # permutation null on the same statistic, matched procedure
        null = np.array([spearmanr(feat, RNG.permutation(truth))[0]
                         for _ in range(20000)])
        p = (null >= rho).mean()
        pred = rank_assign(feat)
        print(f"\n  {name:12s}: Spearman rho = {rho:+.3f}   permutation p = {p:.4f}")
        print(f"  {'':12s}  rank assignment: {(pred==truth).sum()}/{len(truth)} correct")

    # ------------------------------------------------------------------
    banner("CONTROL 2b — the held-out row")
    (y2, y2b), letters2 = KEY_ROWS[1]
    runs2 = seg_profile(ink, y2, y2b)
    truth2 = np.array(arcs_of(letters2))
    print(f"""
  Ink mass was picked on row 1, so row 1 cannot also test it. Row 2 is the
  other row the profile segmenter recovers exactly ({len(runs2)} glyphs for
  {len(letters2)} letters), and it was not used to choose the feature.
  Letters {letters2} -> true arc counts {list(map(int, truth2))}.
""")
    if len(runs2) != len(truth2):
        print("  row 2 does not segment cleanly; held-out test not evaluable.")
        return False
    mass2 = np.array([ink[y2:y2b, a:b].sum() / 255.0 for a, b in runs2])
    print(f"  {'letter':7s} {'true':>5s} {'ink mass':>9s} {'rank pred':>10s}")
    pred2 = rank_assign(mass2)
    for L, t, m, q in zip(letters2, truth2, mass2, pred2):
        print(f"  {L:7s} {int(t):5d} {m:9.1f} {int(q):10d}"
              + ("" if t == q else "   <- miss"))
    rho2, _ = spearmanr(mass2, truth2)
    null2 = np.array([spearmanr(mass2, RNG.permutation(truth2))[0]
                      for _ in range(20000)])
    print(f"\n  HELD-OUT: Spearman rho = {rho2:+.3f}  permutation p = "
          f"{(null2 >= rho2).mean():.4f}   rank assignment "
          f"{(pred2==truth2).sum()}/{len(truth2)} correct")

    # threshold transfer: fit cut points on row 1, apply to row 2 with no
    # per-row renormalisation and no knowledge of the 3-3-3 composition
    cuts = [(mass[truth == 1].max() + mass[truth == 2].min()) / 2,
            (mass[truth == 2].max() + mass[truth == 3].min()) / 2]
    pred_t = np.digitize(mass2, cuts) + 1
    print(f"  threshold transfer (cuts {cuts[0]:.1f} / {cuts[1]:.1f} fitted on row 1,")
    print(f"  applied to row 2 with no renormalisation): "
          f"{(pred_t==truth2).sum()}/{len(truth2)} correct")
    print(f"  the arc channel is quoted at 94-98% on the cipher plate (section 2.3)")

    # ------------------------------------------------------------------
    banner("LEG A — structural: do group sizes match the claimed words?")
    for name, words in CLAIMS.items():
        print(f"  {name:20s} predicts groups {[len(w) for w in words]}"
              f"  arc counts {[arcs_of(w) for w in words]}")
    print("\n  practice lines below the key table, both segmenters:")
    print(f"  {'band':14s} {'profile':>8s} {'components':>11s}")
    for y0, y1 in CAND_LINES:
        print(f"  y={y0:3d}-{y1:3d}     {len(seg_profile(ink, y0, y1)):8d} "
              f"{len(seg_cc(ink, y0, y1)):11d}")
    print(f"""
  MARCO ELGAR needs 10 glyphs, A VERY OLD CYPHER needs 14. The two segmenters
  disagree with each other on every line by more than the difference between
  those two targets, so the lines cannot be assigned to the claimed plaintexts
  on glyph count -- let alone read.
""")
    return False


if __name__ == '__main__':
    ok = main()
    banner("VERDICT")
    print(f"""
  The Marco test cannot be run on this capture, and the reason is now measured
  rather than asserted. Two findings, and they point opposite ways.

  POSITIVE. The arc channel is DETECTABLE at 750x400. Ink mass tracks arc
  count on Elgar's key table at rho = +0.95 on the row it was chosen on and
  rho = +0.90 on a held-out row (p = 0.0016). This is the project's first
  calibration of the arc channel against known plaintext in the arc alphabet
  -- not the Marco line, but the key table on the same page, which is known
  plaintext by construction because Elgar wrote the letters underneath.

  NEGATIVE, and decisive. Detectable is not reliable. On the held-out row the
  channel classifies 7/9 by rank and 6/9 by transferred threshold -- 67-78%,
  against the 94-98% at which this project reads the arc channel on the cipher
  plate. And upstream of that, glyph segmentation itself fails: the two
  segmenters recover the key table's glyph count in 2/3 and 1/3 of rows, and
  disagree on every practice line by more than the 4-glyph difference between
  MARCO ELGAR (10) and A VERY OLD CYPHER (14). A channel read at 70% through
  boundaries that are wrong cannot test a 10-glyph prediction.

  What would unblock it: the median key-table glyph is ~9 px wide, giving a
  3-arc glyph ~3 px per arc, at which an arc is indistinguishable from a
  stroke join. Reliable separation needs ~6 px per arc, so ~18 px per glyph --
  a capture at 2x-3x linear resolution, 1500-2250 px across. The page is held
  by the Elgar Birthplace Museum. TODO item 2's 85% prior is neither confirmed
  nor refuted; the experiment could not be run.

  The claim that the page carries known plaintext in the arc alphabet
  (section 11.3, from Pelling) is NOT tested here and remains uncorroborated
  by this project. It should be carried as a reported reading, not as a
  measurement.
""")
