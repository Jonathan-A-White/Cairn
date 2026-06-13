import { db } from "../../../shared/data/db";
import { newId } from "../../../shared/core/ids";
import { Repository } from "../../../shared/data/repository";
import type { Trip } from "../contracts/types";

export interface NewTripInput {
  destinationId: string;
  /** Trip Kind id. */
  kind: string;
  startDate: string;
  endDate: string;
  travellerIds: string[];
}

/** Repository for Trips (already-decided journeys). */
export class TripRepository extends Repository<Trip> {
  constructor() {
    super(db.trips);
  }

  async create(input: NewTripInput): Promise<Trip> {
    const trip: Trip = { id: newId(), ...input };
    await this.put(trip);
    return trip;
  }

  /** Trips sorted by start date, soonest first. */
  async allByDate(): Promise<Trip[]> {
    const trips = await this.all();
    return trips.sort((a, b) => a.startDate.localeCompare(b.startDate));
  }
}

export const tripRepository = new TripRepository();
