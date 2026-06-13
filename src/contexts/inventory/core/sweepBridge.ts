import {
  sweepRequestSchema,
  sweepResultSchema,
  type SweepRequest,
  type SweepResult,
} from "../../../bridge/schemas";
import { parseBridgeResponse } from "../../../bridge/validate";

/**
 * Build the Sweep Request for a photo-assisted Sweep of one Place. Carries data
 * only — the result schema lives in the Project's standing instructions. The
 * photo never enters the app; the user attaches it by hand (ADR-0003).
 */
export function buildSweepRequest(
  placeName: string,
  path: string,
  hint?: string,
): SweepRequest {
  const request: SweepRequest = {
    schemaVersion: "1.0",
    requestType: "sweep",
    place: { name: placeName, path },
  };
  if (hint?.trim()) request.hint = hint.trim();
  // Validate our own export against the wire schema before it leaves.
  return sweepRequestSchema.parse(request);
}

/** Strip fences, parse, and validate hard a pasted/uploaded Sweep Result. */
export function parseSweepResult(rawText: string): SweepResult {
  return parseBridgeResponse(rawText, sweepResultSchema);
}
