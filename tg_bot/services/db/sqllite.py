import sqlite3



class Database:
    def __init__(self, path_to_db="main.db"):
        self.path_to_db = path_to_db

    # подключаемся к базе данных
    # прописываем проперти для того чтобы каждый раз не вызывать функцию и это уже будет как свойство

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    # когда нам нужно будет сделать какую то команду мы вызываем функцию execute
    # fetchone - забрать одно значение, fetchall = забрать все значения
    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        # пропишем логирование или трейсколлбэк
        connection.set_trace_callback(logger)
        cursor = connection.cursor()
        data = None
        # когда мы захотим использовать какую то команду мы это будем делать таким образом
        cursor.execute(sql, parameters)
        # если мы добавляли или удаляли запись в бд, то нужно сделать коммит
        if commit:
            connection.commit() # только после этого изменится бд
        # а если изменения в бд не нужно то юзаем комманды фетч ван или олл
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data

    def create_table_users(self):
        sql = """
        CREATE TABLE Users (
            id int NOT NULL,
            Name varchar(255) NOT NULL,
            email varchar(255),
            PRIMARY KEY (id)
            );
    """
        self.execute(sql, commit=True) # коммит нужен для того чтобы прописать изменения в базе данных

        # функция для автоматического форматирования keyword arguments
    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f'{item} = ?' for item in parameters
        ])
        return sql, tuple(parameters.values())


    # фукнция которая будет добавлять новых пользователей в эту таблицу
    def add_user(self, id: int, name: str, email: str = None):
        # SQL_EXAMPLE = "INSERT INTO Users(id, Name, email) VALUES(1, 'John', 'John@gmail.com')"

        sql = """
        INSERT INTO Users(id, Name, email) VALUES(?, ?, ?)
        """
        self.execute(sql, parameters=(id, name, email), commit=True)

    def select_all_users(self):
        sql = """
        SELECT * FROM Users
        """
        return self.execute(sql, fetchall=True)


    def select_user(self, **kwargs):
        sql = 'SELECT * FROM users WHERE '
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters, fetchone=True)
    # функция для подсчета пользователей
    def count_users(self, **kwargs):
        return self.execute('SELECT count(*) FROM users;', fetchone=True)

    # функция обновленмя имейла нашего пользователя
    def update_user_email(self, email, id):
        # SQL_EXAMPLE = "UPDATE Users SET email=mail@gmail.com WHERE id=12345"

        sql = f"""
        UPDATE Users SET email=? WHERE id=?
        """
        return self.execute(sql, parameters=(email, id), commit=True) # делаем commit чтобы зафиксировать изменения в таблице

    # функция для очистки базы
    def delete_users(self):
        self.execute('DELETE FROM users WHERE True')




# statment - запрос к базе данных, когда у нас будет выполнятся какая то команда, она будет попадать сюда
def logger(statement):
    print(f"""
    __________________________________________________
    Executing:
    {statement}
    __________________________________________________
    """)