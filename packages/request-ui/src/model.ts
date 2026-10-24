export type Stage = "pre_seed" | "seed" | "series_a";
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
export const requestItems = (
  checklist: ChecklistItem[],
  stage: Stage,
  research?: { room_gaps: { text: string; why: string; ids: string[] }[] }
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
