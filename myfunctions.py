import pyodbc
import tkinter as tk
from tkinter import ttk   # стилізовані віджети Tk
from tkinter import messagebox
from ldap3 import Server, Connection, ALL, SAFE_SYNC, SUBTREE
from ldap3.core.exceptions import LDAPException, LDAPBindError 
from constantu import *      # Для загрузки переменных і констант из .файла
from functions_menubar import *
from functions_podil_mainwind import *
def select_from_db(conn, labl):
    cursor = conn.cursor()
    ins_query = "SELECT Lastname, Firstname, Middlename, Email FROM vpn.Customers"         
    cursor.execute(ins_query)    # Execute the query for all rows of data
    try:
        rows = cursor.fetchall()
        if rows:
            data_list = [str(row) for row in rows]    
            combined_text = "\n".join(data_list)     # Объединяем все строки в одну большую строку через символ \n
            labl.config(text=combined_text)
        else:
            labl.config(text="В базе данных нет записей.")    
    except pyodbc.Error as ex:
        sqlstate = ex.args[0]
        if sqlstate == '28000':
            error_message = "Ошибка аутентификации. Проверьте логин/пароль."
        else:
            error_message = f"Ошибка базы данных: {ex}"
            labl.config(text=error_message)
    finally:
        if cursor:
            cursor.close()

def open_dialog_window(main_wind):
    # Создаем новое окно Toplevel, которое будет дочерним для основного окна (root)
    dialog_window = tk.Toplevel(main_wind)
    dialog_window.title("Enter users data")
    # Делаем окно модальным (пользователь не сможет взаимодействовать с основным окном, пока это открыто)
    dialog_window.grab_set() 
    # Устанавливаем минимальные размеры окна
    dialog_window.geometry("500x350")
    # Функция-обработчик для кнопки в диалоговом окне
    def on_submit():
        lastname   = entry1.get()
        firstname  = entry2.get()
        middlename = entry3.get()
        email      = entry4.get()
        login      = entry5.get()
        print(f"Lastname: {lastname}, Firstname: {firstname}, Middlename: {middlename}, Email: {email}, Login: {login}")
        # Закрываем диалоговое окно после отправки данных
        dialog_window.destroy()

      

    # Label и Entry для 1 поля
    tk.Label(dialog_window, text="Lastname:").pack(pady=4)
    entry1 = tk.Entry(dialog_window)
    entry1.pack(pady=1)

    # Label и Entry для 2 поля
    tk.Label(dialog_window, text="Firstname:").pack(pady=3)
    entry2 = tk.Entry(dialog_window)
    entry2.pack(pady=5)
    
    # Label и Entry для 3 поля
    tk.Label(dialog_window, text="Middlename:").pack(pady=3)
    entry3 = tk.Entry(dialog_window)
    entry3.pack(pady=5)
   
    # Label и Entry для 4 поля
    tk.Label(dialog_window, text="Email:").pack(pady=3)
    entry4 = tk.Entry(dialog_window)
    entry4.pack(pady=5)

    # Label и Entry для 5 поля
    tk.Label(dialog_window, text="Login:").pack(pady=3)
    entry5 = tk.Entry(dialog_window)
    entry5.pack(pady=5)
    
    # Кнопка "Отправить" в диалоговом окне
    submit_button = tk.Button(dialog_window, text="Отправить", command=on_submit)
    submit_button.pack(pady=10)

def authent_in_ad(some_cd, username, password, sproba_enter2):     # number 3
    kilk_bad_cds = 0
    for cd in some_cd:
        try:     # Подключаетса к одному з двох cds AD робить аутентифік користувача і коли все OK вертае true і 
                 # всі групи до яких належить користувач
            # Формируем полное имя пользователя для привязки (bind_user_dn)
            bind_user = f"{username}@{AD_DOMAIN}"    # userPrincipalName (user@domain.com) или (DOMAIN\\user)
            server = Server(cd, get_info=ALL)        # створ обєкт сервера
            conn = Connection(server, user=bind_user, password=password, auto_bind=True)
            if conn.bind:       # Успешная аутентификация
               user_groups = get_users_groups_inAD(username, conn, WHERE_SEARCH_USER)   # отримуємо всі групи по даному користув в AD який вже залогінився
               #print(f"Пользователь {username} входит в группы: {user_groups}")
               conn.unbind()   
               return True, user_groups, cd, None 
        except LDAPBindError as e:
            kilk_bad_cds = kilk_bad_cds + 1
            if kilk_bad_cds == kilk_cds: 
               messagebox.showerror("Error", f"Error of authentification to domain controler: {cd}: {e}")
               sproba_enter2 = sproba_enter2 + 1
        except LDAPException as e:
            kilk_bad_cds = kilk_bad_cds + 1
            if kilk_bad_cds == kilk_cds: 
               messagebox.showerror("Error", f"Error LDAP of connection to domain controler: {cd}: {e}")  
               sproba_enter2 = sproba_enter2 + 1
        except Exception as e:
            kilk_bad_cds = kilk_bad_cds + 1
            if kilk_bad_cds == kilk_cds: 
               messagebox.showerror("Error", f"Unknown Error of connection to domain controler: {cd}: {e}") 
               sproba_enter2 = sproba_enter2 + 1
    return False, [], [], sproba_enter2              

def get_users_groups_inAD(username_tofind, connect, way_to_user_inAD):     # number 4
    #-----------  Отримує з AD для конкретного користувача всі його групи   ------
    search_filter1 = f'(&(objectClass=user)(sAMAccountName={username_tofind}))'
    connect.search(search_base = WHERE_SEARCH_USER, search_filter = search_filter1, search_scope=SUBTREE, attributes=['memberOf']) 
    if len(connect.entries) == 0:
        print(f"Пользователь {username_tofind} не найден.")
        return []
    user_entry = connect.entries[0]
    group_dns = user_entry['memberOf'].values
    group_names = []
    for dn in group_dns:
        # Парсинг CN из DN строки (например, 'CN=GroupName,OU=Groups,...')
        cn_part = next(part for part in dn.split(',') if part.startswith('CN='))
        group_name = cn_part.split('=', 1)[1]
        group_names.append(group_name)
    return group_names

def get_all_groups_inAD(connect, way_to_all_groups):
    # Вертає всікористувацькі групи в list. Але я її наразі ніде не використовую
    connect.search(way_to_all_groups, '(objectclass=group)', search_scope=SUBTREE, attributes='cn')
    if len(connect.entries) > 0:
        list_all_groups = [entry['cn'].value for entry in connect.entries]
        print(list_all_groups) 
        return list_all_groups
    else:
        return []

def open_main_window(username, window_toclose, users_group, logon_cd):    #  number 5
    # ------------Открывает основное окно приложения после успешного входа в AD.------------------
    window_toclose.destroy() # Закрываем окно входа логування в AD
    main_root = tk.Tk()   # use customTkinter
    main_root.title("Vpn user observer")
    screen_width = main_root.winfo_screenwidth()      # Получаем ширину и высоту экрана
    screen_height = main_root.winfo_screenheight()
    main_root.geometry(f"{screen_width}x{screen_height}+0+0")  # Устанавливаем геометрию окна, чтобы оно соответствовало размеру экрана
    forming_menubar(main_root)  # Виклик функц. по створеню menubar типу: Файл   Редактировать  Справка    
    mainwind_to2frame(main_root,username, users_group, logon_cd) # Функція ділить вікно на 2 частини: вузька ліва з меню і права з виводом інфи 
   
def check_login_pass(usernam, passw, wind_tooperate):     # number 2
    username = usernam.get()  # username and password беремо з вікна логування до AD
    password = passw.get()
    global sproba_enter    
    if sproba_enter < gener_kilk_sprob_enter:  # допоки не буде 4 невдалих спроби ввести логін/пароль
        #Проверяет учетные данные і якщо аутентиф в AD пройшла успішно - відкриваємо main вікно.
        status_conn, users_group, logon_cd, sproba_enter = authent_in_ad(DOMAIN_CONTROLLERS, username, password, sproba_enter)
        usernam.delete(0, tk.END)  # очистка полей ввода логина і пароля
        passw.delete(0, tk.END)
        usernam.focus_set() # Возвращаем курсор на поле логина
        if status_conn and users_group and logon_cd != []: # відкр голов вікно коли status_conn = Ok і список груп даного користувача не пустий
           open_main_window(username, wind_tooperate, users_group, logon_cd) # передаємо вікно логування для подальшого його закриття
        elif status_conn and users_group == []:  # вивод попередж коли список груп користувача пустий і status_conn = Ok
           messagebox.showwarning("Warning", "You arent in any group to enter") # виводимо повідомлення і
           wind_tooperate.destroy()           # закриваємо вікно логування бо корист не є в жодній групі
    else:
        messagebox.showerror("Ошибка", "Превышено количество попыток. Окно будет закрыто.")
        wind_tooperate.destroy()  # Закрываем окно        
       
def forming_wind_login_inAD():   #   number 1
    login_wind = tk.Tk()     # це логон вікно аутентиф до AD, яке потім руйнується
    login_wind.title("Enter to the system")
    login_wind.geometry("300x200")
    tk.Label(login_wind, text="Username:").pack(pady=5)
    username_entry = tk.Entry(login_wind)
    username_entry.pack(pady=5)

    tk.Label(login_wind, text="Password:").pack(pady=5)
    password_entry = tk.Entry(login_wind, show="*") # Скрывает ввод пароля
    password_entry.pack(pady=5)

    login_button = tk.Button(login_wind, text="Enter", command=lambda:check_login_pass(username_entry, password_entry, login_wind))
    login_button.pack(pady=10)
    login_wind.bind('<Return>', lambda event: check_login_pass(username_entry, password_entry, login_wind)) # Привязка клавиши Enter ко всему окну
    login_wind.mainloop()                 # щоб кнопка спрацьвувала при нажаті на клавіатурі Enter, а не тільки від спрац від мишки











        
           