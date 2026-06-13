import { useState } from "react";
import { useParams } from "react-router-dom";
import {
  Button,
  Card,
  ErrorNote,
  Screen,
  TextArea,
  TextInput,
} from "../../../app/ui";
import { useAsync } from "../../../app/useAsync";
import { downloadJson, readFileText } from "../../../bridge/file";
import { BridgeError } from "../../../bridge/validate";
import type { TripPlanResponse } from "../../../bridge/schemas";
import { personRepository } from "../../../shared/data/personRepository";
import { destinationRepository } from "../data/destinationRepository";
import { tripKindRepository } from "../data/tripKindRepository";
import { tripRepository } from "../data/tripRepository";
import { tripPlanRepository } from "../data/tripPlanRepository";
import { debriefRepository } from "../data/debriefRepository";
import {
  buildPlanRequestForTrip,
  importTripPlan,
  parseTripPlan,
} from "../core/planBridge";
import { DebriefForm, type ScopeOption } from "./DebriefForm";

async function loadTrip(tripId: string) {
  const trip = await tripRepository.get(tripId);
  if (!trip) return null;
  const [destination, kind, persons, plan, debrief] = await Promise.all([
    destinationRepository.get(trip.destinationId),
    tripKindRepository.get(trip.kind),
    personRepository.all(),
    tripPlanRepository.forTrip(tripId),
    debriefRepository.forTrip(tripId),
  ]);
  const travellerNames = trip.travellerIds.map(
    (id) => persons.find((p) => p.id === id)?.name ?? "Unknown",
  );
  const scopeOptions: ScopeOption[] = [
    { label: "Whole household", scopeType: "household", scopeId: null },
    { label: `Kind: ${kind?.name ?? ""}`, scopeType: "kind", scopeId: trip.kind },
    {
      label: `Destination: ${destination?.name ?? ""}`,
      scopeType: "destination",
      scopeId: trip.destinationId,
    },
    ...trip.travellerIds.map((id, i) => ({
      label: `Traveller: ${travellerNames[i]}`,
      scopeType: "person" as const,
      scopeId: id,
    })),
  ];
  return {
    trip,
    destinationName: destination?.name ?? "Unknown",
    kindName: kind?.name ?? "Unknown",
    travellerNames,
    plan,
    debriefed: Boolean(debrief),
    scopeOptions,
  };
}

const todayIso = () => new Date().toISOString().slice(0, 10);

export function TripScreen() {
  const { tripId } = useParams<{ tripId: string }>();
  const view = useAsync(() => loadTrip(tripId!), [tripId]);
  const [pending, setPending] = useState<TripPlanResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  if (view.loading) return <Screen title="…">{null}</Screen>;
  if (!view.data)
    return (
      <Screen title="Not found">
        <ErrorNote>That trip no longer exists.</ErrorNote>
      </Screen>
    );

  const {
    trip,
    destinationName,
    kindName,
    plan,
    debriefed,
    scopeOptions,
  } = view.data;
  const destScopeIndex = 2; // destination option (see loadTrip)

  async function exportPlanRequest() {
    setError(null);
    try {
      const request = await buildPlanRequestForTrip(trip.id);
      downloadJson(`cairn-plan-${destinationName}.json`, request);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Could not build the request.");
    }
  }

  function ingest(text: string) {
    setError(null);
    try {
      setPending(parseTripPlan(text));
    } catch (e) {
      setPending(null);
      setError(e instanceof BridgeError ? e.message : "Could not read that file.");
    }
  }

  async function onFile(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];
    e.target.value = "";
    if (file) ingest(await readFileText(file));
  }

  async function confirmPlan() {
    if (!pending) return;
    await importTripPlan(trip.id, pending);
    setPending(null);
    view.reload();
  }

  async function toggleChecked(index: number, checked: boolean) {
    if (!plan) return;
    await tripPlanRepository.setChecked(plan.id, index, checked);
    view.reload();
  }

  const endPassed = trip.endDate < todayIso();

  return (
    <Screen title={destinationName}>
      <p className="mb-4 text-sm text-gray-500">
        {trip.startDate} → {trip.endDate} · {kindName} ·{" "}
        {view.data.travellerNames.join(", ")}
      </p>

      <Card className="mb-4">
        <h2 className="mb-2 font-semibold">AI Plan</h2>
        <div className="flex flex-wrap gap-2">
          <Button onClick={exportPlanRequest}>Export Plan Request</Button>
          <label>
            <span className="inline-block cursor-pointer rounded-lg border border-gray-300 bg-white px-4 py-2 font-medium tap-hover">
              Import Trip Plan
            </span>
            <input
              type="file"
              accept="application/json,.json"
              className="hidden"
              onChange={onFile}
            />
          </label>
        </div>
        <details className="mt-2">
          <summary className="cursor-pointer text-sm text-gray-500">
            …or paste the Trip Plan JSON
          </summary>
          <TextArea
            rows={4}
            className="mt-2"
            placeholder="Paste the Trip Plan JSON"
            onChange={(e) => e.target.value.trim() && ingest(e.target.value)}
          />
        </details>
        {error && (
          <div className="mt-3">
            <ErrorNote>{error}</ErrorNote>
          </div>
        )}
      </Card>

      {pending && (
        <Card className="mb-4">
          <h3 className="mb-2 font-semibold">Confirm the Packing List</h3>
          <p className="mb-2 text-sm text-gray-500">
            AI output is fallible — edit before saving.
          </p>
          <div className="space-y-2">
            {pending.packingList.map((entry, i) => (
              <div key={i} className="flex items-center gap-2">
                <TextInput
                  value={entry.item}
                  onChange={(e) =>
                    setPending((cur) =>
                      cur
                        ? {
                            ...cur,
                            packingList: cur.packingList.map((p, j) =>
                              j === i ? { ...p, item: e.target.value } : p,
                            ),
                          }
                        : cur,
                    )
                  }
                />
                <span className="whitespace-nowrap text-xs text-gray-400">
                  {entry.assignedTo ?? "shared"}
                </span>
                <Button
                  variant="ghost"
                  aria-label={`Remove ${entry.item}`}
                  onClick={() =>
                    setPending((cur) =>
                      cur
                        ? {
                            ...cur,
                            packingList: cur.packingList.filter(
                              (_, j) => j !== i,
                            ),
                          }
                        : cur,
                    )
                  }
                >
                  ✕
                </Button>
              </div>
            ))}
          </div>
          <div className="mt-3 flex gap-2">
            <Button onClick={confirmPlan}>Save plan</Button>
            <Button variant="ghost" onClick={() => setPending(null)}>
              Cancel
            </Button>
          </div>
        </Card>
      )}

      {plan && (
        <Card className="mb-4">
          <h2 className="mb-2 font-semibold">Packing List</h2>
          <div className="space-y-1">
            {plan.packingList.map((entry, i) => (
              <label key={i} className="flex items-center gap-2">
                <input
                  type="checkbox"
                  checked={entry.checked}
                  onChange={(e) => toggleChecked(i, e.target.checked)}
                />
                <span className={entry.checked ? "line-through text-gray-400" : ""}>
                  {entry.item}
                </span>
                {entry.assignedTo && (
                  <span className="text-xs text-gray-400">
                    — {entry.assignedTo}
                  </span>
                )}
              </label>
            ))}
          </div>

          {plan.sections.map((section, i) => (
            <section key={i} className="mt-4">
              <h3 className="font-semibold">{section.title}</h3>
              <p className="user-content whitespace-pre-wrap text-sm text-gray-700">
                {section.body}
              </p>
            </section>
          ))}
        </Card>
      )}

      {endPassed &&
        (debriefed ? (
          <Card>
            <p className="text-sm text-gray-500">
              This trip has been debriefed. Its notes feed your next Plan Request.
            </p>
          </Card>
        ) : (
          <DebriefForm
            tripId={trip.id}
            scopeOptions={scopeOptions}
            defaultScopeKey={String(destScopeIndex)}
            onDone={view.reload}
          />
        ))}
    </Screen>
  );
}
