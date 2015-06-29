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

    flask_transmute.autoroute_function(
        app, "/add_pet", add_pet
    )


This is equivalent to:

.. code:: python

   import json
   from flask import Flask, jsonify, request

   app = Flask(__name__)

   class Pet(object):

        def __init__(self, name, classification):
            self.name = name
            self.classification = classification

   @app.route("/add_pet", methods=["POST"])
   def add_pet():
       if request.args.get("name"):
           return
       return jsonify({"success": True, "result": True})



The example above creates a path /add_pet that:

* accepts POST as a method (due to flask_transmute.updates)
* requires a body containing the fields "name" and "type"
* returns a response {"success": True, "response": True}

You can find a more in-depth example here:
https://github.com/toumorokoshi/flask-transmute/blob/master/examples/deck.py

Contents:

.. toctree::
   :maxdepth: 2

   autodocumentation
   serialization


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
