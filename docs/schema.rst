=======
Schemas
=======

To help transmute understand how to serialize and deserialize a class
into a dictionary, a transmute_schema property is required. The
transmute_schema is very similar to `json-schemas
<http://json-schema.org/>`_, with the exception of using Python type objects instead
of strings to define types:

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
