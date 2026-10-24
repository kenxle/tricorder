import { proxyCompany } from "../../../company/proxy";

export const GET = (request: Request) => proxyCompany(request);
