from transmute_core import describe, default_context
from transmute_core.function import TransmuteFunction
from .handler import create_routes_and_handler


def transmute_route(app, context=default_context, **kwargs):
    """ attach a transmute route. """
    def decorator(fn):
        fn = describe(**kwargs)(fn)
        transmute_func = TransmuteFunction(fn)
        routes, handler = create_routes_and_handler(transmute_func, context)
        for r in routes:
            app.route(r)(handler)
        return handler
    return decorator
