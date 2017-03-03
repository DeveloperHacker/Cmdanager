import logging
import os
import sys
import time
from multiprocessing import Value

from src.items import Item, ProgressBar
from src.tasks import Task
from src.utils import expand, unique_integer_key


class _Commands:
    info = "info"
    print = "print"
    show = "show"
    repaint_item = "repaint"


class Logger:
    def __init__(self, name=None):
        self._writer = Writer(name)
        self.add_stream(sys.stdout)

    def add_stream(self, stream):
        self._writer.add_stream(stream)

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
        self._writer.register_command(_Commands.info, obj)

    def print(self, obj):
        self._writer.register_command(_Commands.print, obj)

    def progress(self, task: Task, length: int, description: str = "PROG:"):
        return self._writer.progress(task, length, description)

    def show(self, item: Item):
        self._writer.register_command(_Commands.show, item)


class Writer(logging.Handler):
    def __init__(self, name=None):
        logging.Handler.__init__(self)
        self._logger = logging.getLogger(name)
        self._logger.addHandler(self)
        self._commands = {}
        self._streams = []
        self._items = []
        self._cursor = Value("i", 2)

    def add_stream(self, stream):
        self._streams.append(stream)

    def register_command(self, command: str, *args):
        uid = unique_integer_key(self._commands)
        self._commands[uid] = (command, tuple(args))
        self._logger.log(logging.CRITICAL, uid)

    # noinspection PyBroadException
    def emit(self, record):
        try:
            uid = int(self.format(record))
            command, args = self._commands[uid]
            if command == _Commands.info:
                self._info(*args)
            elif command == _Commands.print:
                self._print(*args)
            elif command == _Commands.show:
                self._show(*args)
            elif command == _Commands.repaint_item:
                self._repaint_item(*args)
        except Exception:
            self.handleError(record)

    # Todo: normal
    @property
    def cursor_position(self):
        return self._cursor.value

    # Todo: remove this operation
    def _shift_cursor_position(self, shift: int):
        self._cursor.value = min(self.cursor_position + shift, self.height)

    @property
    def width(self):
        term_size = os.get_terminal_size()
        return term_size.columns

    @property
    def height(self):
        term_size = os.get_terminal_size()
        return term_size.lines

    def _info(self, obj):
        self._writeln("INFO: " + str(obj))

    def _print(self, obj):
        self._writeln(">>    " + str(obj))

    def _show(self, item: Item):
        item.set_position(self.cursor_position)
        self._write("\n")

    def progress(self, task: Task, length: int, description: str):
        progress_bar = ProgressBar(length, description, task, -1, self._repaint_item)
        self._items.append(progress_bar)
        return progress_bar

    def _repaint_item(self, item: Item):
        self.acquire()
        if item.position > 0:
            go_to_item_pos = "\033[{};1H".format(item.position)
            go_to_cursor_pos = "\033[{};1H".format(self.cursor_position)
            line = self._format(item.to_line(self.width))
            self._log(go_to_item_pos + line + go_to_cursor_pos)
        self.release()

    def _writeln(self, text: str):
        self._write(text + "\n")

    def _write(self, text: str):
        self.acquire()
        width = self.width
        lines = []
        for line in text.split('\n'):
            while len(line) > width:
                lines.append(line[:width])
                line = line[width:]
            lines.append(line)
        self._log("\n".join(lines))
        shift = max(self.cursor_position + len(lines) - 1 - self.height, 0)
        self._shift_cursor_position(len(lines) - 1)
        for i, item in enumerate(self._items):
            item.set_position(item.position - shift)
            self._repaint_item(item)
        self.release()

    def _format(self, string: str):
        length = len(string)
        width = self.width
        return string[:width] if length > width else string + " " * (width - length)

    def _log(self, string: str):
        for stream in self._streams:
            stream.write(string)
            if stream and hasattr(stream, "flush"):
                stream.flush()


logger = Logger()
