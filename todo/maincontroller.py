import tkinter as Tk

from todo.view.main_view import MainView
from todo.model import Model


class MainController:
    def __init__(self):
        self.root = Tk.Tk()
        self.model = Model()
        self.view = MainView(self.root, self.model)
        self.update_tables()

    def run(self):
        self.root.title('TODO List')
        self.root.geometry('300x600')
        self.root.resizable(0, 0)
        self.root.deiconify()
        self.root.mainloop()

    def test(self):
        self.model.load_tasks()
        for task in self.model.tasks:
            print(task)

        for task in self.model.complete_tasks:
            print(task)

    def update_tables(self):
        self.model.load_tasks()
        self.view.update_tables()
