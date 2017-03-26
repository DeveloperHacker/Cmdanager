from src.logger.HandledTypes import HandledTypes
from src.tasks.proxy.ProxyTask import ProxyTask


class ProxyCounterTask(ProxyTask):
    @property
    def length(self):
        return self._length

    def __init__(self, uid: int, logger: 'Logger', length: int):
        super().__init__(logger, uid, HandledTypes.CounterTask, uid, length)
        self._length = length
