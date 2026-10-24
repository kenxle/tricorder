import { readFileSync } from "node:fs";

import { requestItems } from "@tricorder/request-ui/model";
import type {
  CompanyEvidence,
  CompanyReadout,
  CompanySection,
  CompanySectionKey,
  CompanySectionResponse,
} from "@tricorder/schema/company";
import { z } from "zod";

const nonempty = z.string().min(1);
const excerptSchema = z.object({
  after: z.string(),
  before: z.string(),
  match: nonempty,
});
const rowSchema = z.object({
  excerpt: excerptSchema.optional(),
  kind: nonempty.optional(),
  placeholder: z.boolean().optional(),
  quote: nonempty.optional(),
  source: nonempty.optional(),
  text: nonempty,
  url: nonempty.optional(),
});
const gapSchema = z.object({ text: nonempty, why: nonempty });
const sectionKeySchema = z.enum(["founders", "comps", "signals", "outside"]);
const sectionSchema = z.object({
  cards: z
    .array(
      z.object({ claims: z.array(rowSchema), name: nonempty, role: z.string() })
    )
    .optional(),
  claims: z.array(rowSchema).optional(),
  gaps: z.array(gapSchema).optional(),
  key: sectionKeySchema,
  parts: z
    .array(z.object({ claims: z.array(rowSchema), label: nonempty }))
    .optional(),
  title: nonempty,
});
const snapshotSchema = z.object({
  built: nonempty,
  checklist: z.array(
    z.object({
      ask: z.string(),
      closing_at_early_stage: z.boolean(),
      guidance: z.object({ form: z.string(), what: z.string() }).nullable(),
      id: nonempty,
      includes: z.string().nullable(),
      kind: nonempty,
      stages: z.record(z.string()),
      title: nonempty,
    })
  ),
  companies: z.array(
    z.object({
      host: nonempty,
      name: nonempty,
      slug: nonempty,
      website: nonempty,
    })
  ),
  research: z.record(
    z.object({
      room_gaps: z.array(gapSchema.extend({ ids: z.array(nonempty) })),
      sections: z.array(sectionSchema),
      setup: z.record(z.object({ value: z.string() })),
    })
  ),
  sources: z.record(
    z.object({
      id: nonempty,
      path: nonempty,
      title: nonempty,
      url: z.string().nullable(),
    })
  ),
});
const narrativeSegmentSchema = z.object({
  evidenceIds: z.array(nonempty).min(1),
  text: nonempty,
});
const narrativeSchema = z.object({
  evidenceIds: z.array(nonempty).min(1),
  provenance: z.literal("authored-demo"),
  segments: z.array(narrativeSegmentSchema).min(1).optional(),
  text: nonempty,
});
const manifestSchema = z.object({
  companies: z.record(
    z.object({
      evidence: z.array(
        z.object({
          id: nonempty,
          number: z.number().int().positive(),
          quote: nonempty,
          source: nonempty,
        })
      ),
      insights: z.array(
        narrativeSchema.extend({
          id: nonempty,
          mark: z.enum(["strong", "weak", "mixed", "thin"]),
          piece: nonempty,
          title: nonempty,
        })
      ),
      summary: narrativeSchema.extend({
        segments: z.array(narrativeSegmentSchema).min(1),
      }),
    })
  ),
  version: z.literal(1),
});
type Snapshot = z.infer<typeof snapshotSchema>;
type Manifest = z.infer<typeof manifestSchema>;
type ResearchRow = z.infer<typeof rowSchema>;
type RawSection = z.infer<typeof sectionSchema>;
export interface SavedCompanyData {
  snapshot: unknown;
  manifest: unknown;
}
export class CompanyUnavailableError extends Error {
  override name = "CompanyUnavailableError";
}
const invalidFixture = () => new Error("Invalid saved company fixture.");
export const loadSavedCompanyData = (): SavedCompanyData => ({
  manifest: JSON.parse(
    readFileSync(
      new URL("company-data/manifest.json", import.meta.url),
      "utf-8"
    )
  ),
  snapshot: JSON.parse(
    readFileSync(
      new URL(
        "../../../docs/features/20261024.02_first_steps_ui/prototype/data.json",
        import.meta.url
      ),
      "utf-8"
    )
  ),
});
const webURL = (value: string): URL | null => {
  try {
    const url = new URL(value);
    return ["http:", "https:"].includes(url.protocol) &&
      !url.username &&
      !url.password
      ? url
      : null;
  } catch {
    return null;
  }
};
const companyFromURL = (input: string, snapshot: Snapshot) => {
  const value = input.trim();
  const url = webURL(
    /^[a-z][a-z\d+.-]*:/iu.test(value) ? value : `https://${value}`
  );
  if (!url || !value) {
    return;
  }
  const host = url.hostname.toLowerCase().replace(/^www\./u, "");
  if (host === "ycombinator.com") {
    const match = /^\/companies\/(?<slug>[a-z\d-]+)\/?$/iu.exec(url.pathname);
    return snapshot.companies.find(
      (company) => company.slug === match?.groups?.slug?.toLowerCase()
    );
  }
  return snapshot.companies.find((company) => host === company.host);
};
const rawGroups = (section: RawSection) =>
  section.parts?.map((part) => ({
    claims: part.claims,
    subtitle: "",
    title: part.label,
  })) ??
  section.cards?.map((card) => ({
    claims: card.claims,
    subtitle: card.role,
    title: card.name,
  })) ?? [{ claims: section.claims ?? [], subtitle: "", title: "" }];
const rowKey = (row: { source?: string; quote?: string }) =>
  JSON.stringify([row.source, row.quote]);
const sectionOrder: CompanySectionKey[] = [
  "founders",
  "comps",
  "signals",
  "outside",
];
const confidenceFor = (kind: string | undefined) => {
  if (kind === "unconfirmed") {
    return "unverified";
  }
  if (kind === "match") {
    return "judged";
  }
  return "quoted";
};
const validateNarratives = (
  authored: Manifest["companies"][string],
  evidence: Record<string, CompanyEvidence>,
  slug: string
) => {
  const narratives = [authored.summary, ...authored.insights];
  for (const narrative of narratives) {
    if (
      narrative.evidenceIds.some((id) => !evidence[id]) ||
      new Set(narrative.evidenceIds).size !== narrative.evidenceIds.length
    ) {
      throw invalidFixture();
    }
    if (narrative.segments) {
      const ids = new Set(
        narrative.segments.flatMap((part) => part.evidenceIds)
      );
      if (
        narrative.segments.map((part) => part.text).join("") !==
          narrative.text ||
        ids.size !== narrative.evidenceIds.length ||
        narrative.evidenceIds.some((id) => !ids.has(id)) ||
        narrative.segments.some(
          (part) =>
            new Set(part.evidenceIds).size !== part.evidenceIds.length ||
            part.evidenceIds.some((id) => !evidence[id])
        )
      ) {
        throw invalidFixture();
      }
    }
  }
  if (
    new Set(authored.insights.map((entry) => entry.id)).size !==
      authored.insights.length ||
    authored.insights.some((entry) => !entry.id.startsWith(`${slug}:`))
  ) {
    throw invalidFixture();
  }
};
const buildCompany = (snapshot: Snapshot, manifest: Manifest, slug: string) => {
  const company = snapshot.companies.find((entry) => entry.slug === slug);
  const research = snapshot.research[slug];
  const authored = manifest.companies[slug];
  if (!company || !research || !authored) {
    throw new CompanyUnavailableError(
      "No saved public research is available for this company."
    );
  }
  if (
    snapshot.companies.filter((entry) => entry.slug === slug).length !== 1 ||
    !webURL(company.website)
  ) {
    throw invalidFixture();
  }
  const identity = {
    name: company.name,
    slug: company.slug,
    website: company.website,
  };
  const bindings = new Map<string, (typeof authored.evidence)[number]>();
  const ids = new Set<string>();
  const numbers = new Set<number>();
  for (const binding of authored.evidence) {
    if (
      !binding.id.startsWith(`${slug}:`) ||
      ids.has(binding.id) ||
      numbers.has(binding.number) ||
      bindings.has(rowKey(binding))
    ) {
      throw invalidFixture();
    }
    ids.add(binding.id);
    numbers.add(binding.number);
    bindings.set(rowKey(binding), binding);
  }
  const evidence: Record<string, CompanyEvidence> = {};
  const convertRow = (row: ResearchRow): string => {
    const binding = bindings.get(rowKey(row));
    const source = row.source ? snapshot.sources[row.source] : undefined;
    if (
      !binding ||
      !source ||
      source.id !== row.source ||
      !row.quote ||
      evidence[binding.id] ||
      row.excerpt?.match !== row.quote
    ) {
      throw invalidFixture();
    }
    const sourceURL = row.url ?? source.url;
    if (sourceURL && !webURL(sourceURL)) {
      throw invalidFixture();
    }
    evidence[binding.id] = {
      claim: {
        check: {
          kind: "script",
          model: null,
          name: "saved-public-research-adapter",
        },
        confidence: confidenceFor(row.kind),
        conflicts_with: [],
        corroborated_by: [],
        id: binding.id,
        scan: "saved-public-research",
        severity: "info",
        sources: [
          {
            end_s: null,
            kind: sourceURL ? "url" : "file",
            locator: "saved excerpt",
            quote: row.quote,
            retrieved_at: null,
            start_s: null,
            uri: sourceURL ?? source.path,
          },
        ],
        text: row.text,
        value: null,
      },
      excerpt: row.excerpt ?? null,
      id: binding.id,
      number: binding.number,
      qualification: row.kind ?? null,
      sourceId: source.id,
      sourceTitle: source.title,
    };
    return binding.id;
  };
  const sections = new Map<CompanySectionKey, CompanySection>();
  for (const section of research.sections) {
    if (sections.has(section.key)) {
      throw invalidFixture();
    }
    const groupIDs = new Set<string>();
    const groups = rawGroups(section).map((group) => {
      const id = `${slug}:${section.key}:${encodeURIComponent(group.title || section.key)}`;
      if (groupIDs.has(id)) {
        throw invalidFixture();
      }
      groupIDs.add(id);
      return {
        evidenceIds: group.claims
          .filter((row) => !row.placeholder)
          .map(convertRow),
        id,
        subtitle: group.subtitle,
        title: group.title,
        unavailable: group.claims
          .filter((row) => row.placeholder)
          .map((row) => row.text),
      };
    });
    sections.set(section.key, {
      gaps: section.gaps ?? [],
      groups,
      key: section.key,
      title: section.title,
    });
  }
  if (
    Object.keys(evidence).length !== bindings.size ||
    sectionOrder.some((key) => !sections.has(key))
  ) {
    throw invalidFixture();
  }
  validateNarratives(authored, evidence, slug);
  return { authored, company: identity, evidence, research, sections };
};
const selectEvidence = (
  evidence: Record<string, CompanyEvidence>,
  ids: string[]
) => Object.fromEntries([...new Set(ids)].map((id) => [id, evidence[id]]));
export const parseSavedCompanyData = (data: SavedCompanyData) => ({
  manifest: manifestSchema.parse(data.manifest),
  snapshot: snapshotSchema.parse(data.snapshot),
});
export const savedCompanyReadout = (
  data: SavedCompanyData,
  input: string
): CompanyReadout => {
  const { snapshot, manifest } = parseSavedCompanyData(data);
  const identity = companyFromURL(input, snapshot);
  if (!identity) {
    throw new CompanyUnavailableError(
      "This URL does not match a company with saved public research."
    );
  }
  const { company, research, authored, evidence, sections } = buildCompany(
    snapshot,
    manifest,
    identity.slug
  );
  const stage = research.setup.stage?.value;
  const defaultStage =
    stage === "pre_seed" || stage === "series_a" ? stage : "seed";
  return {
    company,
    evidence: selectEvidence(
      evidence,
      [authored.summary, ...authored.insights].flatMap(
        (entry) => entry.evidenceIds
      )
    ),
    insights: authored.insights,
    provenance: "saved-public-research",
    request: {
      defaultStage,
      founder: research.setup.founders?.value ?? "",
      itemsByStage: {
        pre_seed: requestItems(snapshot.checklist, "pre_seed", research),
        seed: requestItems(snapshot.checklist, "seed", research),
        series_a: requestItems(snapshot.checklist, "series_a", research),
      },
    },
    roomGaps: research.room_gaps,
    sections: sectionOrder.map((key) => {
      const section = sections.get(key);
      if (!section) {
        throw invalidFixture();
      }
      return { key, title: section.title };
    }),
    snapshotAt: snapshot.built,
    summary: authored.summary,
    version: 1,
  };
};
export const savedCompanySection = (
  data: SavedCompanyData,
  slug: string,
  key: CompanySectionKey
): CompanySectionResponse => {
  const { snapshot, manifest } = parseSavedCompanyData(data);
  const { company, sections, evidence } = buildCompany(
    snapshot,
    manifest,
    slug
  );
  const section = sections.get(key);
  if (!section) {
    throw new CompanyUnavailableError("This research section is unavailable.");
  }
  return {
    company,
    evidence: selectEvidence(
      evidence,
      section.groups.flatMap((group) => group.evidenceIds)
    ),
    provenance: "saved-public-research",
    section,
    snapshotAt: snapshot.built,
    version: 1,
  };
};
