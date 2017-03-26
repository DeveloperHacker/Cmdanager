from src.logger.HandledTypes import HandledTypes
from src.logger.proxy.Proxy import Proxy


class ProxyWriter(Proxy):
    def __init__(self, logger: 'Logger', uid: int):
        super().__init__(logger, uid, HandledTypes.Writer)

    def open(self, file_name, mode='r', encoding=None):
        self._impact("open", file_name, mode, encoding)

    def print(self, *items):
        self._impact("print", *items)

    def write(self, string: str):
        self._impact("write", string)

    def writeln(self, string: str):
        self._impact("writeln", string)

    def flush(self):
        self._impact("flush")

    def close(self):
        self._impact("close")
