import types
from .exceptions import (
    SerializerException, SerializationException
)
from .schema import validate_schema


def class_is_serializable(cls):
    from_dict = getattr(cls, "from_transmute_dict", None)

    if not from_dict or not isinstance(from_dict, types.FunctionType):
        raise SerializerException(
            "expected from_transmute_dict for {0} to exist and be a function!".format(cls))

    schema = getattr(cls, "transmute_schema", None)
    validate_schema(schema)
    for detail in schema["properties"].values():
        yield detail["type"]


def generate_class_serializer(cls, serializers):
    schema = cls.transmute_schema
    from_transmute_dict = cls.from_transmute_dict

    class ClassSerializer(object):
        """ serializes an object to and from a markup-serializable type """

        @staticmethod
        def serialize(obj):
            data = {}
            for attr_name, attr_details in schema["properties"].items():
                serializer = serializers[attr_details["type"]]
                if hasattr(obj, attr_name):
                    value = getattr(obj, attr_name)
                    data[attr_name] = serializer.serialize(value)
                elif attr_name in schema.get("required", []):
                    raise SerializationException(
                        "required attribute {0} not found".format(attr_name)
                    )
            return data

        @staticmethod
        def deserialize(data):
            return from_transmute_dict(data)

    ClassSerializer.__name__ = "{0}Serializer".format(
        cls.__name__
    )

    return ClassSerializer
