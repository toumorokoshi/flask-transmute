def mutates(f):
    """
    this labels a function as one that mutates data.
    """
    f.mutates = True
    return f


def annotate(annotations):
    """
    in python2, native annotions on parameters do not exist:
    def foo(a : str, b: int):
        ...

    this provides a way to provide attribute annotations:

    @annotate({"a": str, "b": int})
    def foo(a, b):
        ...
    """

    def decorate(func):
        func.__annotations__ = annotations
        return func

    return decorate
