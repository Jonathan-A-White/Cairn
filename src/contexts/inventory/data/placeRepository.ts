import { db } from "../../../shared/data/db";
import { newId } from "../../../shared/core/ids";
import { Repository } from "../../../shared/data/repository";
import type { Place, PlaceType } from "../contracts/types";

/** Repository for Places (the Home Tree nodes). */
export class PlaceRepository extends Repository<Place> {
  constructor() {
    super(db.places);
  }

  /**
   * Direct children of a Place; pass null for the top level (Floors).
   * Scans rather than indexes parentId, since IndexedDB can't index null.
   */
  async children(parentId: string | null): Promise<Place[]> {
    const all = await this.all();
    return all
      .filter((p) => p.parentId === parentId)
      .sort((a, b) => a.name.localeCompare(b.name));
  }

  /** A Floor sits at the top of the tree (parentId null). */
  async createFloor(name: string): Promise<Place> {
    return this.create("floor", name, null);
  }

  async createRoom(name: string, floorId: string): Promise<Place> {
    return this.create("room", name, floorId);
  }

  async createContainer(name: string, parentId: string): Promise<Place> {
    return this.create("container", name, parentId);
  }

  private async create(
    type: PlaceType,
    name: string,
    parentId: string | null,
  ): Promise<Place> {
    const place: Place = {
      id: newId(),
      parentId,
      type,
      name: name.trim(),
      aliases: [],
    };
    await this.put(place);
    return place;
  }

  async rename(id: string, name: string): Promise<void> {
    await this.table.update(id, { name: name.trim() });
  }

  async addAlias(id: string, alias: string): Promise<void> {
    const place = await this.get(id);
    if (!place) return;
    const trimmed = alias.trim();
    if (!trimmed || place.aliases.includes(trimmed)) return;
    await this.table.update(id, { aliases: [...place.aliases, trimmed] });
  }

  /** Ids of a Place and all its descendants (depth-first). */
  async subtreeIds(rootId: string): Promise<string[]> {
    const all = await this.all();
    const byParent = new Map<string | null, Place[]>();
    for (const p of all) {
      const list = byParent.get(p.parentId) ?? [];
      list.push(p);
      byParent.set(p.parentId, list);
    }
    const out: string[] = [];
    const walk = (id: string) => {
      out.push(id);
      for (const child of byParent.get(id) ?? []) walk(child.id);
    };
    walk(rootId);
    return out;
  }
}

export const placeRepository = new PlaceRepository();
