# Home App — Build Spec (one-shot brief)

You are implementing **Home App**, an offline-first PWA for one household. Build
it end-to-end. This document is the connective tissue; the **authorities below
are binding** and you must read them before writing code. Where this spec and an
authority disagree, the authority wins.

## Authorities — read first, in this order

1. `CONTEXT-MAP.md` — the product, its two bounded contexts, the shared kernel, the
   three decisions, and the design priority (**capture over query**).
2. `shared/CONTEXT.md`, `contexts/trips/CONTEXT.md`, `contexts/inventory/CONTEXT.md`
   — the ubiquitous language. **Use these exact terms as your type, route, and
   component names.** Do not invent synonyms the glossary lists under _Avoid_.
3. `docs/adr/0001`, `0002`, `0003` — the AI bridge, local-first snapshot sync,
   and photo-assisted sweep decisions, including what is deliberately **out of
   scope**.
4. The four wire schemas under `contexts/*/schemas/*.json` — the exact bridge
   contracts.
5. `docs/pwa-best-practices.md` — **binding for every PWA concern** (manifest,
   service worker/update flow, safe areas, scroll, keyboard, icons, SPA routing,
   storage persistence, CI). Follow it; do not re-derive it.
6. `docs/claude-project-instructions.md` — the other side of the bridge (context
   only; you don't build it, but the app's exports/imports must match it).

## Stack & conventions (pin these)

- React 18 + TypeScript (strict) + Vite + `vite-plugin-pwa` (Workbox) + Tailwind
  + Dexie (IndexedDB) + React Router 7. Tests: Vitest + `fake-indexeddb` +
  React Testing Library. Host: GitHub Pages via GitHub Actions.
- **Repository pattern** — UI and features never touch Dexie directly; all access
  goes through a context's `data/repositories`.
- **Context-first layout** — each context is a self-contained vertical slice; the
  kernel is shared. One Dexie database for the device; tables grouped by context.
- **Provider pattern with priority fallback** for the AI bridge: a manual,
  file-based provider now, behind a seam a network provider can later fill (ADR-0001).
- **Offline-first** — every feature works with no network; the bridge is the only
  thing that ever leaves the device, and only by manual file.

## Repository layout (target)

```
src/
  shared/            kernel: Person type, repository, the Dexie Db class, snapshot export/import
  contexts/
    inventory/
      contracts/     types + event bus for this context
      core/          domain logic (tree ops, search, verification)
      data/          repositories over Dexie
      features/      UI (home tree, item, search, sweep)
      features/*.feature   Gherkin specs
    trips/
      contracts/ core/ data/ features/ + *.feature
  bridge/            shared bridge plumbing: fence-stripping + schema validation,
                     provider seam, request export / response import
  app/               shell, routing, PWA registration, settings/about (+ version, snapshot UI)
```
Mirror each JSON schema as a Zod schema in `bridge/` (or the owning context) and
infer TS types from it — **the JSON schema is the single source of truth**; do not
hand-maintain a parallel type.

## Data model → Dexie schema

One database. Suggested `stores()` (add indexes you need; keep the keys):

```
// shared
persons:            "id, name"                 // + optional birthdate (unindexed)

// inventory
places:             "id, parentId, type, name, *aliases"   // type: floor|room|container; tree via parentId
items:              "id, name, *aliases"                    // no quantity, ever
placements:         "id, itemId, placeId, lastVerifiedAt"   // item kept at place (many-to-many); + lastVerifiedBy

// trips
destinations:       "id, name, *aliases"        // reusable; created on first use
tripKinds:          "id, name"                  // curated list the household grows
travelNotes:        "id, scopeType, scopeId"    // scopeType: household|kind|person|destination (scopeId null for household)
travellerProfiles:  "personId"                  // trips-only traits: dietary, packingQuirks[]
trips:              "id, destinationId, kind, startDate, *travellerIds"
tripPlans:          "id, tripId, importedAt"    // stores packingList[] (with local checked state) + sections[]
debriefs:           "id, tripId, completedAt"   // tracks which trips have been debriefed
```
Notes: an **Item** may have several **Placements** (multi-place). A **Place** is a
tree node; `parentId` null = a Floor. **Travel Notes** carry a `text` field;
`tripPlans` store the imported plan plus per-item `checked` booleans the app owns.

## The AI bridge (ADR-0001, ADR-0003)

- **Export**: serialise a Request (`plan-request` or `sweep`) to a downloaded
  `.json` file. Carry data only — the schema lives in the Project.
- **Import**: accept an uploaded `.json` file (or pasted text), **strip ```json
  fences if present**, then **validate against the Zod schema and reject hard on
  mismatch** with a clear error. Never persist unvalidated data.
- **Confirm before persist**: a Trip Plan's packing list and a Sweep Result's
  items are AI-fallible — show them for confirm/edit before writing to Dexie.
- The photo for a sweep is **never imported or stored** — it travels by hand.

## Feature acceptance criteria (Gherkin)

Write these as `*.feature` files and make them pass. Representative, not
exhaustive — cover the rest in the same spirit.

### Inventory
```
Scenario: Find by either family member's word
  Given an Item "dining cabinet" with alias "the hutch"
  When I search "hutch"
  Then the Item appears with its full Place path

Scenario: Confirm a placement keeps it fresh
  Given a Placement of "stapler" in "office desk" last verified 30 days ago
  When I tap "Found it"
  Then last verified updates to now and records who verified

Scenario: Correct a wrong placement
  Given a Placement of "stapler" in "junk drawer"
  When I tap "Actually at..." and pick "office desk"
  Then the stapler is placed in "office desk" and removed from "junk drawer"

Scenario: Sweep a place quickly
  When I start a Sweep on "Attic -> eaves closet"
  Then I can rapid-add item after item without leaving the place

Scenario: Photo-assisted sweep round-trip
  Given I exported a Sweep Request for "blue bin"
  When I import a valid Sweep Result file
  Then its items are shown for confirm/edit before being added to "blue bin"

Scenario: Reject a malformed import
  When I import a JSON file that fails the schema
  Then nothing is written and I see a clear validation error
```

### Trips
```
Scenario: Plan an already-decided trip
  Given a Trip to "Norman's house" for 3 named travellers in "family visit"
  When I export the Plan Request
  Then the file matches plan-request.schema.json and bundles every Travel Note
    whose scope (household, this kind, a traveller, or this destination) applies

Scenario: Import a plan and pack from it
  When I import a valid Trip Plan file
  Then the Packing List is interactive (check off items, see who each is for)
    and the other sections render as read-only titled prose

Scenario: Debrief captures knowledge
  Given a Trip whose end date has passed
  When I complete the Debrief (what worked / missing / remember)
  Then each answer is saved as a Travel Note with a confirmable scope
```

### Cross-cutting
```
Scenario: Snapshot sync (ADR-0002)
  When I export a snapshot on device A and import it on device B
  Then device B holds the same data (whole DB, schema-versioned; last import wins)
```

## PWA requirements

Satisfy `docs/pwa-best-practices.md` in full. Non-negotiables: relative
`start_url`/`scope` + Vite `base` for the Pages subpath; `registerType:
"autoUpdate"` + reload on `vite:preloadError`; `viewport-fit=cover` + safe-area
padding; body scroll lock with `100svh`; 16px inputs; native-feel CSS;
`404.html` SPA redirect; `navigator.storage.persist()`; build-time version shown
on an About/Settings screen alongside snapshot export/import.

## Testing & CI

- Cover the data layer with `fake-indexeddb`: schema validation + fence
  stripping, import round-trips, dedupe, search (name + alias), placement
  verification transitions, snapshot export/import, Dexie migrations.
- CI: lint → typecheck → test → build on every PR; deploy gated to `main` push
  (the workflow in the PWA doc). Keep the suite green at every build-order step.

## Build order

Each step ends green (typecheck + tests pass) before the next:
1. Scaffold + PWA shell (manifest, SW, safe areas, routing, 404 trick, About+version).
2. Shared kernel: Person, Dexie Db class, repository base, **snapshot export/import** (ADR-0002).
3. Inventory: Home Tree CRUD → Items + Aliases + multi-place Placements → search → Verification (one-tap confirm/refute/redirect) → typed Sweep.
4. Bridge seam: Zod mirrors of all four schemas, fence-strip + validate, export/import plumbing, provider seam.
5. Inventory photo-assisted Sweep (export Sweep Request → import Sweep Result → confirm → add).
6. Trips: Persons, reusable Destinations, curated Trip Kinds, Traveller Profiles, scoped Travel Notes, Trip CRUD.
7. Trips bridge: export Plan Request (bundling matching notes) → import Trip Plan → interactive Packing List + rendered Sections.
8. Debrief → scoped Travel Notes.
9. Polish: full PWA checklist pass, remaining `*.feature` coverage, CI.

## Definition of done

- [ ] All `*.feature` scenarios pass; data-layer tests green in CI.
- [ ] Both contexts usable offline; bridge export/import works file-based and
      rejects bad input.
- [ ] Code vocabulary matches the glossaries; no `_Avoid_` synonyms.
- [ ] PWA checklist satisfied; installs and runs from the home screen on iOS and Android.
- [ ] Snapshot export/import round-trips between two devices.

## Out of scope for v1 (do not build)

Quantities/stock counts; stored photos; real-time sync or any backend/API key;
destination suggestions; non-household guests; a drawn floor-plan/map. These are
deliberate (see the ADRs and glossaries) — don't gold-plate them.

## How to execute (be efficient)

- **Plan, then build**: read all authorities, restate a short build plan, then
  implement in the order above. Don't start coding before the plan.
- **Schema as source of truth**: generate Zod + types from the JSON schemas;
  never maintain a parallel hand-written copy.
- **BDD target**: write the `*.feature` files first; let them define "done" and
  drive implementation.
- **Reference, don't restate**: rely on the PWA doc and glossaries instead of
  re-deriving them; don't reproduce Workbox/manifest boilerplate the plugin
  generates.
- **Green checkpoints**: keep typecheck + tests passing at each build-order step
  rather than one big-bang integration at the end.
