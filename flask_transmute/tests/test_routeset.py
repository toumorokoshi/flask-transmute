import flask_transmute


def test_route_decorator():
    """ RouteSets should have a route decorator method. """
    route_set = flask_transmute.FlaskRouteSet()

    @route_set.route("/foo")
    def test():
        return {"foo": "bar"}

    assert len(route_set._routes) == 1
    assert route_set._routes[0].transmute_func.raw_func == test
    assert route_set._routes[0].path == "/foo"
