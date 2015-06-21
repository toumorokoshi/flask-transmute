from .exceptions import SerializerException


def list_is_serializable(cls):
    yield cls[0]


def generate_list_serializer(cls, serializers):

    sub_serializer = serializers.get(cls)

    class ListSerializer(object):

        @staticmethod
        def serialize(obj):
            return [
                sub_serializer.serialize(e) for e in obj
            ]

        @staticmethod
        def deserialize(data):
            if not isinstance(data, list):
                raise SerializerException(
                    "unable to serialize a {0} object into a list.".format(type(data.__name__))
                )

            return [sub_serializer.deserialize(e) for e in data]

    ListSerializer.__name__ = "{0}ListSerializer".format(
        cls.__name__
    )

    return ListSerializer
