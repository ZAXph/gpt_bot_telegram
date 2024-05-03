import sqlite3
from config import DB_NAME


class DataBase:
    def __init__(self, TABLE_NAME, CREATE_TABLE):
        self.DB_NAME = DB_NAME
        self.TABLE_NAME = TABLE_NAME
        self.CREATE_TABLE = CREATE_TABLE

    def execute_query(self, query, data=None):
        """
        Функция для выполнения запроса к базе данных.
        Принимает имя файла базы данных, SQL-запрос и опциональные данные для вставки.
        """
        try:
            connection = sqlite3.connect(self.DB_NAME)
            cursor = connection.cursor()

            if data:
                cursor.execute(query, data)
            else:
                cursor.execute(query)
            cursor = cursor.fetchall()
            connection.commit()
            connection.close()
            return cursor

        except sqlite3.Error as e:
            print("Ошибка при выполнении запроса:", e)

        finally:
            connection.close()

    def create_table(self):
        sql_query = self.CREATE_TABLE
        self.execute_query(sql_query)

    def add_data(self, user_id, column_1, column_2, value_1, value_2):

        sql_query = f'INSERT INTO {self.TABLE_NAME} (user_id, {column_1}, {column_2}) VALUES (?, ?, ?);'
        data = (user_id, value_1, value_2,)

        self.execute_query(sql_query, data)

    def update_data(self, user_id, column, value):

        sql_query = f'UPDATE {self.TABLE_NAME} SET {column} = {column} + ? WHERE user_id = ?;'
        data = (value, user_id,)
        self.execute_query(sql_query, data)

    def get_data(self, column, user_id=None):
        if user_id:
            sql_query = f'SELECT {column} FROM {self.TABLE_NAME} WHERE user_id = ?;'
            data = (user_id,)
            result = self.execute_query(sql_query, data)
        else:
            sql_query = f'SELECT {column} FROM {self.TABLE_NAME};'
            result = self.execute_query(sql_query)
        return result

    def last_message(self, column, user_id):
        sql_query = f'SELECT {column} FROM {self.TABLE_NAME} WHERE user_id = ? ORDER BY id DESC LIMIT 5;'
        data = (user_id,)
        result = self.execute_query(sql_query, data)
        return result

    def create_user(self, user_id, gpt_tokens, tokens, blocks):

        sql_query = f'INSERT INTO {self.TABLE_NAME} (user_id, gpt_tokens, tokens, blocks) VALUES (?, ?, ?, ?);'
        data = (user_id, gpt_tokens, tokens, blocks, )
        self.execute_query(sql_query, data)

    def count_all_column(self, column):
        sql_query = f'SELECT COUNT({column}) FROM {self.TABLE_NAME};'
        result = self.execute_query(sql_query)[0]
        if result and result[0]:
            return result[0]
        return 0
