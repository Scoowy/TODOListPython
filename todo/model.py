from todo.dao import DAOTask
from todo.entities import Task
from todo.util import log_info


class Model:
    def __init__(self):
        self.tasks = []
        self.complete_tasks = []
        self.dao = DAOTask()

    def get_task(self, id_task: int):
        for task in self.tasks:
            if task.get_id() == id_task:
                return task
        return None

    def load_tasks(self):
        log_info('Load tasks')
        self.tasks = self.dao.select_for_complete(False)
        self.complete_tasks = self.dao.select_for_complete(True)

    def new_task(self, name: str, description: str):
        task = Task(0, name, description)
        self.dao.create(task)

    def delete_task(self, id_task: int):
        task = self.get_task(id_task)
        if task is not None:
            self.dao.delete(task)
            return True
        else:
            return False

    def modify_task(self, id_task: int, name: str, description: str):
        task = self.get_task(id_task)
        if task is not None:
            task.name = name
            task.description = description
            self.dao.update(task)
            return True
        else:
            return False

    def complete_task(self, id_task: int):
        task = self.get_task(id_task)
        if task is not None:
            task.close_todo()
            self.dao.update(task)
            return True
        else:
            return False
