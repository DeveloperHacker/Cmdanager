import time

from src.logger import logger
from src.tasks import CounterTask

counter_1 = CounterTask(10, 0, "counter_1")
counter_2 = CounterTask(10, 0, "counter_2")
logger.progress_bar(counter_1)
logger.print("print")
logger.progress_bar(counter_1)
logger.info("info")
logger.progress_bar(counter_2)
for i in range(10):
    for j in range(10):
        counter_2.update()
        time.sleep(0.1)
    counter_1.update()
    counter_2.reset()
