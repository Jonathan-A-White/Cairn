import { db } from "../../../shared/data/db";
import { placementRepository } from "../data/placementRepository";
import { inventoryBus } from "../contracts/events";

/**
 * Verification — HomeInventory's learning loop. A Person's one-tap report
 * against a Placement: confirm it (found it), refute it (not here), or
 * redirect it (actually at…). Each updates the Placement and its last-verified
 * stamp.
 */

function nowIso(): string {
  return new Date().toISOString();
}

/** Found it — keep the Placement and refresh its last-verified stamp. */
export async function confirmPlacement(
  placementId: string,
  by: string | null,
  when: string = nowIso(),
): Promise<void> {
  await placementRepository.stampVerified(placementId, by, when);
  inventoryBus.emit("verified", { placementId, outcome: "confirm", by });
}

/** Not here — remove the Placement entirely. */
export async function refutePlacement(
  placementId: string,
  by: string | null = null,
): Promise<void> {
  await placementRepository.delete(placementId);
  inventoryBus.emit("verified", { placementId, outcome: "refute", by });
}

/**
 * Actually at… — move the Item's Placement to a different Place (placed at the
 * new Place and removed from the old) and stamp it verified now.
 */
export async function redirectPlacement(
  placementId: string,
  newPlaceId: string,
  by: string | null,
  when: string = nowIso(),
): Promise<void> {
  const placement = await placementRepository.get(placementId);
  if (!placement) return;
  if (placement.placeId === newPlaceId) {
    // Already there — treat as a confirmation.
    await confirmPlacement(placementId, by, when);
    return;
  }
  // If the Item already has a Placement at the target, collapse onto it.
  const existing = await placementRepository.find(placement.itemId, newPlaceId);
  await db.transaction("rw", db.placements, async () => {
    if (existing) {
      await placementRepository.stampVerified(existing.id, by, when);
      await placementRepository.delete(placementId);
    } else {
      await db.placements.update(placementId, {
        placeId: newPlaceId,
        lastVerifiedAt: when,
        lastVerifiedBy: by,
      });
    }
  });
  inventoryBus.emit("verified", { placementId, outcome: "redirect", by });
}
