import type { AppRouter } from "@tricorder/rpc";
import { createTRPCClient, httpBatchLink } from "@trpc/client";
import type { inferRouterInputs, inferRouterOutputs } from "@trpc/server";

export type { AppRouter } from "@tricorder/rpc";
// Inputs come from the router's Zod schemas, including pre-transform values.
export type RouterInputs = inferRouterInputs<AppRouter>;
export type RouterOutputs = inferRouterOutputs<AppRouter>;

// Same origin in development and in the built page. Server imports are types only.
export const trpc = createTRPCClient<AppRouter>({
  links: [httpBatchLink({ url: "/trpc" })],
});
