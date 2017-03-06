
from cmdmanager.logger import logger


data = range(2 ** 20)
data = tuple(zip(data[0::2], data[1::2]))
data = [datum1 * datum2 for datum1, datum2 in logger.progress_iterator(data, 60)]
logger.print(len(data))
