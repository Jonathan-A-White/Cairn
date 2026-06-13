import { z } from "zod";
import { stripFences } from "./fences";

/** Thrown when an imported file fails parsing or schema validation. */
export class BridgeError extends Error {}

/**
 * Strip any ```json fence, parse JSON, then validate hard against a Zod schema.
 * Rejects on any mismatch with a clear message — nothing unvalidated is ever
 * returned to a caller, so nothing unvalidated is ever persisted.
 */
export function parseBridgeResponse<T>(
  rawText: string,
  schema: z.ZodType<T>,
): T {
  const text = stripFences(rawText);
  if (!text) throw new BridgeError("The file is empty.");

  let data: unknown;
  try {
    data = JSON.parse(text);
  } catch {
    throw new BridgeError("That file is not valid JSON.");
  }

  const result = schema.safeParse(data);
  if (!result.success) {
    throw new BridgeError(describeIssues(result.error));
  }
  return result.data;
}

function describeIssues(error: z.ZodError): string {
  const first = error.issues[0];
  if (!first) return "The file did not match the expected format.";
  const path = first.path.join(".");
  const where = path ? ` at "${path}"` : "";
  return `The file did not match the expected format${where}: ${first.message}.`;
}
