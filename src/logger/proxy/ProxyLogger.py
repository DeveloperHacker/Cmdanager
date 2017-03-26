import sys
from multiprocessing import Pool

from src.items.proxy.ProxyTimeBar import ProxyTimeBar
from src.tasks.proxy.ProxyCounterTask import ProxyCounterTask
from src.tasks.proxy.ProxyMultiTask import ProxyMultiTask
from src.tasks.proxy.ProxySimpleTask import ProxySimpleTask
from src.tasks.proxy.ProxyTask import ProxyTask

from src.items.proxy.ProxyProgressBar import ProxyProgressBar
from src.logger.Logger import Logger


def wrapper(counter: ProxyCounterTask, handle, *args):
    counter.update()
    return handle(*args)


class ProxyLogger:
    def __init__(self, update_delay: int = 0.01):
        self._stdout = sys.stdout
        self._logger = Logger(update_delay, self._stdout)
        sys.stdout = self._logger.writer
        self._item_builder = ProxyLogger.ItemBuilder(self)
        self._task_builder = ProxyLogger.TaskBuilder(self)
        self._iterator_builder = ProxyLogger.IteratorBuilder(self)

    @property
    def item(self) -> 'ProxyLogger.ItemBuilder':
        return self._item_builder

    @property
    def task(self) -> 'ProxyLogger.TaskBuilder':
        return self._task_builder

    @property
    def iterators(self) -> 'ProxyLogger.IteratorBuilder':
        return self._iterator_builder

    def print(self, *items):
        self._logger.writer.print(*items)

    def open(self, file_name: str, mode='r', encoding=None):
        self._logger.writer.open(mode, encoding)

    def start(self):
        self._logger.start()

    def join(self):
        self._logger.wait()
        self._logger.stop()
        sys.stdout = self._stdout

    def __enter__(self) -> 'ProxyLogger':
        self.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.join()

    class TaskBuilder:
        def __init__(self, parent: 'ProxyLogger'):
            self._parent = parent

        def simple(self) -> ProxySimpleTask:
            proxy_uid = self._parent._logger.allot_uid()
            task = ProxySimpleTask(proxy_uid, self._parent._logger)
            return task

        def counter(self, length: int) -> ProxyCounterTask:
            proxy_uid = self._parent._logger.allot_uid()
            task = ProxyCounterTask(proxy_uid, self._parent._logger, length)
            return task

        def multi(self, *tasks) -> ProxyMultiTask:
            proxy_uid = self._parent._logger.allot_uid()
            task = ProxyMultiTask(proxy_uid, self._parent._logger, *tasks)
            return task

    class ItemBuilder:
        def __init__(self, parent: 'ProxyLogger'):
            self._parent = parent

        def progress(self, task: ProxyTask, width: int = 50) -> ProxyProgressBar:
            proxy_uid = self._parent._logger.allot_uid()
            item = ProxyProgressBar(proxy_uid, self._parent._logger, width, task)
            return item

        def counter(self, length: int, width: int = 50) -> ProxyProgressBar:
            task = self._parent.task.counter(length)
            item = self.progress(task, width)
            return item

        def time(self) -> ProxyTimeBar:
            proxy_uid = self._parent._logger.allot_uid()
            item = ProxyTimeBar(proxy_uid, self._parent._logger)
            return item

    class IteratorBuilder:
        def __init__(self, parent: 'ProxyLogger'):
            self._parent = parent

        def map(self, handle, args, pool: Pool):
            counter = self._parent.item.counter(len(args))
            self._parent.print("Mapping ", counter)
            args = [(counter, handle, arg) for arg in args]
            return pool.starmap(wrapper, args)

        def star_map(self, handle, args, pool=None):
            pass

        def foreach(self, handle, args, pool=None):
            pass

        def star_foreach(self, handle, args, pool=None):
            pass

        def reduce(self, handle, args, pool=None):
            pass

        def star_reduce(self, handle, args, pool=None):
            pass
