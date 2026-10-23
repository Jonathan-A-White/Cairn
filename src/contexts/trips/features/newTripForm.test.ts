import { describe, it, expect, beforeEach, afterEach, vi } from "vitest";
import { defineRegistry } from "voice-kit/talks";
import { argsOf, requiredFilled } from "voice-kit/forms";
import { resetDb } from "../../../test/reset";
import { personRepository } from "../../../shared/data/personRepository";
import { destinationRepository } from "../data/destinationRepository";
import { tripKindRepository } from "../data/tripKindRepository";
import { tripRepository } from "../data/tripRepository";
import {
  CREATE_TRIP,
  NEW_TRIP_COMMAND_FORM,
  createTripCommand,
  isIsoDate,
  newTripForm,
} from "./newTripForm";

beforeEach(resetDb);
afterEach(() => vi.restoreAllMocks());

const VALUES = {
  destination: "Norman's house",
  kind: "family visit",
  startDate: "2026-11-02",
  endDate: "2026-11-05",
};

const without = (key: keyof typeof VALUES) =>
  Object.fromEntries(Object.entries(VALUES).filter(([k]) => k !== key));

describe("newTripForm: New trip as the tutor sees it", () => {
  it("has the four fields of the screen, in screen order, all required", () => {
    const form = newTripForm(["camping", "family visit"]);
    expect(form.name).toBe("New trip");
    expect(form.fields.map((f) => [f.name, f.label, f.required])).toEqual([
      ["destination", "Destination", true],
      ["kind", "Trip kind", true],
      ["startDate", "Start", true],
      ["endDate", "End", true],
    ]);
  });

  it("makes Trip kind a choice of the kinds the screen offers", () => {
    const kind = newTripForm(["camping", "family visit"]).fields[1];
    expect(kind.kind).toBe("choice");
    expect(kind.options).toEqual(["camping", "family visit"]);
  });

  it("leaves Trip kind a text field while the household has no kinds yet", () => {
    const kind = newTripForm([]).fields[1];
    expect(kind.kind).toBe("text");
    expect(kind.options).toBeUndefined();
  });

  it("does not ask the tutor for Travellers: they stay his by hand", () => {
    expect(newTripForm(["camping"]).fields.map((f) => f.name)).not.toContain("travellers");
  });
});

describe("create-trip: the command the button and the door share", () => {
  const command = () => createTripCommand({ travellerIds: () => ["p1"] });

  it("is a confirm command named create-trip", () => {
    expect(command().name).toBe(CREATE_TRIP);
    expect(CREATE_TRIP).toBe("create-trip");
    expect(command().kind).toBe("confirm");
  });

  it("requires Destination and Start (and the screen's other two, End and Trip kind)", () => {
    const required = command().args?.required ?? [];
    expect(required).toEqual(expect.arrayContaining(["destination", "startDate"]));
    expect([...required].sort()).toEqual(["destination", "endDate", "kind", "startDate"]);
  });

  it("refuses a call that leaves out Destination or Start, or names an arg it does not take", () => {
    const registry = defineRegistry({ commands: [command()] });
    expect(registry.refuses(CREATE_TRIP, without("destination"))).toMatch(/destination is required/);
    expect(registry.refuses(CREATE_TRIP, without("startDate"))).toMatch(/startDate is required/);
    expect(registry.refuses(CREATE_TRIP, { ...VALUES, travellers: "Grace" })).toMatch(/not an arg/);
    expect(registry.refuses(CREATE_TRIP, VALUES)).toBeUndefined();
  });

  it("takes a Trip kind the household has not used yet, as typing it by hand always did", () => {
    const registry = defineRegistry({ commands: [command()] });
    expect(registry.refuses(CREATE_TRIP, { ...VALUES, kind: "a brand new kind" })).toBeUndefined();
  });

  it("offers one line naming the form and what is filled in", () => {
    expect(command().offer?.(VALUES)).toBe("Send New trip: Norman's house, family visit, 2026-11-02, 2026-11-05?");
  });

  it("run saves the trip once, through the trip repository, with the travellers the screen holds", async () => {
    const grace = await personRepository.create("Grace");
    const create = vi.spyOn(tripRepository, "create");
    const created = vi.fn();
    const registry = defineRegistry({
      commands: [createTripCommand({ travellerIds: () => [grace.id], onCreated: created })],
    });

    const ran = await registry.run(CREATE_TRIP, argsOf(NEW_TRIP_COMMAND_FORM, VALUES));

    expect(ran.ok).toBe(true);
    const destination = (await destinationRepository.all())[0];
    const kind = (await tripKindRepository.all())[0];
    expect(destination.name).toBe("Norman's house");
    expect(kind.name).toBe("family visit");
    expect(create).toHaveBeenCalledTimes(1);
    expect(create).toHaveBeenCalledWith({
      destinationId: destination.id,
      kind: kind.id,
      startDate: "2026-11-02",
      endDate: "2026-11-05",
      travellerIds: [grace.id],
    });
    expect(await tripRepository.count()).toBe(1);
    expect(created).toHaveBeenCalledTimes(1);
    expect(created.mock.calls[0][0]).toMatchObject({ startDate: "2026-11-02" });
  });

  it("saves nothing, and says why, when no traveller is ticked or a date is not a date", async () => {
    const create = vi.spyOn(tripRepository, "create");
    const none = defineRegistry({ commands: [createTripCommand({ travellerIds: () => [] })] });
    const noTraveller = await none.run(CREATE_TRIP, VALUES);
    expect(noTraveller).toEqual({ ok: false, why: expect.stringContaining("Pick at least one traveller") });

    const some = defineRegistry({ commands: [createTripCommand({ travellerIds: () => ["p1"] })] });
    const badDate = await some.run(CREATE_TRIP, { ...VALUES, startDate: "2026-02-30" });
    expect(badDate).toEqual({ ok: false, why: expect.stringContaining("Start") });
    expect(create).not.toHaveBeenCalled();
  });
});

describe("requiredFilled for the New trip form", () => {
  it("is true once the four fields hold something", () => {
    const form = newTripForm(["family visit"]);
    expect(requiredFilled(form, VALUES)).toBe(true);
    expect(requiredFilled(form, { ...VALUES, endDate: "" })).toBe(false);
  });
});

describe("isIsoDate", () => {
  it("accepts a real YYYY-MM-DD date and nothing else", () => {
    expect(isIsoDate("2026-11-02")).toBe(true);
    expect(isIsoDate("2026-02-30")).toBe(false);
    expect(isIsoDate("11/02/2026")).toBe(false);
    expect(isIsoDate("")).toBe(false);
  });
});
