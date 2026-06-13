import { z } from "zod";

/**
 * Zod mirrors of the four wire schemas under contexts/* /schemas/*.json.
 * The JSON Schema is the single source of truth; these mirror it 1:1 and TS
 * types are inferred from them — never hand-maintain a parallel type. `.strict()`
 * mirrors each schema's `additionalProperties: false`.
 */

const isoDate = z
  .string()
  .regex(/^\d{4}-\d{2}-\d{2}$/, "expected a date (YYYY-MM-DD)");

// --- trips: plan-request (app → Project) ---
export const planRequestSchema = z
  .object({
    schemaVersion: z.literal("1.0"),
    requestType: z.literal("trip-plan"),
    trip: z
      .object({
        destination: z
          .object({
            name: z.string().min(1),
            notes: z.array(z.string()).optional(),
          })
          .strict(),
        startDate: isoDate,
        endDate: isoDate,
        kind: z.string().min(1),
        kindNotes: z.array(z.string()).optional(),
        travellers: z
          .array(
            z
              .object({
                name: z.string().min(1),
                ageYears: z.number().int().min(0).optional(),
                dietary: z.string().optional(),
                packingQuirks: z.array(z.string()).optional(),
                notes: z.array(z.string()).optional(),
              })
              .strict(),
          )
          .min(1),
      })
      .strict(),
    householdNotes: z.array(z.string()).optional(),
  })
  .strict();
export type PlanRequest = z.infer<typeof planRequestSchema>;

// --- trips: trip-plan (Project → app) ---
export const tripPlanSchema = z
  .object({
    schemaVersion: z.literal("1.0"),
    responseType: z.literal("trip-plan"),
    packingList: z.array(
      z
        .object({
          item: z.string().min(1),
          assignedTo: z.string().nullable().optional(),
        })
        .strict(),
    ),
    sections: z.array(
      z
        .object({
          title: z.string().min(1),
          body: z.string(),
        })
        .strict(),
    ),
  })
  .strict();
export type TripPlanResponse = z.infer<typeof tripPlanSchema>;

// --- inventory: sweep-request (app → Project) ---
export const sweepRequestSchema = z
  .object({
    schemaVersion: z.literal("1.0"),
    requestType: z.literal("sweep"),
    place: z
      .object({
        name: z.string().min(1),
        path: z.string().min(1),
      })
      .strict(),
    hint: z.string().optional(),
  })
  .strict();
export type SweepRequest = z.infer<typeof sweepRequestSchema>;

// --- inventory: sweep-result (Project → app) ---
export const sweepResultSchema = z
  .object({
    schemaVersion: z.literal("1.0"),
    responseType: z.literal("sweep-result"),
    placeName: z.string().min(1),
    items: z.array(
      z
        .object({
          name: z.string().min(1),
          aliases: z.array(z.string()).optional(),
        })
        .strict(),
    ),
  })
  .strict();
export type SweepResult = z.infer<typeof sweepResultSchema>;
