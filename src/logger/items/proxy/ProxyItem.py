from abc import ABCMeta, abstractmethod


class ProxyItem(metaclass=ABCMeta):
    @property
    def uid(self):
        return self._uid

    def __init__(self, uid: int):
        self._uid = uid
