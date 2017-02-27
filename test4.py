import time
from src.logger import logger
from src.tasks import CounterTask

counter_1 = CounterTask(30, 0, "counter_1")
counter_2 = CounterTask(10, 0, "counter_2")
logger.progress_bar(counter_1)
logger.print("print")
logger.progress_bar(counter_1)
logger.info("info")
logger.progress_bar(counter_2)
for i in range(counter_1._progress_length):
    counter_2.reset()
    for _ in range(counter_2._progress_length):
        counter_2.update()
        time.sleep(0.01)
    time.sleep(0.05)
    counter_1.update()
    logger.info(i)
