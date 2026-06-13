import { db } from "../shared/data/db";

/** Clear every table so each test starts from an empty store. */
export async function resetDb(): Promise<void> {
  await Promise.all(db.tables.map((t) => t.clear()));
}
