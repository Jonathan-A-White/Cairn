/**
 * The Model and Effort the Governor picked for photo sweeps. Kept on this
 * device in localStorage, not in Dexie: never part of a snapshot export.
 */

export const SWEEP_MODELS = ["haiku", "sonnet", "opus"] as const;
export const SWEEP_EFFORTS = ["low", "medium", "high"] as const;

export type SweepModel = (typeof SWEEP_MODELS)[number];
export type SweepEffort = (typeof SWEEP_EFFORTS)[number];

export interface SweepGrind {
  model: SweepModel;
  effort: SweepEffort;
}

export const SWEEP_GRIND_KEY = "cairn.sweep.grind";

/** grinds/sweep.json's values. */
export const DEFAULT_SWEEP_GRIND: SweepGrind = {
  model: "sonnet",
  effort: "low",
};

function pick<T extends string>(
  allowed: readonly T[],
  value: unknown,
  fallback: T,
): T {
  return allowed.find((a) => a === value) ?? fallback;
}

// The future factory provider puts these into every grist header as `model` and `effort` (protocol §19).
export function readSweepGrind(): SweepGrind {
  let stored: unknown;
  try {
    const raw = localStorage.getItem(SWEEP_GRIND_KEY);
    stored = raw === null ? null : JSON.parse(raw);
  } catch {
    stored = null;
  }
  const obj =
    typeof stored === "object" && stored !== null
      ? (stored as Record<string, unknown>)
      : {};
  return {
    model: pick(SWEEP_MODELS, obj.model, DEFAULT_SWEEP_GRIND.model),
    effort: pick(SWEEP_EFFORTS, obj.effort, DEFAULT_SWEEP_GRIND.effort),
  };
}

export function writeSweepGrind(v: SweepGrind): void {
  localStorage.setItem(
    SWEEP_GRIND_KEY,
    JSON.stringify({ model: v.model, effort: v.effort }),
  );
}
