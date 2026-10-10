import { readdirSync, readFileSync, statSync } from "node:fs";
import { extname, resolve } from "node:path";
import {
  EXAMPLE_PHOTO_MAX_BYTES,
  expectProblems,
  schemaProblems,
  type GrindExample,
  type JsonSchema,
} from "./grindExamples";
import { sweepRequest11Schema } from "./schemas";

const repo = resolve(__dirname, "../..");
const readJson = (path: string) => JSON.parse(readFileSync(resolve(repo, path), "utf-8"));

const MIME_BY_EXT: Record<string, string> = {
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".png": "image/png",
  ".webp": "image/webp",
};

// A grind's input schema: contexts/inventory/schemas/<kind>-request-<version>.schema.json
// (the sweep's request is a "sweep-request"; the name is the kind plus "-request").
const inputSchemaPath = (kind: string, version: string) =>
  `contexts/inventory/schemas/${kind}-request-${version}.schema.json`;

const grindFiles = readdirSync(resolve(repo, "grinds")).filter((f) => f.endsWith(".json"));

describe("grind examples (grinds/examples/<kind>/<name>.json, format in grinds/examples/README.md)", () => {
  it("finds the rig's grinds", () => {
    expect(grindFiles.length).toBeGreaterThan(0);
  });

  describe.each(grindFiles)("grinds/%s", (grindFile) => {
    const grind = readJson(`grinds/${grindFile}`);
    const kind: string = grind.kind;
    const dir = `grinds/examples/${kind}`;
    const exampleFiles = (() => {
      try {
        return readdirSync(resolve(repo, dir)).filter((f) => f.endsWith(".json"));
      } catch {
        return [];
      }
    })();
    const answerSchema: JsonSchema = readJson(grind.answerSchema);

    it("has at least one example", () => {
      expect(
        exampleFiles,
        `grinds/${grindFile} has no example: add ${dir}/<name>.json (see grinds/examples/README.md)`,
      ).not.toHaveLength(0);
    });

    it.each(exampleFiles)("%s is a valid scenario", (file) => {
      const example: GrindExample = readJson(`${dir}/${file}`);

      expect(Object.keys(example).sort()).toEqual(
        ["description", "expect", "photos", "request"].filter((k) => k !== "photos" || "photos" in example),
      );
      expect(typeof example.description).toBe("string");

      const version = (example.request as { schemaVersion?: unknown }).schemaVersion;
      expect(grind.versions).toContain(version);
      const input: JsonSchema = readJson(inputSchemaPath(kind, version as string));
      expect(schemaProblems(example.request, input)).toEqual([]);

      const photos = example.photos ?? [];
      expect(photos.length).toBeGreaterThanOrEqual(grind.attachments.min);
      expect(photos.length).toBeLessThanOrEqual(grind.attachments.max);
      for (const photo of photos) {
        expect(grind.attachments.mime).toContain(MIME_BY_EXT[extname(photo)]);
        const size = statSync(resolve(repo, dir, photo)).size;
        expect(size).toBeLessThan(EXAMPLE_PHOTO_MAX_BYTES);
        expect(size).toBeLessThanOrEqual(grind.attachments.maxBytes);
      }

      expect(expectProblems(example.expect, answerSchema)).toEqual([]);
    });
  });

  it("the sweep's example requests also satisfy the app's own Zod mirror", () => {
    const files = readdirSync(resolve(repo, "grinds/examples/sweep")).filter((f) => f.endsWith(".json"));
    for (const file of files) {
      const example: GrindExample = readJson(`grinds/examples/sweep/${file}`);
      expect(sweepRequest11Schema.safeParse(example.request).success, file).toBe(true);
    }
  });
});

describe("schemaProblems", () => {
  const schema: JsonSchema = {
    type: "object",
    additionalProperties: false,
    required: ["a"],
    properties: {
      a: { const: "1.1" },
      b: { type: "string", minLength: 1 },
      c: { type: "array", maxItems: 1, items: { $ref: "#/$defs/n" } },
    },
    $defs: { n: { type: "object", required: ["x"], properties: { x: { type: "boolean" } } } },
  };

  it("accepts a document that fits, reading $ref and arrays", () => {
    expect(schemaProblems({ a: "1.1", b: "z", c: [{ x: true }] }, schema)).toEqual([]);
  });

  it("names a missing required field, an unknown key, a wrong const, type, length and count", () => {
    expect(schemaProblems({ b: "z" }, schema)).toHaveLength(1);
    expect(schemaProblems({ a: "1.1", extra: 1 }, schema)).toHaveLength(1);
    expect(schemaProblems({ a: "1.0" }, schema)).toHaveLength(1);
    expect(schemaProblems({ a: "1.1", b: 4 }, schema)).toHaveLength(1);
    expect(schemaProblems({ a: "1.1", b: "" }, schema)).toHaveLength(1);
    expect(schemaProblems({ a: "1.1", c: [{ x: true }, { x: true }] }, schema)).toHaveLength(1);
    expect(schemaProblems({ a: "1.1", c: [{}] }, schema)).toHaveLength(1);
  });
});

describe("expectProblems", () => {
  const answerSchema: JsonSchema = readJson("contexts/inventory/schemas/sweep-result-1.1.schema.json");

  it("accepts checks on real answer fields, bare values and array positions", () => {
    expect(
      expectProblems(
        {
          placeName: "Top drawer",
          schemaVersion: "1.1",
          items: { equals: [] },
          "items.0.name": { present: true, matches: "^[a-z]" },
          "containers.0.name": { one_of: ["Cables", "Cords"] },
          "containers.0.unsure": { is_null: false },
          note: { contains: "dark" },
        },
        answerSchema,
      ),
    ).toEqual([]);
  });

  it("names a path that is not in the answer schema", () => {
    expect(expectProblems({ price: { equals: 1 } }, answerSchema)).toEqual(["price: not a field of the answer schema"]);
    expect(expectProblems({ "items.0.count": { present: false } }, answerSchema)).toHaveLength(1);
  });

  it("names a value the answer schema would never allow", () => {
    expect(expectProblems({ schemaVersion: "1.0" }, answerSchema)).toHaveLength(1);
    expect(expectProblems({ responseType: { one_of: ["sweep-result", "other"] } }, answerSchema)).toHaveLength(1);
    expect(expectProblems({ placeName: { equals: 4 } }, answerSchema)).toHaveLength(1);
  });

  it("names an unknown check, a bad pattern and a contains on a non-string", () => {
    expect(expectProblems({ note: { around: 4 } }, answerSchema)).toHaveLength(1);
    expect(expectProblems({ note: { isNull: true } }, answerSchema)).toHaveLength(1);
    expect(expectProblems({ note: { matches: "(" } }, answerSchema)).toHaveLength(1);
    expect(expectProblems({ note: { matches: "(?i)dark" } }, answerSchema)).toHaveLength(1);
    expect(expectProblems({ "containers.0.unsure": { contains: "x" } }, answerSchema)).toHaveLength(1);
  });

  it("names an empty expect block and an empty check", () => {
    expect(expectProblems({}, answerSchema)).toHaveLength(1);
    expect(expectProblems({ note: {} }, answerSchema)).toHaveLength(1);
  });
});
