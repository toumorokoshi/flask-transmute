import flask_transmute
from flask import Flask
from flask_transmute.flask import FlaskRouteSet


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

    # transmute_schema is an attribute that helps flask_transmute
    # serialize and deserialize your object.
    #
    # transmute_schema is a modified json-schema: http://json-schema.org/
    # in contrast to using primitive types, you pass in classes for the
    # type definitions.
    transmute_schema = {
        "properties": {
            "name": {"type": str},
            "description": {"type": str}
        },
        "required": ["name", "description"]
    }

    # if you want to be able to automatically populate fields
    # with the desired types, you must specify a from_dict method.
    # this is how flask-transmute will be able to convert a data
    # object to a class instance.
    @staticmethod
    def from_transmute_dict(model):
        return Card(model["name"], model["description"])


class Deck(object):

    def __init__(self):
        self._cards = [Card("foo", "bar"), Card("round", "two")]

    # the update decorator tells
    # flask-transmute that this method will
    # modify data. adding updtate ensures
    # the request will be a POST
    @flask_transmute.updates
    def add_card(self, card: Card) -> Card:
        """ add a card to the deck """
        if len(card.name) > 100:
            raise DeckException(
                "the name is too long! must be under 100 characters."
            )
        self._cards += [card]
        return card

    def cards(self) -> [Card]:
        """ retrieve all cards from the deck """
        return self._cards

app = Flask(__name__)
deck = Deck()

route_set = FlaskRouteSet()
route_set.route_object('/deck', deck,
                       # if exceptions are added to error_exceptions,
                       # they will be caught and raise a success: false
                       # response, with the error message being the message
                       # of the exception
                       error_exceptions=[DeckException])
# swagger = Swagger("myApi", "1.0")
# route_set.add_extension(swagger)

route_set.init_app(app)
# swagger.init_app(app)

app.debug = True
app.run()
