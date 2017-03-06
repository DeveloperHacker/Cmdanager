from abc import ABCMeta, abstractmethod
from multiprocessing import Value

from src.traceable import Traceable


class Item(metaclass=ABCMeta):
    @property
    def width(self):
        return self._width

    @property
    def x(self):
        return self._x.value

    @property
    def y(self):
        return self._y.value

    def set_x(self, x: int):
        with self._x.get_lock():
            self._x.value = x

    def set_y(self, y: int):
        with self._y.get_lock():
            self._y.value = y

    def set_position(self, x: int, y: int):
        with self._x.get_lock(), self._y.get_lock():
            self._x.value = x
            self._y.value = y

    def __init__(self, x: int, y: int, width: int):
        self._x = Value("i", x)
        self._y = Value("i", y)
        self._width = width

    @abstractmethod
    def to_line(self, max_line_length: int):
        pass


class ProgressBar(Item):
    @property
    def completeness(self):
        return self._task.value()

    @property
    def length(self):
        return self._length


    def __init__(self, x: int, y: int, length: int, traceable: Traceable, repaint: callable):
        super().__init__(x, y, length)
        self._task = traceable
        self._length = length
        self._listener_index = traceable.add(lambda: repaint(self))

    def to_line(self, max_line_length: int):
        percent = "{:-3d}%".format(int(self.completeness * 100))
        fill = int(self._length * self.completeness)
        empty = self._length - fill
        length = len(percent)
        segment = (self._length - length) // 2
        left = min(segment, fill)
        right = min(segment, empty)
        progress = ["█" * left, " " * (segment - left), percent, "█" * (segment - right), " " * right]
        return "|{}|".format("".join(progress))

    def update(self):
        self._task.update()

    def reset(self):
        self._task.reset()
