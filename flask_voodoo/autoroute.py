from flask import Blueprint
from .method_wrapper import wrap_method
from .decorators import is_mutates
from .utils import get_public_callables


def autoroute(flask_app, object_to_route, path,
              error_exceptions=None):
    name = _blueprint_name(object_to_route)
    blueprint = Blueprint(name, __name__)

    for method_name, func in get_public_callables(object_to_route):
        autoroute_function(blueprint, func, "/" + method_name,
                           error_exceptions=error_exceptions)
    flask_app.register_blueprint(blueprint, url_prefix=path)


def autoroute_function(router, func_to_route, path,
                       error_exceptions=None):
    methods = ["POST"] if is_mutates(func_to_route) else ["GET"]
    router.route(path, methods=methods)(
        wrap_method(func_to_route, error_exceptions=error_exceptions)
    )


BLUEPRINT_TEMPLATE = "FLASK_VOODOO_{0}"


def _blueprint_name(obj):
    title = type(obj).__name__ + "_" + str(id(obj))
    return BLUEPRINT_TEMPLATE.format(title)
