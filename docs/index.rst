.. flask-transmute documentation master file, created by
   sphinx-quickstart on Wed Jun 17 09:23:47 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

flask-transmute
===============

flask-transmute is a flask extension that generates APIs from standard
python functions and classes. Autodocumention is also provided via `swagger <http://swagger.io/>`_.

Here's a brief example:

.. code:: python

    import flask_transmute
    from flask import Flask

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

    @flask_transmute.updates
    # python 2 doesn't support parameter annotations.
    # instead, you can do
    # @flask_transmute.annotate({"pet": Pet, "return": Pet})
    def add_pet(pet: Pet) -> Pet:
        animals.add(pet)
        return pet

    app = Flask(__name__)
    flask_transmute.autoroute_function(
        app, "/add_pet", add_pet
    )

The example above creates a path /add_pet that:

* accepts POST as a method (due to flask_transmute.updates)
* requires a body containing the fields "name" and "type"
* returns a response {"success": True, "response": True}

You can find a more in-depth example here:
https://github.com/toumorokoshi/flask-transmute/blob/master/examples/deck.py

In raw flask, the above is equivalent to:

.. code:: python

    import json
    from flask import Flask, jsonify, request

    app = Flask(__name__)

    class ApiException(Exception):
        pass

    class Pet(object):

         def __init__(self, name, classification):
             self.name = name
             self.classification = classification

         @staticmethod
         def from_dict(model):
             return Pet(model["name"], model["classification"])

         @staticmethod
         def validate_pet_dict(model):
            errors = []

            if "name" not in model:
                errors.append("name not in model!")
            elif not isinstance(model["name"], str):
                errors.append("expected a string for name. found: {0}".format(type(model["name"]))

            if "classification" not in model:
                errors.append("name not in model!")
            elif not isinstance(model["classification"], str):
                errors.append("expected a string for classification. found: {0}".format(type(model["classification"]))

            return errors

         def to_dict(self):
             return {"name": self.name, "classification": self.classification}

    @app.route("/add_pet", methods=["POST"])
    def add_pet():
        try:
            if "json" in request.content_type:
                request_args = json.loads(request.get_data().decode("UTF-8"))
            else:
                request_args = request.form

            if "pet" not in request_args:
                raise ApiException("pet field is required")

            errors = Pet.validate_pet_dict(request_args["pet"])

            if errors:
                raise ApiException(str(errors))

            pet = request_args["pet"]
            pet_object = Pet.from_dict(model)
            animals.add(pet_object)

            return jsonify({"success": True, "result": pet_object.to_dict()})
        except ApiException as e:
            return jsonify({"success": False, "detail": str(e)})


Contents:

.. toctree::
   :maxdepth: 2

   autodocumentation
   decorators
   serialization


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
