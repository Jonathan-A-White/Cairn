# The form door: "Let the tutor do it"

The Governor's rule (Postern general, 2026-10-23): never make people fill out forms without an option for a tutor to handle the interaction for them. Cairn's tutor for forms is the **form-talk grind** and the **door** that draws it on a form.

## What a person sees

On **New trip** (`/trips/new`) the first thing in the card is a button, **Let the tutor do it**. Tapped, a panel opens where the tutor asks one question at a time in plain words (Where are you going? What kind of trip is it?). Each answer the tutor takes is put into the form's own field, so the person watches **Destination**, **Trip kind**, **Start** and **End** fill. When all four hold something the panel says so and tells them to tick who is travelling, read the form, change anything, and tap **Create trip** themselves. **Stop** closes the panel and leaves what is filled.

The tutor never saves a trip. **Travellers** is a tick list, beyond what the tutor can fill (the kit's choice field takes one value), so it stays the person's, by hand.

## One path for the button and the door

`create-trip` (`src/contexts/trips/features/newTripForm.ts`) is a confirm command made with `formCommand` from `voice-kit/forms`. The **Create trip** button runs it through a registry, with the same args the door's form holds (`argsOf`), so the button and a tutor that one day calls the command save the same trip, through `saveNewTrip` and the trip repository, once. Its args schema is built from the form's fields: Destination, Trip kind, Start and End are required, a date is YYYY-MM-DD, nothing else is allowed. Trip kind is free text in the command because a new kind has always been made by typing it; the **door's** form (`newTripForm(kinds)`) makes Trip kind a choice of the kinds the screen offers, so the tutor can only name one of them.

## The pieces

| Piece | File |
| --- | --- |
| The grind | `grinds/form-talk.json`, instructions `grinds/form-talk.md` (the kit's "Helping him fill in a form" part, copied from `voice-kit/packages/forms/grind/helping-with-a-form.md`, with Cairn's lines first), schemas `contexts/trips/schemas/form-talk-request-1.0.schema.json` and `form-talk-result-1.0.schema.json`, examples `grinds/examples/form-talk/` |
| The request, the send, the answer check | `src/bridge/formTalk.ts` |
| The panel | `src/app/FormDoor.tsx` (it knows no form: a form gives it a `FormSpec`, its values and an `onFill`) |
| New trip as the tutor sees it, and `create-trip` | `src/contexts/trips/features/newTripForm.ts`, drawn by `NewTripScreen.tsx` |

The request carries the four fields with what each holds, Trip kind's options, the last ten turns of the talk, and today's date (so "next Friday" becomes a date). It carries no photo and nothing else of the household. The answer is checked hard (`parseFormTalkAnswer`), and `applyValues` drops any value for a field the form does not have or a choice that is not an option, before anything reaches a field; the screen also keeps a date out of a date field unless it is a real YYYY-MM-DD.

## Sending

The request goes through the bridge's provider seam (`src/bridge/provider.ts`): the highest-priority provider that can `fulfil` it. Until the factory provider (ADR-0004) is registered only the manual file bridge exists, which cannot carry a talk, so the panel says plainly that there is no way to reach the tutor from this phone yet, and the form works by hand as before.

## Forms that have no door, and why

The rule is about forms. Two other places in Cairn take input and are not forms by the rule:

- **Save plan** (the Packing List on a trip, `TripScreen.tsx`): one list of checkboxes and one input to add a thing to it. There is nothing to be walked through; the list is the screen.
- **Add to <place>** (`inventory/features/SweepPanel.tsx`): one input. A tutor would only ask for the one thing the field already asks for.

If either grows a second field it becomes a form and gets a door the same way: a `FormSpec`, a command, a `FormDoor`.
