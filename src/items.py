from abc import ABCMeta, abstractmethod
from multiprocessing import Value

from src.tasks import Task


class Item(metaclass=ABCMeta):
    @property
    def position(self):
        return self._position.value

    def set_position(self, position: int):
        with self._position.get_lock():
            self._position.value = position

    def __init__(self, position: int):
        self._position = Value("i", position)

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
        fill = int(self._length * self.completeness)
        empty = self._length - fill
        # percent = "{:03d}%".format(int(self.completeness * 100))
        # length = len(percent)
        # diff = int(abs(empty - fill))
        # if empty > fill:
        #     progress = "[{}{}{}{}]".format("█" * (fill - length), " " * diff, percent, " " * (empty - diff))
        # else:
        #     progress = "[{}{}{}{}]".format("█" * (fill - diff - length), percent, "█" * diff, " " * empty)
        progress = "[{}{}]".format("█" * fill, " " * empty)
        return self._description + " " + progress

    def update(self):
        self._task.update()

    def reset(self):
        self._task.reset()
