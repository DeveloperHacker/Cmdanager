from src.logger.items.proxy.ProxyItem import ProxyItem
from src.logger.tasks.proxy.ProxyTask import ProxyTask


class ProxyProgressBar(ProxyItem):
    @property
    def width(self):
        return self._width

    @property
    def task(self):
        return self._task

    def __init__(self, uid: int, width: int, task: ProxyTask):
        super().__init__(uid)
        self._width = width
        self._task = task

    # TODO:
    @property
    def completeness(self) -> float:
        pass

    # TODO:
    def update(self):
        pass

    # TODO:
    def reset(self):
        pass
