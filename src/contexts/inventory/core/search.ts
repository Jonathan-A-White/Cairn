import type { Item, Place } from "../contracts/types";
import { indexById, pathOf } from "./tree";
import { itemRepository } from "../data/itemRepository";
import { placeRepository } from "../data/placeRepository";
import { placementRepository } from "../data/placementRepository";

/** One place an Item is kept, with its full Home Tree path. */
export interface SearchPlacement {
  placementId: string;
  placeId: string;
  path: string;
  lastVerifiedAt: string | null;
}

/** A search hit: the Item plus every Place it is kept (with full paths). */
export interface SearchResult {
  item: Item;
  placements: SearchPlacement[];
}

/** True if the query matches an Item's name or any of its aliases. */
export function itemMatches(item: Item, query: string): boolean {
  const q = query.trim().toLowerCase();
  if (!q) return false;
  if (item.name.toLowerCase().includes(q)) return true;
  return item.aliases.some((a) => a.toLowerCase().includes(q));
}

/**
 * Search Items by either family member's word — name or Alias — and return
 * each hit with the full Place path(s) where it is kept.
 */
export async function searchItems(query: string): Promise<SearchResult[]> {
  const q = query.trim();
  if (!q) return [];
  const [items, places, placements] = await Promise.all([
    itemRepository.all(),
    placeRepository.all(),
    placementRepository.all(),
  ]);
  const byId = indexById(places);
  const placementsByItem = new Map<string, typeof placements>();
  for (const p of placements) {
    const list = placementsByItem.get(p.itemId) ?? [];
    list.push(p);
    placementsByItem.set(p.itemId, list);
  }

  return items
    .filter((item) => itemMatches(item, q))
    .map((item) => ({
      item,
      placements: (placementsByItem.get(item.id) ?? []).map((pl) => ({
        placementId: pl.id,
        placeId: pl.placeId,
        path: pathOf(pl.placeId, byId),
        lastVerifiedAt: pl.lastVerifiedAt,
      })),
    }))
    .sort((a, b) => a.item.name.localeCompare(b.item.name));
}

/** Resolve the full path of a single Place (UI convenience). */
export function pathForPlaces(placeId: string, places: Place[]): string {
  return pathOf(placeId, indexById(places));
}
