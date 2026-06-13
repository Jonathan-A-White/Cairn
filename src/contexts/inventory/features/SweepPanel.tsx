import { useRef, useState } from "react";
import { Button, Card, ErrorNote, TextArea, TextInput } from "../../../app/ui";
import { downloadJson, readFileText } from "../../../bridge/file";
import { BridgeError } from "../../../bridge/validate";
import { buildSweepRequest, parseSweepResult } from "../core/sweepBridge";
import { addSweptItems, type SweepEntry } from "../core/sweep";

/**
 * Photo-assisted Sweep (ADR-0003): export a Sweep Request for this Place, then
 * import the Project's Sweep Result. Imported items are shown for confirm/edit
 * before anything is written. The photo never enters the app.
 */
export function SweepPanel({
  placeId,
  placeName,
  path,
  onAdded,
}: {
  placeId: string;
  placeName: string;
  path: string;
  onAdded: () => void;
}) {
  const [hint, setHint] = useState("");
  const [pending, setPending] = useState<SweepEntry[] | null>(null);
  const [error, setError] = useState<string | null>(null);
  const fileInput = useRef<HTMLInputElement>(null);

  function exportRequest() {
    const request = buildSweepRequest(placeName, path, hint);
    downloadJson(`cairn-sweep-${placeName}.json`, request);
  }

  function ingest(text: string) {
    setError(null);
    try {
      const result = parseSweepResult(text);
      setPending(
        result.items.map((i) => ({ name: i.name, aliases: i.aliases })),
      );
    } catch (e) {
      setPending(null);
      setError(e instanceof BridgeError ? e.message : "Could not read that file.");
    }
  }

  async function onFile(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];
    if (file) ingest(await readFileText(file));
    if (fileInput.current) fileInput.current.value = "";
  }

  async function confirmAdd() {
    if (!pending) return;
    const entries = pending.filter((p) => p.name.trim());
    await addSweptItems(placeId, entries);
    setPending(null);
    onAdded();
  }

  return (
    <Card className="mt-4">
      <h3 className="mb-2 font-semibold">Photo-assisted Sweep</h3>
      <p className="mb-2 text-sm text-gray-500">
        Export a request, attach a photo of this place by hand in your Claude
        Project, then import the result.
      </p>
      <TextInput
        placeholder="Optional hint (what to focus on)"
        value={hint}
        onChange={(e) => setHint(e.target.value)}
        className="mb-2"
      />
      <div className="flex flex-wrap gap-2">
        <Button variant="secondary" onClick={exportRequest}>
          Export Sweep Request
        </Button>
        <Button variant="secondary" onClick={() => fileInput.current?.click()}>
          Import Sweep Result
        </Button>
        <input
          ref={fileInput}
          type="file"
          accept="application/json,.json"
          className="hidden"
          onChange={onFile}
        />
      </div>

      <details className="mt-2">
        <summary className="cursor-pointer text-sm text-gray-500">
          …or paste the result JSON
        </summary>
        <TextArea
          rows={4}
          className="mt-2"
          placeholder="Paste the Sweep Result JSON"
          onChange={(e) => e.target.value.trim() && ingest(e.target.value)}
        />
      </details>

      {error && (
        <div className="mt-3">
          <ErrorNote>{error}</ErrorNote>
        </div>
      )}

      {pending && (
        <div className="mt-4">
          <h4 className="mb-2 font-medium">
            Confirm {pending.length} item{pending.length === 1 ? "" : "s"} for{" "}
            {placeName}
          </h4>
          <div className="space-y-2">
            {pending.map((entry, i) => (
              <div key={i} className="flex items-center gap-2">
                <TextInput
                  value={entry.name}
                  onChange={(e) =>
                    setPending((cur) =>
                      cur!.map((p, j) =>
                        j === i ? { ...p, name: e.target.value } : p,
                      ),
                    )
                  }
                />
                <Button
                  variant="ghost"
                  onClick={() =>
                    setPending((cur) => cur!.filter((_, j) => j !== i))
                  }
                  aria-label={`Remove ${entry.name}`}
                >
                  ✕
                </Button>
              </div>
            ))}
          </div>
          <div className="mt-3 flex gap-2">
            <Button onClick={confirmAdd}>Add to {placeName}</Button>
            <Button variant="ghost" onClick={() => setPending(null)}>
              Cancel
            </Button>
          </div>
        </div>
      )}
    </Card>
  );
}
