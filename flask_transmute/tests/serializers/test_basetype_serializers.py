import pytest
from decimal import Decimal
from flask_transmute.serializers import (
    BoolSerializer,
    DecimalSerializer,
    FloatSerializer,
    IntSerializer,
    NoneSerializer,
    StringSerializer
)
from flask_transmute.serializers import SerializerException


@pytest.mark.parametrize("inp, expected_output", [
    ("10", 10), ("-1", -1)
])
def test_int_deserializer_happy(inp, expected_output):
    """ test all happy cases for the integer serializer """
    assert IntSerializer.deserialize(inp) == expected_output


@pytest.mark.parametrize("unhappy_input", [
    "foo", "bar"
])
def test_int_deserializer_unhappy(unhappy_input):
    """ test all unhappy cases for the integer serializer """
    with pytest.raises(SerializerException):
        IntSerializer.deserialize(unhappy_input)


@pytest.mark.parametrize("inp, expected_output", [
    ("10", Decimal(10)),
    ("-1", Decimal(-1)),
    ("-1.2345", Decimal("-1.2345")),
])
def test_decimal_deserializer_happy(inp, expected_output):
    """ test all happy cases for the integer serializer """
    assert DecimalSerializer.deserialize(inp) == expected_output


@pytest.mark.parametrize("unhappy_input", [
    "foo", "bar"
])
def test_decimal_deserializer_unhappy(unhappy_input):
    """ test all unhappy cases for the integer serializer """
    with pytest.raises(SerializerException):
        DecimalSerializer.deserialize(unhappy_input)


@pytest.mark.parametrize("inp, expected_output", [
    ("10", 10), ("1.0", 1.0)
])
def test_float_deserializer_happy(inp, expected_output):
    """ test all happy cases for the integer serializer """
    assert FloatSerializer.deserialize(inp) == expected_output


@pytest.mark.parametrize("unhappy_input", [
    "foo", "bar"
])
def test_float_deserializer_unhappy(unhappy_input):
    """ test all unhappy cases for the integer serializer """
    with pytest.raises(SerializerException):
        FloatSerializer.deserialize(unhappy_input)


@pytest.mark.parametrize("inp, expected_output", [
    ("true", True), ("false", False),
    ("yes", True), ("no", False),
])
def test_bool_deserializer_happy(inp, expected_output):
    assert BoolSerializer.deserialize(inp) is expected_output


@pytest.mark.parametrize("unhappy_input", [
    -1, 0.0
])
def test_bool_deserializer_unhappy(unhappy_input):
    """ test all unhappy cases for the integer serializer """
    with pytest.raises(SerializerException):
        BoolSerializer.deserialize(unhappy_input)


@pytest.mark.parametrize("inp, expected_output", [
    ("foo", "foo")
])
def test_string_deserializer_happy(inp, expected_output):
    assert StringSerializer.deserialize(inp) == expected_output


@pytest.mark.parametrize("unhappy_input", [
    -1, 0.0
])
def test_string_deserializer_unhappy(unhappy_input):
    """ test all unhappy cases for the integer serializer """
    with pytest.raises(SerializerException):
        StringSerializer.deserialize(unhappy_input)


@pytest.mark.parametrize("inp, expected_output", [
    (None, None)
])
def test_none_deserializer_happy(inp, expected_output):
    assert NoneSerializer.deserialize(inp) == expected_output


@pytest.mark.parametrize("unhappy_input", [
    -1,
])
def test_none_deserializer_unhappy(unhappy_input):
    """ test all unhappy cases for the integer serializer """
    with pytest.raises(SerializerException):
        NoneSerializer.deserialize(unhappy_input)
