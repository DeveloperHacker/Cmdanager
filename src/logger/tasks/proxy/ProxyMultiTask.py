from src.logger.tasks.proxy.ProxyTask import ProxyTask


class ProxyMultiTask(ProxyTask):
    @property
    def tasks(self):
        return self._tasks

    def __init__(self, uid: int, *tasks):
        super().__init__(uid)
        self._tasks = tasks
