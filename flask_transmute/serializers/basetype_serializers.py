from .exceptions import SerializationException
from ..compat import string_type


class IntSerializer(object):

    @staticmethod
    def serialize(obj):
        try:
            return int(obj)
        except ValueError:
            raise SerializationException(
                "unable to interpret {0} as an int.".format(str(obj)))

    @staticmethod
    def deserialize(data):
        if isinstance(data, int):
            return data

        try:
            return int(data)
        except ValueError:
            raise SerializationException(
                "unable to interpret {0} as an int.".format(str(data)))


class FloatSerializer(object):

    @staticmethod
    def serialize(obj):
        return obj

    @staticmethod
    def deserialize(data):
        if isinstance(data, float):
            return data

        try:
            return float(data)
        except ValueError:
            raise SerializationException(
                "unable to interpret {0} as an float.".format(str(data)))


class BoolSerializer(object):

    @staticmethod
    def serialize(obj):
        return obj

    @staticmethod
    def deserialize(data):
        if isinstance(data, bool):
            return data

        if not isinstance(data, string_type):
            msg = "unable to interpret data of type {0} as a bool"
            raise SerializationException(msg.format(type(data).__name__))

        data = data.lower()
        return data.startswith("t") or data.startswith("y")


class StringSerializer(object):

    @staticmethod
    def serialize(obj):
        return obj

    @staticmethod
    def deserialize(data):
        if not isinstance(data, string_type):
            msg = "unable to interpret data of type {0} as a string"
            raise SerializationException(
                msg.format(type(data).__name__))
        return data


class NoneSerializer(object):

    @staticmethod
    def serialize(obj):
        return obj

    @staticmethod
    def deserialize(data):
        if data is not None:
            raise SerializationException("Unable to deserialize {0} to None".format(
                data
            ))
        return None
