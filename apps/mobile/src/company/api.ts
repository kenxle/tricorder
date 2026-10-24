import type {
  CompanyReadout,
  CompanySectionKey,
  CompanySectionResponse,
} from "@tricorder/schema/company";
import type { CompanyRoomArrival } from "@tricorder/schema/company-room";

import { serverOrigin } from "../readout/api";

export class CompanyAPIError extends Error {
  readonly status: number;

  constructor(status: number, message: string) {
    super(message);
    this.name = "CompanyAPIError";
    this.status = status;
  }
}

const companyRequest = async <T>(path: string, signal?: AbortSignal) => {
  const response = await fetch(`${serverOrigin()}${path}`, { signal });
  const body: unknown = await response.json().catch(() => null);
  if (!response.ok) {
    const detail =
      body &&
      typeof body === "object" &&
      "detail" in body &&
      typeof body.detail === "string"
        ? body.detail
        : "The saved company request failed. Please retry.";
    throw new CompanyAPIError(response.status, detail);
  }
  if (body === null) {
    throw new CompanyAPIError(502, "The server returned an invalid readout.");
  }
  // The RPC boundary validates the saved fixture and its evidence references.
  // Consumers additionally check company/snapshot identity before displaying it.
  return body as T;
};

export const getCompanyReadout = (url: string, signal?: AbortSignal) =>
  companyRequest<CompanyReadout>(
    `/api/company/readout?${new URLSearchParams({ url }).toString()}`,
    signal
  );

export const getCompanySection = (
  company: string,
  section: CompanySectionKey,
  signal?: AbortSignal
) =>
  companyRequest<CompanySectionResponse>(
    `/api/company/section?${new URLSearchParams({ company, section }).toString()}`,
    signal
  );

export const getCompanyRoom = (
  company: string,
  stage: "partial" | "full",
  signal?: AbortSignal
) =>
  companyRequest<CompanyRoomArrival>(
    `/api/company/room?${new URLSearchParams({ company, stage }).toString()}`,
    signal
  );
