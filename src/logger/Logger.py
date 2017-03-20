import sys
import time
from enum import Enum
from multiprocessing import Process, Value, Manager

from src.items.Item import Item
from src.items.ProgressBar import ProgressBar
from src.items.TimeBar import TimeBar
from src.logger.Writer import Writer
from src.logger.proxy.Proxy import Future
from src.tasks.CounterTask import CounterTask
from src.tasks.MultiTask import MultiTask
from src.tasks.SimpleTask import SimpleTask


class Operation(Enum):
    create = 1
    impact = 2
    request = 3


class Logger(Process):
    def __init__(self, delay: float, stdout: bool):
        self._delay = delay
        self._stdout = stdout
        self._stop_requests = Value("i", False)
        manager = Manager()
        self._object_uid = Value("i", 0)
        self._results = manager.dict()
        self._future_uid = Value("i", 0)
        self._operations = manager.list()
        super().__init__(target=self._handle)

    def stop(self):
        self._stop_requests.value = True

    def proxy_uid(self) -> int:
        with self._object_uid.get_lock():
            object_uid = self._object_uid.value
            self._object_uid.value += 1
        return object_uid

    def future_uid(self) -> int:
        with self._future_uid.get_lock():
            future_uid = self._future_uid.value
            self._future_uid.value += 1
        return future_uid

    def create(self, proxy_uid: int, type_name: str, *args, **kwargs):
        self._operations.append((Operation.create, proxy_uid, type_name, args, kwargs))

    def impact(self, proxy_uid: int, method_name: str, *args, **kwargs):
        self._operations.append((Operation.impact, proxy_uid, method_name, args, kwargs))

    def request(self, proxy_uid: int, future_uid: int, method_name: str, *args, **kwargs) -> Future:
        self._operations.append((Operation.request, proxy_uid, future_uid, method_name, args, kwargs))
        return Future(future_uid, self)

    def wait_result(self, future_uid: int, timeout: float = float("inf")):
        delay = 0.0
        while not self._stop_requests.value and future_uid not in self._results:
            time.sleep(self._delay)
            delay += self._delay
            if delay > timeout:
                break
        with self._results.get_lock():
            result = self._results[future_uid]
            del self._results[future_uid]
        return result

    def wait(self):
        while not self._stop_requests.value and len(self._operations) > 0:
            time.sleep(self._delay)

    def open(self, file_name: str, *args):
        self.impact(-1, "open", file_name, *args)

    def print(self, *items):
        self.impact(-1, "show", *items)

    def error(self, message):
        sys.stderr.write(message + "\n")
        sys.stderr.flush()
        self._stop_requests.value = True

    def _handle(self):
        builders = {
            "ProgressBar": ProgressBar,
            "TimeBar": TimeBar,
            "SimpleTask": SimpleTask,
            "CounterTask": CounterTask,
            "MultiTask": MultiTask,
        }
        objects = {}
        with Writer(self._stdout) as writer:
            objects[-1] = writer
            while not self._stop_requests.value:
                while len(self._operations) > 0:
                    operation, *args = self._operations.pop()
                    if operation is Operation.create:
                        uid, type_name, args, kwargs = args
                        print(type_name)
                        instance = builders[type_name](*args, **kwargs)
                        if isinstance(instance, Item):
                            writer.add_item(instance)
                        objects[uid] = instance
                    elif operation is Operation.impact:
                        proxy_uid, method_name, args, kwargs = args
                        instance = objects[proxy_uid]
                        method = getattr(instance, method_name)
                        method(*args, **kwargs)
                    elif operation is Operation.request:
                        proxy_uid, future_uid, method_name, args, kwargs = args
                        instance = objects[proxy_uid]
                        method = getattr(instance, method_name)
                        result = method(*args, **kwargs)
                        self._results[future_uid] = result
            writer.repaint()
            time.sleep(self._delay)
