import { db } from "../../../shared/data/db";
import { newId } from "../../../shared/core/ids";
import { Repository } from "../../../shared/data/repository";
import type { Destination } from "../contracts/types";

/** Repository for reusable Destinations (created on first use). */
export class DestinationRepository extends Repository<Destination> {
  constructor() {
    super(db.destinations);
  }

  /** Reuse a Destination with the same name (case-insensitive), or create it. */
  async findOrCreate(name: string): Promise<Destination> {
    const trimmed = name.trim();
    const all = await this.all();
    const existing = all.find(
      (d) => d.name.toLowerCase() === trimmed.toLowerCase(),
    );
    if (existing) return existing;
    const destination: Destination = {
      id: newId(),
      name: trimmed,
      aliases: [],
    };
    await this.put(destination);
    return destination;
  }
}

export const destinationRepository = new DestinationRepository();
