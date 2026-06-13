import { EventBus } from "../../../shared/core/eventBus";
import type { VerificationOutcome } from "./types";

/** Domain events published within HomeInventory. */
export type InventoryEvents = {
  placeChanged: { placeId: string };
  itemChanged: { itemId: string };
  placementChanged: { placementId: string; itemId: string; placeId: string };
  verified: {
    placementId: string;
    outcome: VerificationOutcome;
    by: string | null;
  };
  swept: { placeId: string; addedItemIds: string[] };
};

export const inventoryBus = new EventBus<InventoryEvents>();
