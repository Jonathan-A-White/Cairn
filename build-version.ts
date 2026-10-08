// The build stamp Cairn shows in Settings: the package version never changes, so the build
// adds its UTC time and the short git commit beside it and he can tell on his phone whether
// a new build has loaded. Used by vite.config.ts (which also serves vitest).
import { execFileSync } from "node:child_process";

export { buildVersion } from "./src/app/buildVersion";

/** The short HEAD commit of the checkout at `cwd`; 'dev' when there is no git or no checkout, never a throw. */
export function shortCommit(cwd: string = process.cwd(), git = "git"): string {
  try {
    const out = execFileSync(git, ["rev-parse", "--short", "HEAD"], {
      cwd,
      encoding: "utf-8",
      stdio: ["ignore", "pipe", "ignore"],
    }).trim();
    return out || "dev";
  } catch {
    return "dev";
  }
}
