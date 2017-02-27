import logging
import os
import sys
import time

from src.items import Item, ProgressBar
from src.tasks import Task
from src.utils import expand


class Logger:
    _instance = None

    def __new__(cls, *args, **kwargs):
        return Logger._instance or object.__new__(Logger)

    def __init__(self, name=None):
        if Logger._instance is None:
            Logger._instance = self
            self.logger = logging.getLogger(name)
            self.logger.addHandler(Logger.Writer(sys.stdout))
            self._items = []
            self._cursor = 2
            term_size = os.get_terminal_size()
            self.default(term_size.columns, term_size.lines)

    # noinspection PyAttributeOutsideInit
    def default(self, width, height):
        self.max_lines = 1024
        self.width = width
        self.height = height

    def trace(self, foo):
        def wrapper(*args, **kwargs):
            name = foo.__name__
            self.info("Function \"{}\" is invoked".format(name))
            clock = time.time()
            result = foo(*args, **kwargs)
            delay = time.time() - clock
            h, m, s, ms = expand(delay)
            self.info("Function \"{}\" is ended".format(name))
            self.info("Work time {:02d}h {:02d}m {:02d}s {:03d}ms".format(h, m, s, ms))
            return result

        return wrapper

    def info(self, obj):
        self.writeln("INFO: " + str(obj))

    def print(self, obj):
        self.writeln(">>    " + str(obj))

    def progress_bar(self, task: Task):
        item = ProgressBar(task, self._cursor, self.repaint_item)
        self._items.append(item)
        line = self.format(item.to_line(self.width))
        self.writeln(line)

    def repaint_item(self, item: Item):
        if item.position > 0:
            self.set_cursor_pos(1, item.position)
            self.log(self.format(item.to_line(self.width)))
            self.set_cursor_pos(1, self._cursor)

    def writeln(self, text: str):
        lines = []
        for line in text.split('\n'):
            left = 0
            while len(line) > self.width:
                right = left + self.width
                lines.append(line[left:right])
                left = right
            lines.append(line[left:])
        self.log("\n".join(lines) + "\n")
        self._cursor += len(lines)
        shift = max(self._cursor - self.height, 0)
        self._cursor = min(self.height, self._cursor)
        connected = []
        for i, item in enumerate(self._items):
            # item.shift(-shift)
            if item.position <= 0:
                item.disconnect()
            else:
                self.repaint_item(item)
                connected.append(item)
        self._items = connected

    def set_cursor_pos(self, x: int, y: int):
        self.log("\033[{};{}H".format(y, x))

    def format(self, string: str):
        length = len(string)
        return string[:self.width] if length > self.width else string + " " * (self.width - length)

    def log(self, string: str):
        self.logger.log(logging.CRITICAL, string)

    class Writer(logging.Handler):
        def __init__(self, stream):
            logging.Handler.__init__(self)
            self.stream = stream

        def flush(self):
            self.acquire()
            try:
                self.stream.flush()
            finally:
                self.release()

        # noinspection PyBroadException
        def emit(self, record):
            try:
                self.stream.write(self.format(record))
                self.flush()
            except Exception:
                self.handleError(record)


logger = Logger()
