from flask import Flask
import flask_transmute


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

    # transmute_model is an attribute that helps flask_transmute
    # serialize and deserialize your object.
    #
    # the transmute_model is valid if it is a dictionary of string ->
    # type pairs, where the type is either a primitive or another
    # transmutable model.
    #
    # providing a transmute_model ensures that your object can
    # be converted into a return value.
    transmute_model = {
        "name": str,
        "description": str
    }

    # if you want to be able to automatically populate fields
    # with the desired types, you must specify a from_dict method.
    # this is how flask-transmute will be able to convert a data
    # object to a class instance.
    @staticmethod
    def from_dict(model):
        return Card(model["name"], model["decription"])


class Deck(object):

    def __init__(self):
        self._cards = []

    # the update decorator tells
    # flask-transmute that this method will
    # modify data. adding updtate ensures
    # the request will be a POST
    @flask_transmute.updates
    def add_card(self, name):
        """ add a card to the deck """
        if len(name) > 100:
            raise DeckException(
                "the name is too long! must be under 100 characters."
            )
        self._cards += [name]
        return {"card": name}

    def cards(self):
        """ retrieve all cards from the deck """
        return self._cards

deck = Deck()
app = Flask(__name__)
flask_transmute.autoroute(app, '/deck', deck,
                          # if exceptions are added to error_exceptions,
                          # they will be caught and raise a success: false
                          # response, with the error message being the message
                          # of the exception
                          error_exceptions=[DeckException])
app.debug = True
app.run()
