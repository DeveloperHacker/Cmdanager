from abc import ABCMeta


class Future:
    def __init__(self, uid: int, logger):
        self._uid = uid
        self._instance = None
        self._logger = logger

    def get(self, timeout: float = float("inf")):
        if self._instance is not None:
            return self._instance
        self._instance = self._logger.wait_result(self._uid, timeout)
        return self._instance


class Proxy(metaclass=ABCMeta):
    @property
    def uid(self):
        return self._uid

    def __init__(self, proxy_uid: int, type_name: str, logger, *args, **kwargs):
        self._logger = logger
        self._uid = proxy_uid
        self._logger.create(proxy_uid, type_name, *args, **kwargs)

    def _impact(self, method: str, *args):
        self._logger.impact(self._uid, method, *args)

    def _request(self, method: str, *args) -> Future:
        return self._logger.impact(self._uid, method, *args)
