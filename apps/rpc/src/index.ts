import { createRPCServer } from "./server.ts";

const port = Number(process.env.TRICORDER_RPC_PORT ?? 8789);
if (!Number.isInteger(port) || port < 1 || port > 65_535) {
  throw new Error("TRICORDER_RPC_PORT must be a TCP port between 1 and 65535.");
}

const server = createRPCServer({
  apiURL:
    process.env.TRICORDER_API_URL ??
    `http://127.0.0.1:${process.env.PORT ?? 8787}`,
});

server.listen(port, "127.0.0.1", () => {
  console.log(`tRPC listening at http://127.0.0.1:${port}/trpc`);
});
