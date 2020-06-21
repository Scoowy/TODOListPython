from tkinter.ttk import Entry, Label, Button, Frame, Labelframe, Scrollbar
from tkinter import Listbox, END, SINGLE, DISABLED, NORMAL, VERTICAL, messagebox

from todo.entities import Task
from todo.model import Model
from todo.util import log_info, log_error


class MainView(Frame):
    def __init__(self, root, model: Model):
        super().__init__(root)
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        self.model = model
        self.__init_components()
        self.grid(sticky='nsew')
        self.__bind_action_events()

    def __init_components(self):
        # Instanciar widgets
        self.panel_form = Labelframe(self, text='Tarea')
        self.panel_tasks = Labelframe(self, text='Tareas por hacer')
        self.panel_complete_tasks = Labelframe(self, text='Tareas completas')

        self.label_name = Label(self.panel_form, text='Nombre:')
        self.label_description = Label(self.panel_form, text='Descripción:')
        self.entry_name = Entry(self.panel_form)
        self.entry_description = Entry(self.panel_form)

        self.btn_modify_task = Button(self.panel_form, text='Editar tarea', state=DISABLED, command=self.__modify_task)
        self.btn_new_task = Button(self.panel_form, text='Nueva tarea', command=self.__new_task)
        self.btn_delete_task = Button(self.panel_form, text='Eliminar tarea', state=DISABLED,
                                      command=self.__delete_task)
        self.btn_clear_form = Button(self.panel_form, text='Limpiar campos', command=self.__clear_form)
        self.btn_complete_task = Button(self.panel_form, text='Completar tarea', state=DISABLED,
                                        command=self.__complete_task)

        self.scroll_tasks = Scrollbar(self.panel_tasks, orient=VERTICAL)
        self.scroll_complete_tasks = Scrollbar(self.panel_complete_tasks, orient=VERTICAL)
        self.list_tasks = Listbox(self.panel_tasks, selectmode=SINGLE, height=10, width=25,
                                  yscrollcommand=self.scroll_tasks.set)
        self.list_complete_tasks = Listbox(self.panel_complete_tasks, selectmode=SINGLE, height=10, width=25,
                                           yscrollcommand=self.scroll_complete_tasks.set)

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
        self.btn_modify_task.grid(row=2, column=0, ipady=4, sticky='we')
        self.btn_new_task.grid(row=2, column=1, ipady=4, sticky='we')
        self.btn_delete_task.grid(row=3, column=0, ipady=4, sticky='we')
        self.btn_clear_form.grid(row=3, column=1, ipady=4, sticky='we')
        self.btn_complete_task.grid(row=4, column=0, columnspan=2, ipady=4, sticky='we')

        config_list = {'fill': 'both', 'expand': 'yes', 'padx': 10, 'pady': 5, 'ipadx': 5, 'ipady': 5}

        # Panel de lista de tareas pendientes
        self.panel_tasks.pack(config_list)
        self.panel_tasks.columnconfigure(0, weight=20)
        self.panel_tasks.columnconfigure(1, weight=1)
        self.list_tasks.grid(row=0, column=0, sticky='we')
        self.scroll_tasks.configure(command=self.list_tasks.yview)
        self.scroll_tasks.grid(row=0, column=1, sticky='ns')

        # Panel de lista de tareas completas
        self.panel_complete_tasks.pack(config_list)
        self.panel_complete_tasks.columnconfigure(0, weight=20)
        self.panel_complete_tasks.columnconfigure(1, weight=1)
        self.list_complete_tasks.grid(row=0, column=0, sticky='we')
        self.scroll_complete_tasks.configure(command=self.list_complete_tasks.yview)
        self.scroll_complete_tasks.grid(row=0, column=1, sticky='ns')

    def __bind_action_events(self):
        # self.btn_new_task.bind('<Button>', self.__new_task)
        # self.btn_modify_task.bind('<Button>', self.__modify_task)
        # self.btn_delete_task.bind('<Button>', self.__delete_task)
        # self.btn_complete_task.bind('<Button>', self.__complete_task)

        self.list_tasks.bind('<<ListboxSelect>>', self.__select_task)

    def __new_task(self):
        log_info('Botón {} pulsado'.format(self.btn_new_task.config('text')[-1]))

        name_value = self.entry_name.get()
        description_value = self.entry_description.get()

        if name_value:
            self.model.new_task(name_value, description_value)
            self.update_tables()
        else:
            messagebox.showwarning('AVISO', 'Complete el campo de nombre')

    def __modify_task(self):
        index = self.__selected_task()

        name_value = self.entry_name.get()
        description_value = self.entry_description.get()

        if index != -1:
            task = self.model.get_task(self.model.tasks[index].get_id())
            complete = self.model.modify_task(task.get_id(), name_value, description_value)

            if complete:
                messagebox.showinfo('Aviso', 'Tarea: {} editada'.format(task.name))

        self.update_tables()

    def __delete_task(self):
        index = self.__selected_task()

        if index != -1:
            task = self.model.get_task(self.model.tasks[index].get_id())
            self.model.delete_task(task.get_id())
            self.update_tables()

    def __complete_task(self):
        index = self.__selected_task()

        if index != -1:
            task = self.model.get_task(self.model.tasks[index].get_id())
            task.close_todo()
            complete = self.model.modify_task(task.get_id(), task.name, task.description)

            if complete:
                messagebox.showinfo('Aviso', 'Tarea: {} completa'.format(task.name))

        self.update_tables()

    def __clear_form(self):
        self.clear_form()
        self.__change_state_btn(DISABLED)

    def __select_task(self, event):
        self.clear_form()
        index = self.__selected_task()

        if index != -1:
            task = self.model.get_task(self.model.tasks[index].get_id())
            self.set_form(task)
            self.__change_state_btn(NORMAL)

    def __change_state_btn(self, state: str):
        self.btn_new_task.config(state=NORMAL if state == DISABLED else DISABLED)
        self.btn_delete_task.config(state=state)
        self.btn_modify_task.config(state=state)
        self.btn_complete_task.config(state=state)

    def __selected_task(self):
        try:
            return self.list_tasks.curselection()[0]
        except IndexError:
            self.__change_state_btn(DISABLED)
            self.list_complete_tasks.activate(-1)
            return -1

    def update_tables(self):
        log_info('Actualizando tablas')
        self.list_tasks.delete(0, END)
        self.list_complete_tasks.delete(0, END)

        for index in range(len(self.model.tasks)):
            self.list_tasks.insert(index, self.model.tasks[index].name)

        for index in range(len(self.model.complete_tasks)):
            self.list_complete_tasks.insert(index, self.model.complete_tasks[index].name)

    def clear_form(self):
        self.entry_name.delete(0, END)
        self.entry_description.delete(0, END)

    def set_form(self, task: Task):
        if task is not None:
            self.entry_name.insert(0, task.name)
            self.entry_description.insert(0, task.description)
        else:
            log_error('No se encontró la tarea seleccionada')
