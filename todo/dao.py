from todo.connection import Connection
from todo.entities import Task
from todo.util import *


class DAOTask:
    def __init__(self):
        self.DB = Connection('data/todolst.db')

    def create(self, task: Task):
        query = """INSERT INTO tasks (name, description, complete)
                    VALUES ('{}', '{}', '{}')""".format(task.name, task.description, str(task.complete))

        with self.DB.connect() as conn:
            conn.execute(query)
            log_query(query)
            conn.commit()

    def select_one(self, id_task: int):
        with self.DB.connect() as conn:
            cursor = conn.execute("""SELECT *
                                        FROM tasks
                                        WHERE id = ?""", (id_task,))
            row = cursor.fetchone()

            if row is not None:
                task = Task(row[0], row[1], row[2], row[3] == 'True')
            else:
                task = None

        return task

    def select_all(self):
        tasks = []
        query = """SELECT *
                    FROM tasks"""

        with self.DB.connect() as conn:
            cursor = conn.execute(query)
            log_query(query)

            for row in cursor:
                tasks.append(Task(row[0], row[1], row[2], row[3] == 'True'))

        return tasks

    def select_for_complete(self, value: bool):
        tasks = []
        query = """SELECT *
                    FROM tasks
                    WHERE complete = '{}'""".format(value)

        with self.DB.connect() as conn:
            cursor = conn.execute(query)
            log_query(query)
            rows = cursor.fetchall()

            for row in rows:
                tasks.append(Task(row[0], row[1], row[2], row[3] == 'True'))

        return tasks

    def update(self, task: Task):
        query = """UPDATE tasks
                        SET name        = '{}',
                            description = '{}',
                            complete    = '{}'
                        WHERE id = {}""".format(task.name, task.description, str(task.complete), task.get_id())

        with self.DB.connect() as conn:
            conn.execute(query)
            log_query(query)
            conn.commit()

    def delete(self, task: Task):
        query = """DELETE
                    FROM tasks
                    WHERE id = '{}'""".format(task.get_id())

        with self.DB.connect() as conn:
            conn.execute(query)
            log_query()
            conn.commit()
