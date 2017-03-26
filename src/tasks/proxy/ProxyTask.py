from abc import ABCMeta

from src.tasks.proxy.ProxyTraceable import ProxyTraceable


class ProxyTask(ProxyTraceable, metaclass=ABCMeta):
    def is_done(self) -> bool:
        raise AttributeError("attribute 'is_done' is not supported")

    def completeness(self) -> float:
        raise AttributeError("attribute 'completeness' is not supported")
