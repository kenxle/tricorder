import type { PythonAPI } from "@tricorder/schema/api";
// Compile-only assertions for the public client contract, checked by tsc.
import type { inferRouterInputs, inferRouterOutputs } from "@trpc/server";

import type { AppRouter } from "./router.ts";

type Outputs = inferRouterOutputs<AppRouter>;
type Inputs = inferRouterInputs<AppRouter>;
type Equal<A, B> =
  (<T>() => T extends A ? 1 : 2) extends <T>() => T extends B ? 1 : 2
    ? true
    : false;
type Assert<T extends true> = T;

export type RoomContract = Assert<
  Equal<Outputs["room"]["list"], PythonAPI["GET /api/rooms"]["output"]>
>;
export type MemoVersion = Assert<
  Equal<Inputs["memo"]["get"]["version"], number | null | undefined>
>;
export type RoomInput = Assert<Equal<Inputs["room"]["readout"], string>>;
export type ResultInput = Assert<
  Equal<Inputs["room"]["result"], { room: string; scan: string }>
>;
export type SourceInput = Assert<
  Equal<Inputs["room"]["source"], { room: string; claim_id: string; i: number }>
>;
export type MemoInput = Assert<
  Equal<
    Inputs["memo"]["get"],
    { room: string; version?: number | null | undefined }
  >
>;
export type CompanyInput = Assert<
  Equal<
    Inputs["store"]["readout"],
    { fund: string; company: string; version?: number | null | undefined }
  >
>;
export type ScanClaim = Assert<
  Equal<Outputs["room"]["result"]["claims"][number]["text"], string>
>;
export type StoredCompany = Assert<
  Equal<Outputs["store"]["holding"]["company"], string>
>;
export type FounderItem = Assert<
  Equal<Outputs["founderRequests"]["list"]["items"][number]["text"], string>
>;
