import { useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  Button,
  Card,
  ErrorNote,
  Screen,
  TextInput,
} from "../../../app/ui";
import { useAsync } from "../../../app/useAsync";
import { personRepository } from "../../../shared/data/personRepository";
import { destinationRepository } from "../data/destinationRepository";
import { tripKindRepository } from "../data/tripKindRepository";
import { tripRepository } from "../data/tripRepository";

async function loadOptions() {
  const [persons, kinds, destinations] = await Promise.all([
    personRepository.all(),
    tripKindRepository.all(),
    destinationRepository.all(),
  ]);
  return { persons, kinds, destinations };
}

export function NewTripScreen() {
  const navigate = useNavigate();
  const options = useAsync(loadOptions);
  const [destination, setDestination] = useState("");
  const [kind, setKind] = useState("");
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");
  const [travellerIds, setTravellerIds] = useState<string[]>([]);
  const [error, setError] = useState<string | null>(null);

  function toggleTraveller(id: string) {
    setTravellerIds((cur) =>
      cur.includes(id) ? cur.filter((x) => x !== id) : [...cur, id],
    );
  }

  async function save() {
    setError(null);
    if (!destination.trim()) return setError("A destination is required.");
    if (!kind.trim()) return setError("A trip kind is required.");
    if (!startDate || !endDate) return setError("Start and end dates are required.");
    if (travellerIds.length === 0)
      return setError("Pick at least one traveller.");

    // Destinations and Trip Kinds are reusable — created on first use.
    const dest = await destinationRepository.findOrCreate(destination);
    const tripKind = await tripKindRepository.findOrCreate(kind);
    const trip = await tripRepository.create({
      destinationId: dest.id,
      kind: tripKind.id,
      startDate,
      endDate,
      travellerIds,
    });
    navigate(`/trips/${trip.id}`);
  }

  return (
    <Screen title="New trip">
      <Card className="space-y-3">
        <label className="block">
          <span className="text-sm text-cairn-dim">Destination</span>
          <TextInput
            list="destination-list"
            placeholder="e.g. Norman's house"
            value={destination}
            onChange={(e) => setDestination(e.target.value)}
          />
          <datalist id="destination-list">
            {options.data?.destinations.map((d) => (
              <option key={d.id} value={d.name} />
            ))}
          </datalist>
        </label>

        <label className="block">
          <span className="text-sm text-cairn-dim">Trip kind</span>
          <TextInput
            list="kind-list"
            placeholder="e.g. family visit, camping"
            value={kind}
            onChange={(e) => setKind(e.target.value)}
          />
          <datalist id="kind-list">
            {options.data?.kinds.map((k) => (
              <option key={k.id} value={k.name} />
            ))}
          </datalist>
        </label>

        <div className="flex gap-2">
          <label className="block flex-1">
            <span className="text-sm text-cairn-dim">Start</span>
            <TextInput
              type="date"
              value={startDate}
              onChange={(e) => setStartDate(e.target.value)}
            />
          </label>
          <label className="block flex-1">
            <span className="text-sm text-cairn-dim">End</span>
            <TextInput
              type="date"
              value={endDate}
              onChange={(e) => setEndDate(e.target.value)}
            />
          </label>
        </div>

        <div>
          <span className="text-sm text-cairn-dim">Travellers</span>
          {options.data && options.data.persons.length === 0 ? (
            <p className="text-sm text-cairn-dim">
              Add household members on the People tab first.
            </p>
          ) : (
            <div className="mt-1 space-y-1">
              {options.data?.persons.map((p) => (
                <label key={p.id} className="flex items-center gap-2">
                  <input
                    type="checkbox"
                    checked={travellerIds.includes(p.id)}
                    onChange={() => toggleTraveller(p.id)}
                  />
                  <span>{p.name}</span>
                </label>
              ))}
            </div>
          )}
        </div>

        {error && <ErrorNote>{error}</ErrorNote>}
        <Button onClick={save}>Create trip</Button>
      </Card>
    </Screen>
  );
}
