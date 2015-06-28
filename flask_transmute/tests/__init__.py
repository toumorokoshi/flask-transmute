import unittest
from .app import app, deck


class TransmuteTestBase(unittest.TestCase):

    def setUp(self):
        self.real_app = app
        self.app = app.test_client()

    def tearDown(self):
        deck.reset()
