import { useMemo, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import { argsOf } from "voice-kit/forms";
import { defineRegistry } from "voice-kit/talks";
import {
  Button,
  Card,
  ErrorNote,
  Screen,
  TextInput,
} from "../../../app/ui";
import { FormDoor } from "../../../app/FormDoor";
import { useAsync } from "../../../app/useAsync";
import type { FormTalkSender } from "../../../bridge/formTalk";
import { personRepository } from "../../../shared/data/personRepository";
import { destinationRepository } from "../data/destinationRepository";
import { tripKindRepository } from "../data/tripKindRepository";
import {
  CREATE_TRIP,
  NEW_TRIP_COMMAND_FORM,
  createTripCommand,
  isIsoDate,
  newTripForm,
} from "./newTripForm";

async function loadOptions() {
  const [persons, kinds, destinations] = await Promise.all([
    personRepository.all(),
    tripKindRepository.all(),
    destinationRepository.all(),
  ]);
  return { persons, kinds, destinations };
}

export interface NewTripScreenProps {
  /** Sends the tutor's talk to the grind; the bridge's provider unless a test gives a fake. */
  askTutor?: FormTalkSender;
  /** The day it is, YYYY-MM-DD; his phone's unless a test gives one. */
  today?: () => string;
}

export function NewTripScreen({ askTutor, today }: NewTripScreenProps = {}) {
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

  // The tutor fills the four fields; Travellers stay his by hand.
  const kindNames = useMemo(
    () => (options.data?.kinds ?? []).map((k) => k.name).sort((a, b) => a.localeCompare(b)),
    [options.data],
  );
  const form = useMemo(() => newTripForm(kindNames), [kindNames]);

  function fill(field: string, value: string) {
    if (field === "destination") setDestination(value);
    else if (field === "kind") setKind(value);
    else if (field === "startDate" && isIsoDate(value)) setStartDate(value);
    else if (field === "endDate" && isIsoDate(value)) setEndDate(value);
  }

  // The Create trip button and the tutor's door run the same command.
  const travellers = useRef(travellerIds);
  travellers.current = travellerIds;
  const registry = useMemo(
    () =>
      defineRegistry({
        commands: [
          createTripCommand({
            travellerIds: () => travellers.current,
            onCreated: (trip) => navigate(`/trips/${trip.id}`),
          }),
        ],
      }),
    [navigate],
  );

  async function save() {
    setError(null);
    if (!destination.trim()) return setError("A destination is required.");
    if (!kind.trim()) return setError("A trip kind is required.");
    if (!startDate || !endDate) return setError("Start and end dates are required.");
    if (travellerIds.length === 0)
      return setError("Pick at least one traveller.");

    const ran = await registry.run(
      CREATE_TRIP,
      argsOf(NEW_TRIP_COMMAND_FORM, { destination, kind, startDate, endDate }),
    );
    if (!ran.ok) setError(ran.why);
  }

  return (
    <Screen title="New trip">
      <Card className="space-y-3">
        <FormDoor
          form={form}
          values={{ destination, kind, startDate, endDate }}
          onFill={fill}
          sendLabel="Create trip"
          command={CREATE_TRIP}
          beforeSend="Tick who is travelling."
          ask={askTutor}
          today={today}
        />

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
