import inspect


class VoodooFunction(object):
    """
    VoodooFunctions are objects that wrap a method, allowing
    extensions to extract metadata for their own use (such as
    automatic documentation)
    """

    def __init__(self, path, func, error_exceptions=None):
        # arguments should be the arguments passed into
        # the function
        self.arguments = _extract_arguments(func)
        # description should be a description of the api
        # endpoint, for use in autodocumentation
        self.description = func.__doC__
        # error_exceptions represents the exceptions
        # that should be caught and return an API exception
        self.error_exceptions = error_exceptions
        # mutates should be set to True if the function
        # mutates data.
        self.mutates = getattr(func, "mutates", False)
        # the path is the path that will eventually be routed
        # to the flask app.
        self.path = path
        # produces represents the return types supported
        # by the final function
        self.produces = ["application/json"]
        self.raw_func = func
        # status_codes represents the possible status codes
        # the function can return
        self.status_codes = _get_default_status_codes()


def _extract_arguments(func):
    """
    return a dict of <name, type> pairs,
    which should be retrieved and passed
    into the function
    """
    argspec = inspect.getargspec(func)
    annotations = getattr(func, "__annotations__", {})
    arguments = {}
    for attr_name in ["args", "keywords"]:
        for key in (getattr(argspec, attr_name) or []):
            if key != "self":
                arguments[key] = annotations.get(key, str)
    return arguments


def _get_default_status_codes():
    return {
        200: "success",
        400: "invalid input received"
    }
