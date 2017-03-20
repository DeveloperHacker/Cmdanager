from abc import ABCMeta

from src.tasks.proxy.ProxyTraceable import ProxyTraceable


class ProxyTask(ProxyTraceable, metaclass=ABCMeta):
    def is_done(self) -> bool:
        return self._request("is_done").get()

    def completeness(self) -> float:
        return self._request("completeness").get()
