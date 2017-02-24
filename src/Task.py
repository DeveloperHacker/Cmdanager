from abc import ABCMeta, abstractmethod


class Task(metaclass=ABCMeta):
    @property
    def name(self):
        return self.__name

    @property
    def uid(self):
        return self.__uid

    def __init__(self, uid: int, name: str = None):
        self.__name = name or "task{}".format(uid)
        self.__uid = uid
        self.__done_listeners = []
        self.__progress_listeners = []

    @abstractmethod
    def is_done(self):
        pass

    def add_done_listener(self, listener):
        self.__done_listeners.append(listener)

    def add_progress_listener(self, listener):
        self.__progress_listeners.append(listener)

    def _update(self):
        for listener in self.__done_listeners:
            listener(self)

    def _done(self):
        for listener in self.__done_listeners:
            listener(self)


class SimpleTask(Task):
    def __init__(self, uid: int, name: str = None):
        super(SimpleTask, self).__init__(uid, name)
        self.__is_done = False

    def is_done(self):
        return self.__is_done

    def done(self):
        if not self.is_done():
            self._update()
            self._done()
            self.__is_done = True


class CounterTask(Task):
    def __init__(self, progress_length: int, uid: int, name: str = None):
        super(CounterTask, self).__init__(uid, name)
        self.__progress_counter = 0
        self.__progress_length = progress_length

    def is_done(self):
        return self.__progress_counter == self.__progress_length

    def update(self):
        if not self.is_done():
            self.__progress_counter += 1
            self._update()
            if self.is_done():
                self._done()


class MultiTask(Task):
    def __init__(self, uid: int, name: str = None):
        super(MultiTask, self).__init__(uid, name)
        self.__sub_tasks = []

    def __sub_progress_listener(self, _: Task):
        self._update()

    def __sub_done_listener(self, _: Task):
        if self.is_done():
            self._done()

    def is_done(self):
        return all((task.is_done() for task in self.__sub_tasks))

    def add_sub_task(self, task: Task):
        self.__sub_tasks.append(task)
        task.add_progress_listener(self.__sub_progress_listener)
        task.add_done_listener(self.__sub_done_listener)
