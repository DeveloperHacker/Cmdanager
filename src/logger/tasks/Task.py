from abc import abstractmethod

from src.logger.tasks.Traceable import Traceable


class Task(Traceable):
    @property
    def uid(self):
        return self._uid

    def __init__(self, uid: int):
        super().__init__()
        self._uid = uid

    @abstractmethod
    def is_done(self):
        pass

    @abstractmethod
    def completeness(self) -> float:
        pass
