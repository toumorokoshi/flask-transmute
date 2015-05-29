import functools
import inspect
from flask import jsonify, request


def wrap_method(func, error_exceptions=None):
    """
    this handles the conversion of a function
    that returns arbitrary functionality into
    """
    arguments = get_argument_set(func)

    is_post_method = getattr(func, 'mutates', False)

    @functools.wraps(func)
    def wrapper_func():
        kwargs = {}
        request_args = request.form if is_post_method else request.args

        for argument in arguments:
            if argument not in request_args:
                return jsonify({
                    "success": False,
                    "detail": "parameter {0} is required".format(argument)
                })
            kwargs[argument] = request_args[argument]

        try:
            result = func(**kwargs)
        except Exception as e:
            if error_exceptions is not None and isinstance(e, error_exceptions):
                return jsonify({
                    "success": False,
                    "detail": str(e)
                })
            else:
                raise

        return jsonify({
            "success": True,
            "result": result
        })

    return wrapper_func


def get_argument_set(func):
    """
    return a set of arguments, which should be retrieved
    and passed into the function.
    """
    argspec = inspect.getargspec(func)
    argument_set = set()
    for attr_name in ["args", "keywords"]:
        for key in (getattr(argspec, attr_name) or []):
            if key != "self":
                argument_set.add(key)

    return argument_set
