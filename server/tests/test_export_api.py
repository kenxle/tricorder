from copy import deepcopy

from server.app import app
from server.export_api import main, ts_type, typescript


def test_generated_api_contracts_are_current():
    assert main(["--check"]) == 0, "run python -m server.export_api"


def test_openapi_exports_declared_json_routes_and_distinguishes_input_output():
    document = app.openapi()
    generated = typescript(document)
    for operation in ('GET /api/rooms', 'GET /api/rooms/{room}/memo', 'POST /api/rooms/{room}/steer'):
        assert f'"{operation}":' in generated
    for raw in ('GET /trpc/{procedure}', 'GET /api/rooms/{room}/files/{rel}',
                'GET /api/rooms/{room}/memo.pdf', 'GET /api/rooms/{room}/memo.html'):
        assert f'"{raw}":' not in generated
    assert '"version"?: (number | null)' in generated
    assert '"Source-Input"' in generated and '"Source-Output"' in generated
    assert '"has_readout": boolean' in generated
    assert '"claim_ids": (string)[]' in generated


def test_a_python_schema_change_changes_generated_types():
    document = deepcopy(app.openapi())
    document["components"]["schemas"]["RoomInfo"]["properties"]["new_field"] = {"type": "integer"}
    assert '"new_field"?: number' in typescript(document)


def test_json_schema_shapes_preserve_nullable_required_records_and_tuples():
    assert ts_type({"anyOf": [{"type": "string"}, {"type": "null"}]}) == "(string | null)"
    assert ts_type({"type": "object", "properties": {"a-b": {"type": "boolean"}}, "required": ["a-b"]}) == '{ "a-b": boolean; }'
    assert ts_type({"type": "object", "additionalProperties": {"type": "integer"}}) == 'Record<string, number>'
    assert ts_type({"type": "array", "prefixItems": [{"type": "string"}, {"type": "integer"}]}) == '[string, number]'
    assert ts_type({"$ref": "#/components/schemas/A-Output"}) == 'PythonModels["A-Output"]'
    assert ts_type({"type": "object", "additionalProperties": True}) == 'Record<string, unknown>'
