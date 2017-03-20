from src.tasks.proxy.ProxyTask import ProxyTask


class ProxyCounterTask(ProxyTask):
    @property
    def length(self):
        return self._length

    def __init__(self, proxy_uid: int, logger, length: int):
        super().__init__(proxy_uid, "CounterTask", logger, proxy_uid, length)
        self._length = length
