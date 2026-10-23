import { z } from "zod";
import {
  FORM_NAME_MAX,
  requestFields,
  type FormRequest,
  type FormSpec,
} from "voice-kit/forms";
import { stripFences } from "./fences";
import { selectProvider, type BridgeProvider } from "./provider";
import { BridgeError } from "./validate";

/**
 * The form-talk grind (grinds/form-talk.json): the tutor that fills in a form
 * with him, one question at a time. The app builds the request, sends it
 * through the bridge's provider seam (ADR-0004) and validates the answer hard
 * before anything reaches a field.
 */

export const FORM_TALK_KIND = "form-talk";
/** How many earlier turns of the talk the grind is sent. */
export const FORM_TALK_HISTORY_TURNS = 10;
/** The longest thing he can say in one turn. */
export const FORM_TALK_QUESTION_MAX = 1200;

export interface FormTalkTurn {
  q: string;
  a: string;
}

/** Mirrors contexts/trips/schemas/form-talk-request-1.0.schema.json. */
export interface FormTalkRequest {
  schemaVersion: "1.0";
  requestType: "form-talk";
  question: string;
  today?: string;
  history?: FormTalkTurn[];
  form: FormRequest;
}

export interface BuildFormTalkInput {
  form: FormSpec;
  /** What each field holds now, by field name. */
  values: Readonly<Record<string, string>>;
  /** What he just said. */
  question: string;
  /** The talk so far, oldest first. */
  history: readonly FormTalkTurn[];
  /** The command the form's own button sends it with; leave out when the form has none. */
  command?: string;
  /** YYYY-MM-DD, the day it is on his phone. */
  today: string;
}

export function buildFormTalkRequest(input: BuildFormTalkInput): FormTalkRequest {
  const { form, values, question, history, command, today } = input;
  const turns = history.slice(-FORM_TALK_HISTORY_TURNS);
  return {
    schemaVersion: "1.0",
    requestType: "form-talk",
    question: question.slice(0, FORM_TALK_QUESTION_MAX),
    today,
    ...(turns.length > 0 ? { history: turns.map(({ q, a }) => ({ q, a })) } : {}),
    form: {
      name: form.name.slice(0, FORM_NAME_MAX),
      ...(command ? { command } : {}),
      fields: requestFields(form, values),
    },
  };
}

/** Mirrors contexts/trips/schemas/form-talk-result-1.0.schema.json; `.strict()` mirrors its `additionalProperties: false`. */
export const formTalkAnswerSchema = z
  .object({
    answer: z.string().min(1).max(1200),
    form_values: z
      .array(
        z
          .object({ field: z.string().min(1), value: z.string().max(1200) })
          .strict(),
      )
      .max(8)
      .optional(),
    form_ask: z.string().optional(),
  })
  .strict();

export type FormTalkAnswer = z.infer<typeof formTalkAnswerSchema>;

/** Strip any fence, parse, validate hard: nothing unvalidated is ever returned. */
export function parseFormTalkAnswer(rawText: string): FormTalkAnswer {
  const text = stripFences(rawText);
  if (!text) throw new BridgeError("The tutor's answer is empty.");
  let data: unknown;
  try {
    data = JSON.parse(text);
  } catch {
    throw new BridgeError("The tutor's answer is not valid JSON.");
  }
  return validateFormTalkAnswer(data);
}

function validateFormTalkAnswer(data: unknown): FormTalkAnswer {
  const result = formTalkAnswerSchema.safeParse(data);
  if (!result.success) {
    const first = result.error.issues[0];
    const path = first.path.join(".");
    throw new BridgeError(
      `The tutor's answer did not match the expected format${path ? ` at "${path}"` : ""}: ${first.message}.`,
    );
  }
  return result.data;
}

/** Sends a form-talk request and returns the raw answer (an object, or the text of one). */
export type FormTalkSender = (request: FormTalkRequest) => Promise<unknown>;

/**
 * The default sender: the highest-priority provider that can fulfil a request.
 * Until the factory provider exists only the manual file bridge is there, and
 * a talk cannot ride on a file round-trip, so the tutor says so plainly.
 */
export async function sendViaProvider(
  request: FormTalkRequest,
  pick: () => Promise<BridgeProvider> = selectProvider,
): Promise<unknown> {
  const provider = await pick();
  if (!provider.fulfil) {
    throw new BridgeError(
      "There is no way to reach the tutor from this phone yet: it needs the household's factory.",
    );
  }
  return provider.fulfil(request);
}

export async function askFormTalk(
  request: FormTalkRequest,
  send: FormTalkSender = sendViaProvider,
): Promise<FormTalkAnswer> {
  const raw = await send(request);
  return typeof raw === "string" ? parseFormTalkAnswer(raw) : validateFormTalkAnswer(raw);
}
