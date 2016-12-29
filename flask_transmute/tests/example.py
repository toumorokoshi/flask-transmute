from flask_transmute import route, annotate
import flask_transmute
from flask import Flask

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

# finally, you can add a swagger json and a documentation page by:
flask_transmute.add_swagger(app, "/swagger.json", "/swagger")
