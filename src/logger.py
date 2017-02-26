import os
import time
import sys
from src.utils import expand
from src.items import Item, ProgressBar
from src.tasks import Task


class Logger:
    _instance = None

    def __new__(cls, *args, **kwargs):
        return Logger._instance or object.__new__(Logger)

    def __init__(self):
        if Logger._instance is None:
            Logger._instance = self
            self._items = []
            self._cursor = 2
            term_size = os.get_terminal_size()
            self.default(term_size.columns, term_size.lines)
            self.log_file = None

    # noinspection PyAttributeOutsideInit
    def default(self, width, height):
        self.max_lines = 1024
        self.width = width
        self.height = height
        # print(width, height)

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

    # def add_text(self, text: str):
    #     lines = []
    #     for line in text.split('\n'):
    #         left = 0
    #         while len(line) > self.width:
    #             right = left + self.width
    #             lines.append(line[left:right])
    #             left = right
    #         lines.append(line[left:])
    #     self.add_items([Line(line) for line in lines])


    # def add_items(self, items: list):
    #     self._items.extend(items)
    #     dlength = len(self._items) - self.max_lines
    #     if dlength > 0:
    #         for i in range(dlength + 1):
    #             self._items[i].disconnect()
    #         del self._items[:dlength]
    #     for item in self._items:
    #         item.shift(len(items))
    #     self.repaint()

    # def repaint(self):
    #     visible_items = self._items[-min(self.height, len(self._items)):]
    #     line_generator = (self.format(item.to_line(self.width)) for item in visible_items)
    #     Logger.set_cursor_pos(1, 1)
    #     self.write("\n".join(line_generator))
    #     Logger.set_cursor_pos(self.width, self.height)

    def repaint_item(self, item: Item):
        if item.position > 0:
            Logger.set_cursor_pos(1, item.position)
            sys.stdout.write(self.format(item.to_line(self.width)))
            sys.stdout.flush()
            Logger.set_cursor_pos(1, self._cursor)

    def writeln(self, text: str):
        if self.log_file is not None:
            self.log_file.write(text + "\n")
            self.log_file.flush()
        lines = []
        for line in text.split('\n'):
            left = 0
            while len(line) > self.width:
                right = left + self.width
                lines.append(line[left:right])
                left = right
            lines.append(line[left:])
        sys.stdout.write("\n".join(lines) + "\n")
        sys.stdout.flush()
        self._cursor += len(lines)
        shift = max(self._cursor - self.height, 0)
        self._cursor = min(self.height, self._cursor)
        connected = []
        for i, item in enumerate(self._items):
            item.shift(-shift)
            if item.position <= 0:
                item.disconnect()
            else:
                self.repaint_item(item)
                connected.append(item)
        self._items = connected

    @staticmethod
    def set_cursor_pos(x: int, y: int):
        sys.stdout.write("\033[{};{}H".format(y, x))
        sys.stdout.flush()

    def format(self, string: str):
        length = len(string)
        return string[:self.width] if length > self.width else string + " " * (self.width - length)


logger = Logger()
