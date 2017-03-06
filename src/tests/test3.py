import os
from sys import stdout
from time import sleep


def text(string: str, x, y):
    stdout.writeln("\033[{};{}H{}".format(y, x, string))
    stdout.flush()


ts = os.get_terminal_size()
height = ts.lines
width = ts.columns

for i in range(height, 0, -1):
    text("text{}".format(i), 1, i)
    sleep(0.1)
