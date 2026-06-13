import { describe, it, expect, beforeEach } from "vitest";
import { resetDb } from "../../test/reset";
import { personRepository } from "../../shared/data/personRepository";
import { itemRepository } from "./data/itemRepository";
import { placeRepository } from "./data/placeRepository";
import { placementRepository } from "./data/placementRepository";
import { searchItems } from "./core/search";
import {
  confirmPlacement,
  refutePlacement,
  redirectPlacement,
} from "./core/verification";
import { addSweptItems } from "./core/sweep";
import { buildSweepRequest, parseSweepResult } from "./core/sweepBridge";
import { BridgeError } from "../../bridge/validate";

beforeEach(resetDb);

describe("search by either family member's word", () => {
  it("finds an Item by its alias, with the full Place path", async () => {
    const attic = await placeRepository.createFloor("Attic");
    const dining = await placeRepository.createRoom("Dining room", attic.id);
    const item = await itemRepository.create("dining cabinet", ["the hutch"]);
    await placementRepository.place(item.id, dining.id);

    const results = await searchItems("hutch");
    expect(results).toHaveLength(1);
    expect(results[0].item.name).toBe("dining cabinet");
    expect(results[0].placements[0].path).toBe("Attic → Dining room");
  });

  it("finds by name too, case-insensitively", async () => {
    await itemRepository.create("Stapler");
    expect(await searchItems("stap")).toHaveLength(1);
    expect(await searchItems("STAPLER")).toHaveLength(1);
    expect(await searchItems("nope")).toHaveLength(0);
  });
});

describe("verification — the learning loop", () => {
  it("confirm refreshes the last-verified stamp and records who", async () => {
    const place = await placeRepository.createFloor("Office");
    const grace = await personRepository.create("Grace");
    const item = await itemRepository.create("stapler");
    const placement = await placementRepository.place(item.id, place.id);
    // last verified 30 days ago
    const thirtyDaysAgo = new Date(
      Date.now() - 30 * 24 * 60 * 60 * 1000,
    ).toISOString();
    await placementRepository.stampVerified(placement.id, null, thirtyDaysAgo);

    await confirmPlacement(placement.id, grace.id);

    const after = await placementRepository.get(placement.id);
    expect(after?.lastVerifiedBy).toBe(grace.id);
    expect(new Date(after!.lastVerifiedAt!).getTime()).toBeGreaterThan(
      new Date(thirtyDaysAgo).getTime(),
    );
  });

  it("refute removes the Placement (not here)", async () => {
    const place = await placeRepository.createFloor("Office");
    const item = await itemRepository.create("stapler");
    const placement = await placementRepository.place(item.id, place.id);

    await refutePlacement(placement.id);

    expect(await placementRepository.get(placement.id)).toBeUndefined();
  });

  it("redirect moves the Placement to the new Place and off the old one", async () => {
    const junk = await placeRepository.createFloor("Junk drawer");
    const desk = await placeRepository.createFloor("Office desk");
    const grace = await personRepository.create("Grace");
    const item = await itemRepository.create("stapler");
    const placement = await placementRepository.place(item.id, junk.id);

    await redirectPlacement(placement.id, desk.id, grace.id);

    const placements = await placementRepository.byItem(item.id);
    expect(placements).toHaveLength(1);
    expect(placements[0].placeId).toBe(desk.id);
    expect(placements[0].lastVerifiedBy).toBe(grace.id);
    // removed from junk drawer
    expect(await placementRepository.byPlace(junk.id)).toHaveLength(0);
  });
});

describe("sweep — rapid typed capture", () => {
  it("rapid-adds item after item into one Place", async () => {
    const place = await placeRepository.createFloor("Attic");
    const eaves = await placeRepository.createContainer("eaves closet", place.id);
    await addSweptItems(eaves.id, [
      { name: "wreath" },
      { name: "lights" },
      { name: "ornaments" },
    ]);
    expect(await placementRepository.byPlace(eaves.id)).toHaveLength(3);
  });

  it("dedupes the same Item swept twice (no duplicate placements)", async () => {
    const place = await placeRepository.createFloor("Garage");
    await addSweptItems(place.id, [{ name: "rope" }]);
    await addSweptItems(place.id, [{ name: "rope" }]);
    expect(await itemRepository.count()).toBe(1);
    expect(await placementRepository.byPlace(place.id)).toHaveLength(1);
  });
});

describe("photo-assisted sweep round-trip (ADR-0003)", () => {
  it("builds a valid Sweep Request carrying only data", async () => {
    const request = buildSweepRequest(
      "blue bin",
      "Attic → eaves closet → blue bin",
      "focus on the left side",
    );
    expect(request.requestType).toBe("sweep");
    expect(request.place.path).toContain("blue bin");
    expect(request.hint).toBe("focus on the left side");
  });

  it("imports a valid Sweep Result and adds its items after confirm", async () => {
    const bin = await placeRepository.createFloor("blue bin");
    const raw = [
      "```json",
      JSON.stringify({
        schemaVersion: "1.0",
        responseType: "sweep-result",
        placeName: "blue bin",
        items: [{ name: "tent" }, { name: "stakes", aliases: ["pegs"] }],
      }),
      "```",
    ].join("\n");

    const result = parseSweepResult(raw);
    // items shown for confirm/edit first; then added
    expect(result.items.map((i) => i.name)).toEqual(["tent", "stakes"]);
    await addSweptItems(
      bin.id,
      result.items.map((i) => ({ name: i.name, aliases: i.aliases })),
    );
    expect(await placementRepository.byPlace(bin.id)).toHaveLength(2);
    // alias survived for search
    expect(await searchItems("pegs")).toHaveLength(1);
  });

  it("rejects a malformed Sweep Result and writes nothing", async () => {
    const bin = await placeRepository.createFloor("blue bin");
    expect(() => parseSweepResult('{"responseType":"sweep-result"}')).toThrow(
      BridgeError,
    );
    expect(await placementRepository.byPlace(bin.id)).toHaveLength(0);
    expect(await itemRepository.count()).toBe(0);
  });
});
