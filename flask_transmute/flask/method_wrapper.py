import json
import yaml
import functools
from flask import jsonify, request, current_app
from ..serializers import get_serializer, SerializerException
from ..function import NoDefault
from ..exceptions import ApiException


def wrap_method(transmute_function):
    """
    this handles the conversion of a function
    that returns arbitrary functionality into
    """
    tf = transmute_function

    is_post_method = tf.creates or tf.updates
    api_exceptions = tuple(
        list(tf.error_exceptions or []) + [ApiException]
    )
    args_not_empty = len(tf.arguments) > 0
    result_serializer = get_serializer(tf.return_type)

    @functools.wraps(tf.raw_func)
    def wrapper_func(*args, **kwargs):
        try:
            request_params = _retrieve_request_params(args_not_empty, is_post_method)
            _add_request_parameters_to_args(tf.arguments, request_params, kwargs)
            result = tf.raw_func(*args, **kwargs)
        except Exception as e:
            if api_exceptions is not None and isinstance(e, api_exceptions):
                return _return({
                    "success": False,
                    "detail": str(e)
                }, status_code=400)
            else:
                raise

        result = result_serializer.serialize(result)
        return _return({
            "success": True,
            "result": result
        })

    return wrapper_func


def _retrieve_request_params(args_not_empty, is_post_method):
    if not is_post_method:
        request_args = request.args
    else:
        if (not request.content_type or "json" in request.content_type) and request.get_data():
            try:
                request_args = json.loads(request.get_data().decode("UTF-8"))
                if not isinstance(request_args, dict) and args_not_empty:
                    raise ApiException("expected json object: {0}".format(str(e)))
            except ValueError as e:
                raise ApiException("unable to parse json: {0}".format(str(e)))
        else:
            request_args = request.form
    return request_args


def _add_request_parameters_to_args(arguments, request_args, arg_dict):
    for argument, info in arguments.items():
        if argument in arg_dict:
            continue

        if argument not in request_args:
            if info.default is NoDefault:
                raise ApiException("parameter {0} is required".format(argument))
            else:
                continue
        try:
            serializer = get_serializer(info.type)
            if isinstance(info.type, list):
                value = request_args.getlist(argument)
            else:
                value = request_args.get(argument)
            value = serializer.deserialize(value)

        except SerializerException as e:
            raise ApiException("parameter {0}: {1}".format(argument, str(e)))
        arg_dict[argument] = value


def _return(data, status_code=200):
    content_type = request.content_type or "application/json"
    if "yaml" in content_type:
        return current_app.response_class(
            yaml.dump(data, default_flow_style=False),
            mimetype='application/x-yaml'
        ), status_code
    if "json" in content_type:
        return jsonify(data), status_code
    else:
        return jsonify(data), status_code
