from src.tasks.Task import Task


class MultiTask(Task):
    def __init__(self, uid: int, *tasks):
        super(MultiTask, self).__init__(uid)
        self._sub_tasks = []
        for task in tasks:
            task.add(self.update)
            self._sub_tasks.append(task)

    def is_done(self) -> bool:
        return all((task.is_done() for task in self._sub_tasks))

    def _update(self):
        pass

    def _reset(self):
        for task in self._sub_tasks:
            task.reset()

    def completeness(self) -> float:
        if len(self._sub_tasks) == 0: return 1.0
        acc = 0.0
        for task in self._sub_tasks:
            acc += task.completeness()
        return acc / len(self._sub_tasks)
