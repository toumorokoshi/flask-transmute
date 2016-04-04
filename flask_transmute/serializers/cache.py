from decimal import Decimal
from .or_serializer import (
    Or,
    or_is_serializable,
    generate_or_serializer
)
from .basetype_serializers import (
    DecimalSerializer,
    BoolSerializer,
    NoneSerializer,
    IntSerializer,
    FloatSerializer,
    StringSerializer
)

from .list_serializer import (
    generate_list_serializer,
    list_is_serializable
)

from .class_serializer import (
    generate_class_serializer,
    class_is_serializable
)


class SerializerCache(object):

    def __init__(self):
        self._cache = {
            bool: BoolSerializer,
            Decimal: DecimalSerializer,
            type(None): NoneSerializer,
            None: NoneSerializer,
            int: IntSerializer,
            float: FloatSerializer,
            str: StringSerializer
        }

    def __getitem__(self, cls):
        key = self._make_signature_hashable(cls)
        if key not in self._cache:
            self._cache[key] = self._build_serializer(cls)
        return self._cache[key]

    def __contains__(self, cls):
        key = self._make_signature_hashable(cls)
        return key in self._cache

    def _assert_type_is_serializable(self, cls):
        cls = self._make_signature_hashable(cls)
        if cls in self:
            return

        if isinstance(cls, tuple):
            for subclass in list_is_serializable(cls):
                self[subclass]
        elif isinstance(cls, Or):
            for subclass in or_is_serializable(cls):
                self[subclass]
        else:
            for subclass in class_is_serializable(cls):
                self[subclass]

    def _build_serializer(self, cls):
        self._assert_type_is_serializable(cls)
        if isinstance(cls, list):
            serializer = generate_list_serializer(cls[0], self)
        elif isinstance(cls, Or):
            serializer = generate_or_serializer(cls, self)
        else:
            serializer = generate_class_serializer(cls, self)
        return serializer

    @staticmethod
    def _make_signature_hashable(cls):
        """
        convert the class signature to a hashable object
        """
        if isinstance(cls, list):
            return (cls[0],)
        return cls
