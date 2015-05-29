from flask import Flask
import flask_voodoo


# having an exception that is raised in
# a situation like this is valuable. this can help
# indicate to Voodoo what is an expected exception
# based off of incorrect input, or a real error.
# former should raise this.
class DeckException(Exception):
    pass


class Deck(object):

    def __init__(self):
        self._cards = []

    # the mutates decorator tells
    # flask-voodoo that this method will
    # modify data. adding mutates ensures
    # the request will be a POST
    @flask_voodoo.mutates
    def add_card(self, name):
        if len(name) > 100:
            raise DeckException(
                "the name is too long! must be under 100 characters."
            )
        self._cards += [name]
        return {"card": name}

    def cards(self):
        return self._cards


app = Flask(__name__)

deck = Deck()
flask_voodoo.autoroute(app, deck, '/deck',
                       # if exceptions are added to error_exceptions,
                       # they will be caught and raise a success: false
                       # response, with the error message being the message
                       # of the exception
                       error_exceptions=(DeckException))
app.debug = True
app.run()
