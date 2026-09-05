import { useState } from "react";
import { Card, EmptyHint, Screen, TextInput } from "../../../app/ui";
import { useAsync } from "../../../app/useAsync";
import { searchItems } from "../core/search";
import { PlacementActions } from "./PlacementActions";

/** Look up where something is kept by either family member's word. */
export function SearchScreen() {
  const [query, setQuery] = useState("");
  const results = useAsync(() => searchItems(query), [query]);

  return (
    <Screen title="Search">
      <TextInput
        autoFocus
        placeholder="Search by name or any family member's word…"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        className="mb-4"
      />

      {query.trim() === "" ? (
        <EmptyHint>Type to find where something is kept.</EmptyHint>
      ) : results.data && results.data.length === 0 ? (
        <EmptyHint>Nothing matches “{query}”.</EmptyHint>
      ) : (
        <div className="space-y-3">
          {results.data?.map((result) => (
            <Card key={result.item.id}>
              <div className="flex items-baseline justify-between">
                <span className="font-medium">{result.item.name}</span>
                {result.item.aliases.length > 0 && (
                  <span className="text-xs text-cairn-dim">
                    also: {result.item.aliases.join(", ")}
                  </span>
                )}
              </div>
              {result.placements.length === 0 ? (
                <p className="mt-1 text-sm text-cairn-dim">
                  Not placed anywhere yet.
                </p>
              ) : (
                <div className="mt-1 space-y-2">
                  {result.placements.map((pl) => (
                    <div key={pl.placementId}>
                      <p className="text-sm text-cairn-ink">{pl.path}</p>
                      <PlacementActions
                        placementId={pl.placementId}
                        onChange={results.reload}
                      />
                    </div>
                  ))}
                </div>
              )}
            </Card>
          ))}
        </div>
      )}
    </Screen>
  );
}
