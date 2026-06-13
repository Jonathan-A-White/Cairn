import { db } from "../../../shared/data/db";
import { newId } from "../../../shared/core/ids";
import { Repository } from "../../../shared/data/repository";
import type { Placement } from "../contracts/types";

/** Repository for Placements (an Item kept at a Place; many-to-many). */
export class PlacementRepository extends Repository<Placement> {
  constructor() {
    super(db.placements);
  }

  async byItem(itemId: string): Promise<Placement[]> {
    return this.table.where("itemId").equals(itemId).toArray();
  }

  async byPlace(placeId: string): Promise<Placement[]> {
    return this.table.where("placeId").equals(placeId).toArray();
  }

  /** The Placement of an Item at a Place, if one exists. */
  async find(itemId: string, placeId: string): Promise<Placement | undefined> {
    return this.table
      .where("itemId")
      .equals(itemId)
      .filter((p) => p.placeId === placeId)
      .first();
  }

  /**
   * Place an Item at a Place. Idempotent: re-placing where it already lives
   * returns the existing Placement rather than duplicating it.
   */
  async place(itemId: string, placeId: string): Promise<Placement> {
    const existing = await this.find(itemId, placeId);
    if (existing) return existing;
    const placement: Placement = {
      id: newId(),
      itemId,
      placeId,
      lastVerifiedAt: null,
      lastVerifiedBy: null,
    };
    await this.put(placement);
    return placement;
  }

  async stampVerified(
    placementId: string,
    by: string | null,
    when: string,
  ): Promise<void> {
    await this.table.update(placementId, {
      lastVerifiedAt: when,
      lastVerifiedBy: by,
    });
  }
}

export const placementRepository = new PlacementRepository();
