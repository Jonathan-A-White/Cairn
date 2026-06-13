import { EventBus } from "../../../shared/core/eventBus";

/** Domain events published within TripPlanning. */
export interface TripEvents {
  tripChanged: { tripId: string };
  planImported: { tripId: string; tripPlanId: string };
  debriefed: { tripId: string; noteIds: string[] };
  noteChanged: { noteId: string };
}

export const tripsBus = new EventBus<TripEvents>();
