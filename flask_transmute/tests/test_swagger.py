from . import TransmuteTestBase


class TestSwagger(TransmuteTestBase):

    def test_swagger_page_loads(self):
        self.app.get("/swagger.json")
