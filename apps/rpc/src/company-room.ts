import { readFileSync } from "node:fs";

import type { Claim, Source } from "@tricorder/schema";
import type {
  CompanyRoomArrival,
  CompanyRoomStage,
} from "@tricorder/schema/company-room";
import { z } from "zod";

import { CompanyUnavailableError } from "./company-data.ts";

const nonempty = z.string().min(1);
const filePath = nonempty.refine(
  (value) => !value.startsWith("/") && !value.split("/").includes("..")
);
const sourceSchema = z.object({
  locator: nonempty,
  public: nonempty.optional(),
  quote: nonempty.optional(),
  uri: nonempty,
});
const claimSchema = z.object({
  agree: z.array(sourceSchema),
  disagree: z.array(sourceSchema),
  id: nonempty,
  piece: nonempty,
  severity: z.enum(["info", "watch", "flag"]).nullable(),
  sources: z.array(sourceSchema).min(1),
  text: nonempty,
});
const comparisonSchema = z.object({ source: sourceSchema });
const flagSchema = z.object({
  basis: z.enum(["strength", "agreement", "disagreement"]),
  claim_id: nonempty,
  found: comparisonSchema,
  kind: z.enum(["green", "red"]),
  others: z.array(comparisonSchema),
  piece: nonempty,
  stated: comparisonSchema,
  title: nonempty,
  why: nonempty.optional(),
});
const stateSchema = z.object({
  arrived: z.array(filePath),
  files_total: z.number().int().positive(),
  flags: z.object({ green: z.array(nonempty), red: z.array(nonempty) }),
  shown: z.array(nonempty),
  waiting: z.array(z.object({ files: z.array(filePath), piece: nonempty })),
});
const roomSchema = z.object({
  as_of: nonempty,
  claims: z.record(claimSchema),
  drill: z.array(z.object({ gaps: z.array(nonempty) })),
  extra_flags: z.array(flagSchema),
  files: z.array(filePath),
  pieces: z.array(z.object({ label: nonempty, name: nonempty })),
  states: z.object({ full: stateSchema, partial: stateSchema }),
  synthetic_notice: nonempty,
  top_flags: z.object({ green: z.array(flagSchema), red: z.array(flagSchema) }),
});
const snapshotSchema = z.object({
  built: nonempty,
  companies: z.array(
    z.object({ name: nonempty, slug: nonempty, website: nonempty })
  ),
  research: z.record(
    z.object({
      pre: z.record(
        z.object({
          quote: nonempty,
          source: nonempty,
          url: nonempty.optional(),
        })
      ),
      room: roomSchema.optional(),
    })
  ),
  sources: z.record(
    z.object({ id: nonempty, path: nonempty, url: z.string().nullable() })
  ),
});
type Snapshot = z.infer<typeof snapshotSchema>;
type Room = z.infer<typeof roomSchema>;
type RawSource = z.infer<typeof sourceSchema>;
type RawFlag = z.infer<typeof flagSchema>;

const invalid = () => new Error("Invalid saved synthetic room fixture.");
const unique = (values: string[]) => new Set(values).size === values.length;
const fileId = (slug: string, path: string) => `${slug}:synthetic:file:${path}`;
const claimId = (slug: string, id: string) => `${slug}:synthetic:claim:${id}`;
const sourceKey = (source: Source) =>
  JSON.stringify([source.kind, source.uri, source.locator, source.quote]);

export const loadSavedCompanyRoomData = (): unknown =>
  JSON.parse(
    readFileSync(
      new URL(
        "../../../docs/features/20261024.02_first_steps_ui/prototype/data.json",
        import.meta.url
      ),
      "utf-8"
    )
  );

const normalizeSource = (
  snapshot: Snapshot,
  slug: string,
  room: Room,
  source: RawSource
): Source => {
  if (source.public) {
    const entry = snapshot.research[slug].pre[source.public];
    const record = entry && snapshot.sources[entry.source];
    if (!entry || !record) {
      throw invalid();
    }
    const url = entry.url ?? record.url;
    if (url && !/^https?:\/\//u.test(url)) {
      throw invalid();
    }
    return {
      end_s: null,
      kind: url ? "url" : "api",
      locator: record.path,
      quote: entry.quote,
      retrieved_at: null,
      start_s: null,
      uri: url ?? `saved-public:${record.id}`,
    };
  }
  if (!room.files.includes(source.uri) || !source.quote) {
    throw invalid();
  }
  return {
    end_s: null,
    kind: "file",
    locator: source.locator,
    quote: source.quote,
    retrieved_at: null,
    start_s: null,
    uri: source.uri,
  };
};

const validateRoom = (room: Room) => {
  const files = new Set(room.files);
  if (!unique(room.files) || !unique(room.pieces.map((piece) => piece.name))) {
    throw invalid();
  }
  for (const [id, claim] of Object.entries(room.claims)) {
    if (
      id !== claim.id ||
      !room.pieces.some((piece) => piece.name === claim.piece)
    ) {
      throw invalid();
    }
  }
  for (const state of [room.states.partial, room.states.full]) {
    if (
      !unique(state.arrived) ||
      !unique(state.shown) ||
      state.files_total !== files.size
    ) {
      throw invalid();
    }
    if (
      state.arrived.some((file) => !files.has(file)) ||
      state.shown.some((id) => !room.claims[id])
    ) {
      throw invalid();
    }
    for (const waiting of state.waiting) {
      if (waiting.files.some((file) => !files.has(file))) {
        throw invalid();
      }
    }
  }
  if (
    room.states.partial.arrived.some(
      (file) => !room.states.full.arrived.includes(file)
    )
  ) {
    throw invalid();
  }
};

const rawFlagSources = (flag: RawFlag) =>
  [flag.stated, flag.found, ...flag.others].map(
    (comparison) => comparison.source
  );

const collectSources = (snapshot: Snapshot, slug: string, room: Room) => {
  const allFlags = [
    ...room.top_flags.green,
    ...room.top_flags.red,
    ...room.extra_flags,
  ];
  if (!unique(allFlags.map((flag) => flag.claim_id))) {
    throw invalid();
  }
  const flags = new Map(allFlags.map((flag) => [flag.claim_id, flag]));
  for (const flag of allFlags) {
    if (
      !room.claims[flag.claim_id] ||
      room.claims[flag.claim_id].piece !== flag.piece ||
      (flag.kind === "red" && !flag.why)
    ) {
      throw invalid();
    }
  }
  const sources = new Map<string, Source[]>();
  for (const [id, raw] of Object.entries(room.claims)) {
    const refs = [...raw.sources, ...raw.agree, ...raw.disagree];
    const flag = flags.get(id);
    if (flag) {
      refs.push(...rawFlagSources(flag));
    }
    const normalized = refs.map((source) =>
      normalizeSource(snapshot, slug, room, source)
    );
    sources.set(id, [
      ...new Map(
        normalized.map((source) => [sourceKey(source), source])
      ).values(),
    ]);
  }
  return { flags, sources };
};

const categoryFor = (
  flag: RawFlag
): CompanyRoomArrival["flags"][number]["category"] => {
  if (flag.kind === "red") {
    return "red_flag";
  }
  return flag.basis === "strength" ? "strength" : "corroboration";
};

const buildFlags = (
  room: Room,
  stage: CompanyRoomStage,
  slug: string,
  flags: Map<string, RawFlag>,
  claims: Record<string, Claim>
) => {
  const state = room.states[stage];
  const selected: CompanyRoomArrival["flags"] = [];
  for (const kind of ["green", "red"] as const) {
    if (!unique(state.flags[kind])) {
      throw invalid();
    }
    for (const id of state.flags[kind]) {
      const flag = flags.get(id);
      if (!flag || flag.kind !== kind || !state.shown.includes(id)) {
        throw invalid();
      }
      if (!claims[claimId(slug, id)]) {
        continue;
      }
      const piece = room.pieces.find((entry) => entry.name === flag.piece);
      if (!piece) {
        throw invalid();
      }
      selected.push({
        category: categoryFor(flag),
        claimIds: [claimId(slug, id)],
        id: `${slug}:synthetic:flag:${id}`,
        piece: piece.label,
        title: flag.title,
        why: flag.why ?? "",
      });
    }
  }
  return (["strength", "red_flag", "corroboration"] as const).flatMap(
    (category) => selected.filter((flag) => flag.category === category)
  );
};

const buildClaims = (
  room: Room,
  stage: CompanyRoomStage,
  slug: string,
  sourcesByClaim: Map<string, Source[]>
) => {
  const state = room.states[stage];
  const arrived = new Set(state.arrived);
  const waiting = new Map<string, Set<string>>();
  const waitFor = (piece: string, paths: string[]) => {
    const current = waiting.get(piece) ?? new Set<string>();
    for (const path of paths) {
      if (!arrived.has(path)) {
        current.add(fileId(slug, path));
      }
    }
    if (current.size) {
      waiting.set(piece, current);
    }
  };
  for (const entry of state.waiting) {
    waitFor(entry.piece, entry.files);
  }
  const claims: Record<string, Claim> = {};
  for (const [id, raw] of Object.entries(room.claims)) {
    const sources = sourcesByClaim.get(id);
    if (!sources) {
      throw invalid();
    }
    const absent = sources
      .filter((source) => source.kind === "file" && !arrived.has(source.uri))
      .map((source) => source.uri);
    if (absent.length) {
      waitFor(raw.piece, absent);
      continue;
    }
    if (!state.shown.includes(id)) {
      continue;
    }
    const stableId = claimId(slug, id);
    claims[stableId] = {
      check: { kind: "script", model: null, name: "saved-synthetic-replay" },
      confidence: "unverified",
      conflicts_with: [],
      corroborated_by: [],
      id: stableId,
      scan: "saved-synthetic-replay",
      severity: raw.severity,
      sources,
      text: raw.text,
      value: null,
    };
  }
  return {
    claims,
    waiting: [...waiting].map(([piece, ids]) => ({
      fileIds: [...ids],
      piece: room.pieces.find((entry) => entry.name === piece)?.label ?? piece,
    })),
  };
};

/** Replays authored results. It never reads the named room files or reruns a scan. */
export const savedCompanyRoom = (
  data: unknown,
  slug: string,
  stage: CompanyRoomStage
): CompanyRoomArrival => {
  if (stage !== "partial" && stage !== "full") {
    throw invalid();
  }
  const snapshot = snapshotSchema.parse(data);
  const company = snapshot.companies.find((entry) => entry.slug === slug);
  const room = snapshot.research[slug]?.room;
  if (!company || !room) {
    throw new CompanyUnavailableError(
      "No saved synthetic room is available for this company."
    );
  }
  validateRoom(room);
  const { flags, sources } = collectSources(snapshot, slug, room);
  const result = buildClaims(room, stage, slug, sources);
  const arrived = new Set(room.states[stage].arrived);
  const roomId = `${slug}:synthetic:room:v1`;
  return {
    arrivalId: `${roomId}:${stage}`,
    claims: result.claims,
    company,
    files: [...arrived].map((path) => ({ id: fileId(slug, path), path })),
    flags: buildFlags(room, stage, slug, flags, result.claims),
    gaps:
      stage === "full"
        ? [...new Set(room.drill.flatMap((drill) => drill.gaps))].map((gap) =>
            gap.replace(" It was on your request and did not come.", "")
          )
        : [],
    missingFiles: room.files
      .filter((path) => !arrived.has(path))
      .map((path) => ({ id: fileId(slug, path), path })),
    provenance: "saved-synthetic-replay",
    roomId,
    sequence: stage === "partial" ? 1 : 2,
    snapshotAt: snapshot.built,
    stage,
    syntheticNotice: room.synthetic_notice,
    version: 1,
    waiting: result.waiting,
  };
};
