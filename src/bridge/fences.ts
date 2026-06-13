/**
 * A human (via the Claude Project) can paste a JSON object wrapped in a
 * Markdown ```json fenced block. Strip a single surrounding fence if present;
 * leave already-bare JSON untouched.
 */
export function stripFences(input: string): string {
  const text = input.trim();
  if (!text.startsWith("```")) return text;
  // Drop the opening fence line (``` optionally followed by a language tag).
  const firstNewline = text.indexOf("\n");
  if (firstNewline === -1) return text;
  let body = text.slice(firstNewline + 1);
  // Drop the trailing closing fence.
  const lastFence = body.lastIndexOf("```");
  if (lastFence !== -1) {
    body = body.slice(0, lastFence);
  }
  return body.trim();
}
