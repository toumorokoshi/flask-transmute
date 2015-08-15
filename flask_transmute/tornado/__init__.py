import tornado.web
from ..routeset import RouteSet
from .handler_factory import HandlerFactory


class TornadoRouteSet(RouteSet):

    def __init__(self, *args, **kwargs):
        super(TornadoRouteSet, self).__init__(*args, **kwargs)

    def generate_handlers(self):
        handler_factory = HandlerFactory()
        for route_config in self._routes:
            handler_factory.add_handler(
                route_config.path, route_config.transmute_func
            )

        return handler_factory.get_handler_tuples()


def _create_handler(transmute_func):

    class Handler(tornado.web.RequestHandler):

        def get(self):
            self.write("Hello, " + transmute_func.description)

    return Handler
