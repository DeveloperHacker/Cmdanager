from abc import ABCMeta


class Proxy(metaclass=ABCMeta):
    @property
    def uid(self):
        return self._uid

    @property
    def type(self):
        return self._type

    def __init__(self, logger: 'Logger', uid: int, instance_type: str, *args):
        """
            :param args: is list of values with type:
                str, int, float, bool, Proxy
        """
        self._uid = uid
        self._type = instance_type
        self._logger = logger
        self._logger.create(self, *args)

    def _impact(self, method: str, *args):
        """
            :param args: is list of values with type:
                str, int, float, bool, Proxy
        """
        self._logger.impact(self, method, *args)
