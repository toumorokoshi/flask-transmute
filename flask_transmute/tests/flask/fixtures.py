import pytest
from app import app, deck


@pytest.fixture
def flask_app(request):
    request.addfinalizer(lambda: deck.reset())
    return app
