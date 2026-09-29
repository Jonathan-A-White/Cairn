# HomeInventory

Answers "where do we keep it?" by modelling the physical home and the items in
it, and grows more precise as the household corrects and refines what it knows.
Data lives locally; the optional photo-assisted Sweep rides the household's
manual AI bridge (ADR-0001, ADR-0003).

## Language

**Home Tree**: The household's full hierarchy of Places — Floors, their Rooms,
and nested Containers — navigated as lists with full paths ("Attic → eaves
closet → blue bin"). Deliberately not a drawn floor plan. _Avoid_: map, floor
plan, blueprint

**Place**: Any node in the home's location tree — a Floor, a Room, or a
Container — at which Items may be kept, however shallow or deep. _Avoid_:
location, spot, area

**Floor**: A storey of the home, attic included; the top level of the tree.
_Avoid_: level, storey

**Room**: A named space on a Floor. _Avoid_: zone, space

**Container**: A nestable storage Place inside a Room — furniture, cabinet,
closet, shelf, bin. Containers nest to any depth (closet → shelf → blue bin).
_Avoid_: storage unit, compartment

**Item**: A thing the household keeps and may need to find, kept at one or
more Places and never counted — this is knowledge of where kinds of things
live, not stock control. _Avoid_: object, asset, belonging, stock

**Alias**: An alternate name an Item or Place answers to in search, so each
family member's word for a thing finds it. _Avoid_: synonym, tag, nickname

**Placement**: The fact that an Item is kept at a particular Place, stamped
with when and by whom it was last verified. _Avoid_: assignment, entry, link

**Sweep**: A guided capture pass through one Place — typed rapid-entry, or
photo-assisted via a Sweep Request/Result round-trip. The intended way a
household first fills the Home Tree. _Avoid_: bulk add, import, audit

**Sweep Request**: The exported instructions for one photo-assisted Sweep —
the target Place plus the result schema — alongside which the user attaches
the photo by hand in the Claude Project; the photo never enters the app. Since
ADR-0004 a Sweep Request 1.1 can instead travel to the household's factory with
the photos, carrying the Place's known Item and Container names; the photos stay
on the phone only until the Sweep Result is confirmed. _Avoid_: photo upload, scan

**Sweep Result**: The JSON list of Items the Project extracted from the photo,
imported into the target Place after the user confirms or edits it. From the
factory (1.1) it may also mark Items unsure, carry a note, and propose Containers
seen inside the Place with their own Items. _Avoid_: scan result, detection

**Verification**: A Person's one-tap report against a Placement — confirming it
(*found it*), refuting it (*not here*), or redirecting it (*actually at…*) —
which updates the Placement and its last-verified stamp. This is inventory's
learning loop. _Avoid_: feedback, audit, check
