import type { Claim } from "./claim.js";

export type CompanySectionKey = "founders" | "comps" | "signals" | "outside";
export type CompanyStage = "pre_seed" | "seed" | "series_a";

export interface CompanyIdentity {
  slug: string;
  name: string;
  website: string;
}

export interface CompanyEvidence {
  id: string;
  /** Stable display label only. References always use id. */
  number: number;
  claim: Claim;
  sourceId: string;
  sourceTitle: string;
  qualification: string | null;
  excerpt: { before: string; match: string; after: string } | null;
}

export interface CompanyNarrative {
  text: string;
  evidenceIds: string[];
  /** Authored source associations; concatenating segment text preserves text. */
  segments?: { text: string; evidenceIds: string[] }[];
  provenance: "authored-demo";
}

export interface CompanyInsight extends CompanyNarrative {
  id: string;
  mark: "strong" | "weak" | "mixed" | "thin";
  piece: string;
  title: string;
}

export interface CompanySection {
  key: CompanySectionKey;
  title: string;
  groups: {
    id: string;
    title: string;
    subtitle: string;
    evidenceIds: string[];
    unavailable: string[];
  }[];
  gaps: { text: string; why: string }[];
}

/** Structurally compatible with the request UI's RequestItem contract. */
export interface CompanyRequestItem {
  id: string;
  title: string;
  ask: string;
  guidance: string;
  reason: string;
  checked: boolean;
}

export interface CompanyReadout {
  version: 1;
  company: CompanyIdentity;
  snapshotAt: string;
  provenance: "saved-public-research";
  summary: CompanyNarrative;
  insights: CompanyInsight[];
  evidence: Record<string, CompanyEvidence>;
  sections: { key: CompanySectionKey; title: string }[];
  request: {
    founder: string;
    defaultStage: CompanyStage;
    itemsByStage: Record<CompanyStage, CompanyRequestItem[]>;
  };
  roomGaps: { text: string; why: string; ids: string[] }[];
}

export interface CompanySectionResponse {
  version: 1;
  company: CompanyIdentity;
  snapshotAt: string;
  provenance: "saved-public-research";
  section: CompanySection;
  evidence: Record<string, CompanyEvidence>;
}
