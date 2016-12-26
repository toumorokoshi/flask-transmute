from flask_transmute import (
    transmute_route, annotate,
    describe, add_swagger, APIException
)
from flask import Flask

app = Flask(__name__)


@transmute_route(app, paths='/multiply')
@annotate({"left": int, "right": int, "return": int})
def multiply(left, right):
    return left * right


@transmute_route(app, paths='/exception')
def exception():
    raise APIException("api error!")


@transmute_route(app,
                 paths='/complex/{path}',
                 methods=["POST"],
                 body_parameters=["body"],
                 header_parameters=["header"])
@annotate({"body": str, "header": str, "path": str, "return": str})
def complex(body, header, path):
    return body + ":" + header + ":" + path

# finally, you can add a swagger json and a documentation page by:
add_swagger(app, "/swagger.json", "/swagger")
