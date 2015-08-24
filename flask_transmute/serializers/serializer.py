from .class_serializer import (
    class_is_serializable, generate_class_serializer
)
from .list_serializer import (
    list_is_serializable, generate_list_serializer
)
from .basetype_serializers import (
    BoolSerializer,
    NoneSerializer,
    IntSerializer,
    FloatSerializer,
    StringSerializer
)

# the serializer cache contains serializers for
# all known types.
_SERIALIZER_CACHE = {
    bool: BoolSerializer,
    type(None): NoneSerializer,
    None: NoneSerializer,
    int: IntSerializer,
    float: FloatSerializer,
    str: StringSerializer
}


def get_serializer(cls):
    cls = _make_signature_hashable(cls)

    if cls in _SERIALIZER_CACHE:
        return _SERIALIZER_CACHE[cls]

    _assert_type_is_serializable(cls)

    if isinstance(cls, tuple):
        serializer = generate_list_serializer(cls[0], _SERIALIZER_CACHE)
    else:
        serializer = generate_class_serializer(cls, _SERIALIZER_CACHE)

    _SERIALIZER_CACHE[cls] = serializer
    return serializer


def _make_signature_hashable(cls):
    """
    convert the class signature to a hashable object
    """
    if isinstance(cls, list):
        return (cls[0],)
    return cls


def _assert_type_is_serializable(cls):
    if cls in _SERIALIZER_CACHE:
        return

    if isinstance(cls, tuple):
        for subclass in list_is_serializable(cls):
            get_serializer(subclass)

    else:
        for subclass in class_is_serializable(cls):
            get_serializer(subclass)
