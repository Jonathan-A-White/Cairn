import type { Person } from "../contracts/person";
import { db } from "./db";
import { newId } from "../core/ids";
import { Repository } from "./repository";

/** Repository for the household roster (the kernel's Person concept). */
export class PersonRepository extends Repository<Person> {
  constructor() {
    super(db.persons);
  }

  /** Create a Person, returning the stored row. */
  async create(name: string, birthdate?: string): Promise<Person> {
    const person: Person = { id: newId(), name: name.trim(), birthdate };
    await this.put(person);
    return person;
  }

  async rename(id: string, name: string): Promise<void> {
    await this.table.update(id, { name: name.trim() });
  }
}

export const personRepository = new PersonRepository();
