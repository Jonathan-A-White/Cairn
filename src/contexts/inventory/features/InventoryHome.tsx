import { useState } from "react";
import { Link } from "react-router-dom";
import { Button, Card, EmptyHint, Screen, TextInput } from "../../../app/ui";
import { useAsync } from "../../../app/useAsync";
import { placeRepository } from "../data/placeRepository";

/** The Home Tree top level: the household's Floors (attic included). */
export function InventoryHome() {
  const floors = useAsync(() => placeRepository.children(null));
  const [name, setName] = useState("");

  async function addFloor() {
    const trimmed = name.trim();
    if (!trimmed) return;
    await placeRepository.createFloor(trimmed);
    setName("");
    floors.reload();
  }

  return (
    <Screen title="Home Tree">
      <div className="mb-4 flex gap-2">
        <TextInput
          placeholder="Add a floor (e.g. Attic, Main floor)"
          value={name}
          onChange={(e) => setName(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && addFloor()}
        />
        <Button onClick={addFloor}>Add</Button>
      </div>

      {floors.data && floors.data.length === 0 && (
        <EmptyHint>
          No floors yet. Add a floor to start mapping where things are kept.
        </EmptyHint>
      )}

      <div className="space-y-2">
        {floors.data?.map((floor) => (
          <Link key={floor.id} to={`/place/${floor.id}`}>
            <Card className="tap-hover flex items-center justify-between">
              <span className="font-medium">{floor.name}</span>
              <span className="text-gray-400">›</span>
            </Card>
          </Link>
        ))}
      </div>
    </Screen>
  );
}
