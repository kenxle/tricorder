import assert from "node:assert/strict";
import { test } from "node:test";

import { CompanyUnavailableError } from "./company-data.ts";
import { loadSavedCompanyRoomData, savedCompanyRoom } from "./company-room.ts";

const fixture = () =>
  loadSavedCompanyRoomData() as {
    research: Record<
      string,
      {
        room: {
          claims: Record<
            string,
            { sources: { uri: string; locator: string; quote: string }[] }
          >;
          states: {
            partial: {
              shown: string[];
              arrived: string[];
              flags: { green: string[]; red: string[] };
            };
          };
          top_flags: { red: { why?: string }[] };
        };
      }
    >;
  };

for (const company of ["ploy", "sazabi"]) {
  test(`${company}: partial and full arrivals retain stable identities, company isolation and provenance`, () => {
    const data = loadSavedCompanyRoomData();
    const partial = savedCompanyRoom(data, company, "partial");
    const full = savedCompanyRoom(data, company, "full");
    assert.equal(partial.company.slug, company);
    assert.equal(partial.roomId, full.roomId);
    assert.notEqual(partial.arrivalId, full.arrivalId);
    assert.equal(partial.sequence, 1);
    assert.equal(full.sequence, 2);
    assert.deepEqual(full, savedCompanyRoom(data, company, "full"));
    assert.equal(full.provenance, "saved-synthetic-replay");
    assert.match(full.syntheticNotice, /Not this company's data/u);
    assert.ok(partial.files.length < full.files.length);
    assert.equal(full.missingFiles.length, 0);
    assert.equal(full.waiting.length, 0);
    for (const file of partial.files) {
      assert.ok(
        full.files.some(
          (entry) => entry.id === file.id && entry.path === file.path
        )
      );
    }
    for (const arrival of [partial, full]) {
      const paths = new Set(arrival.files.map((file) => file.path));
      for (const [id, claim] of Object.entries(arrival.claims)) {
        assert.ok(id.startsWith(`${company}:synthetic:claim:`));
        assert.equal(id, claim.id);
        assert.equal(claim.confidence, "unverified");
        assert.ok(claim.sources.length);
        for (const source of claim.sources) {
          assert.ok(source.quote);
          if (source.kind === "file") {
            assert.ok(paths.has(source.uri));
          }
        }
      }
      for (const flag of arrival.flags) {
        for (const id of flag.claimIds) {
          assert.ok(arrival.claims[id]);
        }
        if (flag.category === "red_flag") {
          assert.ok(flag.why);
        }
      }
      const categories = arrival.flags.map((flag) => flag.category);
      assert.deepEqual(
        categories,
        ["strength", "red_flag", "corroboration"].flatMap((category) =>
          categories.filter((entry) => entry === category)
        )
      );
      for (const wait of arrival.waiting) {
        for (const id of wait.fileIds) {
          assert.ok(arrival.missingFiles.some((file) => file.id === id));
        }
      }
    }
  });
}

test("partial states withhold later findings even when prototype shown list is overinclusive", () => {
  const data = loadSavedCompanyRoomData();
  for (const slug of ["ploy", "sazabi"]) {
    const partial = savedCompanyRoom(data, slug, "partial");
    const full = savedCompanyRoom(data, slug, "full");
    for (const id of ["tr-3", "bu-2"]) {
      assert.equal(partial.claims[`${slug}:synthetic:claim:${id}`], undefined);
      assert.ok(full.claims[`${slug}:synthetic:claim:${id}`]);
    }
  }
  const raw = fixture();
  raw.research.ploy.room.states.partial.shown.push("tr-3");
  assert.equal(
    savedCompanyRoom(raw, "ploy", "partial").claims[
      "ploy:synthetic:claim:tr-3"
    ],
    undefined
  );
});

test("flag evidence retains exact saved public quotes and synthetic comparisons", () => {
  const result = savedCompanyRoom(loadSavedCompanyRoomData(), "ploy", "full");
  const claim = result.claims["ploy:synthetic:claim:lc-1"];
  assert.ok(
    claim.sources.some(
      (source) =>
        source.kind === "url" &&
        source.quote === "<totalAmountSold>26571989</totalAmountSold>"
    )
  );
  assert.ok(
    claim.sources.some(
      (source) => source.kind === "file" && source.quote === "26571989"
    )
  );
});

test("invalid file, claim, duplicate arrival and missing why references fail closed", () => {
  const changes = [
    (data: ReturnType<typeof fixture>) => {
      data.research.ploy.room.claims["tr-1"].sources[0].uri =
        "../other-company.pdf";
    },
    (data: ReturnType<typeof fixture>) => {
      data.research.ploy.room.states.partial.shown.push("missing-claim");
    },
    (data: ReturnType<typeof fixture>) => {
      data.research.ploy.room.states.partial.arrived.push(
        data.research.ploy.room.states.partial.arrived[0]
      );
    },
    (data: ReturnType<typeof fixture>) => {
      data.research.ploy.room.states.partial.flags.red.push("lc-1");
    },
    (data: ReturnType<typeof fixture>) => {
      delete data.research.ploy.room.top_flags.red[0].why;
    },
  ];
  for (const change of changes) {
    const data = fixture();
    change(data);
    assert.throws(() => savedCompanyRoom(data, "ploy", "partial"));
  }
});

test("unsupported company never gets another company's synthetic room", () => {
  assert.throws(
    () => savedCompanyRoom(loadSavedCompanyRoomData(), "armature", "full"),
    CompanyUnavailableError
  );
});

test("full replay preserves unresolved gaps without pretending a request was sent", () => {
  for (const slug of ["ploy", "sazabi"]) {
    const data = loadSavedCompanyRoomData();
    assert.deepEqual(savedCompanyRoom(data, slug, "partial").gaps, []);
    const full = savedCompanyRoom(data, slug, "full");
    assert.ok(full.gaps.length);
    assert.ok(full.gaps.every((gap) => gap.startsWith("Not in the room:")));
    assert.ok(full.gaps.every((gap) => !gap.includes("on your request")));
  }
});
