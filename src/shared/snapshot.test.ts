import { describe, it, expect, beforeEach } from "vitest";
import { resetDb } from "../test/reset";
import { db } from "./data/db";
import { personRepository } from "./data/personRepository";
import {
  exportSnapshot,
  exportSnapshotJson,
  importSnapshot,
  importSnapshotJson,
  parseSnapshot,
  SnapshotError,
} from "./data/snapshot";
import { itemRepository } from "../contexts/inventory/data/itemRepository";

beforeEach(resetDb);

describe("snapshot sync (ADR-0002)", () => {
  it("round-trips the whole store from device A to device B", async () => {
    // device A populates several tables
    await personRepository.create("Grace");
    await itemRepository.create("stapler", ["the clicker"]);
    const json = await exportSnapshotJson();

    // device B starts with different data, then imports A's snapshot
    await resetDb();
    await personRepository.create("Someone else");
    await importSnapshotJson(json);

    const persons = await personRepository.all();
    expect(persons.map((p) => p.name)).toEqual(["Grace"]); // last import wins
    const items = await itemRepository.all();
    expect(items[0].aliases).toContain("the clicker");
  });

  it("is whole-DB and schema-versioned", async () => {
    await personRepository.create("Grace");
    const snap = await exportSnapshot();
    expect(snap.kind).toBe("cairn-snapshot");
    expect(snap.schemaVersion).toBe(db.verno);
    expect(Object.keys(snap.tables)).toContain("persons");
    expect(Object.keys(snap.tables)).toContain("trips");
  });

  it("clears tables absent from the snapshot (last import wins)", async () => {
    await personRepository.create("Grace");
    const emptySnap = await exportSnapshot();
    emptySnap.tables.persons = [];
    await importSnapshot(emptySnap);
    expect(await personRepository.count()).toBe(0);
  });

  it("rejects a non-snapshot file", () => {
    expect(() => parseSnapshot('{"hello":"world"}')).toThrow(SnapshotError);
    expect(() => parseSnapshot("not json")).toThrow(SnapshotError);
  });

  it("rejects a snapshot from a newer format version", () => {
    const future = JSON.stringify({
      kind: "cairn-snapshot",
      formatVersion: 999,
      schemaVersion: 1,
      exportedAt: new Date().toISOString(),
      tables: {},
    });
    expect(() => parseSnapshot(future)).toThrow(SnapshotError);
  });
});
