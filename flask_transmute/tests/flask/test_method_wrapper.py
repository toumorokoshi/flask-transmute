import json
import pytest
import flask_transmute
from flask import Flask
from flask_transmute.flask import FlaskRouteSet


@pytest.fixture
def app():
    """ a fixture that provides a basic test route. """

    app = Flask(__name__)
    route_set = FlaskRouteSet()

    @route_set.route("/test")
    @flask_transmute.annotate({"arg1": str, "arg2": bool,
                               "return": float})
    def test(arg1, arg2):
        return 1.0

    route_set.init_app(app)
    return app.test_client()


def test_bad_argument(app):
    """ a bad argument should return a success: false. """
    resp = app.get("/test")
    assert resp.status_code == 400
    resp_json = json.loads(resp.get_data().decode())
    assert not resp_json["success"]
