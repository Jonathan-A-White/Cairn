import { useState } from "react";
import { Button, Select } from "../../../app/ui";
import { useAsync } from "../../../app/useAsync";
import { personRepository } from "../../../shared/data/personRepository";
import { placeRepository } from "../data/placeRepository";
import { pathForPlaces } from "../core/search";
import {
  confirmPlacement,
  redirectPlacement,
  refutePlacement,
} from "../core/verification";

/**
 * One-tap Verification controls against a Placement: Found it (confirm),
 * Not here (refute), Actually at… (redirect to another Place). Records who.
 */
export function PlacementActions({
  placementId,
  onChange,
}: {
  placementId: string;
  onChange: () => void;
}) {
  const persons = useAsync(() => personRepository.all());
  const places = useAsync(() => placeRepository.all());
  const [by, setBy] = useState<string>("");
  const [redirecting, setRedirecting] = useState(false);

  const personId = by || null;

  async function confirm() {
    await confirmPlacement(placementId, personId);
    onChange();
  }
  async function refute() {
    await refutePlacement(placementId, personId);
    onChange();
  }
  async function redirect(placeId: string) {
    await redirectPlacement(placementId, placeId, personId);
    setRedirecting(false);
    onChange();
  }

  const placeOptions = (places.data ?? [])
    .map((p) => ({ id: p.id, path: pathForPlaces(p.id, places.data ?? []) }))
    .sort((a, b) => a.path.localeCompare(b.path));

  return (
    <div className="mt-2 space-y-2">
      <div className="flex flex-wrap items-center gap-2">
        <Button variant="secondary" onClick={confirm}>
          Found it
        </Button>
        <Button variant="secondary" onClick={refute}>
          Not here
        </Button>
        <Button variant="secondary" onClick={() => setRedirecting((v) => !v)}>
          Actually at…
        </Button>
        {persons.data && persons.data.length > 0 && (
          <Select
            value={by}
            onChange={(e) => setBy(e.target.value)}
            aria-label="Who is verifying"
          >
            <option value="">Who?</option>
            {persons.data.map((p) => (
              <option key={p.id} value={p.id}>
                {p.name}
              </option>
            ))}
          </Select>
        )}
      </div>
      {redirecting && (
        <Select
          className="w-full"
          defaultValue=""
          onChange={(e) => e.target.value && redirect(e.target.value)}
          aria-label="Move to place"
        >
          <option value="">Move to…</option>
          {placeOptions.map((p) => (
            <option key={p.id} value={p.id}>
              {p.path}
            </option>
          ))}
        </Select>
      )}
    </div>
  );
}
