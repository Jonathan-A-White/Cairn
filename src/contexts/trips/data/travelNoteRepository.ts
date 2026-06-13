import { db } from "../../../shared/data/db";
import { newId } from "../../../shared/core/ids";
import { Repository } from "../../../shared/data/repository";
import type { NoteScopeType, TravelNote } from "../contracts/types";

/** Repository for scoped Travel Notes (the household's travel knowledge). */
export class TravelNoteRepository extends Repository<TravelNote> {
  constructor() {
    super(db.travelNotes);
  }

  async create(
    scopeType: NoteScopeType,
    scopeId: string | null,
    text: string,
  ): Promise<TravelNote> {
    const note: TravelNote = {
      id: newId(),
      scopeType,
      // Household notes carry no scopeId.
      scopeId: scopeType === "household" ? null : scopeId,
      text: text.trim(),
    };
    await this.put(note);
    return note;
  }

  async byScope(
    scopeType: NoteScopeType,
    scopeId: string | null,
  ): Promise<TravelNote[]> {
    const rows = await this.table
      .where("scopeType")
      .equals(scopeType)
      .toArray();
    return rows.filter((n) => n.scopeId === scopeId);
  }
}

export const travelNoteRepository = new TravelNoteRepository();
