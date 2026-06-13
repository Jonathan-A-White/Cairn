import type { PlanRequest, SweepRequest } from "./schemas";

/**
 * The AI bridge provider seam (ADR-0001). In v1 the only provider is the
 * manual, file-based bridge: the app exports a Request file and imports the
 * Project's Response file by hand. A future network provider can register at a
 * higher priority and fulfil requests directly, with no domain changes — the
 * registry just picks the highest-priority available provider.
 */

export type BridgeRequest = PlanRequest | SweepRequest;

export interface BridgeProvider {
  readonly id: string;
  /** Higher wins. The manual file bridge sits at the bottom as the fallback. */
  readonly priority: number;
  /** Whether this provider can service requests right now. */
  available(): boolean | Promise<boolean>;
  /**
   * Fulfil a request automatically (e.g. a real API). Manual providers omit
   * this — their round-trip is the file export/import in the UI.
   */
  fulfil?(request: BridgeRequest): Promise<unknown>;
}

/** The always-available fallback: the human file round-trip (ADR-0001). */
export const manualFileProvider: BridgeProvider = {
  id: "manual-file",
  priority: 0,
  available: () => true,
};

const providers: BridgeProvider[] = [manualFileProvider];

export function registerProvider(provider: BridgeProvider): void {
  if (!providers.some((p) => p.id === provider.id)) providers.push(provider);
}

/** The highest-priority provider that is currently available. */
export async function selectProvider(): Promise<BridgeProvider> {
  const ranked = [...providers].sort((a, b) => b.priority - a.priority);
  for (const provider of ranked) {
    if (await provider.available()) return provider;
  }
  return manualFileProvider;
}
