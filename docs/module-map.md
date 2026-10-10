# Cairn module map

Which module owns what, which files every story collides on, and the splits that would let two stories change two modules at once. Written 2026-10-10 at commit 616f975 (story mw-vtjxh4.23). It describes the code as it is and proposes changes; it moves no source file and changes no behaviour.

The rule behind it is the Governor's: draw the boundaries so two stories can change two modules at once without touching each other (seats/builder/pwa-best-practices/27-modular-boundaries.md). The factory runs stories of one rig in series when they touch the same file, so a file every feature edits serialises the whole backlog.

Writing convention, so a script can check this page: a path in backticks is a file or folder in this repo that exists today. A file or module that is only proposed, a path in another repo, and a library name are written without backticks.

Contents: [1 Modules](#1-modules) · [2 Collisions](#2-collisions) · [3 Proposed refactors](#3-proposed-refactors) · [4 Rule breaks](#4-rule-breaks) · [5 Library candidates](#5-library-candidates)

## 1. Modules

Cairn has two bounded contexts over a tiny shared kernel (`CONTEXT-MAP.md`, `contexts/inventory/CONTEXT.md`, `contexts/trips/CONTEXT.md`, `shared/CONTEXT.md`), plus an app shell and a bridge. Every context has the same four folders: contracts (types and events), data (repositories), core (domain functions), features (screens). No folder has an entry file: callers import deep paths, so the "API" below is the set of files other modules actually import.

| Module | One responsibility | Entry files and exported API | Imports |
| --- | --- | --- | --- |
| App shell | Mount the app, route to screens, draw the tab bar, register the service worker | `src/main.tsx` (no exports); `src/app/App.tsx` exports `App`; `src/app/Layout.tsx` exports `Layout` and holds the tab list | both contexts' screens, `src/app/` modules, react-router |
| UI kit | The look: buttons, fields, card, screen frame, hints | `src/app/ui.tsx`: `Button`, `TextInput`, `TextArea`, `Select`, `Card`, `Screen`, `EmptyHint`, `ErrorNote` | react only |
| Async loading hook | Run a repository loader from a screen and reload after a change | `src/app/useAsync.ts`: `useAsync<T>(loader, deps): AsyncState<T>` | react only |
| App update | A new build waits behind the old one until he taps; check on start, on return, every 30 minutes | `src/app/appUpdate.ts`: `startAppUpdates`, `useUpdateState`, `getUpdateState`, `applyUpdate`, `UPDATE_CHECK_EVERY_MS`, `TAKE_OVER_PATIENCE_MS`; `src/app/UpdateBanner.tsx`: `UpdateBanner` | react only |
| Build stamp | Format the version string Settings shows | `src/app/buildVersion.ts`: `buildVersion(version, when, commit)`; `build-version.ts` (repo root, read by `vite.config.ts`): `shortCommit`, re-exports `buildVersion` | node child_process (root file) |
| Credits | The list of everything Cairn builds on, and the checks that keep it true | `src/app/credits.ts`: `CREDITS`, `CREDIT_GROUPS`, `NEWTON_QUOTE`, `WHY_WE_CREDIT`, type `Credit`; `src/app/creditsCheck.ts`: `staleCredits`, `uncreditedAssets`, `isShippedAsset`; `src/app/AboutScreen.tsx`: `AboutScreen` | `src/app/ui.tsx`, `src/app/credits.ts` |
| Settings | The one screen of options: snapshot sync, photo sweep model and effort, About link | `src/app/SettingsScreen.tsx`: `SettingsScreen` | `src/app/ui.tsx`, `src/bridge/file.ts`, `src/bridge/sweepGrind.ts`, `src/shared/data/snapshot.ts` |
| Bridge | Move JSON between the app and the outside: strip fences, validate hard, download and read files, hold the wire schemas, hold the device-only photo-sweep setting | `src/bridge/validate.ts`: `parseBridgeResponse`, `BridgeError`; `src/bridge/fences.ts`: `stripFences`; `src/bridge/file.ts`: `downloadJson`, `readFileText`, `toJsonText`; `src/bridge/schemas.ts`: the six Zod wire schemas and their inferred types; `src/bridge/provider.ts`: `registerProvider`, `selectProvider`, `manualFileProvider`; `src/bridge/sweepGrind.ts`: `readSweepGrind`, `writeSweepGrind`, `SWEEP_MODELS`, `SWEEP_EFFORTS`, `DEFAULT_SWEEP_GRIND` | zod, the DOM; nothing from the contexts |
| Grind examples support | Test-side checker for `grinds/examples/<kind>/<name>.json`: schema subset check and expect-block check | `src/bridge/grindExamples.ts`: `schemaProblems`, `expectProblems`, types `GrindExample`, `FieldCheck`, `JsonSchema`; the app never imports it | nothing |
| Shared kernel: data | One Dexie database, the base repository, the Person repository, whole-store snapshot export and import | `src/shared/data/db.ts`: `db`, `CairnDb`, `TABLE_NAMES`; `src/shared/data/repository.ts`: `Repository<T>`; `src/shared/data/personRepository.ts`: `personRepository`; `src/shared/data/snapshot.ts`: `exportSnapshot`, `exportSnapshotJson`, `importSnapshot`, `importSnapshotJson`, `parseSnapshot`, `SnapshotError` | dexie; the type files of both contexts |
| Shared kernel: core | A typed publish/subscribe bus and an id generator | `src/shared/core/eventBus.ts`: `EventBus<Events>`; `src/shared/core/ids.ts`: `newId` | nothing |
| Shared kernel: contracts | The one shared concept | `src/shared/contracts/person.ts`: `Person` | nothing |
| HomeInventory: contracts | Types and events of the Home Tree | `src/contexts/inventory/contracts/types.ts`: `Place`, `Item`, `Placement`, `PlaceType`, `VerificationOutcome`; `src/contexts/inventory/contracts/events.ts`: `inventoryBus`, `InventoryEvents` | `src/shared/core/eventBus.ts` |
| HomeInventory: data | Persist Places, Items and Placements | `src/contexts/inventory/data/placeRepository.ts`: `placeRepository`; `src/contexts/inventory/data/itemRepository.ts`: `itemRepository`, `dedupeAliases`; `src/contexts/inventory/data/placementRepository.ts`: `placementRepository` | `src/shared/data/` |
| HomeInventory: core | Home Tree paths, search by name or alias, add swept items, verification (confirm, refute, redirect), build and parse the manual Sweep file | `src/contexts/inventory/core/tree.ts`: `pathOf`, `ancestry`, `indexById`; `src/contexts/inventory/core/search.ts`: `searchItems`, `itemMatches`, `pathForPlaces`; `src/contexts/inventory/core/sweep.ts`: `addSweptItems`; `src/contexts/inventory/core/verification.ts`: `confirmPlacement`, `refutePlacement`, `redirectPlacement`; `src/contexts/inventory/core/sweepBridge.ts`: `buildSweepRequest`, `parseSweepResult` | its own data and contracts, `src/bridge/` (schemas, validate), `src/shared/data/db.ts` (verification only) |
| HomeInventory: screens | Browse the tree, search, sweep, verify | `src/contexts/inventory/features/InventoryHome.tsx`, `src/contexts/inventory/features/PlaceScreen.tsx`, `src/contexts/inventory/features/SearchScreen.tsx`, `src/contexts/inventory/features/PlacementActions.tsx`, `src/contexts/inventory/features/SweepPanel.tsx` | `src/app/ui.tsx`, `src/app/useAsync.ts`, `src/bridge/file.ts`, `src/bridge/validate.ts`, its own data and core, `src/shared/data/personRepository.ts` |
| TripPlanning: contracts | Types and events of trips | `src/contexts/trips/contracts/types.ts`: `Trip`, `Destination`, `TripKind`, `TravelNote`, `TravellerProfile`, `TripPlan`, `Debrief`, `NoteScopeType`; `src/contexts/trips/contracts/events.ts`: `tripsBus`, `TripEvents` | `src/shared/core/eventBus.ts` |
| TripPlanning: data | Persist the seven trip tables | `src/contexts/trips/data/` (seven repositories, one per table: trip, trip plan, destination, trip kind, travel note, traveller profile, debrief) | `src/shared/data/` |
| TripPlanning: core | Build the Plan Request from a Trip and its scoped Travel Notes, parse and store a Trip Plan, complete a Debrief | `src/contexts/trips/core/planBridge.ts`: `buildPlanRequest`, `buildPlanRequestForTrip`, `parseTripPlan`, `importTripPlan`, `ageYearsAt`; `src/contexts/trips/core/debrief.ts`: `completeDebrief` | its own data and contracts, `src/bridge/`, `src/shared/data/personRepository.ts` |
| TripPlanning: screens | List trips, plan one, run the AI Plan round trip, debrief, manage people and notes | `src/contexts/trips/features/TripsHome.tsx`, `src/contexts/trips/features/NewTripScreen.tsx`, `src/contexts/trips/features/TripScreen.tsx`, `src/contexts/trips/features/DebriefForm.tsx`, `src/contexts/trips/features/PeopleScreen.tsx` | `src/app/ui.tsx`, `src/app/useAsync.ts`, `src/bridge/`, its own data and core, `src/shared/data/personRepository.ts` |
| Test support | Reset the database between tests, jest-dom matchers | `src/test/reset.ts`: `resetDb`; `src/test/setup.ts` | `src/shared/data/db.ts` |
| Outside `src/` | Wire contracts, grind definitions and their scenarios, build config, icon script | `contexts/inventory/schemas/`, `contexts/trips/schemas/` (JSON Schemas, the source of truth), `grinds/sweep.json`, `grinds/sweep.md`, `grinds/examples/`, `vite.config.ts`, `scripts/gen-icons.mjs` | |

What crosses a context boundary today: nothing directly. Inventory never imports trips and trips never imports inventory. Both reach the kernel's Person repository, and `src/shared/data/db.ts` imports both contexts' type files (a break, see section 4).

## 2. Collisions

The files changed by the most commits in the last 30 days, from `git log --since=30.days --name-only --format= -- src | sort | uniq -c | sort -rn | head -15`, run at base commit 616f975. Line counts are `wc -l` at that commit. Test files are counted because the command counts them.

| Commits | File | Lines | What the commits were |
| --- | --- | --- | --- |
| 3 | `src/app/SettingsScreen.tsx` | 143 | Photo sweeps card, build stamp, credits link: each new option edits the one screen |
| 3 | `src/app/SettingsScreen.test.tsx` | 98 | the same three stories |
| 2 | `src/bridge/sweep11.test.ts` | 206 | Sweep 1.1 schema parity |
| 2 | `src/app/credits.ts` | 274 | credits list, then credits that follow removals |
| 2 | `src/app/credits.test.tsx` | 198 | the same two stories |
| 1 | `src/main.tsx` | 41 | update banner registration |
| 1 | `src/bridge/sweepGrind.ts` | 57 | photo sweep model and effort setting |
| 1 | `src/bridge/schemas.ts` | 159 | the 1.1 wire schemas |
| 1 | `src/bridge/grindExamples.ts` | 155 | grind scenario checker |
| 1 | `src/bridge/grindExamples.test.ts` | 161 | the same story |
| 1 | `src/app/creditsCheck.ts` | 67 | credits follow removals |
| 1 | `src/app/buildVersion.ts` | 8 | build stamp |
| 1 | `src/app/buildVersion.test.ts` | 27 | build stamp |
| 1 | `src/app/appUpdate.ts` | 151 | update banner |
| 1 | `src/app/appUpdate.test.ts` | 159 | update banner |

Reading it honestly:

- The history is short. Only 14 commits fall in the 30 days, touching 20 distinct files under `src/`; the 15 above are the top of that list, and the cut at 15 splits a tie (every file from the sixth row down has one commit, so which five of the ties are left out is the sort's accident).
- The only file edited by three stories is `src/app/SettingsScreen.tsx` (with its test). It is the live collision, and refactor 2 below removes it.
- Almost everything that collided is in `src/app/` and `src/bridge/`, the two modules every feature passes through. The contexts did not appear: they were last touched before this window, and their next change is the photo Sweep through the factory (ADR-0004), which will land in `src/contexts/inventory/features/SweepPanel.tsx` and `src/bridge/` at the same time as Settings changes. That is the collision the refactors below are ranked to prevent.
- Files that will collide next, by structure rather than by history, because every new screen or table must edit them: `src/app/App.tsx` (43 lines, one route per screen), `src/app/Layout.tsx` (55 lines, the tab list), `src/shared/data/db.ts` (80 lines, every table of both contexts), `src/bridge/schemas.ts` (159 lines, every wire schema of both contexts).
- No file is near the ~500-line split threshold. The largest is `src/contexts/trips/features/TripScreen.tsx` at 282 lines.

## 3. Proposed refactors

Ranked by how much parallel work each frees. Each is a refactor story with no behaviour change: the existing tests are the proof and must pass unchanged, except for imports. New files and modules are named without backticks because they do not exist yet.

### 1. A Sweep source seam: manual file and factory behind one interface

- Responsibility to carve out: how a Sweep gets from a Place to a Sweep Result. Today `src/contexts/inventory/features/SweepPanel.tsx` holds the whole manual round trip (export button, import button, paste box, confirm list) and calls `buildSweepRequest` and `parseSweepResult` directly. `src/bridge/provider.ts` is a provider registry typed to a request union that nothing calls, and the 1.1 schemas (`sweepRequest11Schema`, `sweepResult11Schema`) have no caller outside tests. The factory Sweep (ADR-0004) has nowhere to plug in except by editing SweepPanel.
- New module: src/contexts/inventory/sweep/ with its entry file index.ts. The manual file path moves into it as the first source; the factory source is a later story that adds one file there and uses bsv-kit's grist and bsv packages, never a local client.
- API:

```ts
export interface SweepInput {
  place: { id: string; name: string; path: string };
  hint?: string;
  knownItems?: string[];       // 1.1, at most 300
  knownContainers?: string[];  // 1.1, at most 100
  photos: Blob[];              // never stored; dropped once the result is confirmed or discarded (ADR-0004)
}

export type SweepOutcome =
  | { state: "waiting" }
  | { state: "done"; result: SweepResult11 }
  | { state: "failed"; reason: string };

export type SweepHandle =
  | { kind: "file"; request: SweepRequest; accept(text: string): SweepResult }  // manual: the person carries the file
  | { kind: "job"; jobId: string; poll(): Promise<SweepOutcome>; discard(): Promise<void> };

export interface SweepSource {
  readonly id: "manual-file" | "factory";
  available(): boolean | Promise<boolean>;
  start(input: SweepInput): Promise<SweepHandle>;
}

export function selectSweepSource(sources: SweepSource[], preferred?: SweepSource["id"]): Promise<SweepSource>;
```

- Files it touches: `src/contexts/inventory/features/SweepPanel.tsx` (becomes presentational), `src/contexts/inventory/core/sweepBridge.ts` (moves into the module), `src/bridge/provider.ts` (retired: nothing calls its registry), `src/contexts/inventory/features/PlaceScreen.tsx` (one import line).
- Risk: medium. SweepPanel has no unit test of its own today, so the first step of the story is a test that pins the manual round trip (export file shape, paste, confirm list, nothing written before confirm). ADR-0004's rule that a photo leaves the phone only for the factory and only until confirmed must be a property of the factory source, not of the screen.
- Size: two stories. Story A is the seam with the manual source (the refactor). Story B is the factory source (the feature ADR-0004 already approved), which then needs no edit to SweepPanel.
- Frees: the factory Sweep feature and every manual-Sweep fix can run at once.

### 2. Settings as registered sections

- Responsibility to carve out: each group of options owns its own card. `src/app/SettingsScreen.tsx` holds three unrelated cards (snapshot sync, photo sweeps, About) and was edited by three of the last 14 commits.
- New module: src/app/settings/ with sections.ts and one file per card: SnapshotSection.tsx, PhotoSweepSection.tsx, AboutSection.tsx.
- API:

```ts
export interface SettingsSection {
  id: string;
  order: number;          // lower first
  Component: () => JSX.Element;
}

export function settingsSections(extra?: SettingsSection[]): SettingsSection[];  // built-in sections plus a context's, sorted by order
```

  `SettingsScreen` renders `settingsSections()` inside `Screen`. A context contributes a section by exporting it from its entry file (refactor 3), never by editing the screen. The sections are listed explicitly, not registered by importing a file for its side effect.
- Files it touches: `src/app/SettingsScreen.tsx` (shrinks to the loop), `src/app/SettingsScreen.test.tsx` (imports only; tests stay), three new section files.
- Risk: low. `src/app/SettingsScreen.test.tsx` renders the whole screen by its labels, so it proves nothing moved.
- Size: fits one story.
- Frees: every future setting (a speech voice, a household name, a sync option) becomes a new file instead of an edit to one screen.

### 3. A context manifest: routes and tabs

- Responsibility to carve out: what a context offers the shell. `src/app/App.tsx` lists every route and imports seven screens by deep path; `src/app/Layout.tsx` holds the tab list. A new screen or a new context edits both.
- New module: an entry file per context, src/contexts/inventory/index.ts and src/contexts/trips/index.ts, each exporting one manifest, and a manifest type in src/app/contextModule.ts.
- API:

```ts
import type { RouteObject } from "react-router-dom";

export interface NavTab { to: string; label: string; end?: boolean; order: number }

export interface ContextModule {
  id: string;                             // "inventory", "trips"
  routes: RouteObject[];
  tabs: NavTab[];
  settingsSections?: SettingsSection[];   // added by refactor 2
  schema?: ContextSchema;                 // added by refactor 4
}

export const inventoryModule: ContextModule;
export const tripsModule: ContextModule;
```

  `App` builds its router from `[inventoryModule, tripsModule]`; `Layout` draws `tabs` sorted by `order`. The People and Settings tabs stay in the shell's own list.
- Files it touches: `src/app/App.tsx`, `src/app/Layout.tsx`, two new entry files, one new type file. The screens do not move.
- Risk: low. The route table is small and the redirect for unknown paths stays in the shell. Keep `routerBasename()` exactly as it is.
- Size: fits one story. Refactors 2 and 4 each add one optional field to the manifest type, which is a one-line conflict at most.
- Frees: a new context or screen becomes its own folder plus one line in the shell.

### 4. Each context declares its own tables

- Responsibility to carve out: the database layout of a context. `src/shared/data/db.ts` imports both contexts' types, lists every table, and holds the single `version(1).stores()` map; `TABLE_NAMES` in the same file drives `src/shared/data/snapshot.ts`. Adding a table for any context edits the kernel, and the kernel is meant to hold only Person.
- New module: src/contexts/inventory/data/schema.ts and src/contexts/trips/data/schema.ts, plus src/shared/data/schema.ts for the shape and the composer.
- API:

```ts
export interface ContextSchema {
  context: string;
  tables: Record<string, string>;  // Dexie index spec per table, e.g. { places: "id, parentId, type, name, *aliases" }
}

export function composeSchemas(schemas: ContextSchema[]): {
  stores: Record<string, string>;
  tableNames: readonly string[];   // feeds the snapshot, in a stable order
};
```

  `CairnDb` still declares the typed table properties, but its `stores()` and `TABLE_NAMES` come from `composeSchemas([kernelSchema, inventorySchema, tripsSchema])`. A migration for one context is `version(n)` added beside that context's schema.
- Files it touches: `src/shared/data/db.ts`, `src/shared/data/snapshot.ts` (reads `tableNames`), `src/shared/db.test.ts` and `src/shared/snapshot.test.ts` (must pass unchanged).
- Risk: medium. A mistake silently changes an index or the snapshot order. Keep a test that the composed `stores` equals today's `version(1)` map literally, and that a snapshot exported before the change imports after it.
- Size: fits one story if Dexie's typed table properties stay in `src/shared/data/db.ts`; moving them too is a second story.
- Frees: the next context (or a table in an existing one) no longer edits the kernel or the snapshot file.

### 5. Wire schemas live with their context

- Responsibility to carve out: the Zod mirror of each context's JSON Schemas. `src/bridge/schemas.ts` holds trips and inventory schemas together (six schemas, 159 lines); a trips schema change and an inventory schema change edit the same file. `src/bridge/` then keeps only what is genuinely shared (fences, validate, file).
- New module: src/contexts/trips/contracts/wire.ts and src/contexts/inventory/contracts/wire.ts, each next to the JSON Schemas it mirrors in `contexts/trips/schemas/` and `contexts/inventory/schemas/`.
- API: the same exports as today, moved, with `src/bridge/schemas.ts` deleted:

```ts
// trips: contexts/trips/contracts/wire.ts
export const planRequestSchema: z.ZodType<PlanRequest>;
export const tripPlanSchema: z.ZodType<TripPlanResponse>;
// inventory: contexts/inventory/contracts/wire.ts
export const sweepRequestSchema: z.ZodType<SweepRequest>;
export const sweepResultSchema: z.ZodType<SweepResult>;
export const sweepRequest11Schema: z.ZodType<SweepRequest11>;
export const sweepResult11Schema: z.ZodType<SweepResult11>;
```

- Files it touches: `src/bridge/schemas.ts` (deleted), `src/bridge/provider.ts` (type import, or gone after refactor 1), `src/bridge/sweep11.test.ts`, `src/bridge/validate.test.ts`, `src/contexts/inventory/core/sweepBridge.ts`, `src/contexts/trips/core/planBridge.ts`, `src/contexts/trips/features/TripScreen.tsx` (a type import).
- Risk: low. Imports change, no logic does. Do it after refactor 1 so SweepPanel's story does not rebase over it.
- Size: fits one story.
- Frees: trips wire changes and inventory wire changes (the Sweep 1.2 that will follow 1.1) stop sharing a file.

### 6. One device-settings store

- Responsibility to carve out: reading and writing a setting that lives only on this device. `src/bridge/sweepGrind.ts` hand-rolls a localStorage read with validation and a fallback, and sits in the bridge folder though it is a setting. The next device setting would copy it.
- New module: src/app/settings/deviceSetting.ts; sweepGrind becomes a user of it and moves to src/contexts/inventory/sweep/.
- API:

```ts
export interface DeviceSetting<T> {
  read(): T;                 // stored value if valid, else the default; never throws
  write(value: T): void;
}

export function defineDeviceSetting<T>(
  key: string,                       // e.g. "cairn.sweep.grind"
  defaultValue: T,
  parse: (stored: unknown) => T,     // coerce each field, fall back to the default per field
): DeviceSetting<T>;
```

- Files it touches: `src/bridge/sweepGrind.ts`, `src/app/SettingsScreen.tsx` (or its section, after refactor 2), `src/app/SettingsScreen.test.tsx` (the storage key `cairn.sweep.grind` and its contents must not change).
- Risk: low. The stored format is already on the Governor's phone, so the key and shape must stay byte-for-byte. Never moves into Dexie or a snapshot (mw-r5s2i.6).
- Size: fits one story; do it after refactor 2.
- Frees: new device-only options (a language, a voice, a default floor) are one `defineDeviceSetting` call each.

### 7. One component for the file round trip

- Responsibility to carve out: the "export a request file, import or paste a response file, show an error, confirm" interaction. `src/contexts/inventory/features/SweepPanel.tsx` and the AI Plan card in `src/contexts/trips/features/TripScreen.tsx` each hand-write the hidden file input, the paste `details` box, the `ingest` function and the `BridgeError` message handling.
- New module: src/app/BridgeRoundTrip.tsx.
- API:

```ts
export interface BridgeRoundTripProps<T> {
  title: string;
  exportLabel: string;
  importLabel: string;
  pastePlaceholder: string;
  onExport(): void | Promise<void>;
  parse(text: string): T;                 // throws BridgeError on a bad file
  onParsed(value: T): void;               // the caller shows its own confirm list
}

export function BridgeRoundTrip<T>(props: BridgeRoundTripProps<T>): JSX.Element;
```

- Files it touches: `src/contexts/inventory/features/SweepPanel.tsx`, `src/contexts/trips/features/TripScreen.tsx`, `src/bridge/validate.ts` (read-only: the component catches `BridgeError`).
- Risk: low, but do it after refactor 1, which removes the manual path from SweepPanel's body. If the factory replaces the manual Sweep, only TripScreen keeps the round trip and this refactor shrinks to a TripScreen split.
- Size: fits one story.
- Frees: a third AI round trip (a new request kind) costs a parser and a confirm list, not another 60 lines of file handling.

### 8. Screens that only draw: move the view loaders out

- Responsibility to carve out: assembling what a screen shows. `loadPlace` in `src/contexts/inventory/features/PlaceScreen.tsx` and `loadTrip` in `src/contexts/trips/features/TripScreen.tsx` join four to five repositories and compute labels inside the screen file; `src/contexts/trips/features/PeopleScreen.tsx` does the same with its own loader.
- New modules: src/contexts/inventory/core/placeView.ts, src/contexts/trips/core/tripView.ts, src/contexts/trips/core/peopleView.ts.
- API:

```ts
export interface PlaceView { place: Place; path: string; children: Place[]; items: { placementId: string; itemId: string; name: string }[] }
export function loadPlaceView(placeId: string): Promise<PlaceView | null>;

export interface ScopeOption { label: string; scopeType: NoteScopeType; scopeId: string | null; key: string }
export interface TripView { trip: Trip; destinationName: string; kindName: string; travellerNames: string[]; plan: TripPlan | undefined; debriefed: boolean; scopeOptions: ScopeOption[]; defaultScopeKey: string }
export function loadTripView(tripId: string): Promise<TripView | null>;
```

  `ScopeOption.key` and `defaultScopeKey` replace the `destScopeIndex = 2` magic number in `src/contexts/trips/features/TripScreen.tsx`, which silently depends on the order of an array built 60 lines above it.
- Files it touches: the three screens above and three new core files. `src/contexts/inventory/inventory.test.ts` and `src/contexts/trips/trips.test.ts` gain tests of the loaders (they have none today).
- Risk: low to medium: the loaders are untested today, so the story writes the test first.
- Size: three small stories, one per screen; they do not conflict with one another.
- Frees: a screen restyle and a data-shape change stop sharing a file, and the loaders become testable without rendering.

Not proposed: splitting `src/app/ui.tsx` (123 lines, no commits in 30 days), `src/app/credits.ts` (274 lines, it is data), or `src/contexts/trips/features/TripScreen.tsx` by size alone (282 lines, under the ~500 threshold; refactors 7 and 8 shrink it anyway).

## 4. Rule breaks

Where the code breaks a rule of seats/builder/pwa-best-practices/27-modular-boundaries.md. Facts, not blame; each names the refactor that fixes it.

1. A screen reaches past an interface. `src/contexts/inventory/features/SweepPanel.tsx` and `src/contexts/trips/features/TripScreen.tsx` import `src/bridge/file.ts` (DOM downloads), `src/bridge/validate.ts` (`BridgeError`) and, for TripScreen, `src/bridge/schemas.ts` types. `src/app/SettingsScreen.tsx` calls `src/shared/data/snapshot.ts` and `src/bridge/sweepGrind.ts` (localStorage) directly. No module has an entry file, so there is no interface to import instead. Fixed by refactors 1, 2, 3, 7.
2. Persistence bypasses the repository. `src/contexts/inventory/core/verification.ts` imports `db` and calls `db.transaction` and `db.placements.update` itself, although the repository pattern is the rule ("UI never touches Dexie directly", `CONTEXT-MAP.md`) and `src/contexts/inventory/data/placementRepository.ts` exists for exactly this. Fix inside refactor 8's story or alone: a `move(placementId, newPlaceId, by, when)` method on `PlacementRepository`.
3. The shared kernel depends on its users. `src/shared/data/db.ts` imports type files from both contexts and names every context's tables, though `shared/CONTEXT.md` says a concept enters the kernel only when a second context needs it. Fixed by refactor 4.
4. A screen does the assembling. `loadPlace`, `loadTrip` and the loader in `src/contexts/trips/features/PeopleScreen.tsx` live in the screen files, and `src/contexts/trips/features/TripScreen.tsx` carries `const destScopeIndex = 2; // destination option (see loadTrip)`, a position in an array built elsewhere. Fixed by refactor 8.
5. Seams that exist but connect to nothing. `inventoryBus` and `tripsBus` are emitted from the contexts' core folders (`swept`, `verified`, `planImported`, `debriefed`) but nothing under `src/` subscribes to them, tests included. `src/bridge/provider.ts` has `registerProvider` and `selectProvider`, and nothing calls either. `sweepRequest11Schema` and `sweepResult11Schema` are exercised only by `src/bridge/sweep11.test.ts`. They are the right seams unused, so the next feature will not know to use them, or will add a second. Refactor 1 uses the provider idea and retires the dead registry; the buses stay, and the first subscriber should be named in the story that adds it.
6. A constant that should be data. `src/bridge/sweepGrind.ts` lists `SWEEP_MODELS`, `SWEEP_EFFORTS` and `DEFAULT_SWEEP_GRIND` in code with a comment that they are "grinds/sweep.json's values"; the grind file is the source and the app holds a copy that can drift (no test compares them). Also: every on-screen string is an English literal and names are sorted with `localeCompare` and no locale. Cairn is one household's English app today, so this is a note, not a defect; the day a second language is wanted, it is an edit to every screen (rule: language is data or a setting). Refactor 6 gives the model and effort a settings home; a test that `src/bridge/sweepGrind.ts` matches `grinds/sweep.json` is a small separate story.
7. A shared screen filed under one context. `src/contexts/trips/features/PeopleScreen.tsx` edits Persons, which are the kernel's concept and which inventory also uses (`src/contexts/inventory/features/PlacementActions.tsx` lists them). It sits in trips, so an inventory story that wants to change who is listed edits a trips file. Fixed by moving the screen to the kernel in refactor 3's story (its manifest entry), or leaving it with a note.
8. A duplicate of bsv-kit code: none today, and that is checked, not assumed. `package.json` has no bsv-kit dependency and nothing under `src/` signs a request or holds a key. The warning is forward: the factory Sweep must come from bsv-kit's grist and bsv packages (rule: common functionality lives once). The duplicates that do exist are between Cairn and the other apps, in section 5.
9. Not found: no text rendered twice by two components; no owner data (keys, names, hosts) in the code.

## 5. Library candidates

Rule: the second copy is the signal, and a plainly shareable piece is lifted now into a public library built for strangers to trust (seats/builder/library-best-practices/01-when-code-becomes-a-library.md). Every library below would be a public repo with nothing of the Governor's in it, ESM with an exports map, a README that opens with a ten-line example, semver from 0.1.0, a CHANGELOG with "breaking" first and a migration for each breaking change, a LICENSE file, and an install line pinned to a tag once one exists (04-versioning-and-pinning.md, 07-docs.md, 09-licence-and-attribution.md). A breaking change is a removed or changed export, option or format (0.x: a minor bump); anything else is a patch.

Copies were compared on 2026-10-10 against the working copies in ~/trade-tracker, ~/lampas, ~/postern and ~/spell-forge.

Where it would live: bsv-kit is for the BSV key, the door, grist and their companions (its README says so). Update handling, build stamps and credits are not BSV, so they go in a NEW public library, here called pwa-kit (repo Jonathan-A-White/pwa-kit, the name is the Mayor's to confirm), as separate packages like bsv-kit's, each importing no other. The grind scenario checker belongs to the factory's grist contract, so it goes in bsv-kit.

| Candidate | In Cairn | Other copies found | Belongs in | Proposed public API | Versioning needs |
| --- | --- | --- | --- | --- | --- |
| App update: a new build waits for a tap | `src/app/appUpdate.ts` (151 lines), `src/app/UpdateBanner.tsx` | trade-tracker src/services/app-update.ts (145 lines, same exports; differs mainly in `TAKE_OVER_PATIENCE_MS`, 3 s there, 10 s here, and quote style); Lampas src/sw.ts and `src/main.tsx` hold the same flow | new library pwa-kit, package @pwa-kit/update | `startAppUpdates({ container, registration, reload, checkEveryMs?, patienceMs? }): AppUpdates`; `useUpdateState(): UpdateState`; `applyUpdate(): void`; type `UpdateState = "none" \| "ready" \| "updating"` (React is an optional peer dependency; the banner stays in the app so it matches the app's look) | 0.1.0 then 1.0.0 once two apps run it. The two intervals become options, so the apps' differing values are not a breaking change. The message `{ type: "SKIP_WAITING" }` is a wire format with the generated worker: changing it is breaking and needs a CHANGELOG migration |
| Build stamp | `build-version.ts` (repo root), `src/app/buildVersion.ts` | Lampas, Postern and trade-tracker each have a root `build-version.ts` with `shortCommit` and `buildVersion` (20 to 23 lines each); SpellForge has src/version.ts (not compared) | new library pwa-kit, package @pwa-kit/build-version | `shortCommit(cwd?: string, git?: string): string` (returns "dev" outside git, never throws); `buildVersion(version: string, when: Date, commit: string): string` | The output format `<version> · YYYY-MM-DD HH:MMZ · <commit>` is what the Governor reads and what apps' tests match: a change to it is breaking. The copies already differ: trade-tracker's `buildVersion` adds a leading `v` and Cairn's, Lampas's and Postern's do not (Cairn's Settings screen adds the `v` itself), so the first release must pick one and say so in the CHANGELOG |
| Grind scenario checker | `src/bridge/grindExamples.ts` (155 lines), `src/bridge/grindExamples.test.ts` | trade-tracker src/grinds/examples.ts (184 lines); Lampas tests/support/grind-examples.ts (156 lines); the same `FieldCheck`, `ExpectBlock`, `GrindExample` types and `expectProblems` in all three | bsv-kit, a new package @bsv-kit/grinds (test-only, no DOM, imports nothing from bsv or grist) | `schemaProblems(doc, schema): string[]`; `expectProblems(expect, answerSchema): string[]`; `checkExpect(expect, answer): string[]`; `loadExamples(dir): GrindExample[]`; types `GrindExample`, `FieldCheck`, `ExpectBlock`, `JsonSchema`; constant `EXAMPLE_PHOTO_MAX_BYTES` | The check names (`equals`, `is_null`, `one_of`, `contains`, `matches`, `present`) are the contract with `mw grist smoke`, so adding a check is a minor change and removing or renaming one is breaking. Per 06-testing.md, ship a fixture of valid and invalid examples made by the factory's own reader. Three apps must move onto it, one story per app (08-moving-an-app-onto-the-library.md) |
| Credits list and its checks | `src/app/credits.ts` (the `Credit` type), `src/app/creditsCheck.ts` (67 lines) | trade-tracker src/content/credits-check.ts (same purpose, four functions under other names: `stalePackages`, `uncreditedPackages`, `uncreditedFiles`, `staleFiles`); a credits list but no checks found in Postern src/credits.ts, SpellForge src/features/about/credits.ts and Lampas src/attribution.ts | new library pwa-kit, package @pwa-kit/credits | type `Credit`; `staleCredits(credits, dependencyNames): string[]`; `uncreditedAssets(files, credits): string[]`; `isShippedAsset(path): boolean`; a `readmeCredits(credits): string` renderer so the README and About cannot drift | The `Credit` shape is read by every app's About screen, so a new required field is breaking and a new optional one is not. The credit texts stay in each app: only the type and the checks are shared. Only trade-tracker has the checks (under other names, so the first release must pick the names and trade-tracker's move is a rename); the other three apps hold only a list, so what they gain is the type and the checks they do not have yet |
| Reply validation | `src/bridge/fences.ts` (19 lines), `src/bridge/validate.ts` (39 lines) | none found: SpellForge src/features/tutor/session-json.ts writes a fenced block but does not strip one | bsv-kit, as a helper beside @bsv-kit/grist if a second app reads a fenced JSON reply; otherwise stays | `stripFences(text): string`; `parseJsonReply(text, schema: { safeParse }): T` throwing a typed `ReplyError` | Do not lift until a second app needs it (no second copy found). When it moves, the error message wording is user-visible, so changing it is a minor change |
| Typed event bus and base repository | `src/shared/core/eventBus.ts` (22 lines), `src/shared/data/repository.ts` (34 lines) | none found (SpellForge has its own browser-events.ts for BSV events, not the same thing); Lampas has src/events/bus.ts, a different shape: a typed `publish` and `subscribeAll` over one app event union (compared by export names only) | stays in Cairn for now | `EventBus<Events>` with `on` and `emit`; `Repository<T>` over a Dexie table | Small and generic, but a library of 22 lines no one else uses is a cost to maintain. Revisit when a second app wants the same shape |
| Whole-store snapshot (ADR-0002) | `src/shared/data/snapshot.ts` (96 lines) | none found | stays in Cairn | `createSnapshotter(db, { kind, formatVersion })` returning `export`, `parse`, `import` | Not yet: the table list is Cairn's. After refactor 4 the code takes its table list as an argument and could be lifted, with the snapshot file format (`kind`, `formatVersion`, `tables`) as the wire contract that makes a format change breaking |

Not candidates: `src/app/ui.tsx` (the look is Cairn's own neon theme; another app wants its own), `src/app/useAsync.ts` (48 lines, too small to maintain as a package), the Zod schemas and contexts (Cairn's wire contracts with its own grind).

Order of lifting, by how many apps it saves: grind scenario checker (3 copies), app update (3), build stamp (4), credits checks (2 close, 3 partial). Each is a story the Mayor files with the first step "copy, then add a test whose fixture the original code made", per the library rules.
