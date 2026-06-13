import { describe, it, expect, beforeEach } from "vitest";
import { resetDb } from "../../test/reset";
import { personRepository } from "../../shared/data/personRepository";
import { destinationRepository } from "./data/destinationRepository";
import { tripKindRepository } from "./data/tripKindRepository";
import { travelNoteRepository } from "./data/travelNoteRepository";
import { travellerProfileRepository } from "./data/travellerProfileRepository";
import { tripRepository } from "./data/tripRepository";
import { tripPlanRepository } from "./data/tripPlanRepository";
import { debriefRepository } from "./data/debriefRepository";
import {
  buildPlanRequest,
  importTripPlan,
  parseTripPlan,
  ageYearsAt,
} from "./core/planBridge";
import { completeDebrief } from "./core/debrief";
import { planRequestSchema } from "../../bridge/schemas";

beforeEach(resetDb);

async function seedTrip() {
  const destination = await destinationRepository.findOrCreate("Norman's house");
  const kind = await tripKindRepository.findOrCreate("family visit");
  const grace = await personRepository.create("Grace", "1985-03-02");
  const sam = await personRepository.create("Sam", "1987-07-19");
  const kid = await personRepository.create("Robin", "2018-01-10");
  await travellerProfileRepository.upsert({
    personId: grace.id,
    dietary: "low-FODMAP",
    packingQuirks: ["packs a spare charger"],
  });
  const trip = await tripRepository.create({
    destinationId: destination.id,
    kind: kind.id,
    startDate: "2026-07-01",
    endDate: "2026-07-04",
    travellerIds: [grace.id, sam.id, kid.id],
  });
  return { destination, kind, grace, sam, kid, trip };
}

describe("plan an already-decided trip", () => {
  it("matches plan-request.schema.json and bundles every applicable Travel Note", async () => {
    const { destination, kind, grace, trip } = await seedTrip();
    await travelNoteRepository.create("household", null, "leave a key with neighbour");
    await travelNoteRepository.create("kind", kind.id, "bring board games");
    await travelNoteRepository.create("destination", destination.id, "park out back");
    await travelNoteRepository.create("person", grace.id, "carsick on long drives");
    // a note that must NOT be bundled (different destination)
    const other = await destinationRepository.findOrCreate("Lake George");
    await travelNoteRepository.create("destination", other.id, "irrelevant");

    const request = await buildPlanRequest(trip);

    // schema-valid
    expect(planRequestSchema.safeParse(request).success).toBe(true);
    expect(request.trip.destination.name).toBe("Norman's house");
    expect(request.trip.kind).toBe("family visit");
    expect(request.trip.travellers).toHaveLength(3);

    // every applicable scope bundled
    expect(request.householdNotes).toContain("leave a key with neighbour");
    expect(request.trip.kindNotes).toContain("bring board games");
    expect(request.trip.destination.notes).toContain("park out back");
    const graceTraveller = request.trip.travellers.find((t) => t.name === "Grace");
    expect(graceTraveller?.notes).toContain("carsick on long drives");
    expect(graceTraveller?.dietary).toBe("low-FODMAP");
    expect(graceTraveller?.packingQuirks).toContain("packs a spare charger");

    // the irrelevant destination note is not present anywhere
    expect(JSON.stringify(request)).not.toContain("irrelevant");
  });

  it("computes traveller age at the trip start date", () => {
    expect(ageYearsAt("2018-01-10", "2026-07-01")).toBe(8);
    expect(ageYearsAt(undefined, "2026-07-01")).toBeUndefined();
  });
});

describe("import a plan and pack from it", () => {
  it("stores an interactive Packing List and read-only Sections", async () => {
    const { trip } = await seedTrip();
    const raw = [
      "```json",
      JSON.stringify({
        schemaVersion: "1.0",
        responseType: "trip-plan",
        packingList: [
          { item: "passports", assignedTo: null },
          { item: "Robin's blanket", assignedTo: "Robin" },
        ],
        sections: [{ title: "Itinerary", body: "Day 1: drive up." }],
      }),
      "```",
    ].join("\n");

    const plan = parseTripPlan(raw);
    const stored = await importTripPlan(trip.id, plan);

    expect(stored.packingList).toHaveLength(2);
    expect(stored.packingList.every((e) => e.checked === false)).toBe(true);
    expect(stored.packingList[1].assignedTo).toBe("Robin");
    expect(stored.sections[0].title).toBe("Itinerary");

    // checking an item off persists
    await tripPlanRepository.setChecked(stored.id, 0, true);
    const reloaded = await tripPlanRepository.forTrip(trip.id);
    expect(reloaded?.packingList[0].checked).toBe(true);
  });

  it("replaces a prior plan when a new one is imported (latest wins)", async () => {
    const { trip } = await seedTrip();
    const make = (item: string) => ({
      schemaVersion: "1.0" as const,
      responseType: "trip-plan" as const,
      packingList: [{ item, assignedTo: null }],
      sections: [],
    });
    await importTripPlan(trip.id, make("first"));
    await importTripPlan(trip.id, make("second"));
    const current = await tripPlanRepository.forTrip(trip.id);
    expect(current?.packingList[0].item).toBe("second");
    expect(await tripPlanRepository.count()).toBe(1);
  });
});

describe("debrief captures knowledge", () => {
  it("saves each answer as a Travel Note with its confirmed scope", async () => {
    const { destination, kind, trip } = await seedTrip();
    const noteIds = await completeDebrief(trip.id, [
      { text: "the back room was quiet", scopeType: "destination", scopeId: destination.id },
      { text: "pack rain gear", scopeType: "kind", scopeId: kind.id },
      { text: "", scopeType: "household", scopeId: null }, // blank dropped
    ]);

    expect(noteIds).toHaveLength(2);
    expect(await travelNoteRepository.byScope("destination", destination.id)).toHaveLength(1);
    expect(await travelNoteRepository.byScope("kind", kind.id)).toHaveLength(1);
    // trip marked debriefed
    expect(await debriefRepository.forTrip(trip.id)).toBeDefined();
  });
});
