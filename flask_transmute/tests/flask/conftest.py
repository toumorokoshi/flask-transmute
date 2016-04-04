import pytest
from app import app, deck
from flask import Flask
from flask_transmute.flask import FlaskRouteSet


@pytest.fixture
def flask_app(request):
    request.addfinalizer(lambda: deck.reset())
    return app


def create_test_app(path, func, **options):
    """
    create a test app that wraps a func at the path specified, and
    returns a test client to of the flask app
    """
    app = Flask(__name__)
    app.debug = True
    route_set = FlaskRouteSet()
    route_set.route_function(path, func)
    route_set.init_app(app)
    return app.test_client()
