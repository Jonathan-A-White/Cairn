import { useState } from "react";
import { Button, Card, EmptyHint, Screen, TextInput } from "../../../app/ui";
import { useAsync } from "../../../app/useAsync";
import { personRepository } from "../../../shared/data/personRepository";
import { travellerProfileRepository } from "../data/travellerProfileRepository";
import { travelNoteRepository } from "../data/travelNoteRepository";
import type { Person } from "../../../shared/contracts/person";
import type { TravelNote, TravellerProfile } from "../contracts/types";

async function loadPeople() {
  const [persons, profiles, household, allNotes] = await Promise.all([
    personRepository.all(),
    travellerProfileRepository.all(),
    travelNoteRepository.byScope("household", null),
    travelNoteRepository.all(),
  ]);
  const profileByPerson = new Map(profiles.map((p) => [p.personId, p]));
  const personNotes = new Map<string, TravelNote[]>();
  for (const note of allNotes) {
    if (note.scopeType === "person" && note.scopeId) {
      const list = personNotes.get(note.scopeId) ?? [];
      list.push(note);
      personNotes.set(note.scopeId, list);
    }
  }
  return { persons, profileByPerson, household, personNotes };
}

export function PeopleScreen() {
  const view = useAsync(loadPeople);
  const [name, setName] = useState("");
  const [birthdate, setBirthdate] = useState("");
  const [householdNote, setHouseholdNote] = useState("");

  async function addPerson() {
    if (!name.trim()) return;
    await personRepository.create(name, birthdate || undefined);
    setName("");
    setBirthdate("");
    view.reload();
  }

  async function addHouseholdNote() {
    if (!householdNote.trim()) return;
    await travelNoteRepository.create("household", null, householdNote);
    setHouseholdNote("");
    view.reload();
  }

  return (
    <Screen title="People & Notes">
      <Card className="mb-4">
        <h2 className="mb-2 font-semibold">Add a household member</h2>
        <div className="space-y-2">
          <TextInput
            placeholder="Name"
            value={name}
            onChange={(e) => setName(e.target.value)}
          />
          <label className="block text-sm text-gray-600">
            Birthdate (optional)
            <TextInput
              type="date"
              value={birthdate}
              onChange={(e) => setBirthdate(e.target.value)}
            />
          </label>
          <Button onClick={addPerson}>Add person</Button>
        </div>
      </Card>

      {view.data && view.data.persons.length === 0 && (
        <EmptyHint>No household members yet.</EmptyHint>
      )}

      <div className="space-y-4">
        {view.data?.persons.map((person) => (
          <PersonCard
            key={person.id}
            person={person}
            profile={view.data!.profileByPerson.get(person.id)}
            notes={view.data!.personNotes.get(person.id) ?? []}
            onChange={view.reload}
          />
        ))}
      </div>

      <Card className="mt-6">
        <h2 className="mb-2 font-semibold">Household travel notes</h2>
        <p className="mb-2 text-sm text-gray-500">
          Knowledge that applies to every trip; bundled into each Plan Request.
        </p>
        <ul className="mb-2 list-disc pl-5 text-sm text-gray-700">
          {view.data?.household.map((n) => <li key={n.id}>{n.text}</li>)}
        </ul>
        <div className="flex gap-2">
          <TextInput
            placeholder="Add a household note"
            value={householdNote}
            onChange={(e) => setHouseholdNote(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && addHouseholdNote()}
          />
          <Button onClick={addHouseholdNote}>Add</Button>
        </div>
      </Card>
    </Screen>
  );
}

function PersonCard({
  person,
  profile,
  notes,
  onChange,
}: {
  person: Person;
  profile: TravellerProfile | undefined;
  notes: TravelNote[];
  onChange: () => void;
}) {
  const [dietary, setDietary] = useState(profile?.dietary ?? "");
  const [quirks, setQuirks] = useState(
    (profile?.packingQuirks ?? []).join(", "),
  );
  const [note, setNote] = useState("");

  async function saveProfile() {
    await travellerProfileRepository.upsert({
      personId: person.id,
      dietary,
      packingQuirks: quirks.split(",").map((q) => q.trim()).filter(Boolean),
    });
    onChange();
  }

  async function addNote() {
    if (!note.trim()) return;
    await travelNoteRepository.create("person", person.id, note);
    setNote("");
    onChange();
  }

  return (
    <Card>
      <h3 className="mb-2 font-semibold">{person.name}</h3>
      <div className="space-y-2">
        <label className="block text-sm text-gray-600">
          Dietary needs (treated as hard constraints)
          <TextInput
            value={dietary}
            onChange={(e) => setDietary(e.target.value)}
            placeholder="e.g. low-FODMAP"
          />
        </label>
        <label className="block text-sm text-gray-600">
          Packing quirks (comma-separated)
          <TextInput
            value={quirks}
            onChange={(e) => setQuirks(e.target.value)}
            placeholder="e.g. always forgets a charger"
          />
        </label>
        <Button variant="secondary" onClick={saveProfile}>
          Save profile
        </Button>
      </div>

      <div className="mt-3">
        <span className="text-sm font-medium">Notes about {person.name}</span>
        <ul className="mb-2 list-disc pl-5 text-sm text-gray-700">
          {notes.map((n) => <li key={n.id}>{n.text}</li>)}
        </ul>
        <div className="flex gap-2">
          <TextInput
            placeholder="Add a note"
            value={note}
            onChange={(e) => setNote(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && addNote()}
          />
          <Button onClick={addNote}>Add</Button>
        </div>
      </div>
    </Card>
  );
}
