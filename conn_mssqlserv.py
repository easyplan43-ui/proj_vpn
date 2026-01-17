import pyodbc
import re   # для валідации введеного тексту
import tkinter as tk
from tkinter import messagebox
from constantu import *      # Для загрузки переменных і констант из .файла
#from functions_podil_mainwind import *
def create_db_connection():
    connection = pyodbc.connect(connection_string)
    return connection  # return object soedunenuja

def get_existance_tables_indb():  #reads and saves in list - spusok tabluc jaki stvoreni v bd
    conn = create_db_connection()
    cursor = conn.cursor()
    query = "SELECT name FROM sys.tables WHERE is_ms_shipped = 0 AND name != 'sysdiagrams' ORDER BY name;" # відсіюєм системні таблиці, тільки користувацькі таблиці
    #query ="SELECT SCHEMA_NAME(t.schema_id) + '.' + t.name AS full_table_name FROM sys.tables t WHERE t.is_ms_shipped = 0 ORDER BY full_table_name;"
    cursor.execute(query)
    rows = cursor.fetchall()
    table_names = []
    for row in rows:
        table_names.append(row[0])
    cursor.close()
    conn.close()    
    return table_names  # returns list of tables that i created in some db

def get_table_schema(table_name):  # по назві таблиці вертає її назву схеми
    conn = create_db_connection()
    cursor = conn.cursor()
    query = """SELECT TABLE_SCHEMA FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = ?"""
    cursor.execute(query, (table_name,))
    results = cursor.fetchall()
    cursor.close()
    conn.close() 
    if results:
        for row in results:
            return f"{row[0]}.{table_name}"

def get_column_type(table_name, column_name):    # по назві таблиці вертає тип стовпця і max кількість символів яка відведена для даного стовпця
    conn = create_db_connection()
    cursor = conn.cursor()
    query = "SELECT DATA_TYPE, CHARACTER_MAXIMUM_LENGTH FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = ? AND COLUMN_NAME = ?";
    cursor.execute(query, (table_name, column_name))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return row      # Возвращает (тип_данных, макс_длина)

def get_decimal_prec_scale(table_name, column_name):    # вертае в типу даних decimal/numerical precision and scale, наприклад decimal(5,2)
    conn = create_db_connection()
    cursor = conn.cursor()
    query = "SELECT NUMERIC_PRECISION, NUMERIC_SCALE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = ? AND COLUMN_NAME = ?";
    cursor.execute(query, (table_name, column_name))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return row

def spusok_stovpciv_intable(selected_table): # reads and saves in list - nazvu stovpciv v konkretniy tabluci
    conn = create_db_connection()
    cursor = conn.cursor()
    stovpci_intable = []
    for row in cursor.columns(table = selected_table):
        column_name = row.column_name
        stovpci_intable.append(column_name)
    cursor.close()
    conn.close()    
    return  stovpci_intable  # returns list of stovpciv in selected tables 

def validate_varchar_input(input_text, max_length=25, required=True):  # провірка даних які вводить користувач в полі типу varchar, required це ніби ми ставимо умову щоб текст не був пустий
     # Ограничение по длине (например, 20 символов) и запрет специальных знаков
    if len(input_text) > 20:
        return False
    # Разрешаем только буквы, цифры и пробелы (стандартный VARCHAR)
    return all(char.isalnum() or char.isspace() for char in input_text)
    #if not input_text or input_text.strip() == "":           # 1. Проверка на пустоту
    #    if required:   # Если переменная required имеет значение True (поле обязательно для заполнения), выполняется код в блоке
    #        return False, "Поле не может быть пустым."
    #    return True, "Ок" # якщо поле не пусте то вертаємо True, Ok
    #if len(input_text) > max_length:     # 2. Проверка длины (аналог VARCHAR(N) в БД)
    #    return False, f"Текст слишком длинный (максимум {max_length} символов)."
    #if not re.match(r"^[a-zA-Z0-9А-ЩЬЮЯҐЄІЇа-щьюяґєії\s\.,!\?-]+$", input_text):   # 3. Проверка на опасные символы (защита от базовых инъекций)
     #   return False, "Текст содержит недопустимые спецсимволы."        # Разрешаем буквы, цифры, пробелы и базовую пунктуацию
    #return True, "Данные корректны"

def insert_data_into_db(which_table, dict_stovp_entries, label_v_kotry_vuvodutu):
    conn = create_db_connection()
    cursor = conn.cursor()
    columns = ', '.join(dict_stovp_entries.keys())
    placeholders = ', '.join(['?' for _ in dict_stovp_entries])
    sql = f"INSERT INTO {which_table} ({columns}) VALUES ({placeholders})"
    try:
       # це параметризований запит до бд бо дані які ввів користувач йдуть через ?, а which_table, columns, Поскольку имена таблиц и колонок не могут быть параметризированы
       cursor.execute(sql, list(dict_stovp_entries.values())) # отримуємо тільки значення із dictionary: dict_stovp_entries і перетвор це в тип list
       if cursor.rowcount > 0:
           first_elem_inlist = next(iter(dict_stovp_entries.values())) # поетапний обхід списку, виділяючи тільки 1-ий елемент в dictionary
           label_v_kotry_vuvodutu.config(text=f"Данные внесены для {first_elem_inlist}: верно", fg="blue")
           conn.commit()  # Обов'язково для збереження змін       # так як execute потребує тип list або кортеж  
           return True
    except Exception as e:
       conn.rollback()
       return False
    finally:
       cursor.close()
       conn.close()

def select_all_from_db(which_table, tree):
    conn = create_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ?", (which_table,))
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

   

    
def delete_data_from_db():
    #print (db_var)
    conn = create_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT @@SERVERNAME AS ServerName")
    row = cursor.fetchone()
    conn.close()
    return row

def edit_data_in_db():
   # print (db_var)
    conn = create_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT @@SERVERNAME AS ServerName")
    row = cursor.fetchone()
    conn.close()
    return row


       
