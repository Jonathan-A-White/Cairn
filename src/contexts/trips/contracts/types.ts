/**
 * TripPlanning persistence + domain types. Vocabulary follows
 * contexts/trips/CONTEXT.md exactly.
 */

/**
 * Destination — a saved, reusable place the household travels to, created the
 * first time a Trip goes there. Avoid: location, place.
 */
export interface Destination {
  id: string;
  name: string;
  aliases: string[];
}

/**
 * Trip Kind — the single category a Trip belongs to, from a list the household
 * curates and grows. Avoid: trip type, category, tag.
 */
export interface TripKind {
  id: string;
  name: string;
}

/** A Travel Note is scoped to one of these. */
export type NoteScopeType = "household" | "kind" | "person" | "destination";

/**
 * Travel Note — a free-text piece of the household's travel knowledge, scoped
 * to the whole household, a Trip Kind, a Person, or a Destination. scopeId is
 * null for household scope; otherwise the id of the kind/person/destination.
 * Avoid: tip, rule, template.
 */
export interface TravelNote {
  id: string;
  scopeType: NoteScopeType;
  scopeId: string | null;
  text: string;
}

/**
 * Traveller Profile — a Person's travel-relevant traits, held inside
 * TripPlanning. Keyed by personId. Avoid: preferences, settings.
 */
export interface TravellerProfile {
  personId: string;
  dietary?: string;
  packingQuirks: string[];
}

/**
 * Trip — a journey already decided: destination and dates known at creation.
 * `kind` holds the Trip Kind id (so Travel Notes scoped to a kind match by id).
 * Avoid: vacation, getaway, journey.
 */
export interface Trip {
  id: string;
  destinationId: string;
  /** Trip Kind id. */
  kind: string;
  startDate: string;
  endDate: string;
  /** Person ids of the Travellers. */
  travellerIds: string[];
}

/** One checkable Packing List item; the app owns the local `checked` state. */
export interface PackingListEntry {
  item: string;
  /** Traveller name, or null for shared/unassigned. */
  assignedTo: string | null;
  checked: boolean;
}

/** A titled free-form Plan Section, rendered as-is and never interpreted. */
export interface PlanSection {
  title: string;
  body: string;
}

/**
 * Trip Plan — the structured plan imported for a single Trip. Stores the
 * Packing List (with local checked state) plus the free-form Sections.
 * Avoid: itinerary, suggestion.
 */
export interface TripPlan {
  id: string;
  tripId: string;
  importedAt: string;
  packingList: PackingListEntry[];
  sections: PlanSection[];
}

/**
 * Debrief — the post-trip capture ritual; its answers become scoped Travel
 * Notes. Stored to track which Trips have been debriefed.
 * Avoid: review, retrospective, survey.
 */
export interface Debrief {
  id: string;
  tripId: string;
  completedAt: string;
}
