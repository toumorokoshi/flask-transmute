from flask_transmute import (
    route, annotate, Response, APIException
)
import flask_transmute
from schematics.models import Model
from schematics.types import StringType, IntType
from flask import Flask, Blueprint

app = Flask(__name__)

class Person(Model):
    name = StringType()
    number_of_cats = IntType()


CAT_PEOPLE = {
    "george": Person({"name": "george",
                      "number_of_cats": 2})
}

@flask_transmute.route(app, paths='/cat_person')
#                        methods=["POST"])
def get_cat_person(name: str) -> Person:
    """ find and return a cat person """
    if name in CAT_PEOPLE:
        return CAT_PEOPLE[name]
    raise APIException("no cat person found", code=404)


# alternatively
@flask_transmute.route(app, paths='/multiply')
def multiply(left: int, right: int) -> int:
    """ multiply two integers """
    return left * right

# type hint equivalent in Py2
multiply.__annotations__ = {
    "left": int, "right": int, "return": int
}

@route(app, paths='/exception')
def exception():
    raise flask_transmute.APIException("api error!")


@flask_transmute.route(app,
                       paths='/complex/{path}',
                       methods=["POST"],
                       body_parameters=["body"],
                       header_parameters=["header"])
@annotate({"body": str, "header": str, "path": str, "return": str})
def complex(body, header, path):
    return body + ":" + header + ":" + path

blueprint = Blueprint('blueprint', __name__, url_prefix="/blueprint")


@flask_transmute.route(blueprint, paths='/foo')
@annotate({"return": bool})
def foo():
    return True


@flask_transmute.route(app, paths="/api/v1/header",
                       response_types={
                           200: {"type": str, "description": "success",
                                 "headers": {
                                     "location": {
                                         "description": "url to the location",
                                         "type": str
                                     }
                                 }
                           },
                       }
)
def header():
    return Response(
        "foo", headers={"x-nothing": "value"}
    )



app.register_blueprint(blueprint)

# finally, you can add a swagger json and a documentation page by:
flask_transmute.add_swagger(app, "/swagger.json", "/api/")
