import { db } from "../../../shared/data/db";
import { newId } from "../../../shared/core/ids";
import { Repository } from "../../../shared/data/repository";
import type { Item } from "../contracts/types";

/** Repository for Items (things the household keeps; never counted). */
export class ItemRepository extends Repository<Item> {
  constructor() {
    super(db.items);
  }

  async create(name: string, aliases: string[] = []): Promise<Item> {
    const item: Item = {
      id: newId(),
      name: name.trim(),
      aliases: dedupeAliases(aliases),
    };
    await this.put(item);
    return item;
  }

  async rename(id: string, name: string): Promise<void> {
    await this.table.update(id, { name: name.trim() });
  }

  async setAliases(id: string, aliases: string[]): Promise<void> {
    await this.table.update(id, { aliases: dedupeAliases(aliases) });
  }

  async addAlias(id: string, alias: string): Promise<void> {
    const item = await this.get(id);
    if (!item) return;
    const trimmed = alias.trim();
    if (!trimmed || item.aliases.includes(trimmed)) return;
    await this.table.update(id, { aliases: [...item.aliases, trimmed] });
  }
}

/** Trim, drop blanks, and de-duplicate (case-insensitive) alias lists. */
export function dedupeAliases(aliases: string[]): string[] {
  const seen = new Set<string>();
  const out: string[] = [];
  for (const raw of aliases) {
    const trimmed = raw.trim();
    if (!trimmed) continue;
    const key = trimmed.toLowerCase();
    if (seen.has(key)) continue;
    seen.add(key);
    out.push(trimmed);
  }
  return out;
}

export const itemRepository = new ItemRepository();
