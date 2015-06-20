from .exceptions import SerializerException


def list_is_serializable(cls):
    yield cls[0]


def generate_list_serializer(cls, serializers):

    sub_serializer = serializers.get(cls)

    class ListSerializer(object):

        @staticmethod
        def serializer(obj):
            return [
                sub_serializer.serialize(e) for e in obj
            ]

        @staticmethod
        def deserialize(data):
            if not isinstance(data, list):
            pass

    ListSerializer.__name__ = "{0}ListSerializer".format(
        cls.__name__
    )

    return ListSerializer
