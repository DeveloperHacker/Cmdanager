from abc import ABCMeta, abstractmethod

from src.tasks import Task


class Item(metaclass=ABCMeta):
    @property
    def position(self):
        return self._position

    def __init__(self, position: int = 0):
        self._position = position

    def shift(self, shift: int):
        self._position += shift

    @abstractmethod
    def disconnect(self):
        pass

    @abstractmethod
    def to_line(self, max_line_length: int):
        pass


class ProgressBar(Item):
    def __init__(self, task: Task, repaint: callable, position: int = 0):
        super().__init__(position)
        self._task = task
        self._listener_index = task.add_progress_listener(lambda: repaint(self))

    def disconnect(self):
        self._task.remove_progress_listener(self._listener_index)

    def to_line(self, max_line_length: int):
        return "Progress: {:-3.0f}%".format(self._task.completeness() * 100)


class Line(Item):
    def __init__(self, string: str, position: int = 0):
        super().__init__(position)
        self._instance = string

    def to_line(self, max_line_length: int):
        return self._instance

    def disconnect(self):
        pass
