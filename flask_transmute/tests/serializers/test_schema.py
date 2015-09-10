import pytest
from flask_transmute.serializers.schema import validate_schema
from flask_transmute.serializers.exceptions import InvalidSchema


@pytest.mark.parametrize("schema", [
    {
        "properties": {
            "variable": {"type": int}
        }
    },
    {
        "properties": {
            "variable": {"type": {"val": bool}}
        }
    },
])
def test_validate_schema(schema):
    validate_schema(schema)


@pytest.mark.parametrize("schema", [
    {
        "properties": {
            "variable": {"type": "integer"},
        }
    },
])
def test_validate_bad_schema(schema):
    with pytest.raises(InvalidSchema):
        validate_schema(schema)
