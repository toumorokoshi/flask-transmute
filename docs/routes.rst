======
Routes
======

-------
Example
-------

Adding routes follows the flask pattern, with a decorator
a decorator converting a function to a flask route


.. code-block:: python

    from flask_transmute import route, annotate

    # define a GET endpoint, taking a query parameter integers left and right,
    # which must be integers.
    @route(app, paths="/multiply")
    @annotate({"left": int, "right": int, "return": int})
    def multiply(left, right):
        return left * right

see `transmute-core:function <http://transmute-core.readthedocs.io/en/latest/function.html#functions>`_ for more information on customizing
transmute routes.

-----------------
API Documentation
-----------------

.. autofunction:: flask_transmute.describe
