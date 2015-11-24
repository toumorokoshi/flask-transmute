import tornado.testing
import tornado.web
import flask_transmute


class TestApp(tornado.testing.AsyncHTTPTestCase):

    def get_app(self):
        return tornado.web.Application(_get_route_set())

    def test_app(self):
        response = self.fetch("/")
        assert response.code == 200


def _get_route_set():
    route_set = flask_transmute.TornadoRouteSet()
    route_set.route_function("/", test_foo)
    return route_set.generate_handlers()


def test_foo():
    return "Foo"
