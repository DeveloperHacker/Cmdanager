import sys

sys.stdout.write("text text text\n")
sys.stdout.write("text text text\n")
sys.stdout.write("text text text\n")
sys.stdout.write("text text text\n")
sys.stdout.write("text text text\n")
sys.stdout.write("text text text")
sys.stdout.flush()

home = 7


def go_to(y):
    dy = home - y
    sys.stdout.write("\r" * dy)
    sys.stdout.flush()


go_to(2)
sys.stdout.write("\rlel")
sys.stdout.flush()
print("\033[6;3HHello")
