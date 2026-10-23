import { describe, it, expect, beforeEach, afterEach, vi } from "vitest";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import type { FormSpec } from "voice-kit/forms";
import { FormDoor } from "./FormDoor";
import type { FormTalkRequest } from "../bridge/formTalk";
import { resetDb } from "../test/reset";
import { personRepository } from "../shared/data/personRepository";
import { tripKindRepository } from "../contexts/trips/data/tripKindRepository";
import { destinationRepository } from "../contexts/trips/data/destinationRepository";
import { tripRepository } from "../contexts/trips/data/tripRepository";
import { NewTripScreen } from "../contexts/trips/features/NewTripScreen";

const SPEC: FormSpec = {
  name: "Ask for a thing",
  fields: [
    { name: "what", label: "What", required: true, kind: "text" },
    { name: "size", label: "Size", required: false, kind: "choice", options: ["Small", "Large"] },
  ],
};

/** A fake grind: answers the requests it is sent, in order, and keeps them. */
function fakeGrind(answers: unknown[]) {
  const requests: FormTalkRequest[] = [];
  const ask = vi.fn(async (request: FormTalkRequest) => {
    requests.push(request);
    const next = answers[requests.length - 1];
    if (next instanceof Error) throw next;
    return next;
  });
  return { ask, requests };
}

beforeEach(async () => {
  localStorage.clear();
  await resetDb();
});
afterEach(() => vi.restoreAllMocks());

describe("FormDoor", () => {
  function renderDoor(ask: (r: FormTalkRequest) => Promise<unknown>, onFill = vi.fn(), values: Record<string, string> = {}) {
    render(
      <FormDoor
        form={SPEC}
        values={values}
        onFill={onFill}
        ask={ask}
        sendLabel="Create thing"
        today={() => "2026-10-23"}
      />,
    );
    return onFill;
  }

  it("offers the tutor as a button, and asks nothing until it is tapped", () => {
    const grind = fakeGrind([]);
    renderDoor(grind.ask);
    expect(screen.getByRole("button", { name: "Let the tutor do it" })).toBeInTheDocument();
    expect(grind.ask).not.toHaveBeenCalled();
  });

  it("asks one question, fills what he answers and shows it, then ends at his Send", async () => {
    const user = userEvent.setup();
    const grind = fakeGrind([
      { answer: "What would you like?", form_ask: "what" },
      { answer: "How big?", form_values: [{ field: "what", value: "A kettle" }], form_ask: "size" },
      { answer: "That is everything.", form_values: [{ field: "size", value: "Large" }] },
    ]);
    const onFill = vi.fn();
    const { rerender } = render(
      <FormDoor form={SPEC} values={{}} onFill={onFill} ask={grind.ask} sendLabel="Create thing" today={() => "2026-10-23"} />,
    );

    await user.click(screen.getByRole("button", { name: "Let the tutor do it" }));
    expect(await screen.findByText("What would you like?")).toBeInTheDocument();
    expect(grind.requests[0].question).toBe("Help me fill this in.");
    expect(grind.requests[0].form.command).toBeUndefined();

    await user.type(screen.getByLabelText("Your answer"), "a kettle");
    await user.click(screen.getByRole("button", { name: "Reply" }));
    expect(await screen.findByText("How big?")).toBeInTheDocument();
    expect(onFill).toHaveBeenCalledWith("what", "A kettle");
    expect(grind.requests[1].question).toBe("a kettle");
    expect(grind.requests[1].history).toEqual([{ q: "Help me fill this in.", a: "What would you like?" }]);

    rerender(
      <FormDoor form={SPEC} values={{ what: "A kettle" }} onFill={onFill} ask={grind.ask} sendLabel="Create thing" today={() => "2026-10-23"} />,
    );
    await user.type(screen.getByLabelText("Your answer"), "the large one");
    await user.click(screen.getByRole("button", { name: "Reply" }));
    expect(await screen.findByText(/tap Create thing yourself/)).toBeInTheDocument();
    expect(onFill).toHaveBeenCalledWith("size", "Large");
    expect(screen.queryByLabelText("Your answer")).not.toBeInTheDocument();
    expect(grind.requests[2].form.fields.find((f) => f.name === "what")?.value).toBe("A kettle");
  });

  it("drops a value the form cannot take: an unknown field, or a choice that is not an option", async () => {
    const user = userEvent.setup();
    const grind = fakeGrind([
      {
        answer: "Anything else?",
        form_values: [
          { field: "colour", value: "red" },
          { field: "size", value: "Enormous" },
          { field: "what", value: "  A kettle  " },
        ],
      },
    ]);
    const onFill = renderDoor(grind.ask);
    await user.click(screen.getByRole("button", { name: "Let the tutor do it" }));
    await screen.findByText("Anything else?");
    expect(onFill.mock.calls).toEqual([["what", "A kettle"]]);
  });

  it("keeps only the first question of the answer", async () => {
    const user = userEvent.setup();
    const grind = fakeGrind([{ answer: "What would you like? Is it a kettle?" }]);
    renderDoor(grind.ask);
    await user.click(screen.getByRole("button", { name: "Let the tutor do it" }));
    expect(await screen.findByText("What would you like?")).toBeInTheDocument();
    expect(screen.queryByText(/Is it a kettle/)).not.toBeInTheDocument();
  });

  it("says when the tutor cannot be reached, and Retry asks the same thing again", async () => {
    const user = userEvent.setup();
    const grind = fakeGrind([new Error("The factory is off."), { answer: "What would you like?" }]);
    renderDoor(grind.ask);
    await user.click(screen.getByRole("button", { name: "Let the tutor do it" }));
    expect(await screen.findByRole("alert")).toHaveTextContent("The factory is off.");
    await user.click(screen.getByRole("button", { name: "Retry" }));
    expect(await screen.findByText("What would you like?")).toBeInTheDocument();
    expect(grind.requests.map((r) => r.question)).toEqual(["Help me fill this in.", "Help me fill this in."]);
    expect(screen.queryByRole("alert")).not.toBeInTheDocument();
  });

  it("Stop closes the panel and leaves what is filled", async () => {
    const user = userEvent.setup();
    const grind = fakeGrind([{ answer: "What would you like?" }]);
    renderDoor(grind.ask);
    await user.click(screen.getByRole("button", { name: "Let the tutor do it" }));
    await screen.findByText("What would you like?");
    await user.click(screen.getByRole("button", { name: "Stop" }));
    expect(screen.getByRole("button", { name: "Let the tutor do it" })).toBeInTheDocument();
    expect(screen.queryByText("What would you like?")).not.toBeInTheDocument();
  });
});

describe("New trip with the tutor", () => {
  async function renderNewTrip(ask: (r: FormTalkRequest) => Promise<unknown>) {
    const grace = await personRepository.create("Grace");
    await tripKindRepository.findOrCreate("family visit");
    await tripKindRepository.findOrCreate("camping");
    render(
      <MemoryRouter initialEntries={["/trips/new"]}>
        <Routes>
          <Route path="/trips/new" element={<NewTripScreen askTutor={ask} today={() => "2026-10-23"} />} />
          <Route path="/trips/:id" element={<p>The trip page</p>} />
        </Routes>
      </MemoryRouter>,
    );
    await screen.findByText("Grace");
    return grace;
  }

  it("asks, fills the screen's fields, ends with Create trip, and saves what the button saves", async () => {
    const user = userEvent.setup();
    const grind = fakeGrind([
      { answer: "Where are you going?", form_ask: "destination" },
      {
        answer: "What kind of trip is it?",
        form_values: [{ field: "destination", value: "Norman's house" }],
        form_ask: "kind",
      },
      {
        answer: "That is all I can fill in.",
        form_values: [
          { field: "kind", value: "family visit" },
          { field: "startDate", value: "2026-11-02" },
          { field: "endDate", value: "2026-11-05" },
        ],
      },
    ]);
    const grace = await renderNewTrip(grind.ask);
    const create = vi.spyOn(tripRepository, "create");

    await user.click(screen.getByRole("button", { name: "Let the tutor do it" }));
    expect(await screen.findByText("Where are you going?")).toBeInTheDocument();
    const first = grind.requests[0];
    expect(first.form.name).toBe("New trip");
    expect(first.form.command).toBe("create-trip");
    expect(first.form.fields.map((f) => f.label)).toEqual(["Destination", "Trip kind", "Start", "End"]);
    expect(first.form.fields[1].options).toEqual(["camping", "family visit"]);

    await user.type(screen.getByLabelText("Your answer"), "Norman's house");
    await user.click(screen.getByRole("button", { name: "Reply" }));
    expect(await screen.findByText("What kind of trip is it?")).toBeInTheDocument();
    expect(screen.getByLabelText("Destination")).toHaveValue("Norman's house");

    await user.type(screen.getByLabelText("Your answer"), "a family visit, from the second to the fifth");
    await user.click(screen.getByRole("button", { name: "Reply" }));
    expect(await screen.findByText(/tap Create trip yourself/)).toBeInTheDocument();
    expect(screen.getByLabelText("Trip kind")).toHaveValue("family visit");
    expect(screen.getByLabelText("Start")).toHaveValue("2026-11-02");
    expect(screen.getByLabelText("End")).toHaveValue("2026-11-05");

    // The tutor never sends, and Travellers stay his: nothing is saved until he ticks and taps.
    expect(create).not.toHaveBeenCalled();
    await user.click(screen.getByRole("button", { name: "Create trip" }));
    expect(await screen.findByText("Pick at least one traveller.")).toBeInTheDocument();
    expect(create).not.toHaveBeenCalled();

    await user.click(screen.getByRole("checkbox", { name: "Grace" }));
    await user.click(screen.getByRole("button", { name: "Create trip" }));
    expect(await screen.findByText("The trip page")).toBeInTheDocument();

    const destination = (await destinationRepository.all())[0];
    const kinds = await tripKindRepository.all();
    expect(create).toHaveBeenCalledTimes(1);
    expect(create).toHaveBeenCalledWith({
      destinationId: destination.id,
      kind: kinds.find((k) => k.name === "family visit")?.id,
      startDate: "2026-11-02",
      endDate: "2026-11-05",
      travellerIds: [grace.id],
    });
    expect(await tripRepository.count()).toBe(1);
  });

  it("does not put a kind the household lacks, or a date that is not one, into the screen", async () => {
    const user = userEvent.setup();
    const grind = fakeGrind([
      {
        answer: "Anything else?",
        form_values: [
          { field: "kind", value: "hiking" },
          { field: "startDate", value: "next Friday" },
        ],
      },
    ]);
    await renderNewTrip(grind.ask);
    await user.click(screen.getByRole("button", { name: "Let the tutor do it" }));
    await screen.findByText("Anything else?");
    expect(screen.getByLabelText("Trip kind")).toHaveValue("");
    expect(screen.getByLabelText("Start")).toHaveValue("");
  });

  it("keeps the hand-typed way as it was: a new kind still saves", async () => {
    const user = userEvent.setup();
    const grind = fakeGrind([]);
    const grace = await renderNewTrip(grind.ask);
    const create = vi.spyOn(tripRepository, "create");
    await user.type(screen.getByLabelText("Destination"), "The lake");
    await user.type(screen.getByLabelText("Trip kind"), "swimming");
    await user.type(screen.getByLabelText("Start"), "2026-12-01");
    await user.type(screen.getByLabelText("End"), "2026-12-03");
    await user.click(screen.getByRole("checkbox", { name: "Grace" }));
    await user.click(screen.getByRole("button", { name: "Create trip" }));
    await waitFor(() => expect(create).toHaveBeenCalledTimes(1));
    expect(create.mock.calls[0][0]).toMatchObject({ startDate: "2026-12-01", endDate: "2026-12-03", travellerIds: [grace.id] });
    expect((await tripKindRepository.all()).map((k) => k.name)).toContain("swimming");
    expect(grind.ask).not.toHaveBeenCalled();
  });
});
