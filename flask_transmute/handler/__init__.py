from functools import wraps
from flask import request, Response
from transmute_core import APIException, NoSerializerFound
from .parameters import extract_params


def create_routes_and_handler(transmute_func, context):

    @wraps(transmute_func.raw_func)
    def handler():
        try:
            args, kwargs = extract_params(request, context,
                                          transmute_func.signature,
                                          transmute_func.parameters)
            result = transmute_func(*args, **kwargs)
            if transmute_func.return_type:
                result = context.serializers.dump(
                    transmute_func.return_type, result
                )
            output = {
                "result": result,
                "code": 200,
                "success": True
            }
        except APIException as e:
            output = {
                "result": "invalid api use: {0}".format(str(e)),
                "success": False,
                "code": e.code
            }
        content_type = request.content_type
        try:
            serializer = context.contenttype_serializers[content_type]
        except NoSerializerFound:
            serializer = context.contenttype_serializers.default
            content_type = serializer.main_type
        body = serializer.dump(output)
        return Response(
            body,
            status=output["code"],
            mimetype=content_type
        )
    return (
        _convert_paths_to_flask(transmute_func.paths),
        handler
    )


def _convert_paths_to_flask(transmute_paths):
    """ flask has it's own route syntax, so we convert it. """
    paths = []
    for p in transmute_paths:
        paths.append(p.replace("{", "<").replace("}", ">"))
    return paths
