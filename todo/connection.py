import sqlite3


class Connection:
    def __init__(self, db_name: str):
        """
        Connection Class

        Clase que representa la conexión con la DB

        :param db_name: path del archivo de la DB
        """
        self.__db_name = db_name
        self.__conn = self.connect()
        self.__init_db()
        self.__conn.close()

    def connect(self):
        """
        Abrir conexión

        Método que abre una nueva conexión con la DB, esta debe cerrarse
        usando el método `close()`

        :return: una nueva conexión con la DB
        """
        return sqlite3.connect(self.__db_name)

    def __init_db(self):
        """
        Estructura inicial de la DB

        Método que establece la estructura inicial de la DB, ejemplo las tablas
        """
        self.__conn.execute("""CREATE TABLE IF NOT EXISTS tasks (
                                    id          INTEGER PRIMARY KEY AUTOINCREMENT,
                                    name        TEXT(20) NOT NULL,
                                    description TEXT(255) DEFAULT (''),
                                    complete    TEXT(5)   DEFAULT ('False')
                                )""")
