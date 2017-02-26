import os

import sys

import time

from src.logger import logger

term_size = os.get_terminal_size()
width = term_size.columns
height = term_size.lines

logger.set_cursor_pos(1, 1)
for i in range(height):
    sys.stdout.write("{:03d}>>  \n".format(i))
sys.stdout.flush()
for i in range(5):
    sys.stdout.write("{:03d}>  \n".format(i))
sys.stdout.flush()
for i in range(height + 5):
    if i % 3 == 0:
        logger.set_cursor_pos(1, i + 1)
        sys.stdout.write("{:03d}>>> ".format(i))
        time.sleep(1)
sys.stdout.flush()
