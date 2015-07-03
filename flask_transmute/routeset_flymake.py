from abc import ABCMeta, abstractmethod


class RouteSet(object):
    """
    a base class for a set of routes. a particular framework should
    extend this class and override methods as necessary.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def init_app(self, app):
        """ this is the only method that needs to be overriden. ""
        pass
