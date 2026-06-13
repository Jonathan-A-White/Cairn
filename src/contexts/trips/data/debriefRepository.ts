import { db } from "../../../shared/data/db";
import { newId } from "../../../shared/core/ids";
import { Repository } from "../../../shared/data/repository";
import type { Debrief } from "../contracts/types";

/** Repository tracking which Trips have been debriefed. */
export class DebriefRepository extends Repository<Debrief> {
  constructor() {
    super(db.debriefs);
  }

  async forTrip(tripId: string): Promise<Debrief | undefined> {
    return this.table.where("tripId").equals(tripId).first();
  }

  async record(tripId: string): Promise<Debrief> {
    const debrief: Debrief = {
      id: newId(),
      tripId,
      completedAt: new Date().toISOString(),
    };
    await this.put(debrief);
    return debrief;
  }
}

export const debriefRepository = new DebriefRepository();
