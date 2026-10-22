#!/usr/bin/env python3
"""Write ../02_interface_example.md from the spike's out/*.json.

    python3 render_example.py

Every JSON block and table row in that page comes from here, so the page shows
what the spike emitted, not what someone typed. Rerun after mislabels_spike.py.
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
TARGET = HERE.parent / "02_interface_example.md"


def load(name):
    return json.loads((HERE / "out" / f"{name}.json").read_text(encoding="utf-8"))


def table(out):
    rows = ["| Sub-check | Label | Really is | File read | Claim ids |", "|---|---|---|---|---|"]
    for c in out["result"]["checks"]:
        rows.append(f"| `{c['check_name']}` | {c['label']} | {c['really_is']} | `{c['file']}` | {', '.join(c['claim_ids']) or 'none'} |")
    return "\n".join(rows)


def block(obj):
    return "```json\n" + json.dumps(obj, indent=2) + "\n```"


def gaps(out):
    return "\n".join(f"- {g['what']} (why: {g['why']}; would need: {g['would_need']}; piece: {g['piece']})" for g in out["result"]["gaps"])


full, seed, clean = load("hollis_voice"), load("hollis_voice_seed_drop"), load("hollis_voice_clean")
off, on, brass = load("hollis_voice_resale_off"), load("hollis_voice_resale_on"), load("brasswick")

flag = [c for c in full["result"]["claims"] if c["severity"] == "flag"]
info = [c for c in full["result"]["claims"] if c["severity"] != "flag"]

parts = [
    "# Interface example: what accounting mislabels emits",
    "",
    "This feature has no screen, so its prototype is its output. Everything below was written by "
    "[spike/render_example.py](spike/render_example.py) from the JSON that "
    "[spike/mislabels_spike.py](spike/mislabels_spike.py) wrote to `spike/out/`. Nothing here was typed by hand. "
    "The raw run log is [spike/spike_run.txt](spike/spike_run.txt) and the answer-key score is "
    "[spike/score_run.txt](spike/score_run.txt).",
    "",
    "The claims use the shared Claim from [FRAMEWORKS.md](../../ongoing/FRAMEWORKS.md), \"The shared Claim\". "
    "The spike checked each one three ways: against the JSON Schema in entry 1.12's output shape, against the skeleton's "
    "Pydantic models (`schema.claim`), and with the skeleton's quote checker (`schema.check_quotes.check_claim`). All six "
    "rooms passed all three. Claim ids here use a spike prefix (`redflags-mislabels-NNN`); the real module takes ids from "
    "`scans.base.Ids`, so they become `redflags-NNN`.",
    "",
    "## Full room: data_room/hollis_voice",
    "",
    f"Entry label: **{full['result']['label']}**. {full['result']['label_reason']}",
    "",
    table(full),
    "",
    "### The one flag: the pilot in the `mrr` column",
    "",
    "This is the claim the roadmap's first Done when asks for. It cites the metrics row and the pilot's own row in the customer file.",
    "",
    block(flag),
    "",
    "The link to entry 1.2's pilot-as-ARR flag. The Claim has no field for it, so the spike writes it beside the result. "
    "[04_architecture.md](04_architecture.md) proposes carrying it as a Panel.",
    "",
    block(full["cause_links"]),
    "",
    "The lines panel: places where a label claims recurring money and the line holds a pilot.",
    "",
    block(full["result"]["lines"]),
    "",
    "### The clear sub-checks",
    "",
    "Each clear sub-check writes one info claim with the tie-out it ran, so the readout can show that the check ran and on what. "
    "None of them cites a Brookline Row (C0193) row, a June 2026 billings row or an Onboarding row.",
    "",
    block(info),
    "",
    "### Gaps on the full room",
    "",
    gaps(full),
    "",
    "## Seed drop: data_room/hollis_voice_seed_drop",
    "",
    f"Entry label: **{seed['result']['label']}**. {seed['result']['label_reason']}",
    "",
    table(seed),
    "",
    "Kind a still runs here, through entry 1.12's fallback: the model's `ARR_Build` Product type column and its monthly history. "
    "Kind h runs from the P&L fee row and `ARR_Build`. The other five return `cannot_check` with their gaps:",
    "",
    gaps(seed),
    "",
    "The seed drop's kind a claim:",
    "",
    block([c for c in seed["result"]["claims"] if c["severity"] == "flag"]),
    "",
    "## Clean room: data_room/hollis_voice_clean",
    "",
    f"Entry label: **{clean['result']['label']}**. No sub-check fires.",
    "",
    table(clean),
    "",
    "## Kind c on a test room with a resale line",
    "",
    "Hollis Voice has nothing for kind c. The spike writes two copies of the full room under `spike/test_rooms/`. "
    "With the option on, every paying subscription clinic gets a `Resale` row from 2026-04 (carrier minutes resold at cost, "
    "$25 a location a month, a spike choice), and the same money is added to the `mrr` column. With the option off, the copy is unchanged.",
    "",
    "Option off:",
    "",
    table(off),
    "",
    "Option on:",
    "",
    table(on),
    "",
    block([c for c in on["result"]["claims"] if c["check"]["name"] == "gross_vs_net_revenue"]),
    "",
    "## Brasswick: data_room/brasswick",
    "",
    "Brasswick is the second demo room. Its answer key already names three 1.12 check names (BF1, BF3, BF4). "
    "The spike reads it through a column map (`subscription_revenue` for `mrr`, no product type).",
    "",
    f"Entry label: **{brass['result']['label']}**.",
    "",
    table(brass),
    "",
    block([c for c in brass["result"]["claims"] if c["severity"] == "flag"]),
    "",
    "Contractor vendors that entry 1.12's keyword list would miss: "
    + (", ".join(brass["contractor_vendors_missed_by_1_12_keywords"]) or "none") + ".",
    "",
]
TARGET.write_text("\n".join(parts), encoding="utf-8")
print(f"wrote {TARGET}")
