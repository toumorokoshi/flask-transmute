from abc import ABCMeta, abstractmethod
from collections import namedtuple
from .function import TransmuteFunction
from .utils import get_public_callables


RouteConfig = namedtuple("RouteConfig", ["path", "transmute_func"])


class RouteSet(object):
    """
    a base class for a set of routes. a particular framework should
    extend this class and override methods as necessary.
    """
    __metaclass__ = ABCMeta

    # this is a list of parameters that are important in the
    # context of transmute. This is available for extended route sets
    # to make decisions about which parameters to capture and which to pass
    # through to the framework's routing mechanism.
    transmute_params = TransmuteFunction.params

    # abstract methods (must be overriden)
    @abstractmethod
    def add_route_to_app(self, *args, **kwargs):
        """
        this is the only method that needs to be overriden. all the parameters
        required to add routes should be passed in, and at the end the application
        should have the desired routes attached.
        """
        pass

    # other methods that may be worth overriding
    def init_app(self, *args, **kwargs):
        for extension in self._extensions:
            extension.init_app(self, *args, **kwargs)

    # route function
    def route_function(self, path, function, **options):
        transmute_func = TransmuteFunction(function, **options)
        route_config = RouteConfig(path, transmute_func)
        self._routes.append(route_config)

    def route(self, path, **options):
        """
        to accomodate a more flask-like syntax, you can decorate a single
        method
        """

        def decorator(func):
            self.route_function(path, func, **options)
            return func

        return decorator

    @classmethod
    def _split_options_dict(cls, options_dict):
        """
        oftentimes specific route sets will find the need
        to split parameters between what should be consumed by transmute
        and what should be consumed by your framework's routing mechanism.

        this is a convenience method provided that will help that split for you,
        dividing any options dictionary into {transmute_options}, {other_options}.
        """
        transmute_options, other_options = {}, {}

        for k, v in options_dict.items():
            if k in cls.transmute_params:
                transmute_options[k] = v
            else:
                other_options[k] = v

        return transmute_options, other_options

    def __init__(self):
        self._routes = []
        self._extensions = []
        self._route_set_pairs = []

    def route_object(self, path, obj, **options):
        for method_name, func in get_public_callables(obj):
            func_path = "{0}/{1}".format(path, method_name)
            self.route_function(func_path, func)
