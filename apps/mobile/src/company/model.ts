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
export type Stage = "pre_seed" | "seed" | "series_a";
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
export interface ChecklistItem {
  id: string;
  title: string;
  kind: string;
  ask: string;
  includes: string | null;
  stages: Record<string, string>;
  closing_at_early_stage: boolean;
  guidance: {
    what: string;
    form: string;
  } | null;
}
export interface RequestItem {
  id: string;
  title: string;
  ask: string;
  guidance: string;
  reason: string;
  checked: boolean;
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
export const requestItems = (
  checklist: ChecklistItem[],
  stage: Stage,
  research?: Research
): RequestItem[] => {
  const items = new Map<string, RequestItem>();
  for (const gap of research?.room_gaps ?? []) {
    for (const id of gap.ids) {
      const entry = checklist.find((item) => item.id === id);
      if (!entry) {
        continue;
      }
      const current = items.get(id);
      if (current) {
        current.reason += ` ${gap.text}`;
      } else {
        items.set(id, {
          ask: entry.ask,
          checked: true,
          guidance: entry.guidance?.form ?? entry.includes ?? "",
          id,
          reason: gap.text,
          title: entry.title,
        });
      }
    }
  }
  for (const entry of checklist) {
    if (
      entry.kind !== "document" ||
      entry.stages[stage] !== "yes" ||
      (stage !== "series_a" && entry.closing_at_early_stage) ||
      items.has(entry.id)
    ) {
      continue;
    }
    items.set(entry.id, {
      ask: entry.ask,
      checked: true,
      guidance: entry.guidance?.form ?? entry.includes ?? "",
      id: entry.id,
      reason: "First-tier document for this stage",
      title: entry.title,
    });
  }
  return [...items.values()];
};
export const draftRequest = (
  name: string,
  founder: string,
  items: RequestItem[]
): string => {
  const selected = items.filter((item) => item.checked);
  const first = founder.split(",")[0]?.trim().split(/\s+/u)[0];
  return [
    first ? `Hi ${first},` : "Hello,",
    "",
    `Thanks for talking with us about ${name || "your company"}. Before our next meeting, could you share the following in a data room? A rough version is fine. If something does not exist yet, please let us know.`,
    "",
    ...selected.flatMap((item, index) => [
      `${index + 1}. ${item.ask}`,
      ...(item.guidance ? [`   ${item.guidance}`] : []),
    ]),
    "",
    "Thank you.",
  ].join("\n");
};
