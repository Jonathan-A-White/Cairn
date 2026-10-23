import { useEffect, useId, useRef, useState } from "react";
import {
  FORM_START,
  applyValues,
  oneQuestion,
  requiredFilled,
  type FormSpec,
} from "voice-kit/forms";
import {
  FORM_TALK_HISTORY_TURNS,
  FORM_TALK_QUESTION_MAX,
  askFormTalk,
  buildFormTalkRequest,
  sendViaProvider,
  type FormTalkSender,
  type FormTalkTurn,
} from "../bridge/formTalk";
import { Button, ErrorNote, TextArea } from "./ui";

export const START_LABEL = "Let the tutor do it";

/** The day it is on his phone, YYYY-MM-DD (his own calendar, not UTC's). */
function localToday(): string {
  const now = new Date();
  const pad = (n: number) => String(n).padStart(2, "0");
  return `${now.getFullYear()}-${pad(now.getMonth() + 1)}-${pad(now.getDate())}`;
}

export interface FormDoorProps {
  form: FormSpec;
  /** What each field holds now, by field name. */
  values: Readonly<Record<string, string>>;
  /** Puts the tutor's value in the field; the form does the setting and shows it. */
  onFill: (field: string, value: string) => void;
  /** The name of the form's sending button, so the tutor can say whose tap sends it: "Create trip". */
  sendLabel: string;
  /** The command the form's own button runs; it goes in the request so the tutor can mention the button. */
  command?: string;
  /** A sentence for when everything is filled in: what is still his to do first ("Tick who is travelling."). */
  beforeSend?: string;
  /** Sends a form-talk request to the grind. Defaults to the bridge's provider. */
  ask?: FormTalkSender;
  today?: () => string;
}

type Phase =
  | { name: "idle" }
  | { name: "sending" }
  | { name: "failed"; detail: string };

/**
 * "Let the tutor do it" on a form: a panel where the tutor asks one question at a
 * time and fills the matching field, which he sees filled. The tutor never sends:
 * the form's own button is his (the form-talk grind, docs/form-door.md).
 */
export function FormDoor({
  form,
  values,
  onFill,
  sendLabel,
  command,
  beforeSend,
  ask = sendViaProvider,
  today = localToday,
}: FormDoorProps) {
  const [open, setOpen] = useState(false);
  const [say, setSay] = useState("");
  const [asking, setAsking] = useState<string | undefined>(undefined);
  const [phase, setPhase] = useState<Phase>({ name: "idle" });
  const [typed, setTyped] = useState("");
  const answerId = useId();
  const turns = useRef<FormTalkTurn[]>([]);
  const lastMessage = useRef("");
  // Bumped when the panel is stopped or unmounted, so a late answer is dropped.
  const generation = useRef(0);
  const latest = useRef({ form, values, onFill, command, ask, today });
  useEffect(() => {
    latest.current = { form, values, onFill, command, ask, today };
  });
  useEffect(() => {
    const counter = generation;
    return () => {
      counter.current++;
    };
  }, []);

  async function send(message: string): Promise<void> {
    lastMessage.current = message;
    const mine = generation.current;
    setPhase({ name: "sending" });
    try {
      const now = latest.current;
      const request = buildFormTalkRequest({
        form: now.form,
        values: now.values,
        question: message,
        history: turns.current,
        command: now.command,
        today: now.today(),
      });
      const answer = await askFormTalk(request, now.ask);
      if (generation.current !== mine) return;
      const said = oneQuestion(answer.answer);
      turns.current = [...turns.current, { q: message, a: said }].slice(-FORM_TALK_HISTORY_TURNS);
      for (const { field, value } of applyValues(now.form, answer.form_values)) {
        latest.current.onFill(field, value);
      }
      setSay(said);
      setAsking(now.form.fields.some((f) => f.name === answer.form_ask) ? answer.form_ask : undefined);
      setPhase({ name: "idle" });
    } catch (err) {
      if (generation.current !== mine) return;
      setPhase({
        name: "failed",
        detail: err instanceof Error ? err.message : "Something went wrong.",
      });
    }
  }

  function start(): void {
    generation.current++;
    turns.current = [];
    setSay("");
    setAsking(undefined);
    setTyped("");
    setOpen(true);
    void send(FORM_START);
  }

  function stop(): void {
    generation.current++;
    setOpen(false);
    setPhase({ name: "idle" });
  }

  function reply(): void {
    const text = typed.trim();
    if (!text || phase.name === "sending") return;
    setTyped("");
    void send(text);
  }

  if (!open) {
    return (
      <Button variant="secondary" className="w-full" onClick={start}>
        {START_LABEL}
      </Button>
    );
  }

  const sending = phase.name === "sending";
  const ready = requiredFilled(form, values) && !asking && !sending && phase.name === "idle";
  return (
    <div className="rounded-lg border border-cairn-trace p-3">
      <section
        aria-label="The tutor is helping with this form"
        className="space-y-3"
      >
        {say && (
          <p aria-live="polite" className="text-lg font-semibold text-cairn-ink">
            {say}
          </p>
        )}
        {sending && (
          <p role="status" className="text-sm text-cairn-dim">
            {say ? "The tutor is thinking…" : "The tutor is getting ready…"}
          </p>
        )}
        {phase.name === "failed" && (
          <div role="alert" className="space-y-2">
            <ErrorNote>{phase.detail}</ErrorNote>
            <Button variant="secondary" onClick={() => void send(lastMessage.current)}>
              Retry
            </Button>
          </div>
        )}
        {ready && (
          <p role="status" className="text-sm text-cairn-neon">
            Everything the tutor can fill is in. {beforeSend ? `${beforeSend} ` : ""}
            Read the form, change anything you like, then tap {sendLabel} yourself.
          </p>
        )}
        {!ready && (
          <div className="space-y-2">
            <label htmlFor={answerId} className="block text-sm text-cairn-dim">
              Your answer
            </label>
            <TextArea
              id={answerId}
              rows={2}
              maxLength={FORM_TALK_QUESTION_MAX}
              value={typed}
              disabled={sending}
              onChange={(e) => setTyped(e.target.value)}
            />
            <Button
              className="w-full"
              disabled={sending || typed.trim() === ""}
              onClick={reply}
            >
              Reply
            </Button>
          </div>
        )}
        <Button variant="ghost" className="w-full" onClick={stop}>
          Stop
        </Button>
      </section>
    </div>
  );
}
