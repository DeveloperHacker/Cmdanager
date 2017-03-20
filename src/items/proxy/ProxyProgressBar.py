from src.items.proxy.ProxyItem import ProxyItem
from src.tasks.proxy.ProxyTask import ProxyTask


class ProxyProgressBar(ProxyItem):
    @property
    def width(self):
        return self._width

    @property
    def task(self):
        return self._task

    def __init__(self, proxy_uid: int, logger, width: int, task: ProxyTask):
        super().__init__(proxy_uid, "ProgressBar", logger, proxy_uid, width, task)
        self._width = width
        self._task = task

    @property
    def completeness(self) -> float:
        return self._request("completeness").get()

    def update(self):
        self._impact("update")

    def reset(self):
        self._impact("reset")
