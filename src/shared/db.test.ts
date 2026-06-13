import { describe, it, expect, beforeEach } from "vitest";
import { resetDb } from "../test/reset";
import { CairnDb, db, TABLE_NAMES } from "./data/db";

beforeEach(resetDb);

describe("CairnDb schema", () => {
  it("opens at the current version with every declared table", async () => {
    await db.open();
    const names = db.tables.map((t) => t.name).sort();
    expect(names).toEqual([...TABLE_NAMES].sort());
  });

  it("a fresh database instance migrates cleanly", async () => {
    const fresh = new CairnDb("CairnDB-migration-test");
    await fresh.open();
    expect(fresh.verno).toBe(1);
    await fresh.persons.put({ id: "p1", name: "Grace" });
    expect(await fresh.persons.get("p1")).toMatchObject({ name: "Grace" });
    await fresh.delete();
  });
});
