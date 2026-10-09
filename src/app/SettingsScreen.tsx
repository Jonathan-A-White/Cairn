import { useRef, useState } from "react";
import { Link } from "react-router-dom";
import { Button, Card, ErrorNote, Screen, Select } from "./ui";
import { downloadJson, readFileText } from "../bridge/file";
import {
  exportSnapshot,
  importSnapshotJson,
  SnapshotError,
} from "../shared/data/snapshot";
import {
  readSweepGrind,
  SWEEP_EFFORTS,
  SWEEP_MODELS,
  writeSweepGrind,
  type SweepGrind,
} from "../bridge/sweepGrind";

const label = (s: string) => s.charAt(0).toUpperCase() + s.slice(1);

/** About + the manual snapshot sync UI (ADR-0002). */
export function SettingsScreen() {
  const fileInput = useRef<HTMLInputElement>(null);
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [grind, setGrind] = useState<SweepGrind>(readSweepGrind);

  function onGrind(change: Partial<SweepGrind>) {
    const next = { ...grind, ...change };
    writeSweepGrind(next);
    setGrind(next);
  }

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

      <Card className="mb-4">
        <h2 className="mb-2 font-semibold">Photo sweeps</h2>
        <p className="mb-3 text-sm text-cairn-dim">
          Used for each photo sent to the factory. Higher costs more fuel.
        </p>
        <div className="flex flex-wrap gap-4">
          <label className="flex flex-col gap-1 text-sm text-cairn-dim">
            Model
            <Select
              value={grind.model}
              onChange={(e) =>
                onGrind({ model: e.target.value as SweepGrind["model"] })
              }
            >
              {SWEEP_MODELS.map((m) => (
                <option key={m} value={m}>
                  {label(m)}
                </option>
              ))}
            </Select>
          </label>
          <label className="flex flex-col gap-1 text-sm text-cairn-dim">
            Effort
            <Select
              value={grind.effort}
              onChange={(e) =>
                onGrind({ effort: e.target.value as SweepGrind["effort"] })
              }
            >
              {SWEEP_EFFORTS.map((f) => (
                <option key={f} value={f}>
                  {label(f)}
                </option>
              ))}
            </Select>
          </label>
        </div>
      </Card>

      <Card>
        <h2 className="mb-1 font-semibold">About</h2>
        <p className="text-sm text-cairn-dim">
          Cairn — a cairn for the home. Offline-first; your data stays on this
          device.
        </p>
        <p data-testid="build-version" className="mt-2 break-words text-sm text-cairn-dim">
          v{__APP_VERSION__}
        </p>
        <p className="mt-2 text-sm">
          <Link to="/about" className="text-cairn-neon underline">
            About and credits
          </Link>
        </p>
      </Card>
    </Screen>
  );
}
