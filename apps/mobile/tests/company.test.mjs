import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { test } from "node:test";

import {
  draftRequest,
  requestItems,
  resolveCompany,
  safeWebUrl,
} from "../src/company/model.ts";

const data = JSON.parse(
  readFileSync(
    new URL(
      "../../../docs/features/20261024.02_first_steps_ui/prototype/data.json",
      import.meta.url
    ),
    "utf-8"
  )
);
test("company URLs resolve by exact website host or actual YC host", () => {
  for (const url of [
    "ploy.ai",
    "https://www.ploy.ai/pricing",
    "https://www.ycombinator.com/companies/ploy?from=directory",
  ]) {
    assert.equal(resolveCompany(url, data.companies)?.slug, "ploy");
  }
  for (const url of [
    "https://evil.example/ycombinator.com/companies/ploy",
    "https://ploy.ai.evil.example",
    `${"java"}script:ploy.ai`,
    "https://user:password@ploy.ai",
    "",
    "https://ycombinator.com/companies/ploy/another",
  ]) {
    assert.equal(resolveCompany(url, data.companies), null);
  }
  assert.equal(safeWebUrl("file:///tmp/source.txt"), null);
  assert.equal(safeWebUrl(`${"java"}script:alert(1)`), null);
});
test("request defaults deduplicate gaps, include stage documents, and defer early closing documents", () => {
  const items = requestItems(data.checklist, "seed", data.research.ploy);
  assert.equal(items.length, new Set(items.map((item) => item.id)).size);
  assert.ok(items.find((item) => item.id === "C02"));
  for (const item of items) {
    const source = data.checklist.find((entry) => entry.id === item.id);
    const fromGap = data.research.ploy.room_gaps.some((gap) =>
      gap.ids.includes(item.id)
    );
    assert.ok(
      fromGap ||
        (source.kind === "document" &&
          source.stages.seed === "yes" &&
          !source.closing_at_early_stage)
    );
  }
  assert.ok(requestItems(data.checklist, "series_a").length > 0);
});
test("draft contains selected items only and reflects corrected company and founder", () => {
  const items = [
    {
      ask: "Send monthly revenue.",
      checked: true,
      guidance: "CSV is fine.",
      id: "one",
      reason: "",
      title: "Revenue",
    },
    {
      ask: "Send contracts.",
      checked: false,
      guidance: "",
      id: "two",
      reason: "",
      title: "Contracts",
    },
  ];
  const draft = draftRequest("Corrected company", "Bryant Chou", items);
  assert.match(draft, /^Hi Bryant,/u);
  assert.match(draft, /Corrected company/u);
  assert.match(draft, /1\. Send monthly revenue\./u);
  assert.match(draft, /CSV is fine\./u);
  assert.doesNotMatch(draft, /Send contracts/u);
});
