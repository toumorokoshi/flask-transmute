import pytest
from flask_transmute import FlaskRouteSet


def test_legacy_error():
    """ invoking legacy function should result in an exception. """
    with pytest.raises(NotImplementedError):
        FlaskRouteSet()
