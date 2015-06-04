import json
import functools
from flask import jsonify, request
from .helpers.type_converters import TYPE_CONVERTERS, ConversionError


class ApiException(Exception):
    """ raising this will return a "success": false with some details """


def wrap_method(voodoo_function):
    """
    this handles the conversion of a function
    that returns arbitrary functionality into
    """
    vf = voodoo_function

    is_post_method = vf.mutates
    api_exceptions = list(vf.error_exceptions or []) + [ApiException]
    args_not_empty = len(vf.arguments) > 0

    @functools.wraps(vf.raw_func)
    def wrapper_func():
        try:
            request_params = _retrieve_request_params(args_not_empty, is_post_method)
            kwargs = _extract_and_convert_args(vf.arguments, request_params)
            result = vf.raw_func(**kwargs)
        except Exception as e:
            if api_exceptions is not None and isinstance(e, api_exceptions):
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


def _retrieve_request_params(args_not_empty, is_post_method):
    if not is_post_method:
        request_args = request.args
    else:
        if _request_wants_json():
            try:
                request_args = json.loads(request.get_data())
                if not isinstance(request_args, dict) and args_not_empty:
                    raise ApiException("expected json object: {0}".format(str(e)))
            except ValueError as e:
                raise ApiException("unable to parse json: {0}".format(str(e)))
        else:
            request_args = request.form
    return request_args


def _extract_and_convert_args(arguments, request_args):
    kwargs = {}
    for argument, desired_type in arguments.items():
        if argument not in request_args:
            return jsonify({
                "success": False,
                "detail": "parameter {0} is required".format(argument)
            })

        try:
            convert_type = TYPE_CONVERTERS[desired_type]
            value = convert_type(request_args[argument])
        except ConversionError as e:
            return jsonify({
                "success": False,
                "detail": "parameter {0}: {1}".format(argument, str(e))
            })
        kwargs[argument] = value
    return kwargs


def _request_wants_json():
    best = request.accept_mimetypes \
        .best_match(['application/json', 'text/html'])
    return best == 'application/json' and \
        request.accept_mimetypes[best] > \
        request.accept_mimetypes['text/html']
