// The Sazabi research the working page shows, from the prototype fixture.
// The readout API (src/readout/api.ts) has no Sazabi room yet, so this is the source for now.
import data from "./fixtures/sazabi-data";

export type Claim = {
  text: string;
  source?: string;
  quote?: string;
  url?: string;
  kind?: string;
  placeholder?: boolean;
  n?: number;
};
export type Gap = { text: string; why: string };
export type Section = {
  key: string;
  title: string;
  parts?: { label: string; claims: Claim[] }[];
  cards?: { name: string; role: string; x?: string; github?: string; claims: Claim[] }[];
  claims?: Claim[];
  gaps?: Gap[];
};
export type Insight = { mark: string; piece: string; title: string; text: string; refs: string[] };
export type ChecklistItem = {
  id: string;
  kind: string;
  title: string;
  item: string;
  ask: string;
  includes?: string;
  stages: Record<string, string>;
  guidance?: { what: string; form: string; good: string[]; path: string };
};
export type Research = {
  slug: string;
  name: string;
  website: string;
  founder: string;
  about: { text: string; refs: string[] };
  insights: Insight[];
  sections: Section[];
  roomGaps: { text: string; why: string; ids: string[] }[];
  checklist: ChecklistItem[];
  sources: Record<string, { url?: string | null; title?: string | null }>;
  room: {
    files: string[];
    holds: Record<string, string[]>;
    partial: { arrived: string[]; answered: string[] };
    full: { arrived: string[]; answered: string[] };
    filesTotal: number;
  };
};

const ORDER = ["The founders", "Comps", "Market signals", "The outside world"];

export function sectionClaims(s: Section): Claim[] {
  if (s.parts) return s.parts.flatMap((p) => p.claims);
  if (s.cards) return s.cards.flatMap((c) => c.claims);
  return s.claims ?? [];
}

function build(): Research {
  const raw = data as unknown as {
    slug: string;
    setup: Record<string, { value: string }>;
    sections: Section[];
    room_gaps: Research["roomGaps"];
    checklist: ChecklistItem[];
    sources: Research["sources"];
    insights: Insight[];
    about: Research["about"];
    room: {
      files: string[];
      holds: Record<string, string[]>;
      partial: Research["room"]["partial"];
      full: Research["room"]["full"];
      files_total: number;
    };
  };
  const rank = (s: Section) => {
    const i = ORDER.indexOf(s.title);
    return i < 0 ? 99 : i;
  };
  const sections: Section[] = JSON.parse(JSON.stringify(raw.sections));
  sections.sort((a, b) => rank(a) - rank(b));
  let n = 0;
  sections.forEach((s) =>
    sectionClaims(s).forEach((c) => {
      if (!c.placeholder) c.n = ++n;
    }),
  );
  return {
    slug: raw.slug,
    name: raw.setup.name.value,
    website: raw.setup.website.value,
    founder: raw.setup.founders.value,
    about: raw.about,
    insights: raw.insights,
    sections,
    roomGaps: raw.room_gaps,
    checklist: raw.checklist,
    sources: raw.sources,
    room: { ...raw.room, filesTotal: raw.room.files_total },
  };
}

export const SAZABI = build();

/** Matches a URL to the research we hold. Sazabi is the only company with cached research. */
export function researchFor(url: string): Research | null {
  const u = url.trim().toLowerCase();
  if (!u) return null;
  return u.includes("sazabi") ? SAZABI : null;
}

export function allClaims(r: Research): Claim[] {
  return r.sections.flatMap(sectionClaims);
}

/** The evidence numbers of the claims whose text contains each ref. */
export function refNums(r: Research, refs: string[]): number[] {
  const claims = allClaims(r).filter((c) => !c.placeholder);
  const nums = refs
    .map((ref) => claims.find((c) => c.text.includes(ref))?.n)
    .filter((x): x is number => typeof x === "number");
  return [...new Set(nums)];
}

export function claimByNum(r: Research, n: number): Claim | undefined {
  return allClaims(r).find((c) => c.n === n);
}
