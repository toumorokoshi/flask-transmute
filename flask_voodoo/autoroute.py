from flask import Blueprint
from .method_wrapper import wrap_method
from .utils import get_public_callables
from .function import VoodooFunc


def autoroute(flask_app, path, object_to_route, **options):
    name = _blueprint_name(object_to_route)
    blueprint = Blueprint(name, __name__)

    for method_name, func in get_public_callables(object_to_route):
        autoroute_function(blueprint, "/" + method_name,
                           func, **options)
    flask_app.register_blueprint(blueprint, url_prefix=path)


def autoroute_function(router, path, function, **options):
    vf = VoodooFunc(function, **options)
    autoroute_voodoo_func(router, path, vf)


def autoroute_voodoo_func(router, path, vf):
    method = "GET"
    if vf.creates:
        method = "PUT"
    elif vf.deletes:
        method = "DELETE"
    elif vf.updates:
        method = "POST"
    router.route(path, methods=[method])(wrap_method(vf))

BLUEPRINT_TEMPLATE = "FLASK_VOODOO_{0}"


def _blueprint_name(obj):
    title = type(obj).__name__ + "_" + str(id(obj))
    return BLUEPRINT_TEMPLATE.format(title)
