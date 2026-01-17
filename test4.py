import tkinter as tk
import re

def validate_input(new_value, max_n):
    # Разрешаем пустую строку (чтобы можно было удалять символы)
    if new_value == "":
        return True
    
    # Регулярное выражение: только английские буквы и длина <= max_n
    # ^[a-zA-Z]*$ проверяет только буквы
    if re.match("^[a-zA-Z]*$", new_value) and len(new_value) <= int(max_n):
        return True
    
    return False

root = tk.Tk()
root.title("Varchar Input")

n = 10  # Максимальная длина

# Регистрация функции валидации в Tkinter
vcmd = (root.register(validate_input), '%P', n)

label = tk.Label(root, text=f"Введите текст (только англ., до {n} символов):")
label.pack(pady=5)

# Создание поля ввода с проверкой
entry = tk.Entry(root, validate="key", validatecommand=vcmd)
entry.pack(pady=10, padx=20)

root.mainloop()