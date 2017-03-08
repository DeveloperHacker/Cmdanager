from abc import ABCMeta

from src.logger.tasks.proxy.ProxyTraceable import ProxyTraceable


class ProxyTask(ProxyTraceable, metaclass=ABCMeta):
    @property
    def uid(self):
        return self._uid

    def __init__(self, uid: int):
        self._uid = uid

    # TODO:
    def is_done(self) -> bool:
        pass

    # TODO:
    def completeness(self) -> float:
        pass
