import unittest
from .app import app


class TransmuteTestBase(unittest.TestCase):

    def setUp(self):
        self.real_app = app
        self.app = app.test_client()
