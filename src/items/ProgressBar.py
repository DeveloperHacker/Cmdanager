from src.tasks.Task import Task

from src.items.Item import Item


class ProgressBar(Item):
    @property
    def completeness(self) -> float:
        return self._task.completeness()

    def __init__(self, uid: int, width: int, task: Task):
        super().__init__(uid, width + 2)
        self._task = task
        self._width = width

        # def line(self, width: int):
        # percent = "{:-3d}%".format(int(self.completeness * 100))
        # fill = int(self._width * self.completeness)
        # empty = self._width - fill
        # length = len(percent)
        # segment = (self._width - length) // 2
        # left = min(segment, fill)
        # right = min(segment, empty)
        # progress = ["█" * left, " " * (segment - left), percent, "█" * (segment - right), " " * right]
        # return "|{}|".format("".join(progress))

    def line(self, width: int):
        fill = int(self._width * self.completeness)
        return "█" * fill + " " * (self._width - fill)

    def update(self):
        self._task.update()

    def reset(self):
        self._task.reset()
