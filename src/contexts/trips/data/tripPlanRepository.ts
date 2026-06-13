import { db } from "../../../shared/data/db";
import { newId } from "../../../shared/core/ids";
import { Repository } from "../../../shared/data/repository";
import type { PackingListEntry, PlanSection, TripPlan } from "../contracts/types";

/** Repository for imported Trip Plans (one current plan per Trip). */
export class TripPlanRepository extends Repository<TripPlan> {
  constructor() {
    super(db.tripPlans);
  }

  /** The most recently imported plan for a Trip, if any. */
  async forTrip(tripId: string): Promise<TripPlan | undefined> {
    const plans = await this.table.where("tripId").equals(tripId).toArray();
    return plans.sort((a, b) => b.importedAt.localeCompare(a.importedAt))[0];
  }

  /**
   * Store a freshly imported plan for a Trip, replacing any previous plan for
   * that Trip. Packing items start unchecked; the app owns the checked state.
   */
  async save(
    tripId: string,
    packingList: PackingListEntry[],
    sections: PlanSection[],
  ): Promise<TripPlan> {
    const plan: TripPlan = {
      id: newId(),
      tripId,
      importedAt: new Date().toISOString(),
      packingList,
      sections,
    };
    await db.transaction("rw", db.tripPlans, async () => {
      const previous = await this.table
        .where("tripId")
        .equals(tripId)
        .primaryKeys();
      if (previous.length) await this.table.bulkDelete(previous);
      await this.put(plan);
    });
    return plan;
  }

  /** Toggle the local checked state of one Packing List item. */
  async setChecked(
    planId: string,
    itemIndex: number,
    checked: boolean,
  ): Promise<void> {
    const plan = await this.get(planId);
    if (!plan || !plan.packingList[itemIndex]) return;
    const packingList = plan.packingList.map((entry, i) =>
      i === itemIndex ? { ...entry, checked } : entry,
    );
    await this.table.update(planId, { packingList });
  }
}

export const tripPlanRepository = new TripPlanRepository();
