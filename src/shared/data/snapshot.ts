import { db, TABLE_NAMES, type TableName } from "./db";

/**
 * Snapshot — the whole-store, schema-versioned export/import that is v1's only
 * cross-device sync mechanism (ADR-0002). Last import wins: importing replaces
 * the entire store with the snapshot's contents.
 */

export const SNAPSHOT_FORMAT_VERSION = 1;

export interface Snapshot {
  /** Discriminator so a snapshot file is never confused with a bridge file. */
  kind: "cairn-snapshot";
  /** Format version of the snapshot envelope itself. */
  formatVersion: number;
  /** Dexie schema version the data was exported at. */
  schemaVersion: number;
  exportedAt: string;
  tables: Record<TableName, unknown[]>;
}

/** Read the entire store into a Snapshot object. */
export async function exportSnapshot(): Promise<Snapshot> {
  const tables = {} as Record<TableName, unknown[]>;
  await db.transaction("r", db.tables, async () => {
    for (const name of TABLE_NAMES) {
      tables[name] = await db.table(name).toArray();
    }
  });
  return {
    kind: "cairn-snapshot",
    formatVersion: SNAPSHOT_FORMAT_VERSION,
    schemaVersion: db.verno,
    exportedAt: new Date().toISOString(),
    tables,
  };
}

/** Serialise a Snapshot to a pretty JSON string for download. */
export async function exportSnapshotJson(): Promise<string> {
  return JSON.stringify(await exportSnapshot(), null, 2);
}

export class SnapshotError extends Error {}

/** Parse and structurally validate a snapshot before it touches the store. */
export function parseSnapshot(text: string): Snapshot {
  let data: unknown;
  try {
    data = JSON.parse(text);
  } catch {
    throw new SnapshotError("That file is not valid JSON.");
  }
  if (
    !data ||
    typeof data !== "object" ||
    (data as { kind?: unknown }).kind !== "cairn-snapshot"
  ) {
    throw new SnapshotError("That file is not a Cairn snapshot.");
  }
  const snap = data as Partial<Snapshot>;
  if (
    typeof snap.formatVersion !== "number" ||
    snap.formatVersion > SNAPSHOT_FORMAT_VERSION
  ) {
    throw new SnapshotError(
      "This snapshot was made by a newer version of Cairn.",
    );
  }
  if (!snap.tables || typeof snap.tables !== "object") {
    throw new SnapshotError("This snapshot has no data tables.");
  }
  return data as Snapshot;
}

/**
 * Replace the entire store with the snapshot's contents (last import wins).
 * Tables absent from the snapshot are cleared; unknown tables are ignored.
 */
export async function importSnapshot(snapshot: Snapshot): Promise<void> {
  await db.transaction("rw", db.tables, async () => {
    for (const name of TABLE_NAMES) {
      const table = db.table(name);
      await table.clear();
      const rows = snapshot.tables[name];
      if (Array.isArray(rows) && rows.length > 0) {
        await table.bulkPut(rows);
      }
    }
  });
}

/** Convenience: validate then import from raw file text. */
export async function importSnapshotJson(text: string): Promise<void> {
  await importSnapshot(parseSnapshot(text));
}
