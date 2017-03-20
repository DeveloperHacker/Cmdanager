from abc import abstractmethod, ABCMeta

from src.utils import unique_integer_key


class Traceable(metaclass=ABCMeta):
    def __init__(self):
        self._update_listeners = {}

    def add(self, listener, *args, **kwargs) -> int:
        uid = unique_integer_key(self._update_listeners)
        self._update_listeners[uid] = (listener, args, kwargs)
        return uid

    def remove(self, uid: int):
        del self._update_listeners[uid]

    def update(self):
        self._update()
        for key, (listener, args, kwargs) in self._update_listeners.items():
            listener(*args, **kwargs)

    def reset(self):
        self._reset()
        self.update()

    @abstractmethod
    def _update(self):
        pass

    @abstractmethod
    def _reset(self):
        pass
