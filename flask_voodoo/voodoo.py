from collections import namedtuple
from .autoroute import (
    autoroute_function as _autoroute_function
)
from .utils import get_public_callables

RouteArgs = namedtuple("RouteArgs", ["func", "path", "options"])


class Voodoo(object):
    """
    the voodoo object can be used to group together multiple
    routing objects into a single context.

    it can also accept extensions, allowing it to do
    additional work such as autodocumenting the apis.
    """

    def __init__(self):
        self._extensions = []
        self._routes = []

    def autoroute(self, obj, path, **options):
        for method_name, func in get_public_callables(obj):
            method_path = path + "/" + method_name
            self.autoroute_function(func, method_path, **options)

    def autoroute_function(self, func, path, **options):
        route_args = RouteArgs(func, path, options)
        self._routes.append(route_args)

    def init_app(self, app):
        for route in self._routes:
            func, path, options = route
            self._route_func(app, func, path, **options)

        for ext in self._extensions:
            ext.init_app(app)

    def _route_func(self, app, func, path, **options):
        args = (app, func, path, options)
        for extension in self._extensions:
            args = extension.route_func(app, func, path, **options)
            if args is None:
                break
            app, func, path, options = args

        if args:
            app, func, path, options = args
            _autoroute_function(app, func, path, **options)
