import os
import time
import sys
from src.clock import expand
from src.items import Item, ProgressBar, Line
from src.tasks import Task


class Logger:
    _instance = None

    def __new__(cls, *args, **kwargs):
        return Logger._instance or object.__new__(Logger)

    def __init__(self):
        if Logger._instance is None:
            Logger._instance = self
            self.max_lines = 1024
            self.items = []
            term_size = os.get_terminal_size()
            self.width = term_size.columns
            self.height = term_size.lines

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
        self.add_text("INFO: " + str(obj))

    def print(self, obj):
        self.add_text(">>    " + str(obj))

    def progress_bar(self, task: Task):
        progress_bar = ProgressBar(task, self.repaint_item)
        self.add_items([progress_bar])

    def add_text(self, text: str):
        lines = []
        for line in text.split('\n'):
            left = 0
            while len(line) > self.width:
                right = left + self.width
                lines.append(line[left:right])
                left = right
            lines.append(line[left:])
        self.add_items([Line(line) for line in lines])

    def add_items(self, items: list):
        self.items.extend(items)
        dlength = len(self.items) - self.max_lines
        if dlength > 0:
            for i in range(dlength + 1):
                self.items[i].disconnect()
            del self.items[:dlength]
        for item in self.items:
            item.shift(len(items))
        self.repaint()

    def repaint(self):
        visible_items = self.items[-min(self.height, len(self.items)):]
        line_generator = (self.format(item.to_line(self.width)) for item in visible_items)
        Logger.set_cursor_pos(1, 1)
        self._print("\n".join(line_generator))
        Logger.set_cursor_pos(self.width, self.height)

    def repaint_item(self, item: Item):
        if item.position <= self.height:
            Logger.set_cursor_pos(1, item.position)
            self._print(self.format(item.to_line(self.width)))
            Logger.set_cursor_pos(self.width, self.height)

    def _print(self, string: str):
        sys.stdout.write(string)
        sys.stdout.flush()

    @staticmethod
    def set_cursor_pos(x: int, y: int):
        sys.stdout.write("\033[{};{}H".format(y, x))
        sys.stdout.flush()

    def format(self, string: str):
        length = len(string)
        return string[:self.width] if length > self.width else string + " " * (self.width - length)


logger = Logger()
