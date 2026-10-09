import { describe, it, expect } from "vitest";
import { render, screen, within } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import pkgText from "../../package.json?raw";
import readmeText from "../../README.md?raw";
import { CREDITS, NEWTON_QUOTE, type Credit } from "./credits";
import {
  isShippedAsset,
  staleCredits,
  uncreditedAssets,
} from "./creditsCheck";
import { AboutScreen } from "./AboutScreen";
import { SettingsScreen } from "./SettingsScreen";

const pkg = JSON.parse(pkgText) as {
  dependencies: Record<string, string>;
  devDependencies?: Record<string, string>;
};
const allDeps = [
  ...Object.keys(pkg.dependencies),
  ...Object.keys(pkg.devDependencies ?? {}),
];

// Every font and data file the app ships: public/ and src/ (Vite bundles both).
const everyFile = Object.keys(
  import.meta.glob("/{public,src}/**/*", { query: "?url", import: "default" }),
);
const shippedFiles = everyFile.filter(isShippedAsset);

const base: Credit = {
  id: "x",
  name: "X",
  url: "https://x.example",
  group: "runtime",
  kind: "package",
  use: "u",
  licence: { name: "MIT", url: "https://x.example/licence" },
  changes: "c",
};

describe("credits list", () => {
  it("credits every runtime dependency in package.json", () => {
    const credited = new Set(CREDITS.flatMap((c) => c.packages ?? []));
    const missing = Object.keys(pkg.dependencies).filter(
      (name) => !credited.has(name),
    );
    expect(
      missing,
      `Credit these runtime dependencies in src/app/credits.ts (and the README): ${missing.join(", ")}`,
    ).toEqual([]);
  });

  it("names no package that is not a dependency (credits follow removals)", () => {
    const stale = staleCredits(CREDITS, allDeps);
    expect(
      stale,
      `These credits name a package no longer in package.json; remove the credit (and its README line) or the package name: ${stale.join(", ")}`,
    ).toEqual([]);
  });

  it("fails a credit for a package removed from package.json", () => {
    const credits = [{ ...base, id: "gone", packages: ["gone-lib", "kept-lib"] }];
    expect(staleCredits(credits, ["kept-lib"])).toEqual(["gone: gone-lib"]);
    expect(staleCredits(credits, ["kept-lib", "gone-lib"])).toEqual([]);
  });

  it("requires a package credit to name at least one package", () => {
    expect(staleCredits([{ ...base, id: "bare" }], [])).toEqual([
      "bare: kind is package but names no packages",
    ]);
  });

  it("leaves credits that are not packages alone, by kind", () => {
    const credits: Credit[] = [
      { ...base, id: "svc", kind: "service", packages: undefined },
      { ...base, id: "idea", kind: "idea" },
      { ...base, id: "font", kind: "font", files: ["public/fonts/"] },
      { ...base, id: "data", kind: "data", files: ["public/data/"] },
    ];
    expect(staleCredits(credits, [])).toEqual([]);
    expect(CREDITS.some((c) => c.kind !== "package")).toBe(true);
  });

  it("credits every font and data file the app ships", () => {
    expect(everyFile, "the file scan found nothing").toContain("/public/favicon.svg");
    const missing = uncreditedAssets(shippedFiles, CREDITS);
    expect(
      missing,
      `Credit these files in src/app/credits.ts (kind font or data, with files) and the README: ${missing.join(", ")}`,
    ).toEqual([]);
  });

  it("fails a shipped font or data file that has no credit", () => {
    const files = [
      "/public/fonts/Lora.woff2",
      "/public/data/places.json",
      "/src/app/App.tsx",
      "/public/icon-192.png",
    ];
    expect(files.filter(isShippedAsset)).toEqual([
      "/public/fonts/Lora.woff2",
      "/public/data/places.json",
    ]);
    const font: Credit = { ...base, id: "lora", kind: "font", files: ["public/fonts/"] };
    expect(uncreditedAssets(files.filter(isShippedAsset), [font])).toEqual([
      "public/data/places.json",
    ]);
    expect(uncreditedAssets(files.filter(isShippedAsset), [])).toHaveLength(2);
  });

  it("gives every credit a name, a use, and https links for source and licence", () => {
    expect(CREDITS.length).toBeGreaterThan(0);
    for (const c of CREDITS) {
      expect(c.name, "name").not.toBe("");
      expect(c.use, `${c.name} use`).not.toBe("");
      expect(c.licence.name, `${c.name} licence`).not.toBe("");
      expect(c.changes, `${c.name} changes`).not.toBe("");
      for (const url of [c.url, c.licence.url]) {
        expect(url, `${c.name} link`).toMatch(/^https:\/\/\S+$/);
      }
    }
  });

  it("lists each credit in the README with the same name and links", () => {
    for (const c of CREDITS) {
      expect(readmeText, `${c.name} in README`).toContain(`[${c.name}](${c.url})`);
      expect(readmeText, `${c.name} licence in README`).toContain(
        `[${c.licence.name}](${c.licence.url})`,
      );
    }
    expect(readmeText).toMatch(/^## Credits$/m);
  });
});

describe("About screen", () => {
  function renderAbout() {
    return render(
      <MemoryRouter>
        <AboutScreen />
      </MemoryRouter>,
    );
  }

  it("opens with Newton's line, attributed, and a sentence on why we credit", () => {
    renderAbout();
    const quote = screen.getByTestId("about-quote");
    expect(quote).toHaveTextContent(
      "If I have seen further it is by standing on the shoulders of Giants.",
    );
    expect(NEWTON_QUOTE.text).toBe(
      "If I have seen further it is by standing on the shoulders of Giants.",
    );
    expect(quote).toHaveTextContent("Isaac Newton");
    expect(quote).toHaveTextContent("letter to Robert Hooke, 1675");
    expect(screen.getByTestId("about-why")).toBeInTheDocument();

    // the quote comes before the credits in document order
    const credits = screen.getByTestId("about-credits");
    expect(
      quote.compareDocumentPosition(credits) & Node.DOCUMENT_POSITION_FOLLOWING,
    ).toBeTruthy();
  });

  it("shows every credit with its name as link text, its licence link, use and changes", () => {
    renderAbout();
    for (const c of CREDITS) {
      const item = screen.getByTestId(`credit-${c.id}`);
      const name = within(item).getByRole("link", { name: c.name });
      expect(name).toHaveAttribute("href", c.url);
      const licence = within(item).getByRole("link", { name: c.licence.name });
      expect(licence).toHaveAttribute("href", c.licence.url);
      expect(item).toHaveTextContent(c.use);
      expect(item).toHaveTextContent(c.changes);
    }
  });

  it("never shows a raw URL as link text, and opens links safely", () => {
    renderAbout();
    for (const a of screen.getAllByRole("link")) {
      expect(a.textContent ?? "").not.toMatch(/https?:\/\//);
      expect(a).toHaveAttribute("target", "_blank");
      expect(a.getAttribute("rel") ?? "").toContain("noopener");
    }
  });
});

describe("Settings", () => {
  it("links to the About and credits screen", () => {
    render(
      <MemoryRouter>
        <SettingsScreen />
      </MemoryRouter>,
    );
    expect(
      screen.getByRole("link", { name: /about and credits/i }),
    ).toHaveAttribute("href", "/about");
  });
});
