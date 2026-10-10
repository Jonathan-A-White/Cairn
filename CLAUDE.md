# Cairn

Its own docs are the law: `docs/BUILD-SPEC.md`, `docs/adr/`, `CONTEXT-MAP.md` and `contexts/`.

## Grinds and their examples

Each grind (`grinds/<kind>.json`) keeps BDD-style scenarios under `grinds/examples/<kind>/<name>.json`: the request (with `schemaVersion`), optional photos beside it, and an `expect` block of simple checks on answer fields. Format: `grinds/examples/README.md`. `mw grist smoke cairn` runs them against the real grist; `src/bridge/grindExamples.test.ts` validates every request against the input schema and every `expect` path against the answer schema, and fails when a grind has no example.

**When you change a grind's behaviour (its instructions, schemas, or what the app sends), update or add its examples in the same story. A new grind ships with at least one example.**
