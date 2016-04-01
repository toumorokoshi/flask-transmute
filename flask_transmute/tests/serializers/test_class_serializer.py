import pytest
from flask_transmute.serializers import SerializerCache
from flask_transmute.serializers.exceptions import SerializationException


@pytest.fixture
def myobject_serializer():
    cache = SerializerCache()
    return cache[MyObject]


class NestedObject(object):

    def __init__(self, name):
        self.name = name

    transmute_schema = {
        "properties": {
            "name": {"type": str}
        }
    }

    @staticmethod
    def from_transmute_dict(data):
        return NestedObject(data["name"])


class MyObject(object):

    def __init__(self, name, nested=None, optional=None):
        self.name = name
        if optional:
            self.optional = optional
        if nested:
            self.nested = nested

    transmute_schema = {
        "properties": {
            "name": {"type": str},
            "optional": {"type": int},
            "nested": {"type": [NestedObject]}
        },
        "required": ["name"]
    }

    @staticmethod
    def from_transmute_dict(data):
        kwargs = {"name": data["name"]}
        if "optional" in data:
            kwargs["optional"] = data["optional"]
        if "nested" in data:
            kwargs["nested"] = [
                NestedObject.from_transmute_dict(d) for d in data["nested"]
            ]
        return MyObject(**kwargs)


def test_optional_value_deserialize(myobject_serializer):
    obj = myobject_serializer.deserialize({
        "name": "Mr.T"
    })
    assert obj.name == "Mr.T"
    assert not hasattr(obj, "optional")


def test_optional_value_serialize(myobject_serializer):
    obj = MyObject("Mr.T")
    assert myobject_serializer.serialize(obj) == {
        "name": "Mr.T"
    }


def test_required_value_serialize(myobject_serializer):
    obj = MyObject("Mr.T")
    delattr(obj, "name")
    with pytest.raises(SerializationException):
        myobject_serializer.serialize(obj)


def test_nested_value_serialize(myobject_serializer):
    obj = MyObject("Mr.T")
    obj.nested = [NestedObject("foo")]
    assert myobject_serializer.serialize(obj) == {
        "name": "Mr.T",
        "nested": [{"name": "foo"}]
    }


def test_nested_value_deserialize(myobject_serializer):
    output = myobject_serializer.deserialize({
        "name": "Mr.T",
        "nested": [{"name": "foo"}]
    })
    nested = output.nested
    assert len(nested) == 1
    assert nested[0].name == "foo"
