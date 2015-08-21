import inspect


def get_public_callables(obj):
    """
    return an iterator over all public callables of a function
    """
    for key in dir(obj):
        if key.startswith('_'):
            continue
        value = getattr(obj, key)
        if callable(value):
            yield key, value


def get_raw_function(func):
    if inspect.ismethod(func):
        return func.__func__
    else:
        return func


def join_url_paths(*parts):
    path = parts[0]
    for p in parts[1:]:
        if path == "":
            path = p
        else:
            path = "{0}/{1}".format(path.rstrip("/"), p.lstrip("/"))
    return path
