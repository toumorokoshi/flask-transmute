import pytest
from flask_transmute import FlaskRouteSet
from flask_transmute.swagger import Swagger


@pytest.mark.parametrize("f", [
    FlaskRouteSet, Swagger
])
def test_legacy_error(f):
    """ invoking legacy function should result in an exception. """
    with pytest.raises(NotImplementedError):
        f()
