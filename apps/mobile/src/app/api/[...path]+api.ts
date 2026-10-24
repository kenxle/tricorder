import { proxyReadout } from "../../readout/proxy";

export const GET = (request: Request) => proxyReadout(request);
export const POST = (request: Request) => proxyReadout(request);
