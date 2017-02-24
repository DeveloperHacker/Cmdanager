import time


class Tracked:
    def add_progress_listener(self, listener):
        pass

    def add_done_listener(self, listener):
        pass


class Logger:
    _instance = None

    def __new__(cls, *args, **kwargs):
        return Logger._instance or object.__new__(Logger)

    def __init__(self):
        if Logger._instance is None:
            Logger._instance = self
            self._nested = 0

    def trace(self, foo):
        def wrapper(*args, **kwargs):
            name = foo.__name__
            self.info("Function \"{}\" is invoked".format(name))
            clock = time.time()
            result = foo(*args, **kwargs)
            delay = int((time.time() - clock) * 1000)
            ms = delay % 1000
            s = delay // 1000 % 60
            m = delay // 1000 // 60 % 60
            h = delay // 1000 // 60 // 60
            self.info("Function \"{}\" is ended".format(name))
            self.info("Work time {:02d}h {:02d}m {:02d}s {:03d}ms".format(h, m, s, ms))
            return result

        return wrapper

    def info(self, string: str):
        self._print("INFO: " + string)

    def print(self, string: str):
        self._print(">>    " + string)

    def progress_bar(self):
        pass

    def _print(self, message):
        print(message)


logger = Logger()
