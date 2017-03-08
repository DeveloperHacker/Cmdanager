from src.logger.tasks.Task import Task


class SimpleTask(Task):
    def __init__(self, uid: int):
        super(SimpleTask, self).__init__(uid)
        self._is_done = False

    def is_done(self) -> bool:
        return self._is_done

    def _update(self):
        self._is_done = True

    def _reset(self):
        self._is_done = False

    def completeness(self) -> float:
        return float(self._is_done)
