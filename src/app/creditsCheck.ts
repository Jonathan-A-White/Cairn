import type { Credit } from "./credits";

/**
 * The checks behind credits.test.tsx, kept pure so the test can feed them a fake
 * list. A credit follows what Cairn ships: remove a package and its credit goes
 * in the same commit; add a font or data file and it is credited in the same one.
 */

const ASSET_EXTENSIONS = [
  "woff",
  "woff2",
  "ttf",
  "otf",
  "eot",
  "json",
  "csv",
  "tsv",
  "geojson",
  "xml",
  "txt",
  "sqlite",
  "db",
];

/** True for a font file or a data file, by extension. */
export function isShippedAsset(path: string): boolean {
  const ext = path.split(".").pop()?.toLowerCase() ?? "";
  return ASSET_EXTENSIONS.includes(ext);
}

/**
 * Credits that name a package no longer in package.json (dependencies or
 * devDependencies), or a package credit that names none. Credits of any other
 * kind (service, idea, font, data) are not packages and are left alone.
 */
export function staleCredits(credits: Credit[], dependencies: string[]): string[] {
  const known = new Set(dependencies);
  const problems: string[] = [];
  for (const c of credits) {
    if (c.kind !== "package") continue;
    const names = c.packages ?? [];
    if (names.length === 0) {
      problems.push(`${c.id}: kind is package but names no packages`);
      continue;
    }
    for (const name of names) {
      if (!known.has(name)) problems.push(`${c.id}: ${name}`);
    }
  }
  return problems;
}

/**
 * Shipped files (paths as /public/... or /src/...) that no font or data credit
 * covers. A credit's `files` entries are paths relative to the repo root: an
 * exact file, or a directory ending in "/".
 */
export function uncreditedAssets(files: string[], credits: Credit[]): string[] {
  const covers = credits
    .filter((c) => c.kind === "font" || c.kind === "data")
    .flatMap((c) => c.files ?? []);
  return files
    .map((f) => f.replace(/^\//, ""))
    .filter(
      (f) => !covers.some((p) => (p.endsWith("/") ? f.startsWith(p) : f === p)),
    );
}
