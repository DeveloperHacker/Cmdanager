from abc import ABCMeta, abstractmethod

from src.utils import Point


class Item(Point, metaclass=ABCMeta):
    @property
    def uid(self):
        return self._uid

    @property
    def width(self):
        return self._width

    def __init__(self, uid: int, width: int):
        super().__init__(1, -1)
        self._uid = uid
        self._x = 1
        self._y = -1
        self._width = width

    @abstractmethod
    def line(self, width: int):
        pass
