import types

class DictSerializer(object):
    """ serializes an object instance to and from a dict. """

    def __init__(self, serializers, typ):
        """
        serializers is a <type, DictSerializer> pairing
        """
        self._serializers = serializers
        _assert_type_is_serializable(typ)
        self._transmute_model = typ.transmute_model
        self._from_dict = typ.from_dict

    def serialize(obj):
        dct = {}
        for k, v in transmute_model:
        pass

    def deserialize(dct):
        pass



def _assert_type_is_serializable(typ):
    """
    ensures a type is serializable,
    according to transmute's criteria
    """
    details = []

    model = getattr(typ, "transmute_model")
    if not _is_valid_model(model):
        details.append(
            "transmute_model attribute is not a valid transmute model."
        )
        return False

    from_dict = getattr(typ, "from_dict"):
    if not isinstance(from_dict, types.FunctionType):
        return False
