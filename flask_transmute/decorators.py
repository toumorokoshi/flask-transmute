def updates(f):
    """
    this labels a function as one that updates data.
    """
    f.updates = True
    return f


def creates(f):
    """
    this labels a function as one that creates data.
    """
    f.creates = True
    return f


def deletes(f):
    """
    this labels a function as one that deletes data.
    """
    f.deletes = True
    return f


def annotate(annotations):
    """
    in python2, native annotions on parameters do not exist:
    def foo(a : str, b: int) -> bool:
        ...

    this provides a way to provide attribute annotations:

    @annotate({"a": str, "b": int, "return": bool})
    def foo(a, b):
        ...
    """

    def decorate(func):
        func.__annotations__ = annotations
        return func

    return decorate
