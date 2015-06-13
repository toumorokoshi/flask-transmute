"""
type converts handle converting from one value to another.
"""
from functools import partial


class ConversionError(Exception):
    """ raised if there's an issue converting from one type to another """


def convert_int(value):
    if isinstance(value, int):
        return value

    try:
        return int(value)
    except ValueError:
        raise ConversionError("unable to interpret {0} as an int.")


def convert_bool(value):
    if isinstance(value, bool):
        return value
    if not isinstance(value, str):
        msg = "unable to interpret object of type {0} as a bool"
        raise ConversionError(msg.format(type(value).__name__))

    value = value.lower()
    return value.startswith("t") or value.startswith("y")


def convert_string(value):
    if value is None:
        raise ConversionError("string expected. nonetype received")
    return str(value)


def convert_list(desired_type, value):
    if not isinstance(value, list):
        raise ConversionError("list expected. {0} received".format(value))

    convert_type = get_type_converter(desired_type)
    return [convert_type(v) for v in value]


def get_type_converter(desired_type):
    if isinstance(desired_type, list):
        if len(desired_type) != 1:
            raise ConversionError("unable to generate converter for list with multiple values: ".format(desired_type))
        return partial(convert_list, desired_type[0])

    if desired_type not in TYPE_CONVERTERS:
        raise ConversionError("unable to find converter for type {0}".format(str(desired_type)))

    return TYPE_CONVERTERS[desired_type]


TYPE_CONVERTERS = {
    int: convert_int,
    bool: convert_bool,
    str: convert_string
}
