import { describe, it, expect } from "vitest";
import { stripFences } from "./fences";

describe("stripFences", () => {
  it("strips a ```json fenced block", () => {
    const text = '```json\n{"a":1}\n```';
    expect(stripFences(text)).toBe('{"a":1}');
  });

  it("strips a bare ``` fence with no language tag", () => {
    const text = '```\n{"a":1}\n```';
    expect(stripFences(text)).toBe('{"a":1}');
  });

  it("leaves already-bare JSON untouched", () => {
    expect(stripFences('{"a":1}')).toBe('{"a":1}');
  });

  it("tolerates surrounding whitespace", () => {
    expect(stripFences('\n\n  ```json\n{"a":1}\n```  \n')).toBe('{"a":1}');
  });
});
