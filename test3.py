import tkinter as tk
from tkinter import ttk, messagebox
import pyodbc

# 1. Настройки подключения к базе данных
DB_CONFIG = {
    'server': 'YOUR_SERVER_NAME',
    'database': 'YOUR_DATABASE_NAME',
    'user': 'YOUR_USERNAME',      # Оставьте пустым, если используете Windows Authentication
    'password': 'YOUR_PASSWORD'    # Оставьте пустым, если используете Windows Authentication
}



def fetch_and_display():
    # Очистка текущих данных в таблице
    for row in tree.get_children():
        tree.delete(row)
        
    try:
        # Строка подключения (пример для Windows Authentication)
       sql_server = 'sqlserv03'  # this is virtual WSFC name, consists from sqlserv03/04
       database = 'vpn_serv01' 
       connection_string = (
           f"DRIVER={{SQL Server}};"
           f"SERVER={sql_server};"
           f"DATABASE={database};"
           f"Trusted_Connection=yes;"
       )
       conn = pyodbc.connect(connection_string)
       cursor = conn.cursor()
       cursor.execute("SELECT TOP 50 * FROM vpn.Vpn_type") # Замените YourTableName на вашу таблицу
       # Настройка колонок динамически на основе описания из БД
       columns = [column[0] for column in cursor.description]
       tree["columns"] = columns
       tree["show"] = "headings"
       for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)

       # Вставка данных
       for row in cursor.fetchall():
            tree.insert("", tk.END, values=list(row))
       conn.close()
        
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось подключиться к БД:\n{e}")









# --- Создание интерфейса ---
root = tk.Tk()
root.title("Вывод данных из MS SQL")
root.geometry("800x500")

# Кнопка
btn_fetch = tk.Button(root, text="Загрузить данные из SQL", command=fetch_and_display, bg="#4CAF50", fg="white", pady=10)
btn_fetch.pack(pady=10)

# Контейнер для таблицы и прокрутки
frame = tk.Frame(root)
frame.pack(expand=True, fill="both", padx=10, pady=10)
frame.place(relx=0, rely=0.15, relwidth=1, relheight=0.2)

# Таблица (Treeview)
tree = ttk.Treeview(root)

# Вертикальная прокрутка
scrollbar_v = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scrollbar_v.set)

# Горизонтальная прокрутка (на случай широких таблиц)
scrollbar_h = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
tree.configure(xscrollcommand=scrollbar_h.set)

# Размещение элементов управления
scrollbar_v.pack(side="right", fill="y")
scrollbar_h.pack(side="bottom", fill="x")
tree.pack(expand=False, fill="both")

root.mainloop()