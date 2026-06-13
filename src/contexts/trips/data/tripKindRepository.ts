import { db } from "../../../shared/data/db";
import { newId } from "../../../shared/core/ids";
import { Repository } from "../../../shared/data/repository";
import type { TripKind } from "../contracts/types";

/** Repository for the curated list of Trip Kinds the household grows. */
export class TripKindRepository extends Repository<TripKind> {
  constructor() {
    super(db.tripKinds);
  }

  async findOrCreate(name: string): Promise<TripKind> {
    const trimmed = name.trim();
    const all = await this.all();
    const existing = all.find(
      (k) => k.name.toLowerCase() === trimmed.toLowerCase(),
    );
    if (existing) return existing;
    const kind: TripKind = { id: newId(), name: trimmed };
    await this.put(kind);
    return kind;
  }
}

export const tripKindRepository = new TripKindRepository();
