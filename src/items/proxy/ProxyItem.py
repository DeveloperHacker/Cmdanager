from abc import ABCMeta

from src.logger.proxy.Proxy import Proxy


class ProxyItem(Proxy, metaclass=ABCMeta):
    @property
    def width(self):
        raise AttributeError("attribute 'width' is not supported")

    def line(self, width: int):
        raise AttributeError("attribute 'line' is not supported")
