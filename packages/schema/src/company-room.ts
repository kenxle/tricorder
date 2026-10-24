import type { Claim } from "./claim.js";
import type { CompanyIdentity } from "./company.js";

export type CompanyRoomStage = "partial" | "full";
export interface CompanyRoomFile {
  id: string;
  path: string;
}
export interface CompanyRoomArrival {
  version: 1;
  company: CompanyIdentity;
  roomId: string;
  arrivalId: string;
  stage: CompanyRoomStage;
  sequence: 1 | 2;
  snapshotAt: string;
  provenance: "saved-synthetic-replay";
  syntheticNotice: string;
  files: CompanyRoomFile[];
  claims: Record<string, Claim>;
  flags: {
    id: string;
    category: "strength" | "red_flag" | "corroboration";
    piece: string;
    title: string;
    why: string;
    claimIds: string[];
  }[];
  waiting: { piece: string; fileIds: string[] }[];
  missingFiles: CompanyRoomFile[];
  gaps: string[];
}
