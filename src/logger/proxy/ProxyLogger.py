from src.items.proxy.ProxyTimeBar import ProxyTimeBar
from src.tasks.proxy.ProxyCounterTask import ProxyCounterTask
from src.tasks.proxy.ProxyMultiTask import ProxyMultiTask
from src.tasks.proxy.ProxySimpleTask import ProxySimpleTask
from src.tasks.proxy.ProxyTask import ProxyTask

from src.items.proxy.ProxyProgressBar import ProxyProgressBar
from src.logger.Logger import Logger


class ProxyLogger:
    def __init__(self, update_delay: int = 0.01, stdout: bool = True):
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
        self._logger.print(*items)

    def open(self, file_name: str, *args):
        self._logger.open(file_name, *args)

    def start(self):
        self._logger.start()

    def join(self):
        self._logger.wait()
        self._logger.stop()

    def __enter__(self) -> 'ProxyLogger':
        self.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.join()

    class TaskBuilder:
        def __init__(self, parent: 'ProxyLogger'):
            self._parent = parent

        def simple(self) -> ProxySimpleTask:
            proxy_uid = self._parent._logger.proxy_uid()
            task = ProxySimpleTask(proxy_uid, self._parent._logger)
            return task

        def counter(self, length: int) -> ProxyCounterTask:
            proxy_uid = self._parent._logger.proxy_uid()
            task = ProxyCounterTask(proxy_uid, self._parent._logger, length)
            return task

        def multi(self, *tasks) -> ProxyMultiTask:
            proxy_uid = self._parent._logger.proxy_uid()
            task = ProxyMultiTask(proxy_uid, self._parent._logger, *tasks)
            return task

    class ItemBuilder:
        def __init__(self, parent: 'ProxyLogger'):
            self._parent = parent

        def progress(self, task: ProxyTask, width: int = 50) -> ProxyProgressBar:
            proxy_uid = self._parent._logger.proxy_uid()
            item = ProxyProgressBar(proxy_uid, self._parent._logger, width, task)
            return item

        def counter(self, length: int, width: int = 50) -> ProxyProgressBar:
            task = self._parent.task.counter(length)
            item = self.progress(task, width)
            return item

        def time(self) -> ProxyTimeBar:
            proxy_uid = self._parent._logger.proxy_uid()
            item = ProxyTimeBar(proxy_uid, self._parent._logger)
            return item
