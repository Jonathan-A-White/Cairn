import type { Table } from "dexie";

/**
 * Base repository over a Dexie table. UI and feature code never touch Dexie
 * directly — all access goes through a context's repositories, which extend
 * this. Keeps the data layer swappable and testable behind one seam.
 */
export class Repository<T, Key extends string = string> {
  constructor(protected readonly table: Table<T, Key>) {}

  async all(): Promise<T[]> {
    return this.table.toArray();
  }

  async get(id: Key): Promise<T | undefined> {
    return this.table.get(id);
  }

  async put(row: T): Promise<Key> {
    return this.table.put(row);
  }

  async bulkPut(rows: T[]): Promise<void> {
    await this.table.bulkPut(rows);
  }

  async delete(id: Key): Promise<void> {
    await this.table.delete(id);
  }

  async count(): Promise<number> {
    return this.table.count();
  }
}
