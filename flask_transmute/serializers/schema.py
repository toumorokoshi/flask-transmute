from .exceptions import InvalidSchema


def validate_schema(schema):
    """ validate that the schema is a valid transmute schema """
    required_keys = ["properties"]

    errors = []
    for key in required_keys:
        if key not in schema:
            errors.append("key {0} is required for a valid schema.".format(key))

    properties = schema.get("properties", {})

    if not isinstance(properties, dict):
        errors.append("properties key must be a dict")
    else:
        for name, details in properties.items():
            if not isinstance(name, str):
                errors.append("expected property name to be a string, found {0}".format(str(type(name))))

            if not isinstance(details, dict):
                errors.append("expected property details to be a dict, found {0}".format(str(type(details))))
            else:
                errors.extend(_validate_schema_property(details))

    required = schema.get("required", [])

    if not isinstance(required, list):
        errors.append("expected 'required' to be a list. found {0}".format(str(type(required))))
    elif isinstance(properties, dict):
        for r in required:
            if r not in properties:
                errors.append("{0} is specified as a required parameter, but no definition exists.".format(r))
    if errors:
        raise InvalidSchema(errors, schema)


def _validate_schema_property(prop_dict):
    """ validate that the transmute schema property is valid """
    errors = []
    if "type" in prop_dict:
        if not _is_valid_type_definition(prop_dict["type"]):
            errors.append("{0} is not a valid type definition.".format(prop_dict["type"]))
    else:
        errors.append("property details requires parameter 'type'")
    return errors


def _is_valid_type_definition(type_definition):
    if isinstance(type_definition, list):
        if len(type_definition) != 1:
            return False
        return _is_valid_type_definition(type_definition[0])

    elif isinstance(type_definition, dict):
        for key, value in type_definition.items():
            if not isinstance(key, str):
                return False
            if not _is_valid_type_definition(value):
                return False
        return True
    return isinstance(type_definition, type)
