.. flask-transmute documentation master file, created by
   sphinx-quickstart on Wed Jun 17 09:23:47 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

flask-transmute
===============

flask-transmute is a flask extension that generates APIs from standard
python functions and classes. Autodocumention is also provided via `swagger <http://swagger.io/>`_.

Here's a very brief example:

.. code:: python

    import flask_transmute
    ...

    @flask_transmute.updates
    def add_pet(name: str, type: str) -> bool:
        animals.add({"name": name, "type": type})
        return True

    flask_transmute.autoroute_function(
        app, "/add_pet", add_pet
    )

The example above creates a path /add_pet that:

* accepts POST as a method (due to flask_transmute.updates)
* requires a body containing the fields "name" and "type"
* returns a response {"success": True, "response": True}

You can find a more in-depth example here:
https://github.com/toumorokoshi/flask-transmute/blob/master/examples/deck.py

Contents:

.. toctree::
   :maxdepth: 2

   schema


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
