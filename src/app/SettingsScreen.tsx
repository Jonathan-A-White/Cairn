import { useRef, useState } from "react";
import { Button, Card, ErrorNote, Screen } from "./ui";
import { downloadJson, readFileText } from "../bridge/file";
import {
  exportSnapshot,
  importSnapshotJson,
  SnapshotError,
} from "../shared/data/snapshot";

/** About + the manual snapshot sync UI (ADR-0002). */
export function SettingsScreen() {
  const fileInput = useRef<HTMLInputElement>(null);
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  async function onExport() {
    setError(null);
    const snapshot = await exportSnapshot();
    downloadJson(`cairn-snapshot-${Date.now()}.json`, snapshot);
    setMessage("Snapshot exported.");
  }

  async function onImportFile(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];
    if (fileInput.current) fileInput.current.value = "";
    if (!file) return;
    setError(null);
    setMessage(null);
    try {
      await importSnapshotJson(await readFileText(file));
      setMessage("Snapshot imported. This device now matches it.");
    } catch (err) {
      setError(
        err instanceof SnapshotError
          ? err.message
          : "Could not import that snapshot.",
      );
    }
  }

  return (
    <Screen title="Settings">
      <Card className="mb-4">
        <h2 className="mb-2 font-semibold">Snapshot sync</h2>
        <p className="mb-3 text-sm text-cairn-dim">
          v1 syncs by file: export the whole store on one device and import it on
          another. Importing replaces this device's data (last import wins).
        </p>
        <div className="flex flex-wrap gap-2">
          <Button onClick={onExport}>Export snapshot</Button>
          <Button variant="secondary" onClick={() => fileInput.current?.click()}>
            Import snapshot
          </Button>
          <input
            ref={fileInput}
            type="file"
            accept="application/json,.json"
            className="hidden"
            onChange={onImportFile}
          />
        </div>
        {message && <p className="mt-3 text-sm text-cairn-neon">{message}</p>}
        {error && (
          <div className="mt-3">
            <ErrorNote>{error}</ErrorNote>
          </div>
        )}
      </Card>

      <Card>
        <h2 className="mb-1 font-semibold">About</h2>
        <p className="text-sm text-cairn-dim">
          Cairn — a cairn for the home. Offline-first; your data stays on this
          device.
        </p>
        <p className="mt-2 text-sm text-cairn-dim">Version {__APP_VERSION__}</p>
      </Card>
    </Screen>
  );
}
