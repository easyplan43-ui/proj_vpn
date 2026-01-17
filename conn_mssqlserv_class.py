import pyodbc
from constantu import *      # Для загрузки переменных і констант из .файла
class MsSqlDatabase:
    """
    Класс для управления подключением к базе данных MS SQL Server через ODBC.
    """
    def __init__(self, driver, server, database, username, password):
        self.driver = driver
        self.server = server
        self.database = database
        self.username = username
        self.password = password
        self.conn = None
        self.cursor = None

    def connect(self):
        """Устанавливает соединение с базой данных."""
        try:
            conn_string = (
                f"DRIVER={self.driver};"
                f"SERVER={self.server};"
                f"DATABASE={self.database};"
                f"UID={self.username};"
                f"PWD={self.password}"
            )
            self.conn = pyodbc.connect(conn_string)
            self.cursor = self.conn.cursor()
            print("Подключение к базе данных успешно установлено.")
        except pyodbc.Error as ex:
            sqlstate = ex.args[0]
            if sqlstate == '28000':
                print("Ошибка аутентификации. Проверьте логин и пароль.")
            else:
                print(f"Ошибка подключения: {ex}")
            raise

    def disconnect(self):
        """Закрывает соединение с базой данных."""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
            print("Соединение с базой данных закрыто.")

    def execute_query(self, query, params=None):
        """Выполняет SQL-запрос."""
        if not self.cursor:
            print("Нет активного подключения к базе данных.")
            return None
        
        try:
            self.cursor.execute(query, params or ())
            return self.cursor
        except pyodbc.Error as ex:
            print(f"Ошибка выполнения запроса: {ex}")
            self.conn.rollback() # Откатываем транзакцию в случае ошибки
            return None

    def fetch_all(self, query, params=None):
        """Выполняет запрос SELECT и возвращает все результаты."""
        cursor = self.execute_query(query, params)
        if cursor:
            return cursor.fetchall()
        return []

    def commit(self):
        """Подтверждает транзакцию."""
        if self.conn:
            self.conn.commit()

    def __enter__(self):
        """Метод для использования менеджера контекста (with statement)."""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Метод для использования менеджера контекста (with statement)."""
        self.disconnect()

# --- Пример использования ---

if __name__ == '__main__':
    # Замените эти параметры своими данными
    DB_CONFIG = {
        'driver': '{ODBC Driver 17 for SQL Server}', # Или 18, в зависимости от установленного
        'server': 'your_server_name',
        'database': 'your_database_name',
        'username': 'your_username',
        'password': 'your_password'
    }

    # Использование класса как менеджера контекста (рекомендуемый способ)
    try:
        with MsSqlDatabase(**DB_CONFIG) as db:
            # Выполнение запроса SELECT
            # Например, получить первые 5 строк из таблицы 'Employees'
            employees = db.fetch_all("SELECT TOP 5 FirstName, LastName FROM Employees")
            
            if employees:
                print("\nСотрудники:")
                for row in employees:
                    print(f"{row.FirstName} {row.LastName}")
            
            # Пример выполнения INSERT (раскомментируйте и настройте при необходимости)
            # insert_query = "INSERT INTO Employees (FirstName, LastName) VALUES (?, ?)"
            # db.execute_query(insert_query, ('Test', 'User'))
            # db.commit()
            # print("\nДанные успешно добавлены.")

    except Exception as e:
        print(f"\nПроизошла непредвиденная ошибка во время работы с БД: {e}")
