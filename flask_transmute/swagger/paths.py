from .utils import SWAGGER_TYPEMAP


class Paths(object):

    def __init__(self, definitions):
        self._paths = {}
        # this is a Definitions object.
        self._definitions = definitions

    def extract_from_app(self, app):
        for rule in app.url_map.iter_rules():
            path = rule.rule
            endpoint = rule.endpoint
            func = app.view_functions[endpoint]
            if hasattr(func, "transmute_func"):

                if path not in self._paths:
                    self._paths[path] = {}

                self._paths[path].update(
                    self._extract_swagger_pathspec(func.transmute_func)
                )

    def add_to_spec(self, spec):
        spec["paths"] = self._paths

    def _extract_swagger_pathspec(self, transmute_func):
        path_spec = {
            "description": transmute_func.description,
            "produces": transmute_func.produces,
            "parameters": [],
            "responses": {}
        }

        for arg_name, arg_info in transmute_func.arguments.items():
            in_type = "body" if transmute_func.updates or transmute_func.creates else "query"
            param_spec = {
                "name": arg_name,
                "required": arg_info.default is None,
                "in": in_type
            }

            param_spec.update(self._get_property_definition(arg_info.type))
            path_spec["parameters"].append(param_spec)

        for code, details in transmute_func.responses.items():
            # return_dict = self._get_property_definition(details["return_type"])
            path_spec["responses"][str(code)] = {
                "description": details["description"],
            }

        method = "get"
        if transmute_func.creates:
            method = "put"
        elif transmute_func.updates:
            method = "post"
        elif transmute_func.deletes:
            method = "delete"
        return {method: path_spec}

    def _get_property_definition(self, cls):
        if isinstance(cls, list):
            subtype = self._get_property_definition(cls[0])
            return {
                "type": "array",
                "items": {"type": subtype},
                "collectionFormat": "multi"
            }
        elif cls in SWAGGER_TYPEMAP:
            return SWAGGER_TYPEMAP[cls]
        else:
            return {"schema": self._definitions.get_reference(cls)}
