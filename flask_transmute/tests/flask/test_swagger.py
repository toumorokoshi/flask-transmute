def test_swagger(flask_app):
    app = flask_app.test_client()
    resp = app.get("/swagger.json")
    assert resp.status_code == 200
