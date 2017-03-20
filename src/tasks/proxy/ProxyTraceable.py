from abc import ABCMeta

from src.logger.proxy.Proxy import Proxy


class ProxyTraceable(Proxy, metaclass=ABCMeta):
    def update(self):
        self._impact("update")

    def reset(self):
        self._impact("reset")
