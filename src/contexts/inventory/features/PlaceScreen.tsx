import { useState } from "react";
import { Link, useParams } from "react-router-dom";
import {
  Button,
  Card,
  EmptyHint,
  ErrorNote,
  Screen,
  TextInput,
} from "../../../app/ui";
import { useAsync } from "../../../app/useAsync";
import { placeRepository } from "../data/placeRepository";
import { itemRepository } from "../data/itemRepository";
import { placementRepository } from "../data/placementRepository";
import { addSweptItems } from "../core/sweep";
import { indexById, PATH_SEPARATOR, pathOf } from "../core/tree";
import { PlacementActions } from "./PlacementActions";
import { SweepPanel } from "./SweepPanel";
import type { Place, PlaceType } from "../contracts/types";

interface PlaceView {
  place: Place;
  path: string;
  children: Place[];
  items: { placementId: string; itemId: string; name: string }[];
}

async function loadPlace(placeId: string): Promise<PlaceView | null> {
  const [allPlaces, placements, allItems] = await Promise.all([
    placeRepository.all(),
    placementRepository.byPlace(placeId),
    itemRepository.all(),
  ]);
  const place = allPlaces.find((p) => p.id === placeId);
  if (!place) return null;
  const byId = indexById(allPlaces);
  const itemsById = new Map(allItems.map((i) => [i.id, i]));
  return {
    place,
    path: pathOf(placeId, byId),
    children: allPlaces
      .filter((p) => p.parentId === placeId)
      .sort((a, b) => a.name.localeCompare(b.name)),
    items: placements
      .map((pl) => ({
        placementId: pl.id,
        itemId: pl.itemId,
        name: itemsById.get(pl.itemId)?.name ?? "(unknown item)",
      }))
      .sort((a, b) => a.name.localeCompare(b.name)),
  };
}

const childTypeLabel: Record<PlaceType, string> = {
  floor: "room",
  room: "container",
  container: "container",
};

export function PlaceScreen() {
  const { placeId } = useParams<{ placeId: string }>();
  const view = useAsync(() => loadPlace(placeId!), [placeId]);
  const [childName, setChildName] = useState("");
  const [itemName, setItemName] = useState("");

  if (view.loading) return <Screen title="…">{null}</Screen>;
  if (!view.data)
    return (
      <Screen title="Not found">
        <ErrorNote>That place no longer exists.</ErrorNote>
      </Screen>
    );

  const { place, path, children, items } = view.data;
  const childType = childTypeLabel[place.type];

  async function addChild() {
    const name = childName.trim();
    if (!name || !placeId) return;
    if (place.type === "floor") await placeRepository.createRoom(name, placeId);
    else await placeRepository.createContainer(name, placeId);
    setChildName("");
    view.reload();
  }

  async function addItem() {
    const name = itemName.trim();
    if (!name || !placeId) return;
    // Typed rapid-entry Sweep: add and stay on the place.
    await addSweptItems(placeId, [{ name }]);
    setItemName("");
    view.reload();
  }

  return (
    <Screen title={place.name}>
      {/* The breadcrumb is the signal path down the tree: segments as nodes,
          the separator as the trace between them. */}
      <p className="mb-4 flex flex-wrap items-center gap-1.5 text-sm text-cairn-dim">
        {path.split(PATH_SEPARATOR).map((segment, i) => (
          <span key={i} className="flex items-center gap-1.5">
            {i > 0 && (
              <span aria-hidden className="text-cairn-neon-soft">
                ─●─
              </span>
            )}
            {segment}
          </span>
        ))}
      </p>

      <section className="mb-6">
        <h2 className="mb-2 border-l-2 border-cairn-neon-soft pl-2 text-sm font-semibold uppercase tracking-[0.15em] text-cairn-dim">
          Inside ({childType}s)
        </h2>
        <div className="mb-2 flex gap-2">
          <TextInput
            placeholder={`Add a ${childType}`}
            value={childName}
            onChange={(e) => setChildName(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && addChild()}
          />
          <Button onClick={addChild}>Add</Button>
        </div>
        {children.length === 0 ? (
          <EmptyHint>No {childType}s here yet.</EmptyHint>
        ) : (
          <div className="trace-branch space-y-2">
            {children.map((child) => (
              <Link key={child.id} to={`/place/${child.id}`} className="block">
                <Card className="tap-hover flex items-center justify-between">
                  <span>{child.name}</span>
                  <span className="text-cairn-neon-soft">›</span>
                </Card>
              </Link>
            ))}
          </div>
        )}
      </section>

      <section>
        <h2 className="mb-2 border-l-2 border-cairn-neon-soft pl-2 text-sm font-semibold uppercase tracking-[0.15em] text-cairn-dim">
          Items kept here
        </h2>
        <div className="mb-2 flex gap-2">
          <TextInput
            placeholder="Add an item (rapid Sweep — stays here)"
            value={itemName}
            onChange={(e) => setItemName(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && addItem()}
          />
          <Button onClick={addItem}>Add</Button>
        </div>
        {items.length === 0 ? (
          <EmptyHint>No items captured here yet.</EmptyHint>
        ) : (
          <div className="space-y-2">
            {items.map((it) => (
              <Card key={it.placementId}>
                <div className="flex items-center justify-between">
                  <span className="font-medium">{it.name}</span>
                </div>
                <PlacementActions
                  placementId={it.placementId}
                  onChange={view.reload}
                />
              </Card>
            ))}
          </div>
        )}

        <SweepPanel
          placeId={place.id}
          placeName={place.name}
          path={path}
          onAdded={view.reload}
        />
      </section>
    </Screen>
  );
}
