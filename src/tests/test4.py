import time

from src.tasks import CounterTask

from cmdmanager.logger import logger


@logger.trace
def foo():
    logger.print("print")
    logger.info("info")
    progress1 = logger.progress(CounterTask(30, "counter_1"), 50)
    progress2 = logger.progress(CounterTask(10, "counter_2"), 50)
    logger.show(progress1)
    logger.show(progress2)
    for _ in range(30):
        progress2.reset()
        for _ in range(10):
            progress2.update()
            time.sleep(0.01)
        time.sleep(0.05)
        progress1.update()


foo()
