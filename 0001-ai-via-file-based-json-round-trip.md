# AI integration is a manual, file-based JSON round-trip via a Claude Project — not an API call

**Status:** accepted

The app is a static, offline-first PWA on GitHub Pages with no server and no
secret store, but TripPlanning needs an LLM. Rather than introduce an API key
(which can't live safely in a static client shipped to family members) or a
backend to hold one, the app integrates with the user's own Claude **Project**
by file exchange: it **exports** a JSON file (the Plan Request) which the
Project reads, and **imports** a JSON file (the Trip Plan) which the Project
emits, both conforming to a versioned schema the Project holds in its
instructions. This keeps the app fully static, offline-capable, and
secret-free, and — because the app now holds the structured output — makes the
trip learning loop possible.

## Considered options

- **Direct browser API call with a user-supplied key** — rejected: puts secrets
  in family members' browsers and trusts client storage.
- **Minimal proxy / Go backend holding one key** — rejected for v1: reintroduces
  a server and breaks the static/offline model for a personal app; deferred as a
  possible later provider.
- **One-way prompt only (no import)** — rejected: the app never sees the result,
  so trips would have nothing to learn from.

## Consequences

- The trip "AI provider" sits behind the existing provider seam, so a real API
  provider can replace the manual bridge later with no domain changes.
- Two manual file steps per plan (export -> run in Project -> import).
- A human can supply edited or malformed JSON, so the importer must strip code
  fences and validate against the schema before persisting.
- The Trip Plan / Plan Request schemas must be explicitly versioned, since the
  app and the Project evolve independently.
