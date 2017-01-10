import json
import flask_transmute
from flask import Flask, Blueprint
from flask_transmute.swagger import SWAGGER_ATTR_NAME


def test_blueprint_only_app():
    """
    A flask app that only has transmute routes
    in blueprints should be valide.
    """
    app = Flask(__name__)
    blueprint = Blueprint("foo", __name__)

    # this also unit tests empty url prefix blueprints.
    @flask_transmute.route(blueprint, paths=["/foo"])
    def foo():
        return None

    app.register_blueprint(blueprint)
    flask_transmute.add_swagger(app, "/swagger.json", "/swagger")

    test_client = app.test_client()
    body = json.loads(test_client.get("/swagger.json").data)
    assert "/foo" in body["paths"]
