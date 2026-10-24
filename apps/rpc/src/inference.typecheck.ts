// Compile-only assertions for the public client contract, checked by tsc.
import type { inferRouterInputs, inferRouterOutputs } from "@trpc/server";
import type { PythonAPI } from "@tricorder/schema/api";
import type { AppRouter } from "./router.ts";

type Outputs = inferRouterOutputs<AppRouter>;
type Inputs = inferRouterInputs<AppRouter>;
type Equal<A, B> = (<T>() => T extends A ? 1 : 2) extends (<T>() => T extends B ? 1 : 2) ? true : false;
type Assert<T extends true> = T;

export type RoomContract = Assert<Equal<Outputs["room"]["list"], PythonAPI["GET /api/rooms"]["output"]>>;
export type MemoVersion = Assert<Equal<Inputs["memo"]["get"]["version"], number | null | undefined>>;
export type ScanClaim = Assert<Equal<Outputs["room"]["result"]["claims"][number]["text"], string>>;
export type StoredCompany = Assert<Equal<Outputs["store"]["holding"]["company"], string>>;
export type FounderItem = Assert<Equal<Outputs["founderRequests"]["list"]["items"][number]["text"], string>>;
