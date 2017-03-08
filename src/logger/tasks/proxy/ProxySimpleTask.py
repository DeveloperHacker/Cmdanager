from src.logger.tasks.proxy.ProxyTask import ProxyTask


class ProxySimpleTask(ProxyTask):
    def __init__(self, uid: int):
        super().__init__(uid)
