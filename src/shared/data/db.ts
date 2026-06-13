import Dexie, { type Table } from "dexie";
import type { Person } from "../contracts/person";
import type {
  Item,
  Place,
  Placement,
} from "../../contexts/inventory/contracts/types";
import type {
  Debrief,
  Destination,
  TravelNote,
  TravellerProfile,
  Trip,
  TripKind,
  TripPlan,
} from "../../contexts/trips/contracts/types";

/**
 * The single device database. Tables are grouped by context but share one
 * Dexie instance (one IndexedDB database per device). The schema is versioned;
 * a new `version(n).stores()` here is exercised on every test run via
 * fake-indexeddb so a broken upgrade fails loudly in CI, not on a device.
 */
export class CairnDb extends Dexie {
  // shared kernel
  persons!: Table<Person, string>;

  // inventory
  places!: Table<Place, string>;
  items!: Table<Item, string>;
  placements!: Table<Placement, string>;

  // trips
  destinations!: Table<Destination, string>;
  tripKinds!: Table<TripKind, string>;
  travelNotes!: Table<TravelNote, string>;
  travellerProfiles!: Table<TravellerProfile, string>;
  trips!: Table<Trip, string>;
  tripPlans!: Table<TripPlan, string>;
  debriefs!: Table<Debrief, string>;

  constructor(name = "CairnDB") {
    super(name);
    this.version(1).stores({
      // shared
      persons: "id, name",
      // inventory
      places: "id, parentId, type, name, *aliases",
      items: "id, name, *aliases",
      placements: "id, itemId, placeId, lastVerifiedAt",
      // trips
      destinations: "id, name, *aliases",
      tripKinds: "id, name",
      travelNotes: "id, scopeType, scopeId",
      travellerProfiles: "personId",
      trips: "id, destinationId, kind, startDate, *travellerIds",
      tripPlans: "id, tripId, importedAt",
      debriefs: "id, tripId, completedAt",
    });
  }
}

export const db = new CairnDb();

/** The ordered list of table names — the source of truth for snapshots. */
export const TABLE_NAMES = [
  "persons",
  "places",
  "items",
  "placements",
  "destinations",
  "tripKinds",
  "travelNotes",
  "travellerProfiles",
  "trips",
  "tripPlans",
  "debriefs",
] as const;

export type TableName = (typeof TABLE_NAMES)[number];
