import copy
from flask import jsonify, render_template
from flask_restplus.apidoc import apidoc

SWAGGER_TYPEMAP = {
    str: "string",
    int: "integer",
    bool: "boolean",
    list: "array",
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
        self._paths = {}
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
        swagger_object = {
            "swagger": self.swagger_version,
            "info": {
                "title": self._title,
                "version": self._version
            },
            "paths": {}
        }
        for rule in app.url_map.iter_rules():
            path = rule.rule
            endpoint = rule.endpoint
            func = app.view_functions[endpoint]
            if hasattr(func, "transmute_func"):

                if path not in swagger_object["paths"]:
                    swagger_object["paths"][path] = {}

                swagger_object["paths"][path].update(
                    _extract_swagger_pathspec(func.transmute_func))

        return swagger_object


def _extract_swagger_pathspec(voodoo_func):
    transmute_func = voodoo_func
    path_spec = {
        "description": transmute_func.description,
        "produces": transmute_func.produces,
        "parameters": [],
        "responses": {}
    }

    for arg_name, arg_info in transmute_func.arguments.items():
        in_type = "formData" if transmute_func.updates or transmute_func.creates else "query"
        param_spec = {
            "name": arg_name,
            "required": arg_info.default is None,
            "in": in_type
        }
        if isinstance(arg_info.type, list):
            subtype = arg_info.type[0]
            param_spec["type"] = "array"
            param_spec["items"] = {"type": SWAGGER_TYPEMAP.get(subtype, subtype.__name__)}
            param_spec["collectionFormat"] = "multi"
        else:
            param_spec["type"] = SWAGGER_TYPEMAP.get(arg_info.type,
                                                     arg_info.type.__name__)
        path_spec["parameters"].append(param_spec)

    for code, description in transmute_func.status_codes.items():
        path_spec["responses"][str(code)] = {
            "description": description
        }

    method = "get"
    if transmute_func.creates:
        method = "put"
    elif transmute_func.updates:
        method = "post"
    elif transmute_func.deletes:
        method = "delete"
    return {method: path_spec}
