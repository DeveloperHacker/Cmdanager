from abc import ABCMeta, abstractmethod

from logger import Tracked


class Task(Tracked, metaclass=ABCMeta):
    @property
    def name(self):
        return self._name

    @property
    def uid(self):
        return self._uid

    def __init__(self, uid: int, name: str = None):
        self._name = name or "task{}".format(uid)
        self._uid = uid
        self._done_listeners = []
        self._progress_listeners = []

    @abstractmethod
    def is_done(self):
        pass

    def add_done_listener(self, listener) -> 'Task':
        self._done_listeners.append(listener)
        return self

    def add_progress_listener(self, listener) -> 'Task':
        self._progress_listeners.append(listener)
        return self

    def _update(self):
        for listener in self._done_listeners:
            listener(self)

    def _done(self):
        for listener in self._done_listeners:
            listener(self)


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
