import { describe, it, expect } from "vitest";
import { parseBridgeResponse, BridgeError } from "./validate";
import { sweepResultSchema, tripPlanSchema } from "./schemas";

describe("parseBridgeResponse", () => {
  it("accepts a valid fenced Sweep Result", () => {
    const raw = [
      "```json",
      JSON.stringify({
        schemaVersion: "1.0",
        responseType: "sweep-result",
        placeName: "blue bin",
        items: [{ name: "tent stakes" }, { name: "mallet", aliases: ["hammer"] }],
      }),
      "```",
    ].join("\n");
    const result = parseBridgeResponse(raw, sweepResultSchema);
    expect(result.items).toHaveLength(2);
    expect(result.placeName).toBe("blue bin");
  });

  it("rejects malformed JSON with a clear error", () => {
    expect(() => parseBridgeResponse("not json", sweepResultSchema)).toThrow(
      BridgeError,
    );
  });

  it("rejects JSON that fails the schema", () => {
    const raw = JSON.stringify({
      schemaVersion: "1.0",
      responseType: "sweep-result",
      // missing placeName, items
    });
    expect(() => parseBridgeResponse(raw, sweepResultSchema)).toThrow(
      /did not match the expected format/,
    );
  });

  it("rejects unknown extra properties (strict schemas)", () => {
    const raw = JSON.stringify({
      schemaVersion: "1.0",
      responseType: "trip-plan",
      packingList: [],
      sections: [],
      surprise: true,
    });
    expect(() => parseBridgeResponse(raw, tripPlanSchema)).toThrow(BridgeError);
  });

  it("rejects the wrong responseType", () => {
    const raw = JSON.stringify({
      schemaVersion: "1.0",
      responseType: "sweep-result",
      placeName: "x",
      items: [],
    });
    expect(() => parseBridgeResponse(raw, tripPlanSchema)).toThrow(BridgeError);
  });
});
