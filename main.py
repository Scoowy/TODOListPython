# -*- coding: utf-8 -*-


from todo.entities import Task


def main():
    todo1 = Task(0, 'Nombre', 'Descripcion')

    try:
        todo1.name = ''
    except ValueError as e:
        print('ERROR: {}'.format(e))

    print(todo1)


if __name__ == '__main__':
    main()
