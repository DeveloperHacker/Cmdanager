from src.items.proxy.ProxyItem import ProxyItem
from src.logger.HandledTypes import HandledTypes


class ProxyTimeBar(ProxyItem):
    def __init__(self, uid: int, logger: 'Logger'):
        super().__init__(logger, uid, HandledTypes.TimeBar, uid)

    def reset(self):
        self._impact("reset")

    def stop(self):
        self._impact("stop")
