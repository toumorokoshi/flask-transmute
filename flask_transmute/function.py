import inspect
from collections import namedtuple
from .compat import getfullargspec


ArgumentInfo = namedtuple("ArgumentInfo", ["default", "type"])
NoDefault = object()


class TransmuteFunction(object):
    """
    VoodooFunctions are objects that wrap a method, allowing
    extensions to extract metadata for their own use (such as
    automatic documentation)
    """

    def __init__(self, func, error_exceptions=None):
        # arguments should be the arguments passed into
        # the function
        #
        # the return type should be specified. If nothing is
        # passed in, a NoneType is returned.
        # for a dynamic language like Python, it's not a huge deal:
        # transmute will still json serialize whatever object you pass it.
        # however, the return type is valuable for autodocumentation systems.
        self.arguments, self.return_type = _extract_arguments_and_return_type(func)
        # description should be a description of the api
        # endpoint, for use in autodocumentation
        self.description = func.__doc__
        # error_exceptions represents the exceptions
        # that should be caught and return an API exception
        self.error_exceptions = error_exceptions
        # these are set if the function performs some
        # operation that modifies data.
        self.creates = getattr(func, "creates", False)
        self.deletes = getattr(func, "deletes", False)
        self.updates = getattr(func, "updates", False)
        # produces represents the return types supported
        # by the final function
        self.produces = ["application/json"]
        self.raw_func = func
        # status_codes represents the possible status codes
        # the function can return
        self.status_codes = _get_default_status_codes()
        # this is to make discovery easier.
        # TODO: make sure this doesn't mess up GC, as it's
        # a cyclic reference.
        if inspect.ismethod(func):
            func.__func__.transmute_func = self
        else:
            func.transmute_func = self


def _extract_arguments_and_return_type(func):
    """
    return a dict of <name, type> pairs and a <type>,
    which represent arguments and a return type that
    should passed into the function and returned.
    """
    argspec = getfullargspec(func)
    attributes = (getattr(argspec, "args", []) +
                  getattr(argspec, "keywords", []))
    defaults = argspec.defaults or []

    arguments = {}
    for i, name in enumerate(reversed(attributes)):
        if name == "self":
            continue

        default = NoDefault if len(defaults) <= i else defaults[i]
        arguments[name] = ArgumentInfo(
            default, argspec.annotations.get(name, str)
        )

    return arguments, argspec.annotations.get("return", type(None))


def _get_default_status_codes():
    return {
        200: "success",
        400: "invalid input received"
    }
