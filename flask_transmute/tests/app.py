from flask import Flask
import flask_transmute
from flask_transmute.swagger import Swagger


# having an exception that is raised in
# a situation like this is valuable. this can help
# indicate to Transmute what is an expected exception
# based off of incorrect input, or a real error.
# former should raise this.
class DeckException(Exception):
    pass


class Card(object):

    def __init__(self, name, description):
        self.name = name
        self.description = description

    transmute_schema = {
        "properties": {
            "name": {"type": str},
            "description": {"type": str}
        },
        "required": ["name", "description"]
    }

    @staticmethod
    def from_transmute_dict(model):
        return Card(model["name"], model["decription"])


class Deck(object):

    def __init__(self):
        self._cards = []

    # the update decorator tells
    # flask-transmute that this method will
    # modify data. adding updtate ensures
    # the request will be a POST
    @flask_transmute.updates
    def add_card(self, card: Card):
        """ add a card to the deck """
        if len(card.name) > 100:
            raise DeckException(
                "the name is too long! must be under 100 characters."
            )
        self._cards += [card]
        return {"card": card}

    def cards(self) -> [Card]:
        """ retrieve all cards from the deck """
        return self._cards

deck = Deck()
app = Flask(__name__)
swagger = Swagger("myApi", "1.0")
flask_transmute.autoroute(app, '/deck', deck,
                          # if exceptions are added to error_exceptions,
                          # they will be caught and raise a success: false
                          # response, with the error message being the message
                          # of the exception
                          error_exceptions=[DeckException])
swagger.init_app(app)
