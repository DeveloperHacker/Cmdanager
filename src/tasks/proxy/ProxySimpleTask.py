from src.logger.HandledTypes import HandledTypes
from src.tasks.proxy.ProxyTask import ProxyTask


class ProxySimpleTask(ProxyTask):
    def __init__(self, uid: int, logger: 'Logger'):
        super().__init__(logger, uid, HandledTypes.SimpleTask, uid)
