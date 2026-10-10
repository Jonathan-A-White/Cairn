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
binding design. [`docs/module-map.md`](./docs/module-map.md) maps each module's
job and API, the files stories collide on, and the proposed splits.
[`docs/best-practices-audit.md`](./docs/best-practices-audit.md) reads the app against the Governor's PWA checklist, line by line, and ranks the fixes.

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

## Credits

> "If I have seen further it is by standing on the shoulders of Giants." — [Isaac Newton](https://en.wikipedia.org/wiki/Standing_on_the_shoulders_of_giants), letter to Robert Hooke, 1675

Cairn stands on other people's work, so we name every source we build on, with a link and its licence, because credit is owed whether or not a licence asks for it. The same list is on the app's About screen (Settings → About and credits), generated from `src/app/credits.ts`; a test fails if a runtime dependency or a credit is missing from either.

A source added or removed changes its credit in the same commit, and the test says so: it fails on a credit for a package no longer in `package.json`, and on a bundled font or data file with no credit (non-package credits, such as services and ideas, carry a `kind` and are left alone).

### Libraries inside the app

- [Dexie.js](https://dexie.org): The on-device database that holds your places, containers and items. Licence: [Apache-2.0](https://github.com/dexie/Dexie.js/blob/master/LICENSE). Changes: None; used as published.
- [React](https://react.dev): Draws every screen. React DOM puts it on the page. Licence: [MIT](https://github.com/facebook/react/blob/main/LICENSE). Changes: None; used as published.
- [React Router](https://reactrouter.com): Moves between screens and gives each one an address. Licence: [MIT](https://github.com/remix-run/react-router/blob/main/LICENSE.md). Changes: None; used as published.
- [Zod](https://zod.dev): Checks every snapshot and every file that crosses the AI bridge before it is trusted. Licence: [MIT](https://github.com/colinhacks/zod/blob/main/LICENSE). Changes: None; used as published.
- [Workbox](https://developer.chrome.com/docs/workbox): Generates the service worker that makes Cairn work offline and notices a new version. Licence: [MIT](https://github.com/GoogleChrome/workbox/blob/v7/LICENSE). Changes: None; used as published.

### Tools that build and test it

- [Vite](https://vite.dev): Builds and serves the app. Licence: [MIT](https://github.com/vitejs/vite/blob/main/LICENSE). Changes: None; used as published.
- [vite-plugin-pwa](https://vite-pwa-org.netlify.app): Turns the build into an installable, offline app with a manifest. Licence: [MIT](https://github.com/vite-pwa/vite-plugin-pwa/blob/main/LICENSE). Changes: None; used as published.
- [Tailwind CSS](https://tailwindcss.com): Styles every screen. Licence: [MIT](https://github.com/tailwindlabs/tailwindcss/blob/main/LICENSE). Changes: None; the Cairn colours and glow are our own theme on top of it.
- [TypeScript](https://www.typescriptlang.org): The language Cairn is written in. Licence: [Apache-2.0](https://github.com/microsoft/TypeScript/blob/main/LICENSE.txt). Changes: None; used as published.
- [Vitest](https://vitest.dev): Runs the tests. Licence: [MIT](https://github.com/vitest-dev/vitest/blob/main/LICENSE). Changes: None; used as published.
- [React Testing Library](https://testing-library.com/docs/react-testing-library/intro): Tests the screens the way a person uses them. Licence: [MIT](https://github.com/testing-library/react-testing-library/blob/main/LICENSE). Changes: None; used as published.
- [fake-indexeddb](https://github.com/dumbmatter/fakeIndexedDB): Stands in for the phone's database so tests never touch a device. Licence: [Apache-2.0](https://github.com/dumbmatter/fakeIndexedDB/blob/master/LICENSE). Changes: None; used as published.

### Ideas, services and the people behind them

- [Claude](https://www.anthropic.com/claude): The AI behind trip plans and photo sweeps, reached through the household's Claude Project and the household's software factory. Licence: [Anthropic Commercial Terms](https://www.anthropic.com/legal/commercial-terms). Changes: None; it is a service we use, not code we ship.
- [Claude Code](https://www.anthropic.com/claude-code): The coding assistant that helps write and test Cairn. Licence: [Anthropic Commercial Terms](https://www.anthropic.com/legal/commercial-terms). Changes: None; it is a tool we use, not code we ship.
- [Beads, by Steve Yegge](https://github.com/gastownhall/beads): The memory-for-coding-agents idea behind the factory's work tracking. Licence: [MIT](https://github.com/gastownhall/beads/blob/main/LICENSE). Changes: We borrow the idea; none of its code ships in Cairn.
- [Gas Town, by Steve Yegge](https://github.com/gastownhall/gastown): The idea of a workshop of coding agents, which shaped the household's software factory. Licence: [MIT](https://github.com/gastownhall/gastown/blob/main/LICENSE). Changes: We borrow the idea; none of its code ships in Cairn.

Cairn borrows no fonts or icons: the text uses the phone's own monospace font and the app icons are drawn by `scripts/gen-icons.mjs`.
