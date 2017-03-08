import time
from enum import Enum
from multiprocessing import Process, Value, Queue

from src.logger.items.proxy.ProxyProgressBar import ProxyProgressBar
from src.logger.items.proxy.ProxyTimeBar import ProxyTimeBar
from src.logger.tasks.proxy.ProxyCounterTask import ProxyCounterTask
from src.logger.tasks.proxy.ProxySimpleTask import ProxySimpleTask

from src.logger.Writer import Writer
from src.logger.items.ProgressBar import ProgressBar
from src.logger.items.TimeBar import TimeBar
from src.logger.items.proxy.ProxyItem import ProxyItem
from src.logger.tasks.CounterTask import CounterTask
from src.logger.tasks.MultiTask import MultiTask
from src.logger.tasks.SimpleTask import SimpleTask
from src.logger.tasks.proxy.ProxyMultiTask import ProxyMultiTask


class Command(Enum):
    SHOW = 1
    OPEN = 2
    PROGRESS_BAR = 3
    TIME_BAR = 4
    SIMPLE_TASK = 5
    COUNTER_TASK = 6
    MULTI_TASK = 7


class Logger(Process):
    def __init__(self, delay: float, stdout: bool):
        self._stop_requests = Value("i", False)
        self._queue = Queue()
        self._commands = Value("i", 0)
        self._delay = delay
        self._stdout = stdout
        super().__init__(target=self._handle)

    def execute(self, command: Command, *args, **kwargs):
        with self._commands.get_lock():
            self._commands.value += 1
            self._queue.put((command, args, kwargs))

    def stop(self):
        self._stop_requests.value = True

    def wait(self, timeout: float = float("inf")):
        delay = 0.0
        while not self._stop_requests.value and self._commands.value != 0:
            time.sleep(self._delay)
            delay += self._delay
            if delay > timeout:
                break

    def _handle(self):
        items = {}
        tasks = {}
        with Writer(self._stdout) as writer:
            while not self._stop_requests.value:
                with self._commands.get_lock():
                    while not self._queue.empty():
                        command, args, kwargs = self._queue.get()
                        self._commands.value -= 1
                        if command is Command.SHOW:
                            args = [(items[arg.uid] if isinstance(arg, ProxyItem) else arg) for arg in args]
                            writer.show(*args)
                        elif command is Command.PROGRESS_BAR:
                            proxy = args[0]  # type: ProxyProgressBar
                            task = tasks[proxy.task.uid]
                            item = ProgressBar(proxy.uid, proxy.width, task)
                            items[item.uid] = item
                            writer.add_item(item)
                        elif command is Command.TIME_BAR:
                            proxy = args[0]  # type: ProxyTimeBar
                            item = TimeBar(proxy.uid)
                            items[item.uid] = item
                            writer.add_item(item)
                        elif command is Command.SIMPLE_TASK:
                            proxy = args[0]  # type: ProxySimpleTask
                            task = SimpleTask(proxy.uid)
                            tasks[task.uid] = task
                        elif command is Command.COUNTER_TASK:
                            proxy = args[0]  # type: ProxyCounterTask
                            task = CounterTask(proxy.uid, proxy.length)
                            tasks[task.uid] = task
                        elif command is Command.MULTI_TASK:
                            proxy = args[0]  # type: ProxyMultiTask
                            task = MultiTask(proxy.uid, *proxy.tasks)
                            tasks[task.uid] = task
                        elif command is Command.OPEN:
                            writer.open(*args, **kwargs)
                writer.repaint()
                time.sleep(self._delay)
