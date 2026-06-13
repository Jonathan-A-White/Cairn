import { useState } from "react";
import { Button, Card, TextArea } from "../../../app/ui";
import { completeDebrief, type DebriefAnswer } from "../core/debrief";
import type { NoteScopeType } from "../contracts/types";

/** A selectable scope a Debrief answer can be saved against. */
export interface ScopeOption {
  label: string;
  scopeType: NoteScopeType;
  scopeId: string | null;
}

const PROMPTS = [
  "What worked?",
  "What was missing?",
  "What to remember next time?",
];

/**
 * The Debrief ritual: each answer becomes a Travel Note with a confirmable
 * scope. This is the trips learning loop — notes feed the next Plan Request.
 */
export function DebriefForm({
  tripId,
  scopeOptions,
  defaultScopeKey,
  onDone,
}: {
  tripId: string;
  scopeOptions: ScopeOption[];
  defaultScopeKey: string;
  onDone: () => void;
}) {
  const [answers, setAnswers] = useState(
    PROMPTS.map(() => ({ text: "", scopeKey: defaultScopeKey })),
  );

  function update(i: number, patch: Partial<{ text: string; scopeKey: string }>) {
    setAnswers((cur) => cur.map((a, j) => (j === i ? { ...a, ...patch } : a)));
  }

  async function submit() {
    const payload: DebriefAnswer[] = answers
      .filter((a) => a.text.trim())
      .map((a) => {
        const scope = scopeOptions[Number(a.scopeKey)];
        return {
          text: a.text,
          scopeType: scope.scopeType,
          scopeId: scope.scopeId,
        };
      });
    await completeDebrief(tripId, payload);
    onDone();
  }

  return (
    <Card>
      <h2 className="mb-1 font-semibold">Debrief</h2>
      <p className="mb-3 text-sm text-gray-500">
        Capture what you learned. Each answer is saved as a Travel Note under the
        scope you confirm.
      </p>
      <div className="space-y-4">
        {PROMPTS.map((prompt, i) => (
          <div key={prompt}>
            <span className="text-sm font-medium">{prompt}</span>
            <TextArea
              rows={2}
              className="mt-1"
              value={answers[i].text}
              onChange={(e) => update(i, { text: e.target.value })}
            />
            <select
              className="mt-1 w-full rounded-lg border border-gray-300 px-2 py-2"
              value={answers[i].scopeKey}
              onChange={(e) => update(i, { scopeKey: e.target.value })}
              aria-label="Note scope"
            >
              {scopeOptions.map((opt, idx) => (
                <option key={idx} value={String(idx)}>
                  {opt.label}
                </option>
              ))}
            </select>
          </div>
        ))}
      </div>
      <Button className="mt-4" onClick={submit}>
        Save Debrief
      </Button>
    </Card>
  );
}
