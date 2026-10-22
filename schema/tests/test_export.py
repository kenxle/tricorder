from schema.claim import Claim
from schema.export import main, structured_output_schema


def test_generated_files_are_current():
    assert main(["--check"]) == 0, "run python -m schema.export and commit the result"


def test_structured_output_schema_requires_every_property():
    s = structured_output_schema(Claim)
    claim = s
    assert set(claim["required"]) == set(claim["properties"])
    assert claim["additionalProperties"] is False
    for d in s["$defs"].values():
        if d.get("type") == "object":
            assert set(d["required"]) == set(d["properties"]) and d["additionalProperties"] is False
