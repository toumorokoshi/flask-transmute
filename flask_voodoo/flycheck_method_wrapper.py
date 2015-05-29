import functools
import inspect
from flask import jsonify


def wrap_method(func):
    """
    this handles the conversion of a function
    that returns arbitrary functionality into
    """
    argspec = inspect.getargspec(func)
    import pdb; pdb.set_trace()

    @functools.wraps(func)
    def wrapper_func(*args, **kwargs):
        result = func(*args, **kwargs)
        return jsonify({
            'success': True,
            'result': result
        })

    return wrapper_func


def get_argument_set(argspec):
    """ return a set of arguments
    return a 