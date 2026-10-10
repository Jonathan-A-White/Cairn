/**
 * Support for the grind scenarios under grinds/examples/<kind>/<name>.json
 * (format: grinds/examples/README.md). Test-side only: the app never imports it.
 *
 * The check names are the ones `mw grist smoke` reads (is_null, one_of, ...), and
 * an expect path is dotted, array positions included ("containers.0.name").
 */

/** An example photo has to stay public-safe and small. */
export const EXAMPLE_PHOTO_MAX_BYTES = 200 * 1024;

export interface JsonSchema {
  $ref?: string;
  $defs?: Record<string, JsonSchema>;
  const?: unknown;
  enum?: unknown[];
  type?: string | string[];
  minLength?: number;
  maxItems?: number;
  required?: string[];
  additionalProperties?: boolean;
  properties?: Record<string, JsonSchema>;
  items?: JsonSchema;
}

/** What one answer field must show. A bare value in `expect` means `equals`. */
export interface FieldCheck {
  equals?: unknown;
  is_null?: boolean;
  one_of?: unknown[];
  contains?: unknown;
  matches?: string;
  present?: boolean;
}

export type ExpectBlock = Record<string, FieldCheck | string | number | boolean | null>;

export interface GrindExample {
  description: string;
  /** The grind's input exactly as the app sends it, schemaVersion included. */
  request: Record<string, unknown>;
  /** File names beside the example. */
  photos?: string[];
  expect: ExpectBlock;
}

const CHECKS = ["equals", "is_null", "one_of", "contains", "matches", "present"];

const deref = (root: JsonSchema, node: JsonSchema): JsonSchema =>
  node.$ref ? root.$defs?.[node.$ref.replace("#/$defs/", "")] ?? {} : node;

const typeOf = (value: unknown): string =>
  value === null ? "null" : Array.isArray(value) ? "array" : typeof value;

const allowsType = (schema: JsonSchema, type: string): boolean =>
  Array.isArray(schema.type) ? schema.type.includes(type) : schema.type === type;

/** What is wrong with a document against a JSON Schema (the subset the grinds use); empty when it fits. */
export function schemaProblems(doc: unknown, schema: JsonSchema, root: JsonSchema = schema, at = "(root)"): string[] {
  const node = deref(root, schema);
  const problems: string[] = [];
  const type = typeOf(doc);
  if (node.type && !(Array.isArray(node.type) ? node.type : [node.type]).includes(type)) {
    return [`${at}: is ${type}, the schema wants ${JSON.stringify(node.type)}`];
  }
  if ("const" in node && JSON.stringify(doc) !== JSON.stringify(node.const)) {
    problems.push(`${at}: is ${JSON.stringify(doc)}, the schema wants ${JSON.stringify(node.const)}`);
  }
  if (node.enum && !node.enum.some((v) => JSON.stringify(v) === JSON.stringify(doc))) {
    problems.push(`${at}: is ${JSON.stringify(doc)}, not one of ${JSON.stringify(node.enum)}`);
  }
  if (typeof doc === "string" && node.minLength !== undefined && doc.length < node.minLength) {
    problems.push(`${at}: is shorter than ${node.minLength}`);
  }
  if (Array.isArray(doc)) {
    if (node.maxItems !== undefined && doc.length > node.maxItems) problems.push(`${at}: has more than ${node.maxItems} items`);
    if (node.items) doc.forEach((v, i) => problems.push(...schemaProblems(v, node.items!, root, `${at}.${i}`)));
  }
  if (type === "object") {
    const obj = doc as Record<string, unknown>;
    for (const key of node.required ?? []) if (!(key in obj)) problems.push(`${at}: is missing "${key}"`);
    for (const [key, value] of Object.entries(obj)) {
      const child = node.properties?.[key];
      if (child) problems.push(...schemaProblems(value, child, root, `${at}.${key}`));
      else if (node.additionalProperties === false) problems.push(`${at}: has "${key}", which the schema does not allow`);
    }
  }
  return problems;
}

/** The schema of the field at a dotted path (numbers step into `items`), or undefined. */
function schemaAt(root: JsonSchema, path: string): JsonSchema | undefined {
  let node = deref(root, root);
  for (const part of path.split(".")) {
    const next: JsonSchema | undefined = /^\d+$/.test(part) ? node.items : node.properties?.[part];
    if (!next) return undefined;
    node = deref(root, next);
  }
  return node;
}

/** What is wrong with an expect block against the grind's answer schema; empty when it is sound. */
export function expectProblems(expectBlock: unknown, answerSchema: JsonSchema): string[] {
  if (typeof expectBlock !== "object" || expectBlock === null || Array.isArray(expectBlock)) {
    return ["expect: must be an object of answer path to checks"];
  }
  const entries = Object.entries(expectBlock as Record<string, unknown>);
  if (entries.length === 0) return ["expect: has no checks"];

  const problems: string[] = [];
  for (const [path, raw] of entries) {
    const schema = schemaAt(answerSchema, path);
    if (!schema) {
      problems.push(`${path}: not a field of the answer schema`);
      continue;
    }
    const isCheckObject = typeof raw === "object" && raw !== null && !Array.isArray(raw);
    const c: FieldCheck = isCheckObject ? (raw as FieldCheck) : { equals: raw };
    const keys = Object.keys(c);
    if (keys.length === 0) problems.push(`${path}: has no checks`);
    for (const key of keys) if (!CHECKS.includes(key)) problems.push(`${path}: unknown check "${key}"`);

    const fits = (value: unknown) => schemaProblems(value, schema, answerSchema, path).length === 0;
    if ("equals" in c && !fits(c.equals)) problems.push(`${path}: equals ${JSON.stringify(c.equals)} is never a valid answer`);
    if ("one_of" in c) {
      if (!Array.isArray(c.one_of) || c.one_of.length === 0) problems.push(`${path}: one_of must be a non-empty list`);
      else for (const v of c.one_of) if (!fits(v)) problems.push(`${path}: one_of ${JSON.stringify(v)} is never a valid answer`);
    }
    if ("is_null" in c) {
      if (typeof c.is_null !== "boolean") problems.push(`${path}: is_null must be true or false`);
      else if (c.is_null && !allowsType(schema, "null")) problems.push(`${path}: is never null in the answer schema`);
    }
    if ("present" in c && typeof c.present !== "boolean") problems.push(`${path}: present must be true or false`);
    if ("contains" in c && !allowsType(schema, "string") && !allowsType(schema, "array")) {
      problems.push(`${path}: contains needs a string or list field`);
    }
    if ("matches" in c) {
      if (typeof c.matches !== "string") problems.push(`${path}: matches must be a string`);
      else if (!allowsType(schema, "string")) problems.push(`${path}: matches needs a string field`);
      else {
        // mw runs the pattern with Go's RE2 and this test with JavaScript: keep to what both read
        // (no inline flags like (?i), lookaround or back-references).
        if (/\(\?[=!<i]|\\[1-9]/.test(c.matches)) problems.push(`${path}: matches uses syntax RE2 and JavaScript do not share`);
        else {
          try {
            new RegExp(c.matches);
          } catch {
            problems.push(`${path}: matches is not a valid pattern`);
          }
        }
      }
    }
  }
  return problems;
}
