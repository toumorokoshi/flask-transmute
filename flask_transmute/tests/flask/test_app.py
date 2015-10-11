import json
import yaml
import pytest
from conftest import create_test_app


def test_cards(flask_app):
    app = flask_app.test_client()
    resp = app.get("/deck/cards")
    assert resp.status_code == 200
    resp_json = json.loads(resp.data.decode("UTF-8"))
    assert resp_json == {"success": True, "result": []}


def test_add_card(flask_app):
    app = flask_app.test_client()
    data = {"card": {"name": "foo", "description": "bar"}}
    resp = app.post(
        "/deck/add_card",
        data=json.dumps(data),
        headers={"content-type": "application/json"}
    )
    resp_json = json.loads(resp.data.decode("UTF-8"))
    assert resp_json == {"success": True, "result": data["card"]}


@pytest.mark.parametrize("ret_val", [
    {"a": "b"}, 10, "string", True,
])
def test_route_with_no_type_hints(ret_val):
    """
    with no type hinting, the serializer should just try to serialize
    to json with json.dumps
    """

    def return_foo():
        return ret_val

    test_app = create_test_app("/foo", return_foo)
    assert json.loads(test_app.get("/foo").data.decode("UTF-8")) == {
        "success": True,
        "result": ret_val
    }


def test_route_with_no_type_hints_argument():

    def return_input_string(input_string):
        return input_string

    test_app = create_test_app("/foo", return_input_string)
    assert json.loads(test_app.get("/foo?input_string=testme").data.decode("UTF-8")) == {
        "success": True,
        "result": "testme"
    }


def test_route_yaml():

    def return_input_string(input_string):
        return input_string

    test_app = create_test_app("/foo", return_input_string)
    resp = test_app.get("/foo?input_string=testme", headers={
        "content-type": "application/yaml"
    })
    assert "success: true" in resp.data.decode("UTF-8")
    assert yaml.load(resp.data.decode("UTF-8")) == {
        "success": True,
        "result": "testme"
    }
