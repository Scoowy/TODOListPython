import tkinter as Tk
from tkinter.ttk import Entry, Label, Button, Frame, Labelframe
from tkinter import Listbox, TOP, LEFT, RIGHT, BOTTOM, SINGLE

from todo.model import Model
# from todo.maincontroller import MainController
from todo.util import log_info


class MainView(Frame):
    def __init__(self, root, model: Model):
        super().__init__(root)
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        self.model = model
        self.__init_components()
        self.grid(sticky='nsew')
        self.__set_controller_buttons()

    def __init_components(self):
        # Instanciar widgets
        self.panel_form = Labelframe(self, text='Tarea')
        self.panel_tasks = Labelframe(self, text='Tareas por hacer')
        self.panel_complete_tasks = Labelframe(self, text='Tareas completas')
        self.label_name = Label(self.panel_form, text='Nombre:')
        self.label_description = Label(self.panel_form, text='Descripción:')
        self.entry_name = Entry(self.panel_form)
        self.entry_description = Entry(self.panel_form)
        self.btn_new_task = Button(self.panel_form, text='Nueva tarea')
        self.btn_complete_task = Button(self.panel_form, text='Completar tarea')
        self.btn_delete_task = Button(self.panel_form, text='Eliminar tarea')
        self.btn_modify_task = Button(self.panel_form, text='Editar tarea')
        self.list_tasks = Listbox(self.panel_tasks, selectmode=SINGLE, height=10, width=25)
        self.list_complete_tasks = Listbox(self.panel_complete_tasks, selectmode=SINGLE, height=10, width=25)

        # Posicionar los widgets
        # Panel de formulario de tareas
        self.panel_form.pack(fill='both', expand='yes', padx=10, pady=5, ipadx=5, ipady=5)
        self.panel_form.columnconfigure(0, weight=1)
        self.panel_form.rowconfigure(0, weight=1)

        self.label_name.grid(row=0, column=0, padx=5, sticky='w')
        self.entry_name.grid(row=0, column=1, padx=5, sticky='w')
        self.label_description.grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.entry_description.grid(row=1, column=1, padx=5, pady=10, sticky='w')

        # Botones
        self.btn_new_task.grid(row=2, column=0, columnspan=2, ipady=4, sticky='we')
        self.btn_delete_task.grid(row=3, column=0, ipady=4, sticky='we')
        self.btn_modify_task.grid(row=3, column=1, ipady=4, sticky='we')
        self.btn_complete_task.grid(row=4, column=0, columnspan=2, ipady=4, sticky='we')

        # Panel de lista de tareas pendientes
        self.panel_tasks.pack(fill='both', expand='yes', padx=10, pady=5, ipadx=5, ipady=5)
        self.list_tasks.pack(fill='both')

        # Panel de lista de tareas completas
        self.panel_complete_tasks.pack(fill='both', expand='yes', padx=10, pady=5, ipadx=5, ipady=5)
        self.list_complete_tasks.pack(fill='both')

    def __set_controller_buttons(self):
        self.btn_new_task.bind('<Button>', self.__new_task)
        self.btn_modify_task.bind('<Button>', self.__modify_task)
        self.btn_delete_task.bind('<Button>', self.__delete_task)
        self.btn_complete_task.bind('<Button>', self.__complete_task)

    def __new_task(self, event):
        log_info('Botón {} pulsado'.format(self.btn_new_task.config('text')[-1]))
        self.model.new_task(self.entry_name.get(), self.entry_description.get())
        self.updateTables()

    def __modify_task(self, event):
        log_info('Botón {} pulsado'.format(self.btn_modify_task.config('text')[-1]))

    def __delete_task(self, event):
        log_info('Botón {} pulsado'.format(self.btn_delete_task.config('text')[-1]))

    def __complete_task(self, event):
        log_info('Botón {} pulsado'.format(self.btn_complete_task.config('text')[-1]))

    def updateTables(self):
        for index in range(len(self.model.tasks)):
            self.list_tasks.insert(index, self.model.tasks[index].name)

        for index in range(len(self.model.complete_tasks)):
            self.list_complete_tasks.insert(index, self.model.complete_tasks[index].name)
