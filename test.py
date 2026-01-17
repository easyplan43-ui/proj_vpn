import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
import pyodbc

# Настройки оформления
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("SQL Data Viewer 2026")
        self.geometry("800x500")

        # Кнопка загрузки
        self.button = ctk.CTkButton(self, text="Загрузить данные из SQL", command=self.load_data)
        self.button.pack(pady=20)

        # Контейнер для таблицы и прокрутки
        self.table_frame = ctk.CTkFrame(self)
        self.table_frame.pack(expand=True, fill="both", padx=20, pady=20)

        # Создание таблицы (Treeview)
        # Treeview пока входит в стандартный tkinter.ttk
        self.tree = ttk.Treeview(self.table_frame, columns=("ID", "Name", "Value"), show='headings')
        
        # Настройка заголовков
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Имя")
        self.tree.heading("Value", text="Значение")

        # Добавление вертикальной прокрутки
        self.scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        # Размещение таблицы и скроллбара
        self.tree.pack(side="left", expand=True, fill="both")
        self.scrollbar.pack(side="right", fill="y")

    def load_data(self):
        # Очистка таблицы перед загрузкой новых данных
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Параметры подключения к MS SQL
        conn_str = (
            "Driver={SQL Server};"
            "Server=sqlserv03;"
            "Database=vpn_serv01;"
            "Trusted_Connection=yes;" # Использует Windows аутентификацию
        )

        try:
            # Подключение к БД
            conn = pyodbc.connect(conn_str)
            cursor = conn.cursor()
            
            # Выполнение запроса
            cursor.execute("SELECT TOP 50 Vpnid, Vpnname, description FROM vpn.Vpn_type")

            # Вставка строк в таблицу приложения
            for row in cursor:
                self.tree.insert("", tk.END, values=(row[0], row[1], row[2]))

            conn.close()
        except Exception as e:
            print(f"Ошибка подключения: {e}")
            # Можно вывести сообщение об ошибке в интерфейс
            self.tree.insert("", tk.END, values=("Ошибка", "Не удалось", "подключиться"))

if __name__ == "__main__":
    app = App()
    app.mainloop()