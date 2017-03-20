from src.tasks.proxy.ProxyTask import ProxyTask


class ProxyMultiTask(ProxyTask):
    def __init__(self, proxy_uid: int, logger, *tasks):
        super().__init__(proxy_uid, "MultiTask", logger, proxy_uid, *tasks)
