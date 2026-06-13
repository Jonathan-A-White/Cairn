import {
  planRequestSchema,
  tripPlanSchema,
  type PlanRequest,
  type TripPlanResponse,
} from "../../../bridge/schemas";
import { parseBridgeResponse } from "../../../bridge/validate";
import { personRepository } from "../../../shared/data/personRepository";
import { destinationRepository } from "../data/destinationRepository";
import { tripKindRepository } from "../data/tripKindRepository";
import { travelNoteRepository } from "../data/travelNoteRepository";
import { travellerProfileRepository } from "../data/travellerProfileRepository";
import { tripRepository } from "../data/tripRepository";
import { tripPlanRepository } from "../data/tripPlanRepository";
import { tripsBus } from "../contracts/events";
import type { Trip, TripPlan } from "../contracts/types";

/** Whole years between a birthdate and a reference date, or undefined. */
export function ageYearsAt(
  birthdate: string | undefined,
  on: string,
): number | undefined {
  if (!birthdate) return undefined;
  const born = new Date(birthdate);
  const ref = new Date(on);
  if (Number.isNaN(born.getTime()) || Number.isNaN(ref.getTime())) return undefined;
  let age = ref.getFullYear() - born.getFullYear();
  const monthDiff = ref.getMonth() - born.getMonth();
  if (monthDiff < 0 || (monthDiff === 0 && ref.getDate() < born.getDate())) {
    age -= 1;
  }
  return age >= 0 ? age : undefined;
}

const noteTexts = (notes: { text: string }[]): string[] | undefined =>
  notes.length ? notes.map((n) => n.text) : undefined;

/**
 * Assemble the Plan Request for an already-decided Trip, bundling every Travel
 * Note whose scope applies — household, this Trip Kind, each Traveller, and the
 * Destination. The result is validated against plan-request.schema.json before
 * it leaves the device.
 */
export async function buildPlanRequest(trip: Trip): Promise<PlanRequest> {
  const [destination, kind, householdNotes, destinationNotes, kindNotes] =
    await Promise.all([
      destinationRepository.get(trip.destinationId),
      tripKindRepository.get(trip.kind),
      travelNoteRepository.byScope("household", null),
      travelNoteRepository.byScope("destination", trip.destinationId),
      travelNoteRepository.byScope("kind", trip.kind),
    ]);

  if (!destination) throw new Error("Trip is missing its Destination.");
  if (!kind) throw new Error("Trip is missing its Trip Kind.");

  const travellers = await Promise.all(
    trip.travellerIds.map(async (personId) => {
      const [person, profile, personNotes] = await Promise.all([
        personRepository.get(personId),
        travellerProfileRepository.forPerson(personId),
        travelNoteRepository.byScope("person", personId),
      ]);
      const traveller: PlanRequest["trip"]["travellers"][number] = {
        name: person?.name ?? "Unknown traveller",
      };
      const age = ageYearsAt(person?.birthdate, trip.startDate);
      if (age !== undefined) traveller.ageYears = age;
      if (profile?.dietary) traveller.dietary = profile.dietary;
      if (profile?.packingQuirks.length)
        traveller.packingQuirks = profile.packingQuirks;
      const notes = noteTexts(personNotes);
      if (notes) traveller.notes = notes;
      return traveller;
    }),
  );

  const request: PlanRequest = {
    schemaVersion: "1.0",
    requestType: "trip-plan",
    trip: {
      destination: {
        name: destination.name,
        ...(noteTexts(destinationNotes)
          ? { notes: noteTexts(destinationNotes) }
          : {}),
      },
      startDate: trip.startDate,
      endDate: trip.endDate,
      kind: kind.name,
      ...(noteTexts(kindNotes) ? { kindNotes: noteTexts(kindNotes) } : {}),
      travellers,
    },
    ...(noteTexts(householdNotes)
      ? { householdNotes: noteTexts(householdNotes) }
      : {}),
  };

  return planRequestSchema.parse(request);
}

/** Build the Plan Request for a Trip by id. */
export async function buildPlanRequestForTrip(
  tripId: string,
): Promise<PlanRequest> {
  const trip = await tripRepository.get(tripId);
  if (!trip) throw new Error("Trip not found.");
  return buildPlanRequest(trip);
}

/** Strip fences, parse, and validate hard a pasted/uploaded Trip Plan. */
export function parseTripPlan(rawText: string): TripPlanResponse {
  return parseBridgeResponse(rawText, tripPlanSchema);
}

/**
 * Validate and persist a Trip Plan for a Trip. The caller shows the Packing
 * List for confirm/edit first (AI-fallible); this writes the confirmed plan,
 * seeding each item's local `checked` state to false.
 */
export async function importTripPlan(
  tripId: string,
  plan: TripPlanResponse,
): Promise<TripPlan> {
  const packingList = plan.packingList.map((entry) => ({
    item: entry.item,
    assignedTo: entry.assignedTo ?? null,
    checked: false,
  }));
  const stored = await tripPlanRepository.save(tripId, packingList, plan.sections);
  tripsBus.emit("planImported", { tripId, tripPlanId: stored.id });
  return stored;
}
