class FlaskTransmuteException(Exception):
    pass


class ApiException(FlaskTransmuteException):
    """ raising this will return a "success": false with some details """


class UnableToParseBody(ApiException):
    """ unable to parse body as a valid object. """

class UnrecognizedContentType(ApiException):
    """ unable to parse body as a valid object. """
