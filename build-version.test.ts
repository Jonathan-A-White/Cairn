import { describe, it, expect, afterEach } from "vitest";
import { execFileSync } from "node:child_process";
import { mkdtempSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { stampedPackageVersion } from "./build-version";

const dirs: string[] = [];
afterEach(() => {
  while (dirs.length) rmSync(dirs.pop() as string, { recursive: true, force: true });
});

function git(cwd: string, ...args: string[]): void {
  execFileSync(
    "git",
    ["-c", "user.name=t", "-c", "user.email=t@example.com", ...args],
    { cwd, stdio: "ignore" },
  );
}

function checkout(version: string): string {
  const dir = mkdtempSync(join(tmpdir(), "cairn-ver-"));
  dirs.push(dir);
  git(dir, "init", "-q");
  writeFileSync(join(dir, "package.json"), JSON.stringify({ version }));
  git(dir, "add", "package.json");
  git(dir, "commit", "-q", "-m", "v");
  return dir;
}

describe("stampedPackageVersion", () => {
  it("is HEAD's package.json version when the working file is edited to an older one, uncommitted", () => {
    const dir = checkout("1.0.7");
    writeFileSync(join(dir, "package.json"), JSON.stringify({ version: "0.9.0" }));
    expect(stampedPackageVersion(dir)).toBe("1.0.7");
  });

  it("is the working file's version when there is no git checkout", () => {
    const dir = mkdtempSync(join(tmpdir(), "cairn-ver-"));
    dirs.push(dir);
    writeFileSync(join(dir, "package.json"), JSON.stringify({ version: "2.3.4" }));
    expect(stampedPackageVersion(dir)).toBe("2.3.4");
  });
});
