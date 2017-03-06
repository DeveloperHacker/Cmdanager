import time

from cmdmanager.logger import logger


@logger.trace
def foo1():
    logger.print("message from begin foo1")
    foo2(3)
    logger.print("message from end foo1")


@logger.trace
def foo2(i: int):
    logger.print("message from begin foo2 with i = {}".format(i))
    time.sleep(0.1)
    if i > 0:
        foo2(i - 1)
    logger.print("text text")
    logger.print("message from end foo2 with i = {}".format(i))


if __name__ == '__main__':
    logger.print("lel")
    foo1()
    logger.print("lol")
