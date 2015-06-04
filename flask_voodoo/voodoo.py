from collections import namedtuple
from .autoroute import autoroute_voodoo_func
from .function import VoodooFunc
from .utils import get_public_callables

RouteArgs = namedtuple("RouteArgs", ["path", "voodoo_func"])


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

    def add_extension(self, extension):
        self._extensions.append(extension)

    def autoroute(self, path, obj, **options):
        for method_name, func in get_public_callables(obj):
            method_path = path + "/" + method_name
            self.autoroute_function(method_path, func, **options)

    def autoroute_function(self, path, func, **options):
        route_args = RouteArgs(path, VoodooFunc(func, **options))
        self._routes.append(route_args)

    def init_app(self, app):
        router = app
        for route in self._routes:
            path, func = route
            self._route_func(router, path, func)

        for ext in self._extensions:
            ext.init_app(app)

    def _route_func(self, router, path, func):
        args = (router, path, func)
        for extension in self._extensions:
            args = extension.route_func(router, path, func)
            if args is None:
                break

        if args:
            router, path, func = args
            autoroute_voodoo_func(router, path, func)
