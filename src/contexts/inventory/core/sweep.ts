import { itemRepository, dedupeAliases } from "../data/itemRepository";
import { placementRepository } from "../data/placementRepository";
import { inventoryBus } from "../contracts/events";
import type { Item } from "../contracts/types";

/** One item captured during a Sweep, before it is written. */
export interface SweepEntry {
  name: string;
  aliases?: string[];
}

/**
 * Add swept Items to a Place. Rapid-entry friendly: an existing Item with the
 * same name (case-insensitive) is reused rather than duplicated, and placing it
 * where it already lives is idempotent — so the same Sweep imported twice does
 * not create duplicates.
 */
export async function addSweptItems(
  placeId: string,
  entries: SweepEntry[],
): Promise<Item[]> {
  const existing = await itemRepository.all();
  const byName = new Map(existing.map((i) => [i.name.trim().toLowerCase(), i]));
  const added: Item[] = [];

  for (const entry of entries) {
    const name = entry.name.trim();
    if (!name) continue;
    const key = name.toLowerCase();
    let item = byName.get(key);
    if (!item) {
      item = await itemRepository.create(name, entry.aliases ?? []);
      byName.set(key, item);
    } else if (entry.aliases?.length) {
      // Fold any new aliases into the reused Item.
      const merged = dedupeAliases([...item.aliases, ...entry.aliases]);
      if (merged.length !== item.aliases.length) {
        await itemRepository.setAliases(item.id, merged);
        item = { ...item, aliases: merged };
      }
    }
    await placementRepository.place(item.id, placeId);
    added.push(item);
  }

  inventoryBus.emit("swept", {
    placeId,
    addedItemIds: added.map((i) => i.id),
  });
  return added;
}
