export type {
  Stage,
  ChecklistItem,
  RequestItem,
} from "@tricorder/request-ui/model";
export { requestItems, draftRequest } from "@tricorder/request-ui/model";
export interface Company {
  name: string;
  slug: string;
  website: string;
  host: string;
  batch: string;
  one_liner: string;
  team_size: number;
  regions: string[];
}
export interface ResearchClaim {
  text: string;
  source?: string;
  quote?: string;
  excerpt?: {
    before: string;
    match: string;
    after: string;
  };
  url?: string;
  kind?: string;
  placeholder?: boolean;
}
export interface ResearchSection {
  key: string;
  title: string;
  claims?: ResearchClaim[];
  parts?: {
    label: string;
    claims: ResearchClaim[];
  }[];
  cards?: {
    name: string;
    role: string;
    claims: ResearchClaim[];
  }[];
  gaps?: {
    text: string;
    why: string;
  }[];
}
export interface SetupField {
  value: string;
  source?: string;
  note?: string;
  edited?: boolean;
}
export interface Research {
  setup: Record<string, SetupField>;
  sections: ResearchSection[];
  room_gaps: {
    text: string;
    why: string;
    ids: string[];
  }[];
}
export const safeWebUrl = (input: string): string | null => {
  try {
    const url = new URL(input);
    return ["https:", "http:"].includes(url.protocol) &&
      !url.username &&
      !url.password
      ? url.href
      : null;
  } catch {
    return null;
  }
};
export const resolveCompany = (
  input: string,
  companies: Company[]
): Company | null => {
  const raw = input.trim();
  const normalized = safeWebUrl(
    /^[a-z][a-z\d+.-]*:/iu.test(raw) ? raw : `https://${raw}`
  );
  if (!normalized) {
    return null;
  }
  const url = new URL(normalized);
  const host = url.hostname.toLowerCase().replace(/^www\./u, "");
  if (host === "ycombinator.com") {
    const slug = /^\/companies\/(?<slug>[a-z\d-]+)\/?$/iu.exec(url.pathname)
      ?.groups?.slug;
    return (
      companies.find((company) => company.slug === slug?.toLowerCase()) ?? null
    );
  }
  return (
    companies.find(
      (company) => host === company.host || host.endsWith(`.${company.host}`)
    ) ?? null
  );
};
