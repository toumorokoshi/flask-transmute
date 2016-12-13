from transmute_core import describe, default_context
from transmute_core.function import TransmuteFunction
from .handler import create_routes_and_handler
from .swagger import SWAGGER_ATTR_NAME


def transmute_route(app, context=default_context, **kwargs):
    """ attach a transmute route. """
    def decorator(fn):
        fn = describe(**kwargs)(fn)
        transmute_func = TransmuteFunction(fn)
        routes, handler = create_routes_and_handler(transmute_func, context)
        for r in routes:
            _push_swagger_info(app, transmute_func, context)
            app.route(r)(handler)
        return handler
    return decorator


def _push_swagger_info(app, transmute_func, context=default_context):
    """
    add swagger info to the global transmute swagger object.
    """
    swagger_obj = getattr(app, SWAGGER_ATTR_NAME, {})
    swagger_path = transmute_func.get_swagger_path(context)
    for p in transmute_func.paths:
        if p not in swagger_obj:
            swagger_obj[p] = swagger_path
        else:
            for method, definition in swagger_path.items():
                setattr(swagger_obj[p], method, definition)
    setattr(app, SWAGGER_ATTR_NAME, swagger_obj)
