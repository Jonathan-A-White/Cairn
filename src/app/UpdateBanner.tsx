// 'Update ready, tap to reload', above the app while a newer build waits. The tap goes dead and
// says 'Updating…' until the page reloads.
import { applyUpdate, useUpdateState } from "./appUpdate";

export function UpdateBanner() {
  const state = useUpdateState();
  if (state === "none") return null;
  const updating = state === "updating";
  return (
    <button
      type="button"
      onClick={applyUpdate}
      disabled={updating}
      className="app-chrome flex w-full items-center justify-center border-b border-cairn-trace bg-cairn-panel px-3 py-3 text-base font-semibold text-cairn-neon disabled:opacity-70"
    >
      {updating ? "Updating…" : "Update ready, tap to reload"}
    </button>
  );
}
