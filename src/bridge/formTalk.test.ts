import { describe, it, expect } from "vitest";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import type { FormSpec } from "voice-kit/forms";
import { schemaProblems, type JsonSchema } from "./grindExamples";
import {
  FORM_TALK_HISTORY_TURNS,
  askFormTalk,
  buildFormTalkRequest,
  parseFormTalkAnswer,
  sendViaProvider,
} from "./formTalk";
import { BridgeError } from "./validate";
import { manualFileProvider, type BridgeProvider } from "./provider";
import { newTripForm } from "../contexts/trips/features/newTripForm";

const repo = resolve(__dirname, "../..");
const readJson = (path: string) => JSON.parse(readFileSync(resolve(repo, path), "utf-8"));
const inputSchema: JsonSchema = readJson("contexts/trips/schemas/form-talk-request-1.0.schema.json");
const answerSchema: JsonSchema = readJson("contexts/trips/schemas/form-talk-result-1.0.schema.json");

const FORM: FormSpec = newTripForm(["camping", "family visit"]);
const START = "Help me fill this in.";

describe("buildFormTalkRequest", () => {
  const request = buildFormTalkRequest({
    form: FORM,
    values: { destination: "Norman's house", kind: "", startDate: "", endDate: "" },
    question: START,
    history: [],
    command: "create-trip",
    today: "2026-10-23",
  });

  it("carries the four fields, in screen order, with what each holds", () => {
    expect(request.form.name).toBe("New trip");
    expect(request.form.fields.map((f) => [f.name, f.label, f.required, f.value])).toEqual([
      ["destination", "Destination", true, "Norman's house"],
      ["kind", "Trip kind", true, ""],
      ["startDate", "Start", true, ""],
      ["endDate", "End", true, ""],
    ]);
  });

  it("gives Trip kind its options and no other field any", () => {
    const options = request.form.fields.map((f) => [f.name, f.kind, f.options]);
    expect(options).toEqual([
      ["destination", "text", undefined],
      ["kind", "choice", ["camping", "family visit"]],
      ["startDate", "text", undefined],
      ["endDate", "text", undefined],
    ]);
  });

  it("names the sending command, the day it is, and what he said", () => {
    expect(request).toMatchObject({
      schemaVersion: "1.0",
      requestType: "form-talk",
      question: START,
      today: "2026-10-23",
      form: { command: "create-trip" },
    });
  });

  it("fits the grind's input schema", () => {
    expect(schemaProblems(request, inputSchema)).toEqual([]);
  });

  it("sends only the last turns of the talk, and cuts a message that is too long", () => {
    const history = Array.from({ length: 14 }, (_, i) => ({ q: `q${i}`, a: `a${i}` }));
    const long = buildFormTalkRequest({
      form: FORM,
      values: {},
      question: "x".repeat(5000),
      history,
      today: "2026-10-23",
    });
    expect(long.history).toHaveLength(FORM_TALK_HISTORY_TURNS);
    expect(long.history?.[0]).toEqual({ q: "q4", a: "a4" });
    expect(long.question.length).toBeLessThanOrEqual(1200);
    expect(schemaProblems(long, inputSchema)).toEqual([]);
  });

  it("leaves out history and command when there are none", () => {
    const bare = buildFormTalkRequest({ form: FORM, values: {}, question: START, history: [], today: "2026-10-23" });
    expect("history" in bare).toBe(false);
    expect("command" in bare.form).toBe(false);
  });
});

describe("parseFormTalkAnswer", () => {
  it("accepts a question with the values it fills and the field it asks about", () => {
    const answer = parseFormTalkAnswer(
      JSON.stringify({
        answer: "When does it start?",
        form_values: [{ field: "destination", value: "Norman's house" }],
        form_ask: "startDate",
      }),
    );
    expect(answer).toEqual({
      answer: "When does it start?",
      form_values: [{ field: "destination", value: "Norman's house" }],
      form_ask: "startDate",
    });
    expect(schemaProblems(answer, answerSchema)).toEqual([]);
  });

  it("reads an answer inside a json fence, and one with only its sentence", () => {
    expect(parseFormTalkAnswer('```json\n{"answer":"Where to?"}\n```')).toEqual({ answer: "Where to?" });
  });

  it.each([
    ["not JSON", "not json"],
    ["no answer", '{"form_ask":"kind"}'],
    ["an empty answer", '{"answer":""}'],
    ["a field the schema does not have", '{"answer":"Hi?","price":3}'],
    ["a value with no field", '{"answer":"Hi?","form_values":[{"value":"x"}]}'],
    [
      "more than eight values",
      JSON.stringify({ answer: "Hi?", form_values: Array.from({ length: 9 }, () => ({ field: "kind", value: "x" })) }),
    ],
  ])("refuses %s, and says so", (_name, raw) => {
    expect(() => parseFormTalkAnswer(raw)).toThrow(BridgeError);
  });
});

describe("askFormTalk", () => {
  const request = buildFormTalkRequest({ form: FORM, values: {}, question: START, history: [], today: "2026-10-23" });

  it("sends the request and returns the validated answer", async () => {
    const seen: unknown[] = [];
    const answer = await askFormTalk(request, async (r) => {
      seen.push(r);
      return { answer: "Where are you going?", form_ask: "destination" };
    });
    expect(seen).toEqual([request]);
    expect(answer).toEqual({ answer: "Where are you going?", form_ask: "destination" });
  });

  it("refuses an answer that does not fit, rather than hand the screen anything unvalidated", async () => {
    await expect(askFormTalk(request, async () => ({ nope: true }))).rejects.toBeInstanceOf(BridgeError);
  });

  it("reads an answer that comes back as text", async () => {
    const answer = await askFormTalk(request, async () => '{"answer":"Where to?"}');
    expect(answer.answer).toBe("Where to?");
  });
});

describe("sendViaProvider", () => {
  const request = buildFormTalkRequest({ form: FORM, values: {}, question: START, history: [], today: "2026-10-23" });

  it("says plainly that the tutor cannot be reached when only the manual file bridge is there", async () => {
    await expect(sendViaProvider(request, async () => manualFileProvider)).rejects.toThrow(
      /no way to reach the tutor/i,
    );
  });

  it("hands the request to a provider that can fulfil it", async () => {
    const factory: BridgeProvider = {
      id: "factory",
      priority: 10,
      available: () => true,
      fulfil: async (r) => ({ answer: `got ${(r as { requestType: string }).requestType}` }),
    };
    expect(await sendViaProvider(request, async () => factory)).toEqual({ answer: "got form-talk" });
  });
});
