import copy
import pytest
from flask_transmute.serializers.serializer import _SERIALIZER_CACHE
from flask_transmute.serializers.class_serializer import generate_class_serializer
from flask_transmute.serializers.exceptions import SerializationException


@pytest.fixture
def serializers():
    return copy.copy(_SERIALIZER_CACHE)


@pytest.fixture
def myobject_serializer(serializers):
    return generate_class_serializer(MyObject,
                                     serializers)


class MyObject(object):

    def __init__(self, name, optional=None):
        self.name = name
        if optional:
            self.optional = optional

    transmute_schema = {
        "properties": {
            "name": {"type": str},
            "optional": {"type": int},
        },
        "required": ["name"]
    }

    @staticmethod
    def from_transmute_dict(data):
        kwargs = {"name": data["name"]}
        if "optional" in data:
            kwargs["optional"] = data["optional"]
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
