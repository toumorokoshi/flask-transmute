import json


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
