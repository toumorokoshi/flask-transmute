from ..routeset import RouteSet
from .method_wrapper import wrap_method
from ..function import TransmuteFunction


class FlaskRouteSet(RouteSet):

    def __init__(self, *args, **kwargs):
        self._route_options = {}
        super(FlaskRouteSet, self).__init__(*args, **kwargs)

    def init_app(self, app):
        for route_config in self._routes:
            _route_transmute_func(app,
                                  route_config.path,
                                  route_config.transmute_func)

    def route_function(self, path, function, **options):
        transmute_options, flask_options = self._split_options_dict(options)
        self._route_options[path] = flask_options
        super(FlaskRouteSet, self).route_function(path, function,
                                                  **transmute_options)


def _route_transmute_func(router, path, transmute_func, **options):
    method = "GET"
    if transmute_func.creates:
        method = "PUT"
    elif transmute_func.deletes:
        method = "DELETE"
    elif transmute_func.updates:
        method = "POST"
    return router.route(path, methods=[method], **options)(wrap_method(transmute_func))


# to accomodate a more flask-like syntax, you can decorate a single
# method, a la flask.
def route(router, path, **options):

    transmute_options, flask_options = \
        FlaskRouteSet._split_options_dict(options)

    def decorator(func):
        transmute_func = TransmuteFunction(func, **transmute_options)
        return _route_transmute_func(router, path, transmute_func, **flask_options)

    return decorator
