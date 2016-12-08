import json


def test_happy_path(test_app):
    r = test_app.get("/multiply?left=3&right=3")
    assert json.loads(r.data)["result"] == 9
