import time

from src import utils
from src.items.Item import Item


class TimeBar(Item):
    def __init__(self, uid: int):
        super().__init__(uid, 17)
        self._stop = False
        self._start = time.time()
        self._value = 0

    def reset(self):
        self._stop = False
        self._start = time.time()
        self._value = 0

    def stop(self):
        self._update()
        self._stop = True

    def _update(self):
        self._value = time.time() - self._start

    def line(self, width: int) -> str:
        self._update()
        return utils.expand(self._value)
