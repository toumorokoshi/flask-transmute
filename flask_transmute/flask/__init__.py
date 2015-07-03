from ..routeset import RouteSet
from .method_wrapper import wrap_method


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


def _route_transmute_func(router, path, vf):
    method = "GET"
    if vf.creates:
        method = "PUT"
    elif vf.deletes:
        method = "DELETE"
    elif vf.updates:
        method = "POST"
    router.route(path, methods=[method])(wrap_method(vf))
