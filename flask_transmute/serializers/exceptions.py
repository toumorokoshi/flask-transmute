class SerializerException(Exception):
        pass


class SerializationException(SerializerException):
        pass


class DeserializationException(SerializerException):
        pass
