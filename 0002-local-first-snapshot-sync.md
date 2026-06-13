# v1 is local-first per device; cross-device sync is a manual snapshot file

**Status:** accepted

The app serves multiple family members on multiple devices, but v1 ships with
no real-time sync: each device holds its own local store (Dexie), and sync is a
manual export/import of a full snapshot file — the same file-bridge muscle as
ADR-0001. This is deliberate: real sharing requires OAuth or a backend, and
neither may delay the primary goal (capturing tacit household knowledge). The
repository layer keeps a clean sync seam so a shared-doc or backend provider
can be added later without domain changes; choosing that mechanism will be its
own ADR.

## Considered options

- **Shared doc (Google Drive / Gist)** — real multi-device without our own
  backend; rejected for v1 due to OAuth + conflict handling cost.
- **Sync backend (Supabase / PocketBase / Go)** — rejected for v1: breaks the
  static, secret-free model.
- **Single keeper device** — rejected: can't read on the go.

## Consequences

- Devices can be stale between snapshot syncs; last-import-wins for v1.
- Snapshot export/import must cover the *entire* store and be versioned.
