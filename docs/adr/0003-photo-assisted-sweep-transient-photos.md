# Photo-assisted Sweep rides the manual AI bridge; photos are transient and never stored

**Status:** accepted

A Sweep can be accelerated by photographing an open Place (cabinet, shelf, bin)
and letting the household's Claude Project extract its contents: the app
exports a **Sweep Request** (target Place + instructions + result schema), the
user attaches the photo by hand in the Project chat, and the app imports the
returned **Sweep Result** JSON as Items in that Place. This widens ADR-0001's
round-trip bridge to a second consumer (HomeInventory), which is therefore no
longer a strictly AI-free context. The photo itself never enters the app — it
travels camera-roll → chat by hand — so the store stays text-only and
ADR-0002's snapshot files stay small.

## Considered options

- **Store photos on Items/Places** — rejected for v1: balloons snapshot-file
  sync and adds blob handling for little gain in answering "where is it?".
- **No photo path (typed Sweeps only)** — rejected: photographing a shelf is
  the single cheapest way to capture its contents, and capture is the product's
  center of gravity.

## Consequences

- The importer gains a second versioned schema (Sweep Result) with the same
  fence-stripping, validate-hard discipline as Trip Plans.
- AI-extracted item names will need a confirm/edit step before persisting —
  vision output is fallible.
