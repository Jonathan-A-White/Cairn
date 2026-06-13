/**
 * Browser file plumbing for the manual bridge and snapshots: serialise a
 * payload to a downloaded .json file, and read an uploaded file's text.
 */

export function toJsonText(payload: unknown): string {
  return JSON.stringify(payload, null, 2);
}

/** Trigger a download of `payload` as a pretty-printed .json file. */
export function downloadJson(filename: string, payload: unknown): void {
  const blob = new Blob([toJsonText(payload)], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename.endsWith(".json") ? filename : `${filename}.json`;
  document.body.appendChild(a);
  a.click();
  a.remove();
  URL.revokeObjectURL(url);
}

/** Read a picked File as text. */
export function readFileText(file: File): Promise<string> {
  return file.text();
}
