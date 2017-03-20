from abc import ABCMeta

from src.logger.proxy.Proxy import Proxy


class ProxyItem(Proxy, metaclass=ABCMeta):
    def __init__(self, proxy_uid: int, type_name: str, logger, *args, **kwargs):
        super().__init__(proxy_uid, type_name, logger, *args, **kwargs)
