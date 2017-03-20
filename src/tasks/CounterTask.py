from src.tasks.Task import Task


class CounterTask(Task):
    def __init__(self, uid: int, length: int):
        super(CounterTask, self).__init__(uid)
        self._progress = 0
        self._length = length

    def is_done(self) -> bool:
        return self._progress >= self._length

    def _update(self):
        self._progress += 1

    def _reset(self):
        self._progress.value = 0

    def completeness(self) -> float:
        return self._progress / self._length
