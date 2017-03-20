from src.items.proxy.ProxyItem import ProxyItem


class ProxyTimeBar(ProxyItem):
    def __init__(self, proxy_uid: int, logger):
        super().__init__(proxy_uid, "TimeBar", logger, proxy_uid)

    def reset(self):
        self._impact("reset")

    def stop(self):
        self._impact("stop")
