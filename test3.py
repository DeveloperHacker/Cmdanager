import os


def text(string: str, x, y):
    str = "\033[{};{}H{}".format(y, x, string)
    print(str)


text("text", 3, 0)
text("text", 6, 3)
text("text", 7, 4)

ts = os.get_terminal_size()
print(ts.lines)
print(ts.columns)
