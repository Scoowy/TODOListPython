# -*- coding: utf-8 -*-


from todo.entities import Task
from todo.maincontroller import MainController


def main():
    controller = MainController()
    # controller.test()
    controller.run()


if __name__ == '__main__':
    main()
