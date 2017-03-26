import os

from src.items.Item import Item
from src.utils import Point


class Writer:
    @property
    def width(self):
        term_size = os.get_terminal_size()
        return term_size.columns

    @property
    def height(self):
        term_size = os.get_terminal_size()
        return term_size.lines

    def __init__(self, stdout):
        self._files = []
        self._items = {}
        self._cursor = Point(1, 2)
        self._stdout = stdout

    def open(self, file_name, mode='r', encoding=None):
        self._files.append(open(file_name, mode=mode, encoding=encoding))

    def flush(self):
        for file in self._files:
            file.flush()
        self._stdout.flush()

    def close(self):
        for file in self._files:
            file.close()

    def print(self, *items):
        for item in items:
            if isinstance(item, Item):
                if item.uid not in self._items:
                    self._items[item.uid] = item
                item.move(self._cursor.x, self._cursor.y)
                line = self._truncate(item.line(self.width - self._cursor.x))
                self.write(line + " " * (item.width - len(line)))
            else:
                self.write(str(item))
        self.writeln()

    def repaint(self):
        for item in self._items.values():
            if item.y > 0:
                go_to_item_pos = "\033[{};{}H".format(item.y, item.x)
                go_to_cursor_pos = "\033[{};{}H".format(self._cursor.y, self._cursor.x)
                line = self._truncate(item.line(self.width - self._cursor.x))
                self._to_stdout(go_to_item_pos + line + " " * (item.width - len(line)) + go_to_cursor_pos)

    def writeln(self, string: str = ""):
        self.write(string + "\n")

    def write(self, string: str):
        string = string
        self._to_files(string)
        width = self.width
        lines = []
        for line in string.split('\n'):
            while len(line) > width:
                lines.append(line[:width])
                line = line[width:]
            lines.append(line)
        if len(lines) == 1:
            self._cursor.dx(len(lines[-1]))
        else:
            self._cursor.set_x(len(lines[-1]) + 1)
        self._to_stdout("\n".join(lines))
        shift = self._cursor.y + len(lines) - 1
        self._cursor.set_y(min(shift, self.height))
        shift = max(shift - self.height, 0)
        for item in self._items.values():
            item.set_y(item.y - shift)
        self.repaint()

    def _truncate(self, string: str):
        return string[:min(len(string), self.width - self._cursor.x)]

    def _to_stdout(self, string: str):
        self._stdout.write(string)
        self._stdout.flush()

    def _to_files(self, string: str):
        for file in self._files:
            file.write(string)
        self.flush()
