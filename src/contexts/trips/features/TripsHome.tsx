import { Link } from "react-router-dom";
import { Button, Card, EmptyHint, Screen } from "../../../app/ui";
import { useAsync } from "../../../app/useAsync";
import { tripRepository } from "../data/tripRepository";
import { destinationRepository } from "../data/destinationRepository";
import { tripKindRepository } from "../data/tripKindRepository";

async function loadTrips() {
  const [trips, destinations, kinds] = await Promise.all([
    tripRepository.allByDate(),
    destinationRepository.all(),
    tripKindRepository.all(),
  ]);
  const destById = new Map(destinations.map((d) => [d.id, d.name]));
  const kindById = new Map(kinds.map((k) => [k.id, k.name]));
  return trips.map((trip) => ({
    trip,
    destination: destById.get(trip.destinationId) ?? "Unknown",
    kind: kindById.get(trip.kind) ?? "Unknown",
  }));
}

export function TripsHome() {
  const trips = useAsync(loadTrips);

  return (
    <Screen
      title="Trips"
      action={
        <Link to="/trips/new">
          <Button>New trip</Button>
        </Link>
      }
    >
      {trips.data && trips.data.length === 0 && (
        <EmptyHint>
          No trips yet. Plan an already-decided trip to get started.
        </EmptyHint>
      )}
      <div className="space-y-2">
        {trips.data?.map(({ trip, destination, kind }) => (
          <Link key={trip.id} to={`/trips/${trip.id}`}>
            <Card className="tap-hover">
              <div className="flex items-center justify-between">
                <span className="font-medium">{destination}</span>
                <span className="text-xs text-gray-400">{kind}</span>
              </div>
              <p className="text-sm text-gray-500">
                {trip.startDate} → {trip.endDate} · {trip.travellerIds.length}{" "}
                traveller{trip.travellerIds.length === 1 ? "" : "s"}
              </p>
            </Card>
          </Link>
        ))}
      </div>
    </Screen>
  );
}
