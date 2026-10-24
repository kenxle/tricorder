import assert from "node:assert/strict";
import { once } from "node:events";
import { test } from "node:test";
import type { TestContext } from "node:test";

import {
  CompanyUnavailableError,
  loadSavedCompanyData,
  parseSavedCompanyData,
  savedCompanyReadout,
  savedCompanySection,
} from "./company-data.ts";
import type { SavedCompanyData } from "./company-data.ts";
import { createRPCServer } from "./server.ts";

const mutableFixture = () => parseSavedCompanyData(loadSavedCompanyData());
for (const slug of ["ploy", "sazabi"]) {
  test(`${slug}: website and YC URL produce the same sourced overview`, () => {
    const data = loadSavedCompanyData();
    const website =
      slug === "ploy"
        ? "https://www.ploy.ai/pricing"
        : "https://www.sazabi.com/";
    const readout = savedCompanyReadout(data, website);
    assert.deepEqual(
      readout,
      savedCompanyReadout(
        data,
        `https://www.ycombinator.com/companies/${slug}?from=directory`
      )
    );
    assert.equal(readout.company.slug, slug);
    assert.equal(readout.provenance, "saved-public-research");
    assert.equal(readout.snapshotAt, "2026-10-24T13:40:37");
    assert.deepEqual(
      readout.sections.map((section) => section.key),
      ["founders", "comps", "signals", "outside"]
    );
    assert.equal(readout.summary.provenance, "authored-demo");
    for (const narrative of [readout.summary, ...readout.insights]) {
      assert.ok(narrative.evidenceIds.length);
      for (const id of narrative.evidenceIds) {
        const evidence = readout.evidence[id];
        assert.ok(evidence);
        assert.equal(evidence.claim.id, id);
        assert.ok(id.startsWith(`${slug}:`));
        assert.equal(evidence.claim.sources[0].quote, evidence.excerpt?.match);
        assert.equal(evidence.claim.sources[0].retrieved_at, null);
      }
    }
    assert.ok(readout.request.itemsByStage.seed.length);
    assert.equal(
      new Set(readout.request.itemsByStage.seed.map((item) => item.id)).size,
      readout.request.itemsByStage.seed.length
    );
    assert.ok(!JSON.stringify(readout).includes('"room":'));
    assert.ok(!JSON.stringify(readout).includes('"synthetic_notice":'));
  });
  test(`${slug}: independently loaded sections contain only their own evidence and keep placeholders separate`, () => {
    const data = loadSavedCompanyData();
    const sections = ["founders", "comps", "signals", "outside"] as const;
    const seen = new Set<string>();
    for (const key of sections) {
      const response = savedCompanySection(data, slug, key);
      assert.equal(response.company.slug, slug);
      assert.equal(response.section.key, key);
      const ids = response.section.groups.flatMap((group) => group.evidenceIds);
      assert.deepEqual(new Set(Object.keys(response.evidence)), new Set(ids));
      for (const id of ids) {
        assert.ok(!seen.has(id));
        seen.add(id);
        assert.ok(response.evidence[id].claim.sources[0].quote);
      }
    }
    const comps = savedCompanySection(data, slug, "comps");
    assert.ok(comps.section.groups.some((group) => group.unavailable.length));
    assert.ok(comps.section.gaps.length);
  });
}
test("reordering raw rows and company directory does not change evidence identity or authored references", () => {
  const data = mutableFixture();
  const before = savedCompanyReadout(data, "ploy.ai");
  data.snapshot.companies.reverse();
  data.snapshot.research.ploy.sections.reverse();
  for (const section of data.snapshot.research.ploy.sections) {
    section.claims?.reverse();
    section.parts?.reverse();
    section.cards?.reverse();
    for (const group of [...(section.parts ?? []), ...(section.cards ?? [])]) {
      group.claims.reverse();
    }
  }
  assert.deepEqual(savedCompanyReadout(data, "ploy.ai"), before);
});
test("unknown, deceptive and credential-bearing URLs never substitute saved research", () => {
  const data = loadSavedCompanyData();
  for (const url of [
    "",
    "https://unknown.example",
    "https://ploy.ai.evil.example",
    "https://evil.example/ycombinator.com/companies/ploy",
    "https://user:secret@ploy.ai",
    "file:///ploy.ai",
    "https://ycombinator.com/companies/ploy/other",
    "https://subdomain.ploy.ai",
  ]) {
    assert.throws(
      () => savedCompanyReadout(data, url),
      CompanyUnavailableError
    );
  }
  assert.equal(savedCompanyReadout(data, "ploy.ai").company.slug, "ploy");
  const missing = mutableFixture();
  delete missing.snapshot.research.ploy;
  assert.throws(
    () => savedCompanyReadout(missing, "ploy.ai"),
    CompanyUnavailableError
  );
  assert.throws(
    () => savedCompanySection(data, "missing", "founders"),
    CompanyUnavailableError
  );
});
test("fixture validation rejects stale, duplicate, missing, unsafe and cross-company evidence", () => {
  const mutateCases = [
    (data: ReturnType<typeof mutableFixture>) => {
      data.manifest.companies.ploy.summary.evidenceIds[0] = "sazabi:pricing";
    },
    (data: ReturnType<typeof mutableFixture>) => {
      data.manifest.companies.ploy.evidence[0].quote =
        "not in the saved fixture";
    },
    (data: ReturnType<typeof mutableFixture>) => {
      data.manifest.companies.ploy.evidence[1].id =
        data.manifest.companies.ploy.evidence[0].id;
    },
    (data: ReturnType<typeof mutableFixture>) => {
      data.manifest.companies.ploy.evidence[1].number =
        data.manifest.companies.ploy.evidence[0].number;
    },
    (data: ReturnType<typeof mutableFixture>) => {
      delete data.snapshot.sources.site_ploy_pricing;
    },
    (data: ReturnType<typeof mutableFixture>) => {
      data.snapshot.sources.site_ploy_pricing.url = `${"java"}script:alert(1)`;
    },
    (data: ReturnType<typeof mutableFixture>) => {
      const row = data.snapshot.research.ploy.sections[0].parts?.[0].claims[0];
      assert.ok(row?.excerpt);
      row.excerpt.match = "incorrect quote";
    },
  ];
  for (const mutate of mutateCases) {
    const data = mutableFixture();
    mutate(data);
    assert.throws(() => savedCompanyReadout(data, "ploy.ai"));
  }
});
test("qualification preserves unconfirmed identity and absence of signals", () => {
  const data = loadSavedCompanyData();
  const founders = savedCompanySection(data, "ploy", "founders");
  assert.equal(
    founders.evidence["ploy:github-unconfirmed"].qualification,
    "unconfirmed"
  );
  assert.equal(
    founders.evidence["ploy:github-unconfirmed"].claim.confidence,
    "unverified"
  );
  const outside = savedCompanySection(data, "sazabi", "outside");
  assert.equal(
    outside.evidence["sazabi:form-d-search"].qualification,
    "no signal"
  );
});
const serve = async (t: TestContext, companyData?: () => SavedCompanyData) => {
  const server = createRPCServer({
    apiURL: "http://127.0.0.1:8787",
    companyData,
  });
  const listening = once(server, "listening");
  server.listen(0, "127.0.0.1");
  await listening;
  t.after(async () => {
    const closed = once(server, "close");
    server.closeAllConnections();
    server.close();
    await closed;
  });
  const address = server.address();
  assert.ok(address && typeof address === "object");
  return `http://127.0.0.1:${address.port}`;
};
test("company HTTP endpoints validate queries, guard origins, and return contract responses", async (t) => {
  const origin = await serve(t);
  const overview = await fetch(`${origin}/company/readout?url=ploy.ai`);
  assert.equal(overview.status, 200);
  assert.equal(overview.headers.get("cache-control"), "no-store");
  const overviewBody = await overview.json();
  assert.equal(overviewBody.company.slug, "ploy");
  const section = await fetch(
    `${origin}/company/section?company=sazabi&section=founders`
  );
  assert.equal(section.status, 200);
  const sectionBody = await section.json();
  assert.equal(sectionBody.section.key, "founders");
  const invalidPaths = [
    "/company/readout",
    "/company/readout?url=",
    "/company/readout?url=ploy.ai&url=sazabi.com",
    "/company/readout?url=ploy.ai&extra=1",
    `/company/readout?url=${"a".repeat(2049)}`,
    "/company/section?company=ploy&section=unknown",
    "/company/section?company=../ploy&section=outside",
  ];
  await Promise.all(
    invalidPaths.map(async (path) => {
      const response = await fetch(origin + path);
      assert.equal(response.status, 400, path);
    })
  );
  const missing = await fetch(`${origin}/company/readout?url=unknown.example`);
  assert.equal(missing.status, 404);
  const post = await fetch(`${origin}/company/readout?url=ploy.ai`, {
    method: "POST",
  });
  assert.equal(post.status, 405);
  const foreignHeaders: Record<string, string>[] = [
    { origin: "https://evil.example" },
    { referer: "https://evil.example" },
    { "sec-fetch-site": "cross-site" },
  ];
  await Promise.all(
    foreignHeaders.map(async (headers) => {
      const response = await fetch(`${origin}/company/readout?url=ploy.ai`, {
        headers,
      });
      assert.equal(response.status, 403);
    })
  );
});
test("fixture failure returns a retryable 503 without internal details", async (t) => {
  const origin = await serve(t, () => {
    throw new Error("private filename and stack");
  });
  const response = await fetch(`${origin}/company/readout?url=ploy.ai`);
  assert.equal(response.status, 503);
  const body = await response.json();
  assert.match(body.detail, /unavailable/u);
  assert.doesNotMatch(body.detail, /private/u);
});
