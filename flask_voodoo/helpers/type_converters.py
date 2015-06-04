"""
type converts handle converting from one value to another.
"""


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


TYPE_CONVERTERS = {
    int: convert_int,
    bool: convert_bool
}
