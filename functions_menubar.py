import tkinter as tk
from tkinter import messagebox
# Функции, которые будут вызываться при выборе пунктов меню
def new_file():
    """Обработчик пункта меню 'Новый'."""
    messagebox.showinfo("Действие", "Создан новый файл!")

def open_file():
    """Обработчик пункта меню 'Открыть'."""
    messagebox.showinfo("Действие", "Открытие файла...")

def save_file():
    """Обработчик пункта меню 'Сохранить'."""
    messagebox.showinfo("Действие", "Сохранение файла...")

def about_app():
    """Обработчик пункта меню 'О программе'."""
    messagebox.showinfo("О программе", "Это простое приложение с меню на Tkinter.")

def quit_app(wind_toquit):
    """Обработчик пункта меню 'Выход'."""
    wind_toquit.quit() # Завершает работу приложения

def forming_menubar(for_which_wind_menubar):
    # ---------- Функція формує меню в самій горі main_window типу:   Файл     Редактировать    Справка 
    menubar = tk.Menu(for_which_wind_menubar)   #  создание главной строки меню menubar для главного окна main_root
    for_which_wind_menubar.config(menu=menubar)   # привязка меню до вікна main_root
    # --- Создание меню "Файл" ---
    file_menu = tk.Menu(menubar, tearoff=0)       # tearoff=0 убирает пунктирную линию
    menubar.add_cascade(label="Файл", menu=file_menu)

    # Добавление пунктов в меню "Файл"
    file_menu.add_command(label="Новый", command=new_file)
    file_menu.add_command(label="Открыть...", command=open_file)
    file_menu.add_command(label="Сохранить", command=save_file)
    file_menu.add_separator() # Разделительная линия
    file_menu.add_command(label="Выход", command=lambda:quit_app(for_which_wind_menubar))

    # --- Создание меню "Править" ---
    edit_menu = tk.Menu(menubar, tearoff=0)       # tearoff=0 убирает пунктирную линию
    menubar.add_cascade(label="Редактировать", menu=edit_menu)

     # Добавление пунктов в меню "Править"
    edit_menu.add_command(label="Копировать", command=new_file)
    edit_menu.add_command(label="Вставить", command=open_file)
    edit_menu.add_command(label="Поиск", command=save_file)

    # --- Создание меню "Справка" ---
    help_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Справка", menu=help_menu)

    # Добавление пунктов в меню "Справка"
    help_menu.add_command(label="О программе", command=about_app)
    