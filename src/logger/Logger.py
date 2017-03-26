from enum import Enum

from multiprocessing import Process, Value, Queue

import time

import sys

from src.items.Item import Item
from src.logger.HandledTypes import HandledTypes
from src.logger.proxy.Proxy import Proxy
from src.items.ProgressBar import ProgressBar
from src.items.TimeBar import TimeBar
from src.logger.Writer import Writer
from src.logger.proxy.ProxyWriter import ProxyWriter
from src.tasks.CounterTask import CounterTask
from src.tasks.MultiTask import MultiTask
from src.tasks.SimpleTask import SimpleTask


class Operation(Enum):
    CREATE = 1
    IMPACT = 2


class Logger(Process):
    def __init__(self, delay: int, stdout):
        self._stop_requests = Value("i", False)
        self._operations = Queue()
        self._max_id = Value("i", 0)
        self._delay = delay
        self._stdout = stdout
        self.writer = ProxyWriter(self, -1)
        super().__init__(target=self._handle)

    def stop(self):
        self._stop_requests.value = True

    def stopped(self) -> bool:
        return self._stop_requests.value

    def allot_uid(self):
        self._max_id.value += 1
        return self._max_id.value

    def create(self, proxy: Proxy, *args):
        args = [("proxy", arg.uid) if isinstance(arg, Proxy) else arg for arg in args]
        self._operations.put((Operation.CREATE, proxy.uid, proxy.type, args))

    def impact(self, proxy: Proxy, method: str, *args):
        args = [("proxy", arg.uid) if isinstance(arg, Proxy) else arg for arg in args]
        self._operations.put((Operation.IMPACT, proxy.uid, method, args))

    def wait(self):
        while not self._stop_requests.value and not self._operations.empty():
            time.sleep(self._delay)

    def _handle(self):
        objects = {}
        writer = Writer(self._stdout)
        builders = {
            HandledTypes.ProgressBar: ProgressBar,
            HandledTypes.TimeBar: TimeBar,
            HandledTypes.SimpleTask: SimpleTask,
            HandledTypes.CounterTask: CounterTask,
            HandledTypes.MultiTask: MultiTask,
            HandledTypes.Writer: lambda: writer
        }
        while not self._stop_requests.value:
            while not self._operations.empty():
                operation, *args = self._operations.get()
                if operation is Operation.CREATE:
                    uid, type_name, args = args
                    args = (objects[arg[1]] if isinstance(arg, tuple) and arg[0] == "proxy" else arg for arg in args)
                    instance = builders[type_name](*args)
                    objects[uid] = instance
                elif operation is Operation.IMPACT:
                    uid, method, args = args
                    args = (objects[arg[1]] if isinstance(arg, tuple) and arg[0] == "proxy" else arg for arg in args)
                    instance = objects[uid]
                    method = getattr(instance, method)
                    method(*args)
            writer.repaint()
            time.sleep(self._delay)
        writer.close()
