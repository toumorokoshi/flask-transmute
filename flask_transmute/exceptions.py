class FlaskTransmuteException(Exception):
    pass


class ApiException(FlaskTransmuteException):
    """ raising this will return a "success": false with some details """

    def __init__(self, message=None, status_code=400):
        super(ApiException, self).__init__(message)
        self.status_code = status_code

class APIException(FlaskTransmuteException):
    """ Properly named version of ApiException - raising this will return a "success": false with some details """

    def __init__(self, message=None, status_code=400):
        super(APIException, self).__init__(message)
        self.status_code = status_code

class UnableToParseBody(ApiException):
    """ unable to parse body as a valid object. """


class UnrecognizedContentType(ApiException):
    """ unable to parse body as a valid object. """


class NotFoundException(ApiException):
    """ a convenience exception for 404 not found. """
    def __init__(self, message=None):
        super(NotFoundException, self).__init__(message, status_code=404)
