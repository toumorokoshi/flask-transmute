from flask import Blueprint
from .method_wrapper import wrap_method
from .decorators import is_mutates


def autoroute(flask_app, object_to_route, path,
              error_exceptions=None):
    name = _blueprint_name(object_to_route)
    blueprint = Blueprint(name, __name__)

    for method_name, func in _get_public_callables(object_to_route):
        methods = ["POST"] if is_mutates(func) else ["GET"]
        blueprint.route("/" + method_name, methods=methods)(
            wrap_method(func, error_exceptions=error_exceptions)
        )

    flask_app.register_blueprint(blueprint, url_prefix=path)


BLUEPRINT_TEMPLATE = "FLASK_VOODOO_{0}"


def _blueprint_name(obj):
    title = type(obj).__name__ + "_" + str(id(obj))
    return BLUEPRINT_TEMPLATE.format(title)


def _get_public_callables(obj):
    for key in dir(obj):
        if key.startswith('_'):
            continue
        value = getattr(obj, key)
        if callable(value):
            yield key, value
