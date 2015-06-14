from flask import Blueprint
from .method_wrapper import wrap_method
from .utils import get_public_callables
from .function import TransmuteFunction


def autoroute(flask_app, path, object_to_route, **options):
    name = _blueprint_name(object_to_route)
    blueprint = Blueprint(name, __name__)

    for method_name, func in get_public_callables(object_to_route):
        autoroute_function(blueprint, "/" + method_name,
                           func, **options)
    flask_app.register_blueprint(blueprint, url_prefix=path)


def autoroute_function(router, path, function, **options):
    vf = TransmuteFunction(function, **options)
    autoroute_transmute_func(router, path, vf)


def autoroute_transmute_func(router, path, vf):
    method = "GET"
    if vf.creates:
        method = "PUT"
    elif vf.deletes:
        method = "DELETE"
    elif vf.updates:
        method = "POST"
    router.route(path, methods=[method])(wrap_method(vf))

BLUEPRINT_TEMPLATE = "FLASK_TRANSMUTE_{0}"


def _blueprint_name(obj):
    title = type(obj).__name__ + "_" + str(id(obj))
    return BLUEPRINT_TEMPLATE.format(title)
