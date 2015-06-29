=============
serialization
=============

Due to the dynamic nature of Python objects, it's necessary to provide some attributes
on class declarations that flask-transmute uses when serializing to and from a dictionary.

Two attributes are required:

* a dictionary attribute "transmute_schema" that specifies the structure of the object.
* a static method "from_transmute_dict" that receives a dictionary and
  should return an instance of the class.

The transmute_schema property is very similar to `json-schemas
<http://json-schema.org/>`_, with the exception of using Python type
objects instead of strings to define types:

.. code:: python

   class Deck(object):
      transmute_schema = {
          "properties": {
              "cards": {
                "type": [Card]
              }
              "name": {"type": str}
          },
          "required": ["name"]
      }


The following types may be used:

   * [Type] (a list type)
   * str
   * bool
   * NoneType
   * int
   * any class that is also serializable

The following keys are available:

   * properties: this should be a dictionary of string keys and type
     declaration values, of the format {"type": cls}.
   * required: this should be a list of attributes on the object that
     are required.

Here's a complete example:

.. code:: python

    class Card(object):

        def __init__(self, name, description):
            self.name = name
            self.description = description

        transmute_schema = {
            "properties": {
                "name": {"type": str},
                "description": {"type": str}
            },
            "required": ["name", "description"]
        }

        @staticmethod
        def from_transmute_dict(model):
            return Card(model["name"], model["description"])
