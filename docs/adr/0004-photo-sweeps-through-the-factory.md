# Photo Sweeps go through the household's factory; the photo stays on the phone only until confirmed

**Status:** accepted (the Governor, 2026-09-29; vault `plans/0024-grist-plan.md`)

Photographing an open Place is the cheapest way to capture what is in it, but
ADR-0003's round-trip asks a person to carry every photo into the Claude Project
by hand and carry the Sweep Result back. That is too slow to photograph a whole
kitchen. So a photo-assisted Sweep can now go straight from the app to the
household's own software factory: Postern's backend (the licensed door, protocol
§18) and the factory's mill, which runs the app's **sweep grind** and returns a
Sweep Result. The app sends the photo and a Sweep Request, carries on at once, and
shows the result for confirm/edit whenever it arrives. Several photos can be in
flight at a time.

This supersedes two earlier rules for this one path:

- **ADR-0003's "the photo never enters the app".** A photo now enters the app. It
  is kept on the phone only until its Sweep Result is confirmed or discarded, and
  is then deleted. It is never stored on an Item or Place, and never goes into a
  snapshot (ADR-0002 is unchanged). At the factory it is sealed to the mill's key
  in transit, opened only for the grind, and deleted once answered.
- **BUILD-SPEC's "no backend/API key" for v1.** The app now talks to one backend,
  through the provider seam ADR-0001 left for it. It still holds no secret: it
  proves itself with a key of its own and a licence the household's Governor
  issues. There is no API key in the app, in the factory, or anywhere else.

## How it works

- **Key and licence.** Each phone makes its own key, kept like Postern keeps its
  key (12 words, a passkey, one unlock a day) through the shared library both apps
  use. The Governor licenses a phone from Postern by scanning the QR code Cairn
  shows, and can revoke one phone alone.
- **The factory provider.** It sits in the bridge's provider seam above the manual
  file provider, which stays at priority 0 as the fallback (offline, no licence, or
  the factory down for good). Unlike the manual provider, it is asynchronous:
  submit, keep a pending Sweep, and receive the answer later.
- **Pending Sweeps.** Each pending Sweep is stored on the phone with its photo, in
  a table left out of snapshots. It moves waiting to send → at the factory → ready
  → added, discarded or failed. Nothing blocks the person.
- **Sweep Request / Sweep Result 1.1.** These are added beside 1.0, which the
  manual round-trip keeps using unchanged:
  - The request may carry the Place's known item and Container names, so the answer
    reuses them.
  - The result may mark an item `unsure`, may carry a `note`, and may propose
    Containers seen inside the photo, each with its own items.
- **Confirm before persist stays binding.** A Sweep Result is shown beside its
  photo for edit, and nothing is written until the person confirms.
- **The sweep grind.** Its instructions and answer schema live in this repo
  (`grinds/sweep.json`, `grinds/sweep.md`, the 1.1 schemas). The factory reads them
  at a landed commit, so they are versioned and reviewed with the app.

## Considered options

- **Keep the manual round-trip only**: rejected. Capture is the product's centre of
  gravity, and a whole-house sweep by hand does not happen.
- **Call a model API from the browser**: rejected, as in ADR-0001. It puts a
  secret on family phones.
- **Store photos on Places as a reference**: rejected for now, for ADR-0003's
  reasons (snapshot size, little gain for "where is it?").

## Consequences

- The importer gains 1.1 schemas with the same fence-stripping, validate-hard
  discipline.
- The app gains network code for the first time. It must behave offline: queue,
  send when online, and show *waiting for the factory* while its host is off.
- Household photos leave the house, to the factory and the model it runs, and are
  deleted after answering. The sweep grind is told never to describe people.
