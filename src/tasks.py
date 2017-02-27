from abc import ABCMeta, abstractmethod

from src.utils import unique_integer_key


class Task(metaclass=ABCMeta):
    @property
    def name(self):
        return self._name

    @property
    def uid(self):
        return self._uid

    def __init__(self, uid: int, name: str = None):
        super().__init__()
        self._name = name or "task{}".format(uid)
        self._uid = uid
        self._done_listeners = {}
        self._progress_listeners = {}

    def add_done_listener(self, listener) -> int:
        uid = unique_integer_key(self._done_listeners)
        self._done_listeners[uid] = listener
        return uid

    def add_progress_listener(self, listener) -> int:
        uid = unique_integer_key(self._progress_listeners)
        self._progress_listeners[uid] = listener
        return uid

    def remove_done_listener(self, uid: int):
        del self._done_listeners[uid]

    def remove_progress_listener(self, uid: int):
        del self._progress_listeners[uid]

    def _update(self):
        for key, listener in self._progress_listeners.items():
            listener()

    def _done(self):
        for key, listener in self._done_listeners.items():
            listener()

    @abstractmethod
    def is_done(self):
        pass

    @abstractmethod
    def completeness(self) -> float:
        pass


class SimpleTask(Task):
    def __init__(self, uid: int, name: str = None):
        super(SimpleTask, self).__init__(uid, name)
        self._is_done = False

    def is_done(self):
        return self._is_done

    def done(self):
        if not self.is_done():
            self._update()
            self._done()
            self._is_done = True

    def completeness(self) -> float:
        return int(self._is_done)


class CounterTask(Task):
    def __init__(self, progress_length: int, uid: int, name: str = None):
        super(CounterTask, self).__init__(uid, name)
        self._progress_counter = 0
        self._progress_length = progress_length

    def is_done(self):
        return self._progress_counter == self._progress_length

    def update(self):
        if not self.is_done():
            self._progress_counter += 1
            self._update()
            if self.is_done():
                self._done()

    def completeness(self) -> float:
        return self._progress_counter / self._progress_length

    def reset(self):
        self._progress_counter = 0


class MultiTask(Task):
    def __init__(self, uid: int, name: str = None):
        super(MultiTask, self).__init__(uid, name)
        self._sub_tasks = []

    def _sub_progress_listener(self, _: Task):
        self._update()

    def _sub_done_listener(self, _: Task):
        if self.is_done():
            self._done()

    def is_done(self):
        return all((task.is_done() for task in self._sub_tasks))

    def add_sub_task(self, task: Task) -> 'MultiTask':
        self._sub_tasks.append(task)
        task.add_progress_listener(self._sub_progress_listener)
        task.add_done_listener(self._sub_done_listener)
        return self

    def add(self, task: Task) -> 'MultiTask':
        return self.add_sub_task(task)

    def completeness(self) -> float:
        if len(self._sub_tasks) == 0: return 1.0
        acc = 0.0
        for task in self._sub_tasks:
            acc += task.completeness()
        return acc / len(self._sub_tasks)
