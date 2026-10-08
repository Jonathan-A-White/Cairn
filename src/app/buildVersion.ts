/** '<version> · YYYY-MM-DD HH:MMZ · <commit>', the time in UTC. Stamped at build time (vite.config.ts). */
export function buildVersion(
  version: string,
  when: Date,
  commit: string,
): string {
  return `${version} · ${when.toISOString().slice(0, 16).replace("T", " ")}Z · ${commit}`;
}
