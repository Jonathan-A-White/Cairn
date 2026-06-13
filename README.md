# Cairn

A cairn for the home: an offline-first PWA that marks where things are kept and helps plan trips.

Two bounded contexts over a small shared kernel:

- **HomeInventory** — answers "where do we keep it?" via the Home Tree (Floors →
  Rooms → Containers), Items with Aliases, multi-place Placements, one-tap
  Verification, and typed or photo-assisted Sweeps.
- **TripPlanning** — turns an already-decided Trip into a structured Trip Plan
  through the household's Claude Project (a manual, file-based AI bridge), and
  accumulates scoped Travel Notes via the post-trip Debrief.

The app is fully static and offline-first; the only thing that ever leaves the
device is a manual JSON file (the AI bridge or a sync snapshot). See
[`docs/BUILD-SPEC.md`](./docs/BUILD-SPEC.md) and the context maps for the
binding design.

## Develop

```sh
npm install
npm run dev        # local dev server
npm run typecheck  # tsc --noEmit
npm test           # Vitest (data layer, fake-indexeddb)
npm run lint
npm run build      # tsc -b && vite build (emits PWA service worker + manifest)
```

Icons are generated from `scripts/gen-icons.mjs` (`node scripts/gen-icons.mjs`).

CI (`.github/workflows/ci.yml`) runs lint → typecheck → test → build on every
PR and deploys to GitHub Pages on push to `main`.
