from src.logger.HandledTypes import HandledTypes
from src.tasks.proxy.ProxyTask import ProxyTask


class ProxyMultiTask(ProxyTask):
    def __init__(self, uid: int, logger: 'Logger', *tasks):
        super().__init__(logger, uid, HandledTypes.MultiTask, uid, *tasks)
