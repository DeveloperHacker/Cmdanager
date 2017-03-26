from src.items.proxy.ProxyItem import ProxyItem
from src.logger.HandledTypes import HandledTypes
from src.tasks.proxy.ProxyTask import ProxyTask


class ProxyProgressBar(ProxyItem):
    @property
    def width(self):
        return self._width

    @property
    def task(self):
        return self._task

    def __init__(self, uid: int, logger: 'Logger', width: int, task: ProxyTask):
        super().__init__(logger, uid, HandledTypes.ProgressBar, uid, width, task)
        self._width = width
        self._task = task

    @property
    def completeness(self) -> float:
        raise AttributeError("attribute 'completeness' is not supported")

    def update(self):
        self._impact("update")

    def reset(self):
        self._impact("reset")
