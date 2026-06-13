# TripPlanning

Turns an already-decided trip (who, where, when, what kind) into a structured
plan via the household's Claude Project, and accumulates the family's travel
knowledge — currently tacit — as a side effect of planning and finishing trips.

## Language

**Trip**: A journey the household has already decided to take — destination and
dates are known at creation. _Avoid_: vacation, getaway, journey

**Traveller**: A household Person going on a Trip. Always a reference to the
household roster; non-household companions are not modelled. _Avoid_: guest,
passenger, participant

**Destination**: A saved, reusable place the household travels to (Norman's
house, Lake George), created the first time a Trip goes there. Every Trip
references exactly one; the system never suggests one. _Avoid_: location, place

**Trip Kind**: The single category a Trip belongs to, picked from a list the
household curates and grows (camping, beach week, family visit, …). _Avoid_:
trip type, category, tag

**Traveller Profile**: A Person's travel-relevant traits — dietary needs,
age-driven gear, packing quirks — held inside TripPlanning. A trait is promoted
to the shared kernel only when a second context needs it. _Avoid_: preferences,
settings

**Debrief**: The short post-trip capture ritual — what worked, what was
missing, what to remember next time — whose answers become scoped Travel Notes.
_Avoid_: review, retrospective, survey

**Travel Note**: A free-text piece of the household's travel knowledge, scoped
to the whole household, a Trip Kind, a Person, or a Destination. _Avoid_: tip,
rule, template

**Plan Request**: The exported JSON file describing a Trip and the household
knowledge relevant to it, written for the Claude Project to read. _Avoid_:
prompt, export file

**Trip Plan**: The structured, detailed plan for a single Trip, imported as a
JSON file emitted by the Claude Project. _Avoid_: itinerary (an itinerary is at
most one part of a plan), suggestion

**Packing List**: The single structured part of a Trip Plan — checkable items,
each optionally assigned to a Traveller. _Avoid_: checklist, gear list

**Plan Section**: A titled free-form portion of a Trip Plan (itinerary, dining,
logistics, …) rendered as-is, never interpreted. _Avoid_: chapter, block
