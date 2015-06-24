class SerializerException(Exception):
    pass


class InvalidSchema(SerializerException):

    def __init__(self, message, schema):
        super(SerializerException, self).__init__(message)
        self.schema = schema


class SerializationException(SerializerException):
    pass


class DeserializationException(SerializerException):
    pass
