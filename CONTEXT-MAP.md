# Context Map — Cairn

A multi-context Progressive Web App for the household. Each capability is a
self-contained bounded context layered over a small shared kernel, so new
contexts can be added without disturbing existing ones.

## Purpose (the "why")

Much of how this household runs — where things are kept, and how this family
travels — lives as tacit knowledge in one person's head (Grace). This app
exists to **externalize that knowledge** into a shared, structured form that
both spouses and the kids can use. The product's center of gravity is therefore
**low-friction capture**, not querying: getting knowledge in (and keeping it
fresh) is the hard, valuable part; looking it up is the easy payoff.

## Design priorities (consequences of the purpose)

- **Capture over query.** Optimize first for the experience of *entering* and
  *correcting* knowledge. Lookups are simple reads and can stay plain.
- **Learning loop = progressive capture.** In both contexts the "learning loop"
  is the mechanism by which tacit knowledge becomes explicit over time — every
  correction (inventory) and every completed trip (trips) leaves the store a
  little richer. For trips, that accumulated knowledge is also what feeds the
  next AI Plan Request, so the loop and the AI bridge reinforce each other.

## Contexts

- [HomeInventory](./contexts/inventory/CONTEXT.md) — answers "where is it?" by
  modelling the physical home (floors incl. attic, rooms, storage) and the
  items kept in it. Data is local; capture can optionally ride the AI bridge
  (photo-assisted Sweep, ADR-0003).
- [TripPlanning](./contexts/trips/CONTEXT.md) — turns travellers + an
  already-chosen destination + dates + trip kind into a structured, detailed
  Trip Plan, drafted by an external Claude Project via a manual file-based AI
  bridge. Destination is always provided; there is no "suggest a destination"
  mode.

## Shared kernel

Lives in [shared/CONTEXT.md](./shared/CONTEXT.md). Deliberately minimal — a
concept only enters the kernel once a second context genuinely needs it.

- **Person** — a member of the household; referenced by TripPlanning (as a
  traveller) and available to future contexts. The kernel's only concept:
  "Feedback" was deliberately dropped — each context owns its concrete
  learning-loop mechanism, and no shared type is needed.

## Relationships

- **HomeInventory → shared**: depends on **Person** (who verifies a
  Placement). Its loop: Verification -> last-verified stamps.
- **TripPlanning → shared**: depends on **Person** (travellers, note scopes).
  Its loop: Debrief -> scoped Travel Notes -> richer next Plan Request.
- **HomeInventory ↔ TripPlanning**: no coupling today. Likely future bridge: a
  "what do we already own that we should pack?" query — noted, not built.

## AI integration (v1) — see ADR-0001

No LLM API, no secret, no backend. The app exchanges JSON **files** with the
user's own Claude **Project**, against versioned schemas the Project holds in
its instructions. Two consumers: TripPlanning (Plan Request -> Trip Plan) and
HomeInventory's photo-assisted Sweep (Sweep Request -> Sweep Result, the photo
travelling by hand and never stored — ADR-0003). The importer strips code
fences and validates hard. The bridge sits behind the provider seam so a real
API can replace it later.

## Conventions inherited from SpellForge

- Repository pattern — UI never touches Dexie directly.
- Central contracts + event bus, scoped per context.
- Provider pattern with priority fallback — in v1 the trip "AI provider" is a
  human, file-based bridge, not an HTTP client.
- Offline-first — every context works with no connectivity.

## Decisions (ADRs)

- [ADR-0001](./docs/adr/0001-ai-via-file-based-json-round-trip.md) — AI via a
  manual, file-based JSON round-trip through a Claude Project (accepted).
- [ADR-0002](./docs/adr/0002-local-first-snapshot-sync.md) — v1 is local-first
  per device; cross-device sync is a manual snapshot file (accepted).
- [ADR-0003](./docs/adr/0003-photo-assisted-sweep-transient-photos.md) —
  photo-assisted Sweep rides the manual bridge; photos transient, never stored
  (accepted).

## Build artifacts

- [docs/BUILD-SPEC.md](./docs/BUILD-SPEC.md) — the one-shot brief for Claude
  Fable 5 in Claude Code; references everything here as binding authorities.
- [docs/claude-project-instructions.md](./docs/claude-project-instructions.md) —
  the standing instructions for the household's Claude Project (the other side
  of the bridge; holds the response schemas).
- [docs/pwa-best-practices.md](./docs/pwa-best-practices.md) — copied in from
  night-stack; binding for every PWA concern.

### Wire schemas (bridge contracts, source of truth)

- trips: [plan-request](./contexts/trips/schemas/plan-request.schema.json)
  (app → Project), [trip-plan](./contexts/trips/schemas/trip-plan.schema.json)
  (Project → app)
- inventory:
  [sweep-request](./contexts/inventory/schemas/sweep-request.schema.json)
  (app → Project),
  [sweep-result](./contexts/inventory/schemas/sweep-result.schema.json)
  (Project → app)

## Status

- [x] Context boundaries: two contexts + shared kernel, extensible
- [x] Product purpose: externalize one family member's tacit knowledge; capture
      is the primary surface
- [x] AI delivery: file-based two-way JSON round-trip via the user's Claude
      Project; no API/backend (ADR-0001)
- [x] Trip destination is always given; "suggestions" variant dropped; Trip Plan
      is always the detailed kind
- [x] Data residence: local-first per device; sync is a manual snapshot
      export/import behind a sync seam (ADR-0002)
- [ ] "Learning loop" semantics, per context
- [x] TripPlanning domain model — glossary complete (Trip, Traveller, Traveller
      Profile, Trip Kind, Destination, Travel Note, Debrief, Plan Request, Trip
      Plan, Packing List, Plan Section); JSON schemas are implementation work
      under ADR-0001's versioning rule
- [x] Photo-assisted Sweep through the same bridge; photos transient
      (ADR-0003); inventory is no longer a strictly AI-free context
- [x] HomeInventory domain model — glossary complete (Home Tree, Place, Floor,
      Room, Container, Item, Alias, Placement, Verification, Sweep, Sweep
      Request, Sweep Result); no quantities, no stored photos
