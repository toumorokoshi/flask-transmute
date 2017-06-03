from flask_transmute import route, annotate, Response
import flask_transmute
from flask import Flask, Blueprint

app = Flask(__name__)


@flask_transmute.route(app, paths='/multiply')
@annotate({"left": int, "right": int, "return": int})
def multiply(left, right):
    return left * right


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
flask_transmute.add_swagger(app, "/swagger.json", "/swagger")
