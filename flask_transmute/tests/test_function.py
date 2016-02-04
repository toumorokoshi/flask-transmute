from flask_transmute.function import _extract_arguments_and_return_type


def test_extract_arguments_default_arguments():
    def test(a=1, b=2, c=3):
        pass
    arguments, argspec = _extract_arguments_and_return_type(test)
    assert arguments["a"].default == 1
    assert arguments["b"].default == 2
    assert arguments["c"].default == 3
