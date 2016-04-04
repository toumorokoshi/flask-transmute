from .exceptions import SerializerException


class Or(object):

    def __init__(self, *classes):
        self.classes = classes

    def __hash__(self):
        return hash(tuple(self.classes))


def or_is_serializable(cls):
    for c in cls.classes:
        yield c


def generate_or_serializer(or_obj, serializers):

    or_serializers = [serializers[c] for c in or_obj.classes]

    class OrSerializer(object):

        @staticmethod
        def serialize(obj):
            for s in or_serializers:
                try:
                    return s.serialize(obj)
                except:
                    continue
            raise SerializerException("Unable to serialize {0} into one of {1}".format(
                str(obj), str(or_obj.classes)
            ))

        @staticmethod
        def deserialize(data):
            for s in or_serializers:
                try:
                    return s.deserialize(obj)
                except:
                    continue
            raise SerializerException("Unable to deserialize {0} into one of {1}".format(
                str(data), str(or_obj.classes)
            ))

    return OrSerializer
