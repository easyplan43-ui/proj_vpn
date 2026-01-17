import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import scrolledtext
from constantu import *
from functions_check_entereddata import *
from conn_mssqlserv import *
import PIL as PIL      # Для отображения изображений иконок ImageTk из библиотеки Pillow (PIL)
from PIL import Image, ImageTk
def mainwind_to2frame(wind_todivide, username, users_group, logon_cd):   # number 6
   left_frame = tk.Frame(wind_todivide, bg='#333333', width=200)
   left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)
   left_frame.pack_propagate(False) # Запрещает фрейму менять размер под содержимое

   right_container = tk.Frame(wind_todivide, bg='#eeeeee')
   right_container.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
   right_top_frame = tk.Frame(right_container, bg='#eeeeee', height=30)    # Сюди виводжу інфо хто підключений 
   right_top_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=False)             # і до якого контр домену
   right_middle_frame = tk.Frame(right_container, bg='#cccccc', height=75) # Сюди виводжу іконки
   right_middle_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=False)
   right_bottom_frame = tk.Frame(right_container, bg="#b6b6b6")      # Нижний фрейм в правом контейнере
   right_bottom_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)   # Найбільший і Інформативний фрейм

   # Размещение username в верхнем правом углу верхнего правого фрейма
   username_label = tk.Label( right_top_frame, text=f"Log as: {username} at: {logon_cd}", font=("Helvetica", 10))
   username_label.place(relx=1.0, rely=0.0, anchor='ne', x=-5, y=5) # anchor='ne' - привязка к северо-восточному (NE) углу

   left_menu_stovbec(users_group, left_frame, right_bottom_frame)  # меню яке відкривається в залежності від групи залогін користувача
   add_icons(right_middle_frame)

def add_icons(vkotruy_frame_add_icons):
   create_icon_button(vkotruy_frame_add_icons, 'icons/home.png', lambda: show_text("Нажата иконка 1"))
   create_icon_button(vkotruy_frame_add_icons, 'icons/print.png', lambda: show_text("Нажата иконка 2"))
   create_icon_button(vkotruy_frame_add_icons, 'icons/prukrepit.png', lambda: show_text("Нажата иконка 3"))
   create_icon_button(vkotruy_frame_add_icons, 'icons/analize.png', lambda: show_text("Нажата иконка 4"))
   create_icon_button(vkotruy_frame_add_icons, 'icons/delete.png', lambda: show_text("Нажата иконка 5"))
   create_icon_button(vkotruy_frame_add_icons, 'icons/download.png', lambda: show_text("Нажата иконка 6"))
   create_icon_button(vkotruy_frame_add_icons, 'icons/koshuk.png', lambda: show_text("Нажата иконка 7"))
   create_icon_button(vkotruy_frame_add_icons, 'icons/system.png', lambda: show_text("Нажата иконка 8"))

def show_content_pru_nazati_left_menu_button(frame_to_vuvidvidget, pressed_button):     # number 8
   #Frame_vuvodyinfu = tk.Frame(frame_to_vuvidvidget) 
   for widget in frame_to_vuvidvidget.winfo_children():
        widget.destroy()      # Очищаем правый фрейм перед добавлением новых элементов
   tk.Label(frame_to_vuvidvidget, text="Выберите таблицю:", bg="lightgray").pack(pady=5)
   which_table_selected = tk.StringVar(frame_to_vuvidvidget)   # Переменная для хранения выбора в списке
   list_tables = get_existance_tables_indb() # підкл до бд і виводимо список існуючих таблиць у форматі ['table1', 'table2', .....]
   which_table_selected.set("Таблица") # Значение по умолчанию
   tk.OptionMenu(frame_to_vuvidvidget, which_table_selected, *list_tables).pack(pady=5) # випадаюче меню
   ahead_btn = tk.Button(frame_to_vuvidvidget, text="Вперед", command=lambda: kotry_diu_vukonatu(pressed_button, frame_to_vuvidvidget, which_table_selected.get(), ahead_btn))
   ahead_btn.pack(pady=10)  # при нажаті на цю кнопку передается таблиця яку вибрав оператор для подальших дій - which_table_selected.get
   #print(which_table_selected.get())

def kotry_diu_vukonatu(edit_or_del, frame_tofilldanux, kotra_table, btn_toblock):  # number 9 - a same enter/delete/edit data in some tables
        if edit_or_del == 'enter':
            btn_toblock.config(state="disabled", text="Нажато")
            stovpci = spusok_stovpciv_intable(kotra_table)
            table_with_schema = get_table_schema(kotra_table)    # format schema.table
            entries = [] # Це значення полів вводу від користувача занесені в список list
            entries1 = []
            kilkist = len(stovpci) - 1
            for i in range(kilkist):                                           
                label = tk.Label(frame_tofilldanux, text=stovpci[i+1])
                label.pack(pady=5)
                data_type, max_length = get_column_type(kotra_table, stovpci[i+1])   # для кожного стовпця отримуємо його тип і max довжину
                if data_type in ['text', 'ntext'] or ( data_type in ['nvarchar', 'varchar'] and max_length == -1 ):  # тобто довгий текст
                   entry = scrolledtext.ScrolledText(frame_tofilldanux, width = 50, height = 10) 
                   entry.pack(pady = 5)
                   entry.bind("<Key>", validate_scrolledtext)
                elif data_type in ["varchar", "nvarchar"]: 
                   val_varchar  = (frame_tofilldanux.register(validate_varchar), '%P', max_length)   # Регистрация функции проверки введених даних від користувача
                   entry = tk.Entry(frame_tofilldanux, validate="key", validatecommand=val_varchar)  
                   entry.pack(pady=5)
                elif  data_type in ["decimal", "numeric"]:  
                   precision, scale = get_decimal_prec_scale(kotra_table, stovpci[i+1])
                   val_dec_num  = (frame_tofilldanux.register(validate_dec_num),'%P', precision, scale)   # Регистрация функции проверки введених даних від користувача
                   entry = tk.Entry(frame_tofilldanux, validate="key", validatecommand=val_dec_num)   
                   entry.pack(pady=5) 
                elif  data_type in ["smallint"]:   
                   val_smallint = frame_tofilldanux.register(validate_smallint)   # Регистрация функции проверки введених даних від користувача
                   entry = tk.Entry(frame_tofilldanux, validate="key", validatecommand=(val_smallint, '%P'))   
                   entry.pack(pady=5) 
                elif  data_type in ["int"]: 
                   val_int = frame_tofilldanux.register(validate_int)       # Регистрация функции проверки введених даних від користувача
                   entry = tk.Entry(frame_tofilldanux, validate="key", validatecommand=(val_int, '%P'))   
                   entry.pack(pady=5) 
                entries.append((stovpci[i+1], entry))  # list - формату [('імя стовпця', <tkinter.Entry object .!frame2.!frame3.!entry>), ('імя стовпця 2', <tkinter.scrolledtext.ScrolledText object .!frame2.!frame3.!frame.!scrolledtext>)], тобто в список добавляється 1 кортеж із двох елементів
                entries1.append(entry) # list - формату  [<tkinter.Entry object .!frame2.!frame3.!entry>, <tkinter.scrolledtext.ScrolledText object .!frame2.!frame3.!frame.!scrolledtext>                
            def formyem_dictionary():  # якщо це entry то застос entry.get, якщо це текстове поле scrolledtext то застос entry.get("1.0", tk.END).strip() і так проходимось поцілому списку entries
               result_dict = {  name: entry.get().strip() if isinstance(entry, tk.Entry) 
                                else entry.get("1.0", tk.END).strip() 
                                for name, entry in entries  }
               # Проверяем, есть ли хотя бы одно пустое значение
               if any(not value for value in result_dict.values()):
                  messagebox.showwarning("Предупреждение", "Все поля ввода должны быть заполнены!")
               else:   
                  success = insert_data_into_db(table_with_schema, result_dict, label_information)
                  if success:
                     for entry in entries1:
                        if isinstance(entry, tk.Entry):
                           entry.delete(0, tk.END)   # Очистка однострочного поля
                        elif isinstance(entry, scrolledtext.ScrolledText):
                           entry.delete("1.0", tk.END)   # Очистка многострочного текста 
                  entries1[0].focus_set()  
            tk.Button(frame_tofilldanux, text="Вставить", command = formyem_dictionary).pack(pady=5) 
            label_information = tk.Label(frame_tofilldanux, text="") 
            label_information.pack()  # сюда виводиться інфа: дані внесено успішно для когось/чогось 
        elif  edit_or_del == 'del': 
            btn_toblock.config(state="disabled", text="Нажато")
            stovpci = spusok_stovpciv_intable(kotra_table)
            table_with_schema = get_table_schema(kotra_table)    # format schema.table
            frame_table = tk.Frame(frame_tofilldanux)           # Контейнер для таблицы куда я виводжу select з бд і прокрутка
            frame_table.pack(expand=True, fill="both", padx=10, pady=10)
            frame_table.place(relx=0, rely=0.18, relwidth=0.9, relheight=0.4)
            tree = ttk.Treeview(frame_tofilldanux)   #  создаем виджет Treeview (древовидную структуру или таблицу) из модуля tkinter.ttk
            scrollbar_v = ttk.Scrollbar(frame_table, orient="vertical", command=tree.yview)         # Вертикальная прокрутка
            tree.configure(yscrollcommand=scrollbar_v.set)
            scrollbar_h = ttk.Scrollbar(frame_table, orient="horizontal", command=tree.xview)
            tree.configure(xscrollcommand=scrollbar_h.set)
            scrollbar_v.pack(side="right", fill="y")          # Размещение элементов управления
            scrollbar_h.pack(side="bottom", fill="x")
            tree.pack(expand=True, fill="both")
            select_all_from_db(kotra_table, tree)

        elif edit_or_del == 'edit': 
            btn_toblock.config(state="disabled", text="Нажато")
            stovpci = spusok_stovpciv_intable(kotra_table)
            table_with_schema = get_table_schema(kotra_table)    # format schema.table
            data = edit_data_in_db() 
                  
def create_icon_button(frame, image_path, command):
    try:
        # Открываем изображение с помощью PIL и изменяем размер при необходимости
        img = Image.open(image_path)
        img = img.resize((30, 30), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(img)

        # Создаем кнопку с изображением
        icon_button = tk.Button(frame, image=photo, command=command, bd=0, relief=tk.FLAT, bg='#cccccc')
        icon_button.image = photo # Сохраняем ссылку на изображение
        icon_button.pack(side=tk.LEFT, padx=5, pady=5)
    except FileNotFoundError:
        # Если изображение не найдено, можно добавить обычную текстовую кнопку
        tk.Button(frame, text="Icon missing", command=command).pack(side=tk.LEFT, padx=5, pady=5)

def left_menu_stovbec(users_group, frame_tooperate, frame_to_vuvid_vidget):   # number 7 - меню яке відкривається в залежності від групи залогін користувача
        if 'operat_vpnobs' in users_group  or 'admin_vpnobs' in users_group: 
           btn_enter = ttk.Button( frame_tooperate, text="Внести дані", command=lambda: show_content_pru_nazati_left_menu_button(frame_to_vuvid_vidget, 'enter'))
           btn_enter.pack(fill=tk.X, pady=5, padx=5)
           btn_del = ttk.Button( frame_tooperate, text="Видалити дані", command=lambda: show_content_pru_nazati_left_menu_button(frame_to_vuvid_vidget, 'del'))
           btn_del.pack(fill=tk.X, pady=5, padx=5)
           btn_edit = ttk.Button( frame_tooperate, text="Редагувати дані", command=lambda: show_content_pru_nazati_left_menu_button(frame_to_vuvid_vidget, 'edit'))
           btn_edit.pack(fill=tk.X, pady=5, padx=5)
        if 'ekobezpeka' in users_group  or 'prodazi' in users_group  or 'bychalt' in users_group or 'fin_chief' in users_group: 
           button2 = ttk.Button( frame_tooperate, text="Продажи", command=lambda: show_content_pru_nazati_left_menu_button(frame_to_vuvid_vidget))
           button2.pack(fill=tk.X, pady=5, padx=5)
        if 'ekobezpeka' in users_group  or 'zakypku' in users_group  or 'bychalt' in users_group or 'fin_chief' in users_group:     
           button3 = ttk.Button( frame_tooperate, text="Покупки", command=lambda: show_content_pru_nazati_left_menu_button(frame_to_vuvid_vidget))
           button3.pack(fill=tk.X, pady=5, padx=5)
        if 'ekobezpeka' in users_group  or 'zakypku' in users_group  or 'prodazi' in users_group  or 'bychalt' in users_group or 'fin_chief' in users_group:
           button4 = ttk.Button( frame_tooperate, text="Отчети", command=lambda: show_content_pru_nazati_left_menu_button(frame_to_vuvid_vidget))
           button4.pack(fill=tk.X, pady=5, padx=5)
        if 'bychalt' in users_group or 'fin_chief' in users_group:
           button5 = ttk.Button( frame_tooperate, text="Банк и операции", command=lambda: show_content_pru_nazati_left_menu_button(frame_to_vuvid_vidget))
           button5.pack(fill=tk.X, pady=5, padx=5)
        if 'sklad' in users_group:    
           button6 = ttk.Button( frame_tooperate, text="Склад", command=lambda: show_content_pru_nazati_left_menu_button(frame_to_vuvid_vidget))
           button6.pack(fill=tk.X, pady=5, padx=5)
           button7 = ttk.Button( frame_tooperate, text="Центральний склад", command=lambda: show_content_pru_nazati_left_menu_button(frame_to_vuvid_vidget))
           button7.pack(fill=tk.X, pady=5, padx=5)
        if 'admin_vpnobs' in users_group: 
           button8 = ttk.Button( frame_tooperate, text="Администрирование", command=lambda: show_content_pru_nazati_left_menu_button(frame_to_vuvid_vidget))
           button8.pack(fill=tk.X, pady=5, padx=5)
        if 'fin_chief' in users_group:   
           button9 = ttk.Button( frame_tooperate, text="Руководителю", command=lambda: show_content_pru_nazati_left_menu_button(frame_to_vuvid_vidget))
           button9.pack(fill=tk.X, pady=5, padx=5)

