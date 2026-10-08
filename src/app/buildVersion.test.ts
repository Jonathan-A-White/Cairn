import { describe, it, expect } from "vitest";
import { buildVersion } from "./buildVersion";

describe("buildVersion", () => {
  it("joins the package version, the UTC build time and the short commit", () => {
    const when = new Date(Date.UTC(2026, 9, 8, 16, 5, 59));
    expect(buildVersion("1.0.0", when, "abc1234")).toBe(
      "1.0.0 · 2026-10-08 16:05Z · abc1234",
    );
  });

  it("differs for two commits and for two build times", () => {
    const t = new Date(Date.UTC(2026, 9, 8, 16, 5));
    expect(buildVersion("1.0.0", t, "abc1234")).not.toBe(
      buildVersion("1.0.0", t, "def5678"),
    );
    expect(buildVersion("1.0.0", t, "abc1234")).not.toBe(
      buildVersion("1.0.0", new Date(t.getTime() + 60_000), "abc1234"),
    );
  });

  it("is what the build stamped into __APP_VERSION__", () => {
    expect(__APP_VERSION__).toMatch(
      /^\d+\.\d+\.\d+ · \d{4}-\d{2}-\d{2} \d{2}:\d{2}Z · ([0-9a-f]{7,}|dev)$/,
    );
  });
});
