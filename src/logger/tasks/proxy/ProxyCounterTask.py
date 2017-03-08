from src.logger.tasks.proxy.ProxyTask import ProxyTask


class ProxyCounterTask(ProxyTask):
    @property
    def length(self):
        return self._length

    def __init__(self, uid: int, length: int):
        super().__init__(uid)
        self._length = length
