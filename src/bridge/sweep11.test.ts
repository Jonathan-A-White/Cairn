import { readFileSync, existsSync } from "node:fs";
import { resolve } from "node:path";
import { sweepRequest11Schema, sweepResult11Schema } from "./schemas";

const repo = resolve(__dirname, "../..");
const readJson = (path: string) => JSON.parse(readFileSync(resolve(repo, path), "utf-8"));

// A real answer from the factory's sweep grind (Sonnet, low effort) to a photo
// of a drawer, 2026-09-29: the shape the confirm step will receive.
const factoryAnswer = {
  schemaVersion: "1.1",
  responseType: "sweep-result",
  placeName: "Top drawer",
  items: [
    { name: "scissors" },
    { name: "AA batteries", aliases: ["Duracell AA"] },
    { name: "tape measure" },
  ],
  containers: [
    {
      name: "Cables",
      aliases: ["CABLES"],
      items: [{ name: "USB-C cable" }, { name: "phone charger" }],
    },
  ],
};

describe("Sweep Request / Result 1.1 (ADR-0004)", () => {
  it("accepts a real answer from the factory's sweep grind", () => {
    expect(sweepResult11Schema.safeParse(factoryAnswer).success).toBe(true);
  });

  it("accepts unsure items and a note, and a result with no containers", () => {
    const result = {
      schemaVersion: "1.1",
      responseType: "sweep-result",
      placeName: "Top drawer",
      items: [{ name: "birthday candles", unsure: true }],
      note: "The back of the drawer is too dark to read.",
    };
    expect(sweepResult11Schema.safeParse(result).success).toBe(true);
  });

  it("rejects quantities, nested containers and a 1.0 result", () => {
    const withCount = { ...factoryAnswer, items: [{ name: "scissors", count: 2 }] };
    const nested = {
      ...factoryAnswer,
      containers: [{ name: "box", items: [], containers: [{ name: "tin", items: [] }] }],
    };
    const older = { ...factoryAnswer, schemaVersion: "1.0" };
    for (const bad of [withCount, nested, older]) {
      expect(sweepResult11Schema.safeParse(bad).success).toBe(false);
    }
  });

  it("builds a request that carries the Place's known names", () => {
    const request = {
      schemaVersion: "1.1",
      requestType: "sweep",
      place: { name: "Top drawer", path: "Kitchen -> Top drawer" },
      knownItems: ["tape measure"],
      knownContainers: ["Cables"],
    };
    expect(sweepRequest11Schema.safeParse(request).success).toBe(true);
    expect(sweepRequest11Schema.safeParse({ ...request, schemaVersion: "1.0" }).success).toBe(false);
  });

  it("keeps the JSON Schemas and the Zod mirrors on the same version and fields", () => {
    const result = readJson("contexts/inventory/schemas/sweep-result-1.1.schema.json");
    const request = readJson("contexts/inventory/schemas/sweep-request-1.1.schema.json");
    expect(result.properties.schemaVersion.const).toBe("1.1");
    expect(request.properties.schemaVersion.const).toBe("1.1");
    expect(Object.keys(result.properties).sort()).toEqual(Object.keys(sweepResult11Schema.shape).sort());
    expect(Object.keys(request.properties).sort()).toEqual(Object.keys(sweepRequest11Schema.shape).sort());
    expect(result.additionalProperties).toBe(false);
    expect(result.$defs.item.additionalProperties).toBe(false);
  });
});

describe("the sweep grind (grinds/sweep.json)", () => {
  const grind = readJson("grinds/sweep.json");

  it("names Cairn's sweep at 1.1 and files that exist", () => {
    expect(grind).toMatchObject({ grind: 1, app: "cairn", kind: "sweep", versions: ["1.1"] });
    expect(existsSync(resolve(repo, grind.instructions))).toBe(true);
    expect(readJson(grind.answerSchema).$id).toMatch(/sweep-result\/1\.1$/);
  });

  it("accepts only photos, at most four", () => {
    expect(grind.attachments.min).toBe(1);
    expect(grind.attachments.max).toBeLessThanOrEqual(4);
    expect(grind.attachments.mime.every((m: string) => m.startsWith("image/"))).toBe(true);
  });

  it("tells the model never to describe people and to give no quantities", () => {
    const instructions = readFileSync(resolve(repo, grind.instructions), "utf-8");
    expect(instructions).toMatch(/Never describe people/);
    expect(instructions).toMatch(/never give a quantity/i);
  });
});
