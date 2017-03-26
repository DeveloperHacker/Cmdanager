import time
from multiprocessing.pool import Pool

from src.logger.proxy.ProxyLogger import ProxyLogger


def mapper(value: int):
    time.sleep(0.01)
    return value


def main():
    with ProxyLogger() as logger, Pool(2) as pool:
        data = range(10000)
        # counter = logger.item.counter(len(data))
        # timer = logger.item.time()
        # print("some\n\tthing")
        print("lol")
        logger.iterators.map(mapper, data, pool)
        print("lel")
        # logger.print("Counter: ", counter, " ", timer)
        # print("first")
        # # logger.print("Timer: ", timer, " :timer")
        # pool.map(mapper, data)
        # timer.stop()
        # print("second")
        # pool.map(mapper, data)
        # print("third")


if __name__ == '__main__':
    main()
