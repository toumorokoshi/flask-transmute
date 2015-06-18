import types
from .exceptions import SerializerException
from .basetype_serializers import (
    BoolSerializer,
    IntSerializer,
    StringSerializer
)

# the serializer cache contains serializers for
# all known types.
_SERIALIZER_CACHE = {
    bool: BoolSerializer,
    int: IntSerializer,
    str: StringSerializer
}


def get_serializer(cls, serializers=_SERIALIZER_CACHE):
    _assert_type_is_serializable(cls, serializers)
    model = cls.transmute_model
    from_dict = cls.from_dict

    class ClassSerializer(object):
        """ serializes an object to and from a markup-serializable type """

        @staticmethod
        def serialize(obj):
            data = {}
            for attr_name, cls in model.items():
                serializer = serializers[cls]
                value = getattr(cls, attr_name)
                data[attr_name] = serializer.serialize(value)
            return data

        @staticmethod
        def deserialize(data):
            return from_dict(data)

    ClassSerializer.__name__ = "{0}Serializer".format(
        cls.__name__
    )

    serializers[cls] = ClassSerializer
    return ClassSerializer


def _assert_type_is_serializable(cls, serializers):
    if cls in [bool, str, int]:
        return

    from_dict = getattr(cls, "from_dict", None)

    if not from_dict or not isinstance(from_dict, types.FunctionType):
        raise SerializerException(
            "class requires from_dict static method to be serializable!")

    model = getattr(cls, "transmute_model", None)

    if not model or not isinstance(model, dict):
        raise SerializerException(
            "class requires transmute_model dict attribute to be serializable!")

    for key, value in model:
        if not isinstance(key, str):
            raise SerializerException(
                "key {0} is not a string when loading transmute_model for {1}".format(
                    key, cls
                ))

        if not isinstance(value, type):
            raise SerializerException("expected a type for a value in when loading transmute_model for {1}. got {0} instead.".format(
                value, cls
            ))

        get_serializer(value)
