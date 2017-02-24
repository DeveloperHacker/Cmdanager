from tasks import *


class TaskNotFoundException(Exception):
    def __init__(self, uid: int):
        super("Task with uid \"{}\" not found.".format(uid))


class TaskAlreadyTrackException(Exception):
    def __init__(self, uid: int):
        super("Task with uid \"{}\" is already tracked.".format(uid))


class Manager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        return Manager._instance or object.__new__(Manager)

    def __init__(self):
        if Manager._instance is None:
            Manager._instance = self

    _tasks = {}

    def unique_id(self) -> int:
        prev = None
        for uid in sorted(self._tasks.keys()):
            if prev and uid - prev != 1:
                return uid - 1
            prev = uid
        return prev + 1

    def simple_task(self, name: str = None) -> SimpleTask:
        task = SimpleTask(self.unique_id(), name)
        self.track(task)
        return task

    def counter_task(self, progress_length: int, name: str = None) -> CounterTask:
        task = CounterTask(progress_length, self.unique_id(), name)
        self.track(task)
        return task

    def multitask(self, name: str = None) -> MultiTask:
        task = MultiTask(self.unique_id(), name)
        self.track(task)
        return task

    def track(self, task: Task):
        if task.uid in self._tasks: raise TaskAlreadyTrackException(task.uid)
        self._tasks[task.uid] = task
        task.add_progress_listener(self._update)
        task.add_done_listener(self._done)

    def is_tracked(self, uid: int):
        return uid in self._tasks

    def remove(self, uid: int):
        if uid not in self._tasks: raise TaskNotFoundException(uid)
        del self._tasks[uid]

    def _update(self, task: Task):
        pass

    def _done(self, task: Task):
        pass
