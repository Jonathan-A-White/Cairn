import { formCommand, type FormArgs, type FormSpec } from "voice-kit/forms";
import type { Command } from "voice-kit/talks";
import { destinationRepository } from "../data/destinationRepository";
import { tripKindRepository } from "../data/tripKindRepository";
import { tripRepository } from "../data/tripRepository";
import type { Trip } from "../contracts/types";

/**
 * New trip as the tutor sees it (the form-talk grind), and create-trip, the one
 * command the Create trip button and the door share. Travellers are a tick list,
 * beyond the kit's one-value choice, so the tutor fills the four fields below and
 * Travellers stay his by hand.
 */

export const NEW_TRIP_FORM_NAME = "New trip";
export const CREATE_TRIP = "create-trip";

export interface NewTripValues {
  destination: string;
  kind: string;
  startDate: string;
  endDate: string;
}

/** The form for the door: Trip kind is a choice of the kinds the screen offers (a text field while there are none). */
export function newTripForm(kinds: readonly string[]): FormSpec {
  return {
    name: NEW_TRIP_FORM_NAME,
    fields: [
      { name: "destination", label: "Destination", required: true, kind: "text" },
      kinds.length > 0
        ? { name: "kind", label: "Trip kind", required: true, kind: "choice", options: [...kinds] }
        : { name: "kind", label: "Trip kind", required: true, kind: "text" },
      { name: "startDate", label: "Start", hint: "A date, YYYY-MM-DD.", required: true, kind: "text", maxLength: 10 },
      { name: "endDate", label: "End", hint: "A date, YYYY-MM-DD.", required: true, kind: "text", maxLength: 10 },
    ],
  };
}

/**
 * The form create-trip's args are checked against. Trip kind is free text here:
 * by hand a new kind has always been made on first use, so the command takes one.
 */
export const NEW_TRIP_COMMAND_FORM: FormSpec = newTripForm([]);

/** A real calendar date written YYYY-MM-DD. */
export function isIsoDate(text: string): boolean {
  if (!/^\d{4}-\d{2}-\d{2}$/.test(text)) return false;
  const date = new Date(`${text}T00:00:00Z`);
  return !Number.isNaN(date.getTime()) && date.toISOString().slice(0, 10) === text;
}

/** The one place a New trip is saved: Destinations and Trip Kinds are reusable, created on first use. */
export async function saveNewTrip(values: NewTripValues, travellerIds: string[]): Promise<Trip> {
  const destination = await destinationRepository.findOrCreate(values.destination);
  const kind = await tripKindRepository.findOrCreate(values.kind);
  return tripRepository.create({
    destinationId: destination.id,
    kind: kind.id,
    startDate: values.startDate,
    endDate: values.endDate,
    travellerIds,
  });
}

export interface CreateTripOptions {
  /** Who is ticked on the screen now. */
  travellerIds: () => string[];
  /** Called with the Trip once it is saved (the screen opens it). */
  onCreated?: (trip: Trip) => void;
}

export function createTripCommand({ travellerIds, onCreated }: CreateTripOptions): Command {
  return formCommand(NEW_TRIP_COMMAND_FORM, {
    name: CREATE_TRIP,
    tell: "Creates the trip with the Destination, Trip kind, Start and End given, for the travellers ticked on the New trip screen",
    async send(values: FormArgs) {
      if (!isIsoDate(values.startDate)) throw new Error("Start must be a date, YYYY-MM-DD.");
      if (!isIsoDate(values.endDate)) throw new Error("End must be a date, YYYY-MM-DD.");
      const travellers = travellerIds();
      if (travellers.length === 0) throw new Error("Pick at least one traveller.");
      const trip = await saveNewTrip(
        { destination: values.destination, kind: values.kind, startDate: values.startDate, endDate: values.endDate },
        travellers,
      );
      onCreated?.(trip);
      return { said: `Created the trip to ${values.destination}.` };
    },
  });
}
