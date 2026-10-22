"""The quote checker: is each claim's quote really at its locator?

Opens each source through schema.readers and looks for the quote with spacing
and case ignored. A claim whose quote is not found at every one of its sources
gets the confidence label "unverified" and moves to the "could not verify"
box. It needs no model.

    python -m schema.check_quotes <room_dir> <result.json>...
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from schema.claim import Claim, Readout, ScanResult, Source
from schema.readers import LocatorError, text_at

_SPACE = re.compile(r"\s+")


def _norm(text: str) -> str:
    # Spacing and case ignored; typographic quotes and dashes folded to ASCII.
    text = text.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    text = text.replace("–", "-").replace("—", "-").replace(" ", " ")
    return _SPACE.sub(" ", text).strip().lower()


def _number_forms(quote: str) -> set[str]:
    """A spreadsheet cell holds 2240868 where a quote may say 2,240,868 or 2240868.0."""
    forms = {quote}
    bare = quote.replace(",", "").replace("$", "").strip()
    try:
        f = float(bare)
    except ValueError:
        return forms
    forms.update({bare, str(f)})
    if f.is_integer():
        forms.update({str(int(f)), f"{int(f):,}"})
    return forms


def source_holds_quote(source: Source, room_dir: str | Path) -> tuple[bool, str]:
    """(found, why). why is empty when found."""
    if not source.quote.strip():
        return False, "empty quote"
    try:
        haystack = _norm(text_at(source, room_dir))
    except (LocatorError, OSError) as err:
        return False, str(err)
    for form in _number_forms(source.quote):
        if _norm(form) and _norm(form) in haystack:
            return True, ""
    return False, f"quote not found at {source.uri} {source.locator}"


def check_claim(claim: Claim, room_dir: str | Path) -> tuple[Claim, list[str]]:
    """The claim back, marked unverified if any source fails, with the reasons."""
    problems = []
    for source in claim.sources:
        ok, why = source_holds_quote(source, room_dir)
        if not ok:
            problems.append(why)
    if problems:
        return claim.model_copy(update={"confidence": "unverified"}), problems
    return claim, []


def check_result(result: ScanResult, room_dir: str | Path) -> tuple[ScanResult, dict[str, list[str]]]:
    checked, failures = [], {}
    for claim in result.claims:
        new, problems = check_claim(claim, room_dir)
        checked.append(new)
        if problems:
            failures[claim.id] = problems
    return result.model_copy(update={"claims": checked}), failures


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(__doc__.strip().splitlines()[-1].strip())
        return 2
    room_dir, files = argv[0], argv[1:]
    bad = 0
    for f in files:
        data = json.loads(Path(f).read_text(encoding="utf-8"))
        result = Readout.model_validate(data) if "pieces" in data else ScanResult.model_validate(data)
        claims = result.claims
        for claim in claims:
            _, problems = check_claim(claim, room_dir)
            for p in problems:
                bad += 1
                print(f"{f}: {claim.id}: {p}")
        print(f"{f}: {len(claims)} claims checked")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
