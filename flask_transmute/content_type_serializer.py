"""
contains the logic that handles serialization to and from markup
types.
"""
from abc import ABCMeta, abstractmethod


class ContentTypeSerializer(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def foo():
        pass
