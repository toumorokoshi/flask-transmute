import copy
from flask_restplus.apidoc import apidoc
from flask import jsonify, render_template
from web_transmute.swagger import Definitions, Paths


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
