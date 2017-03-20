from src.tasks.proxy.ProxyTask import ProxyTask


class ProxySimpleTask(ProxyTask):
    def __init__(self, proxy_uid: int, logger):
        super().__init__(proxy_uid, "SimpleTask", logger, proxy_uid)
