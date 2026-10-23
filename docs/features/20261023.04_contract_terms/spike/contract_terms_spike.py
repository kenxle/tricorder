"""Spike for contract-terms: run the real reader and checks on the rooms and test rooms,
write their JSON to spike/out/, and render 02_interface_example.md from it.

    python3 docs/features/20261023.04_contract_terms/spike/contract_terms_spike.py

Test rooms are built in a scratch folder (TMPDIR) from data_room/hollis_voice with the
made-up test contracts in scans/redflags/tests/contract_fixtures.py. data_room/ is never written.
"""

from __future__ import annotations

import json
import shutil
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT))

from schema.check_quotes import check_claim  # noqa: E402
from scans.base import Ids  # noqa: E402
from scans.redflags import contract_terms_full  # noqa: E402
from scans.redflags.tests.contract_fixtures import (  # noqa: E402
    CHANGE_OF_CONTROL, HOLLIS, ONE_YEAR, THIRTY_DAY, a_counted_customer, copy_room, one_year_from, order_form, write_pdf,
)

OUT = HERE / "out"


def run(name: str, room: Path, only: str | None = None) -> dict:
    claims, gaps, panels = contract_terms_full.check(room, Ids("redflags"))
    bad = {c.id: check_claim(c, room)[1] for c in claims if check_claim(c, room)[1]}
    data = {"room": name, "claims": [c.model_dump(exclude_none=True) for c in claims],
            "gaps": [g.model_dump(exclude_none=True) for g in gaps], "panels": [p.model_dump() for p in panels],
            "quote_check": {"claims": len(claims), "failed": bad}}
    if only:
        data["claims"] = [c for c in data["claims"] if any(s["uri"] == only for s in c["sources"])]
        data["panels"] = [{**p, "rows": [r for r in p["rows"] if r[0] == only]} for p in data["panels"]]
    (OUT / f"{name}.json").write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    return data


def main() -> None:
    OUT.mkdir(exist_ok=True)
    tmp = Path(tempfile.mkdtemp(prefix="contract_terms_spike_"))
    results = {"hollis_voice": run("hollis_voice", HOLLIS)}

    room = copy_room(tmp, "test_30day")
    who, _, first = a_counted_customer(room)
    uri = "04_customers/order_form_test_30day.pdf"
    write_pdf(room / uri, order_form(who, term_line="Term month to month.", termination=THIRTY_DAY, effective=first))
    results["test_30day"] = run("test_30day", room, only=uri)

    room = copy_room(tmp, "test_one_year")
    write_pdf(room / uri, order_form(who, term_line=one_year_from(first), termination=ONE_YEAR, effective=first))
    results["test_one_year"] = run("test_one_year", room, only=uri)

    room = copy_room(tmp, "test_change_of_control")
    coc = "04_customers/order_form_test_coc.pdf"
    write_pdf(room / coc, order_form(who, term_line=one_year_from(first), effective=first,
                                     termination=ONE_YEAR, extra=CHANGE_OF_CONTROL))
    results["test_change_of_control"] = run("test_change_of_control", room, only=coc)

    folder = tmp / "contracts_only"
    folder.mkdir()
    for i, rel in enumerate(("04_customers/pilot_agreement_marlow.pdf", "04_customers/order_form_cedar_pine.pdf",
                             "04_customers/order_form_brookline_row.pdf")):
        shutil.copyfile(HOLLIS / rel, folder / f"contract_{i}.pdf")
    results["contracts_only"] = run("contracts_only", folder)
    results["brasswick"] = run("brasswick", ROOT / "data_room" / "brasswick")
    results["seed_drop"] = run("seed_drop", ROOT / "data_room" / "hollis_voice_seed_drop")
    print(json.dumps({k: {"claims": v["quote_check"]["claims"], "gaps": len(v["gaps"]),
                          "quotes_failed": len(v["quote_check"]["failed"])} for k, v in results.items()}, indent=2))
    print(f"test rooms built in {tmp}")


if __name__ == "__main__":
    main()
