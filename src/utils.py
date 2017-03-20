def unique_integer_key(dictionary: dict) -> int:
    prev = 0
    for uid in sorted(dictionary.keys()):
        if uid - prev != 1:
            return uid - 1
        prev = uid
    return prev + 1


def expand(clock: float):
    clock = int(clock * 1000)
    s, ms = divmod(clock, 1000)
    m, s = divmod(s, 60)
    h, m = divmod(m, 60)
    if h != 0:
        return "{:02d}h {:02d}m {:02d}s {:03d}ms".format(h, m, s, ms)
    elif m != 0:
        return "{:02d}m {:02d}s {:03d}ms".format(m, s, ms)
    elif s != 0:
        return "{:02d}s {:03d}ms".format(s, ms)
    else:
        return "{:03d}ms".format(ms)


class Point:
    @property
    def x(self) -> int:
        return self._x

    @property
    def y(self) -> int:
        return self._y

    def __init__(self, x: int, y: int):
        self._x = x
        self._y = y

    def move(self, x: int, y: int):
        self._x = x
        self._y = y

    def shift(self, dx: int, dy: int):
        self._x += dx
        self._y += dy

    def dx(self, dx: int):
        self.shift(dx, 0)

    def dy(self, dy: int):
        self.shift(0, dy)

    def set_x(self, x: int):
        self.move(x, self.y)

    def set_y(self, y: int):
        self.move(self.x, y)