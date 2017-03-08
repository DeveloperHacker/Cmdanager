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
