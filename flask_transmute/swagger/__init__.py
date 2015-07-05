import pkg_resources
import copy
from flask import jsonify, render_template
from flask_restplus.apidoc import apidoc
from .definitions import Definitions
from .paths import Paths

SWAGGER_FILES_ROOT = pkg_resources.resource_filename(
    "flask_transmute", "swagger-ui"
)

EXAMPLE_SWAGGER_JSON = {
    "info": {"title": "myApi", "version": "1.0"},
    "swagger": "2.0",
    "tags": [{
        "name": "pet"
    }],
    "paths": {
        "/deck/add_card": {
            "post": {
                "tags": ["card"],
                "summary": "add a card to a deck.",
                "description": "",
                "produces": ["application/json"],
                "parameters": [{
                    "in": "body",
                    "name": "body",
                    "required": True,
                    #"schema": {
                    #   "$ref": "#/definitions/Card"
                    #}
                    "schema": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "description": {"type": "string"}
                        }
                    }
                }],
                "responses": {
                    "200": {"description": "good input"}
                }
            }
        }
    },
    "definitions": {
        "Card": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "description": {"type": "string"}
            }
        }
    }
}


class Swagger(object):
    """
    A flask-transmute extension that generates
    a swagger route
    """
    swagger_version = "2.0"

    def __init__(self, title, version, route_prefix="/"):
        self._title = title
        self._version = version
        self._swagger_object = None
        self._definitions = Definitions()
        self._paths = Paths(self._definitions)
        self._restplus_apidoc = copy.deepcopy(apidoc)
        self._route_prefix = route_prefix

    def init_app(self, app):
        swagger_json = self._generate_swagger_json(app)
        swagger_route = self._route_prefix + "swagger.json"
        swagger_ui_route = self._route_prefix

        @app.route(swagger_route)
        def return_swagger_json():
            # return jsonify(EXAMPLE_SWAGGER_JSON)
            return jsonify(swagger_json)

        @self._restplus_apidoc.route(swagger_ui_route)
        def return_swagger_ui():
            return render_template("swagger-ui.html",
                                   specs_url=swagger_route)

        app.register_blueprint(self._restplus_apidoc)

    def _generate_swagger_json(self, app):
        """
        write a swagger json object. this method should be
        re-run if any changes are made to the routing.
        """
        self._paths.extract_from_app(app)

        swagger_object = {
            "swagger": self.swagger_version,
            "info": {
                "title": self._title,
                "version": self._version
            },
            "paths": {}
        }
        self._paths.add_to_spec(swagger_object)
        self._definitions.add_to_spec(swagger_object)

        return swagger_object
