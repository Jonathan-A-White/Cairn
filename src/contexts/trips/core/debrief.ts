import { travelNoteRepository } from "../data/travelNoteRepository";
import { debriefRepository } from "../data/debriefRepository";
import { tripsBus } from "../contracts/events";
import type { NoteScopeType } from "../contracts/types";

/** One Debrief answer the user has assigned a (confirmable) scope to. */
export interface DebriefAnswer {
  text: string;
  scopeType: NoteScopeType;
  scopeId: string | null;
}

/**
 * Complete a Trip's Debrief: each non-empty answer is saved as a Travel Note
 * with its confirmed scope, and the Trip is marked debriefed. This is the
 * trips learning loop — captured knowledge feeds the next Plan Request.
 */
export async function completeDebrief(
  tripId: string,
  answers: DebriefAnswer[],
): Promise<string[]> {
  const noteIds: string[] = [];
  for (const answer of answers) {
    const text = answer.text.trim();
    if (!text) continue;
    const note = await travelNoteRepository.create(
      answer.scopeType,
      answer.scopeId,
      text,
    );
    noteIds.push(note.id);
  }
  await debriefRepository.record(tripId);
  tripsBus.emit("debriefed", { tripId, noteIds });
  return noteIds;
}
