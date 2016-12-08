from flask_transmute import (
    transmute_route, annotate,
    add_swagger
)
from flask import Flask

app = Flask(__name__)


@transmute_route(app, paths='/multiply')
@annotate({"left": int, "right": int, "return": int})
def multiply(left, right):
    return left * right

# finally, you can add a swagger json and a documentation page by:
add_swagger(app, "/swagger.json", "/swagger")
