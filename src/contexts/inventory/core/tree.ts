import type { Place } from "../contracts/types";

export const PATH_SEPARATOR = " → ";

/** Index Places by id for path lookups. */
export function indexById(places: Place[]): Map<string, Place> {
  return new Map(places.map((p) => [p.id, p]));
}

/** The ancestor chain of a Place, from its Floor down to the Place itself. */
export function ancestry(placeId: string, byId: Map<string, Place>): Place[] {
  const chain: Place[] = [];
  let current = byId.get(placeId);
  const guard = new Set<string>();
  while (current && !guard.has(current.id)) {
    guard.add(current.id);
    chain.unshift(current);
    current = current.parentId ? byId.get(current.parentId) : undefined;
  }
  return chain;
}

/** The full Home Tree path of a Place, e.g. "Attic → eaves closet → blue bin". */
export function pathOf(placeId: string, byId: Map<string, Place>): string {
  return ancestry(placeId, byId)
    .map((p) => p.name)
    .join(PATH_SEPARATOR);
}
