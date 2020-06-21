class Task(object):

    def __init__(self, id_task: int, name: str, description: str, complete=False):
        """
        Task Class

        Clase que representa una tarea.

        :param id: Identificador unico de la tarea
        :param name: Nombre de la tarea
        :param description: Descripcion de la tarea
        :param complete: Si la tarea esta completa o no
        """

        self.__id_task = id_task
        self.set_name(name)
        self.set_description(description)
        self.complete = complete

    def close_todo(self):
        self.complete = True

    def open_todo(self):
        self.complete = False

    def get_id(self):
        return self.__id_task

    def is_complete(self):
        return self.complete

    def get_name(self):
        return self.__name

    def set_name(self, name):
        if len(name) == 0:
            raise ValueError('El nombre no puede ser vacio')
        elif len(name) > 20:
            raise ValueError('El nombre debe ser menos de 20 caracteres')
        self.__name = name

    def get_description(self):
        return self.__description

    def set_description(self, description):
        if len(description) > 256:
            raise ValueError('La descripcion no debe ser mas de 256 caracteres')
        self.__description = description

    def __str__(self):
        return 'Task: {:3} - {} | Complete: {}'.format(self.__id_task, self.name, self.complete)

    name = property(get_name, set_name)
    description = property(get_description, set_description)
