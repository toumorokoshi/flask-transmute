import tornado.web


class HandlerFactory(object):
    """
    HandleFactory handles aggregating transmute functions
    into a set of handlers.
    """

    def __init__(self):
        self._handlers = {}

    def add_handler(self, path, transmute_func):
        if path not in self._handlers:
            self._handlers[path] = _create_handler()

        handler = self._handlers[path]

        _add_transmute_func_to_handler(transmute_func, handler)

    def get_handler_tuples(self):
        handlers = []
        for path, handler in self._handlers.items():
            handlers.append((path, handler))
        return handlers


def _create_handler():

    class Handler(tornado.web.RequestHandler):
        pass

    return Handler

METHOD_MAP = {
    "creates": "PUT",
    "deletes": "delete",
    "updates": "POST",
}


def _add_transmute_func_to_handler(transmute_func, handler):
    handler_method = _generate_handler_method(transmute_func)

    is_get = True
    for attr, method in METHOD_MAP.items():
        if getattr(transmute_func, attr, False):
            is_get = False
            setattr(handler, attr.lower(), handler_method)

    if is_get:
        setattr(handler, "get", handler_method)


def _generate_handler_method(transmute_func):

    def method(self):
        self.write(transmute_func.description)

    return method
