from abc import ABCMeta, abstractmethod
from multiprocessing import Value

from src.tasks import Task


class Item(metaclass=ABCMeta):
    @property
    def position(self):
        return self._position.value

    @property
    def width(self):
        return self._width

    def set_position(self, position: int):
        with self._position.get_lock():
            self._position.value = position

    def __init__(self, position: int, width: int):
        self._position = Value("i", position)
        self._width = width

    @abstractmethod
    def to_line(self, max_line_length: int):
        pass


class ProgressBar(Item):
    @property
    def completeness(self):
        return self._task.completeness()

    @property
    def length(self):
        return self._length

    @property
    def description(self):
        return self._description

    def __init__(self, length: int, description: str, task: Task, position: int, repaint: callable):
        super().__init__(position)
        self._task = task
        self._length = length
        self._description = description
        self._listener_index = task.add(lambda: repaint(self))

    def to_line(self, max_line_length: int):
        percent = "{:-3d}%".format(int(self.completeness * 100))
        fill = int(self._length * self.completeness)
        empty = self._length - fill
        length = len(percent)
        segment = (self._length - length) // 2
        left = min(segment, fill)
        right = min(segment, empty)
        progress = ["█" * left, " " * (segment - left), percent, "█" * (segment - right), " " * right]
        return "{} |{}|".format(self.description, "".join(progress))

    def update(self):
        self._task.update()

    def reset(self):
        self._task.reset()
