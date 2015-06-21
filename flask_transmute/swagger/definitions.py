from .utils import SWAGGER_TYPEMAP


class Definitions(object):
    """ stores the definitons for objects used in swagger. """

    def __init__(self):
        self._element_name = "definitions"
        self._definitions = {}

    def add_to_spec(self, spec):
        """ add definitions to the swagger spec """
        definitions = {}
        for cls, cls_spec in self._definitions.items():
            definitions[cls.__name__] = cls_spec

        spec[self._element_name] = definitions

    def add_definition(self, cls):
        if cls in self._definitions:
            return self._definitions[cls]

        model = cls.transmute_model
        properties = {}
        for name, prop_cls in model.items():

            if prop_cls in SWAGGER_TYPEMAP:
                prop = {"type": SWAGGER_TYPEMAP.get(prop_cls)}
            else:
                self.add_definition(prop_cls)
                prop = self.get_reference(prop_cls)

            properties[name] = prop

        schema = {
            "type": "object",
            "properties": properties
        }
        self._definitions[cls] = schema
        return schema

    def get_reference(self, cls):
        if cls not in self._definitions:
            self.add_definition(cls)

        reference = "#/{0}/{1}".format(
            self._element_name, cls.__name__
        )
        return {"$ref": reference}

    def get_definition(self, cls):
        if cls in SWAGGER_TYPEMAP:
            return {"type": SWAGGER_TYPEMAP[cls]}

        if cls in self._definitions:
            return self._definitions[cls]

        return self.add_definition(cls)
