import json
from . import TransmuteTestBase


class TestApp(TransmuteTestBase):

    def test_cards(self):
        resp = self.app.get("/deck/cards")
        self.assertEqual(resp.status_code, 200)
        resp_json = json.loads(resp.data.decode("UTF-8"))
        self.assertEqual(
            resp_json,
            {"success": True, "result": []}
        )
