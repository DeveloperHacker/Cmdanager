from src.logger.items.proxy.ProxyProgressBar import ProxyProgressBar
from src.logger.items.proxy.ProxyTimeBar import ProxyTimeBar
from src.logger.tasks.proxy.ProxyCounterTask import ProxyCounterTask
from src.logger.tasks.proxy.ProxySimpleTask import ProxySimpleTask
from src.logger.tasks.proxy.ProxyTask import ProxyTask

from src.logger import utils
from src.logger.Logger import Logger, Command
from src.logger.items.proxy.ProxyItem import ProxyItem
from src.logger.tasks.proxy.ProxyMultiTask import ProxyMultiTask


class ProxyLogger:
    def __init__(self, update_delay: int = 0.01, stdout: bool = True):
        self._items = {}
        self._tasks = {}
        self._logger = Logger(update_delay, stdout)
        self._item_builder = ProxyLogger.ItemBuilder(self)
        self._task_builder = ProxyLogger.TaskBuilder(self)

    @property
    def item(self) -> 'ProxyLogger.ItemBuilder':
        return self._item_builder

    @property
    def task(self) -> 'ProxyLogger.TaskBuilder':
        return self._task_builder

    def print(self, *items):
        self._logger.execute(Command.SHOW, *items)

    def start(self):
        self._logger.start()

    def join(self):
        self._logger.wait()
        self._logger.stop()

    def open(self, file_name: str, *args):
        self._logger.execute(Command.OPEN, file_name, *args)

    def __enter__(self) -> 'ProxyLogger':
        self.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.join()

    class TaskBuilder:
        def __init__(self, parent: 'ProxyLogger'):
            self._parent = parent

        def simple(self) -> ProxySimpleTask:
            uid = utils.unique_integer_key(self._parent._tasks)
            task = ProxySimpleTask(uid)
            self._parent._tasks[uid] = task
            self._parent._logger.execute(Command.COUNTER_TASK, task)
            return task

        def counter(self, length: int) -> ProxyCounterTask:
            uid = utils.unique_integer_key(self._parent._tasks)
            task = ProxyCounterTask(uid, length)
            self._parent._tasks[uid] = task
            self._parent._logger.execute(Command.COUNTER_TASK, task)
            return task

        def multi(self, *tasks) -> ProxyMultiTask:
            uid = utils.unique_integer_key(self._parent._tasks)
            task = ProxyMultiTask(uid, *tasks)
            self._parent._tasks[uid] = task
            self._parent._logger.execute(Command.MULTI_TASK, task)
            return task

    class ItemBuilder:
        def __init__(self, parent: 'ProxyLogger'):
            self._parent = parent

        def progress(self, task: ProxyTask, width: int = 50) -> ProxyProgressBar:
            uid = utils.unique_integer_key(self._parent._items)
            item = ProxyProgressBar(uid, width, task)
            self._parent._items[uid] = item
            self._parent._logger.execute(Command.PROGRESS_BAR, item)
            return item

        def counter(self, length: int, width: int = 50) -> ProxyProgressBar:
            task = self._parent.task.counter(length)
            return self.progress(task, width)

        def time(self) -> ProxyTimeBar:
            uid = utils.unique_integer_key(self._parent._items)
            item = ProxyTimeBar(uid)
            self._parent._items[uid] = item
            self._parent._logger.execute(Command.TIME_BAR, item)
            return item

        def proxy(self, uid: int) -> ProxyItem:
            return self._parent._items[uid]
