import pytest
from flask_transmute.utils import join_url_paths


@pytest.mark.parametrize("inp, expected_output", [
    (["", "foobar"], "foobar")
])
def test_join_url_paths(inp, expected_output):
    assert join_url_paths(*inp) == expected_output
