from .exceptions import SerializationException


class IntSerializer(object):

    @staticmethod
    def serialize(obj):
        return obj

    @staticmethod
    def deserialize(data):
        if isinstance(data, int):
            return data

        try:
            return int(data)
        except ValueError:
            raise SerializationException(
                "unable to interpret {0} as an int.".format(str(data)))


class BoolSerializer(object):

    @staticmethod
    def serialize(obj):
        return obj

    @staticmethod
    def deserialize(data):
        if isinstance(data, bool):
            return data

        if not isinstance(data, str):
            msg = "unable to interpret dataect of type {0} as a bool"
            raise SerializationException(msg.format(type(data).__name__))

        data = data.lower()
        return data.startswith("t") or data.startswith("y")


class StringSerializer(object):

    @staticmethod
    def serialize(obj):
        return obj

    @staticmethod
    def deserialize(data):
        if isinstance(data, bool):
            return data
        if not isinstance(data, str):
            msg = "unable to interpret dataect of type {0} as a bool"
            raise SerializationException(
                msg.format(type(data).__name__))
        data = data.lower()
        return data.startswith("t") or data.startswith("y")
