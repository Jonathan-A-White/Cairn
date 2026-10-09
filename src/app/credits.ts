/**
 * Everything Cairn is built on, credited by name, with what it is used for, its
 * licence and any changes we made. The About screen renders this list, the README
 * Credits section repeats it, and credits.test.tsx fails if a runtime dependency
 * in package.json is missing here or a credit is missing from the README. Add a
 * library, and credit it in the same commit.
 */

export interface Credit {
  /** Stable key for tests and React. */
  id: string;
  /** Shown as the link text. Never a raw URL. */
  name: string;
  url: string;
  group: CreditGroup;
  /** What Cairn uses it for. */
  use: string;
  licence: { name: string; url: string };
  /** What we changed, or that we changed nothing. */
  changes: string;
  /** The package.json dependency names this credit covers. */
  packages?: string[];
}

export type CreditGroup = "runtime" | "build" | "ideas";

export const CREDIT_GROUPS: { id: CreditGroup; title: string }[] = [
  { id: "runtime", title: "Libraries inside the app" },
  { id: "build", title: "Tools that build and test it" },
  { id: "ideas", title: "Ideas, services and the people behind them" },
];

export const NEWTON_QUOTE = {
  text: "If I have seen further it is by standing on the shoulders of Giants.",
  author: "Isaac Newton",
  source: "letter to Robert Hooke, 1675",
  url: "https://en.wikipedia.org/wiki/Standing_on_the_shoulders_of_giants",
};

export const WHY_WE_CREDIT =
  "Cairn stands on other people's work, so we name every source we build on, with a link and its licence, because credit is owed whether or not a licence asks for it.";

const none = "None; used as published.";

export const CREDITS: Credit[] = [
  {
    id: "dexie",
    name: "Dexie.js",
    url: "https://dexie.org",
    group: "runtime",
    use: "The on-device database that holds your places, containers and items.",
    licence: {
      name: "Apache-2.0",
      url: "https://github.com/dexie/Dexie.js/blob/master/LICENSE",
    },
    changes: none,
    packages: ["dexie"],
  },
  {
    id: "react",
    name: "React",
    url: "https://react.dev",
    group: "runtime",
    use: "Draws every screen. React DOM puts it on the page.",
    licence: {
      name: "MIT",
      url: "https://github.com/facebook/react/blob/main/LICENSE",
    },
    changes: none,
    packages: ["react", "react-dom"],
  },
  {
    id: "react-router",
    name: "React Router",
    url: "https://reactrouter.com",
    group: "runtime",
    use: "Moves between screens and gives each one an address.",
    licence: {
      name: "MIT",
      url: "https://github.com/remix-run/react-router/blob/main/LICENSE.md",
    },
    changes: none,
    packages: ["react-router-dom"],
  },
  {
    id: "zod",
    name: "Zod",
    url: "https://zod.dev",
    group: "runtime",
    use: "Checks every snapshot and every file that crosses the AI bridge before it is trusted.",
    licence: {
      name: "MIT",
      url: "https://github.com/colinhacks/zod/blob/main/LICENSE",
    },
    changes: none,
    packages: ["zod"],
  },
  {
    id: "workbox",
    name: "Workbox",
    url: "https://developer.chrome.com/docs/workbox",
    group: "runtime",
    use: "Generates the service worker that makes Cairn work offline and notices a new version.",
    licence: {
      name: "MIT",
      url: "https://github.com/GoogleChrome/workbox/blob/v7/LICENSE",
    },
    changes: none,
  },
  {
    id: "vite",
    name: "Vite",
    url: "https://vite.dev",
    group: "build",
    use: "Builds and serves the app.",
    licence: {
      name: "MIT",
      url: "https://github.com/vitejs/vite/blob/main/LICENSE",
    },
    changes: none,
  },
  {
    id: "vite-plugin-pwa",
    name: "vite-plugin-pwa",
    url: "https://vite-pwa-org.netlify.app",
    group: "build",
    use: "Turns the build into an installable, offline app with a manifest.",
    licence: {
      name: "MIT",
      url: "https://github.com/vite-pwa/vite-plugin-pwa/blob/main/LICENSE",
    },
    changes: none,
  },
  {
    id: "tailwindcss",
    name: "Tailwind CSS",
    url: "https://tailwindcss.com",
    group: "build",
    use: "Styles every screen.",
    licence: {
      name: "MIT",
      url: "https://github.com/tailwindlabs/tailwindcss/blob/main/LICENSE",
    },
    changes: "None; the Cairn colours and glow are our own theme on top of it.",
  },
  {
    id: "typescript",
    name: "TypeScript",
    url: "https://www.typescriptlang.org",
    group: "build",
    use: "The language Cairn is written in.",
    licence: {
      name: "Apache-2.0",
      url: "https://github.com/microsoft/TypeScript/blob/main/LICENSE.txt",
    },
    changes: none,
  },
  {
    id: "vitest",
    name: "Vitest",
    url: "https://vitest.dev",
    group: "build",
    use: "Runs the tests.",
    licence: {
      name: "MIT",
      url: "https://github.com/vitest-dev/vitest/blob/main/LICENSE",
    },
    changes: none,
  },
  {
    id: "testing-library",
    name: "React Testing Library",
    url: "https://testing-library.com/docs/react-testing-library/intro",
    group: "build",
    use: "Tests the screens the way a person uses them.",
    licence: {
      name: "MIT",
      url: "https://github.com/testing-library/react-testing-library/blob/main/LICENSE",
    },
    changes: none,
  },
  {
    id: "fake-indexeddb",
    name: "fake-indexeddb",
    url: "https://github.com/dumbmatter/fakeIndexedDB",
    group: "build",
    use: "Stands in for the phone's database so tests never touch a device.",
    licence: {
      name: "Apache-2.0",
      url: "https://github.com/dumbmatter/fakeIndexedDB/blob/master/LICENSE",
    },
    changes: none,
  },
  {
    id: "claude",
    name: "Claude",
    url: "https://www.anthropic.com/claude",
    group: "ideas",
    use: "The AI behind trip plans and photo sweeps, reached through the household's Claude Project and the household's software factory.",
    licence: {
      name: "Anthropic Commercial Terms",
      url: "https://www.anthropic.com/legal/commercial-terms",
    },
    changes: "None; it is a service we use, not code we ship.",
  },
  {
    id: "claude-code",
    name: "Claude Code",
    url: "https://www.anthropic.com/claude-code",
    group: "ideas",
    use: "The coding assistant that helps write and test Cairn.",
    licence: {
      name: "Anthropic Commercial Terms",
      url: "https://www.anthropic.com/legal/commercial-terms",
    },
    changes: "None; it is a tool we use, not code we ship.",
  },
  {
    id: "beads",
    name: "Beads, by Steve Yegge",
    url: "https://github.com/gastownhall/beads",
    group: "ideas",
    use: "The memory-for-coding-agents idea behind the factory's work tracking.",
    licence: {
      name: "MIT",
      url: "https://github.com/gastownhall/beads/blob/main/LICENSE",
    },
    changes: "We borrow the idea; none of its code ships in Cairn.",
  },
  {
    id: "gas-town",
    name: "Gas Town, by Steve Yegge",
    url: "https://github.com/gastownhall/gastown",
    group: "ideas",
    use: "The idea of a workshop of coding agents, which shaped the household's software factory.",
    licence: {
      name: "MIT",
      url: "https://github.com/gastownhall/gastown/blob/main/LICENSE",
    },
    changes: "We borrow the idea; none of its code ships in Cairn.",
  },
];
