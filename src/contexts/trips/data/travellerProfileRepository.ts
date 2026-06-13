import { db } from "../../../shared/data/db";
import { Repository } from "../../../shared/data/repository";
import type { TravellerProfile } from "../contracts/types";

/** Repository for Traveller Profiles, keyed by Person id. */
export class TravellerProfileRepository extends Repository<
  TravellerProfile,
  string
> {
  constructor() {
    super(db.travellerProfiles);
  }

  async forPerson(personId: string): Promise<TravellerProfile | undefined> {
    return this.table.get(personId);
  }

  /** Create or replace a Person's travel-relevant traits. */
  async upsert(profile: TravellerProfile): Promise<void> {
    await this.put({
      personId: profile.personId,
      dietary: profile.dietary?.trim() || undefined,
      packingQuirks: profile.packingQuirks
        .map((q) => q.trim())
        .filter(Boolean),
    });
  }
}

export const travellerProfileRepository = new TravellerProfileRepository();
