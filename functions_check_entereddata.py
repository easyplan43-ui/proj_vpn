import re   # для работы с регулярными выражениями (regular expressions, regex). Он используется для сложного поиска, извлечения, замены фрагментов текста и валидации данных (например, email или номеров телефонов
def validate_varchar(new_value, max_value):
    # Разрешаем пустую строку (для удаления), англ. буквы, макс длина задана max_value
    if new_value == "":
        return True
    if len(new_value) == 0:
        return False
    pattern = fr"^[a-zA-Z0-9\s\.,!\?-]{{0,{max_value}}}+$"   
    return re.fullmatch(pattern, new_value) is not None  # Если строка яку ввів користувач полностью соответствует шаблону pattern, 
                                                         # fullmatch возвращает объект совпадения (match object), если соответствия нет, функция возвращает None

def validate_dec_num(new_value, precision, scale):      # precision and scale це наприклад decimal(5,2)
    if new_value == "":
        return True
    pattern = rf"^\d{{0,{precision}}}(\.\d{{0,{scale}}})?$"
    return re.fullmatch(pattern, new_value) is not None     # используется для проверки того, соответствует ли вся строка целиком заданному регулярному выражению

def validate_scrolledtext(event):
    forbid_symb = "@#$%&^|\/"
    # event.char содержит символ, который пытается ввести пользователь
    if event.char in forbid_symb:
        return "break"  # Останавливает дальнейшую обработку события (символ не появится)

def validate_smallint(new_value):
    if new_value == "":          # Разрешаем пустое поле (чтобы можно было стирать символы)
        return True
    if new_value.isdigit() and len(new_value) <=5:             # Проверяем, состоит ли ввод только из цифр
        value = int(new_value)
        # Проверка диапазона положительного smallint (0 - 32767)
        if 0 <= value <= 32767:
            return True
    return False # Блокирует ввод, если условия не выполнены
   
def validate_int(new_value):
    if new_value == "":          # Разрешаем пустое поле (чтобы можно было стирать символы)
        return True
    if new_value.isdigit() and len(new_value) <= 10:             # Проверяем, состоит ли ввод только из цифр
        value = int(new_value)
        # Проверка диапазона положительного smallint (0 - 32767)
        if 0 <= value <= 2147483647:
            return True
    return False # Блокирует ввод, если условия не выполнены    
   