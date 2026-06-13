/**
 * Person — the shared kernel's only concept: a member of the household.
 * Referenced by TripPlanning (as a Traveller) and HomeInventory (who verified
 * a Placement). Avoid: user, account, family member, traveller, owner.
 */
export interface Person {
  id: string;
  name: string;
  /** Optional; unindexed. */
  birthdate?: string;
}
