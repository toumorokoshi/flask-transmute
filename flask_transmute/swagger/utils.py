from ..compat import string_type
from decimal import Decimal

SWAGGER_TYPEMAP = {
    string_type: "string",
    Decimal: "string",
    int: "integer",
    bool: "boolean",
    list: "array",
    type(None): "null",
}
