=================================
Migrating to flask-transmute 1.0+
=================================

Migrating to the new transmute framework has multiple advantages:

* better swagger compliance
* customizable validation frameworks, default is Schematics
* up-to-date Swagger UI
* lack of dependencies on other unrelated libraries (such as flask-restful)

Migrating includes the following steps:

1. switch each model in transmute to schematics.
2. replace each FlaskRouteSet() with a blueprint
3. aggregating all decorators and routes to flask_transmute.route()
4. replace Swagger and swagger.init_app with add_swagger

The steps are outlined in detail below.

---------------------------
1. Converting to Schematics
---------------------------

flask-transmute has dropped it's proprietary json-schema based model
definition, and adopted the `Schematics
<http://schematics.readthedocs.io/>`_ library as the default
serializer.

.. note:: the serializer is customizable. See `TransmuteContext <http://transmute-core.readthedocs.io/en/latest/context.html>`_

flask_transmute.annotate() is still the correct function to use,
to annotate rich types.

Primitive objects (str, int, float) are still supported.
Complex objects should be represented as a Schematics schema
instead:

.. code-block:: python

    # old style
    class Pet(object):

        def __init__(self, name, classification):
            self.name = name
            self.classification = classification

        transmute_model = {
            "properties": {
                "name": {"type": str},
                "classification": {"type": str}
            },
            "required": ["name", "classification"]
        }

        @staticmethod
        def from_transmute_dict(model):
            return Pet(model["name"], model["classification"])

        @flask_transmute.annotate({"pet": Pet, "return": bool})
        def my_method(pet):
            return True

.. code-block:: python

    # new style
    import flask_transmute
    from schematics.models import Model
    from schematics.types import StringType

    class Pet(Model):
        name = StringType(required=True)
        classification = StringType(required=True)

    @flask_transmute.annotate({"pet": Pet, "return": bool})
    def my_method(pet):
        return True


----------------------------------------
2. Replace FlaskRouteSet with blueprints
----------------------------------------

flask-transmute now supports blueprints natively, and there is no
longer a need for a custom object such as FlaskRouteSet. However, the
flask_transmute.route should still be used over the standard blueprint.route:


.. code-block:: python

    # before
    import flask_transmute
    route_set = flask_transmute.FlaskRouteSet()

    @route_set.route("/is_programming_fun")
    @flask_transmute.updates
    @flask_transmute.annotate({"answers": bool, "return": bool})
    def is_programming_fun(answer):
        return True

    route_set.init_app(app)


.. code-block:: python

    # after
    from flask import Blueprint
    import flask_transmute

    blueprint = Blueprint("blueprint", __name__, url_prefix="/blueprint")

    @flask_transmute.route(blueprint, paths="/is_programming_fun")
    @flask_transmute.annotate({"answers": bool, "return": bool})
    def is_programming_fun(answer):
        return True

    app.register_blueprint(blueprint)

---------------------------------------
3. aggregate route descriptors to route
---------------------------------------

flask-transmute now aggregates all decorators into a single one:
flask_transmute.describe. All arguments passed into the new
flask_transmute.route are also passed along to a describe() call:

.. code-block:: python

    # before
    @route_set.route("/is_programming_fun")
    @flask_transmute.updates
    @flask_transmute.annotate({"answers": bool, "return": bool})
    def is_programming_fun(answer):
        return True


.. code-block:: python

    # after
    @flask_transmute.route(app)
    @flask_transmute.describe(paths="/is_programming_fun", methods=["POST"])
    @flask_transmute.annotate({"answers": bool, "return": bool})
    def is_programming_fun(answer):
        return True


Even simpler, arguments to describe can be passed into route directly:


.. code-block:: python

    # after
    @flask_transmute.route(app, paths="/is_programming_fun", methods=["POST"])
    @flask_transmute.annotate({"answers": bool, "return": bool})
    def is_programming_fun(answer):
        return True



.. warning:: the new transmute syntax does not use the flask routing
             syntax, and uses the generic transmute-core
             path. Specifically, the path wildcard "/path/<var_name>"
             should be replaced with the wildcard "/path/{var_name}"
             instead.


----------------------------------------
4. replace init_swagger with add_swagger
----------------------------------------

Instead of instantiating and calling a swagger object,
the add_swagger method should be used instead:


.. code-block:: python

    # before
    from flask_transmute.swagger import Swagger

    swagger = Swagger("myApi", "1.0", route_prefix="/api")
    swagger.init_app(app)

.. code-block:: python

    # after
    import flask_transmute

    flask_transmute.add_swagger(app, "/api/swagger.json", "/api/",
                                title="myApi", version="1.0")


And you're done! You can learn more about how to customize in this document, and the `transmute-core <http://transmute-core.readthedocs.io/en/latest/>`_ docs.
