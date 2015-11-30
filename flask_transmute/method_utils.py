from .exceptions import UnableToParseBody
import json
import yaml


def parse_body(data, content_type):
    """
    given a content type, parse the body appropriately. raises an
    unable to parse exception if content is not valid markup.

    returns (dict, mime_type)
    """
    if "yaml" in content_type:
        return yaml.load(data), "application/x-yaml"
    elif "json" in content_type:
        return json.loads, "application/json"


def dump_body(data, content_type):
    """
    given a content type, dumps the data to the desired type.
    desired type. An UnrecognizedContentType exception will be
    raised if an non-accepted content type is passed.
    """
