from multiprocessing.pool import Pool

import time

from src.logger.ProxyLogger import ProxyLogger


def mapper(value: int):
    logger.print(value)
    # counter.update()
    time.sleep(0.5)
    return value


with ProxyLogger() as logger, Pool(2) as pool:
    data = range(10)
    counter = logger.item.counter(len(data))
    logger.print("Counter: ", counter, " :end")
    logger.print("first")
    timer = logger.item.time()
    logger.print("Timer: ", timer, " :timer")
    pool.map(mapper, data)
    timer.stop()
    logger.print("second")
    pool.map(mapper, data)
    logger.print("third")
