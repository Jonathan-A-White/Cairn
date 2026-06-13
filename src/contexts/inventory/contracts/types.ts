/**
 * HomeInventory persistence + domain types. Vocabulary follows
 * contexts/inventory/CONTEXT.md exactly.
 */

/** A Place is a Floor, a Room, or a Container (the Home Tree node kinds). */
export type PlaceType = "floor" | "room" | "container";

/**
 * Place — any node in the home's location tree. parentId null = a Floor
 * (the top level). Rooms sit on Floors; Containers nest inside Rooms to any
 * depth. Avoid: location, spot, area.
 */
export interface Place {
  id: string;
  parentId: string | null;
  type: PlaceType;
  name: string;
  aliases: string[];
}

/**
 * Item — a thing the household keeps and may need to find. Never counted
 * (no quantity, ever). Kept at one or more Places via Placements.
 */
export interface Item {
  id: string;
  name: string;
  aliases: string[];
}

/**
 * Placement — the fact that an Item is kept at a particular Place, stamped
 * with when and by whom it was last verified. An Item may have several
 * Placements (multi-place). Avoid: assignment, entry, link.
 */
export interface Placement {
  id: string;
  itemId: string;
  placeId: string;
  /** ISO timestamp of the last Verification, or null if never verified. */
  lastVerifiedAt: string | null;
  /** Person id who last verified, or null. */
  lastVerifiedBy: string | null;
}

/** The three one-tap Verification outcomes against a Placement. */
export type VerificationOutcome = "confirm" | "refute" | "redirect";
