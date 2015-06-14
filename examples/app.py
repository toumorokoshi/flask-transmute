from flask import Flask
import flask_transmute


# having an exception that is raised in
# a situation like this is valuable. this can help
# indicate to Transmute what is an expected exception
# based off of incorrect input, or a real error.
# former should raise this.
class DeckException(Exception):
    pass


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
