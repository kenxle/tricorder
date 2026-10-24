import assert from "node:assert/strict";
import { test } from "node:test";

import {
  loadSavedCompanyData,
  parseSavedCompanyData,
  savedCompanyReadout,
} from "./company-data.ts";

type Summary = ReturnType<
  typeof parseSavedCompanyData
>["manifest"]["companies"][string]["summary"];

test("summary citations preserve prose and bind pricing to its own source", () => {
  for (const slug of ["ploy", "sazabi"]) {
    const { summary, evidence } = savedCompanyReadout(
      loadSavedCompanyData(),
      slug === "ploy" ? "ploy.ai" : "sazabi.com"
    );
    assert.ok(summary.segments);
    assert.equal(
      summary.segments.map((part) => part.text).join(""),
      summary.text
    );
    assert.deepEqual(
      new Set(summary.segments.flatMap((part) => part.evidenceIds)),
      new Set(summary.evidenceIds)
    );
    const pricing = summary.segments.find((part) =>
      part.text.includes("Plans run")
    );
    assert.deepEqual(pricing?.evidenceIds, [`${slug}:pricing`]);
    for (const part of summary.segments) {
      for (const id of part.evidenceIds) {
        assert.ok(
          evidence[id],
          `${id} must be included in the overview response`
        );
      }
    }
    if (slug === "sazabi") {
      assert.deepEqual(
        summary.segments.find((part) => part.text.includes("usage billed"))
          ?.evidenceIds,
        ["sazabi:usage-pricing"]
      );
    }
  }
});

test("invalid sentence-level attribution cannot reach a readout", () => {
  const mutations = [
    (summary: Summary) => {
      summary.segments[0].text = "Changed research";
    },
    (summary: Summary) => {
      summary.segments[0].evidenceIds = ["sazabi:pricing"];
    },
    (summary: Summary) => {
      summary.segments[0].evidenceIds.push(summary.segments[0].evidenceIds[0]);
    },
    (summary: Summary) => {
      summary.evidenceIds.push("ploy:hn-attention");
    },
    (summary: Summary) => {
      summary.evidenceIds = summary.evidenceIds.filter(
        (id) => id !== "ploy:pricing"
      );
    },
    (summary: Summary) => {
      Reflect.deleteProperty(summary, "segments");
    },
  ];
  for (const mutate of mutations) {
    const data = parseSavedCompanyData(loadSavedCompanyData());
    mutate(data.manifest.companies.ploy.summary);
    assert.throws(() => savedCompanyReadout(data, "ploy.ai"));
  }
});
