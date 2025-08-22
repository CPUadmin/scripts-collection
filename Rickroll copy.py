import time
import keyboard
from pynput.keyboard import Controller, Key

# Инициализация контроллера клавиатуры
keyboard_controller = Controller()

# Настройки задержки (в секундах)
delay_settings = {
    'char_delay': 0.05,    # Задержка между символами
    'line_delay': 0.1,     # Задержка между строками
    'enter_delay': 0.1     # Задержка после нажатия Enter
}

# Текст песни
song_lyrics = [
    "We're no strangers to love",
    "You know the rules and so do I",
    "A full commitment's what I'm thinking of",
    "You wouldn't get this from any other guy",
    "I just wanna tell you how I'm feeling",
    "Gotta make you understand",
    "",
    "Never gonna give you up",
    "Never gonna let you down",
    "Never gonna run around and desert you",
    "Never gonna make you cry",
    "Never gonna say goodbye",
    "Never gonna tell a lie and hurt you",
    "",
    "We've known each other for so long",
    "Your heart's been aching but you're too shy to say it",
    "Inside we both know what's been going on",
    "We know the game and we're gonna play it",
    "And if you ask me how I'm feeling",
    "Don't tell me you're too blind to see",
    "",
    "Never gonna give you up",
    "Never gonna let you down",
    "Never gonna run around and desert you",
    "Never gonna make you cry",
    "Never gonna say goodbye",
    "Never gonna tell a lie and hurt you",
    "",
    "Never gonna give you up",
    "Never gonna let you down",
    "Never gonna run around and desert you",
    "Never gonna make you cry",
    "Never gonna say goodbye",
    "Never gonna tell a lie and hurt you",
    "",
    "(Ooh, give you up)",
    "(Ooh, give you up)",
    "Never gonna give, never gonna give",
    "(Give you up)",
    "Never gonna give, never gonna give",
    "(Give you up)",
    "",
    "We've known each other for so long",
    "Your heart's been aching but you're too shy to say it",
    "Inside we both know what's been going on",
    "We know the game and we're gonna play it",
    "",
    "I just wanna tell you how I'm feeling",
    "Gotta make you understand",
    "",
    "Never gonna give you up",
    "Never gonna let you down",
    "Never gonna run around and desert you",
    "Never gonna make you cry",
    "Never gonna say goodbye",
    "Never gonna tell a lie and hurt you",
    "",
    "Never gonna give you up",
    "Never gonna let you down",
    "Never gonna run around and desert you",
    "Never gonna make you cry",
    "Never gonna say goodbye",
    "Never gonna tell a lie and hurt you",
    "",
    "Never gonna give you up",
    "Never gonna let you down",
    "Never gonna run around and desert you",
    "Never gonna make you cry",
    "Never gonna say goodbye",
    "Never gonna tell a lie and hurt you"
]

def update_delays():
    """Функция для обновления задержек через горячие клавиши"""
    print("\nТекущие задержки:")
    print(f"1. Между символами: {delay_settings['char_delay']} сек")
    print(f"2. Между строками: {delay_settings['line_delay']} сек")
    print(f"3. После Enter: {delay_settings['enter_delay']} сек")
    print("Используйте Num+ и Num- для регулировки выбранной задержки")

def type_line(line):
    """Печатает одну строку с текущими настройками задержки"""
    # Нажимаем Enter перед строкой
    keyboard_controller.press(Key.enter)
    keyboard_controller.release(Key.enter)
    time.sleep(delay_settings['enter_delay'])
    
    # Печатаем строку
    for char in line:
        if stop_flag:
            return
        keyboard_controller.press(char)
        keyboard_controller.release(char)
        time.sleep(delay_settings['char_delay'])
    
    # Нажимаем Enter после строки
    keyboard_controller.press(Key.enter)
    keyboard_controller.release(Key.enter)
    time.sleep(delay_settings['line_delay'])

def run_song():
    """Основная функция для печати песни"""
    global stop_flag
    stop_flag = False
    print("\nНачало печати песни...")
    for line in song_lyrics:
        if stop_flag:
            print("Печать остановлена")
            return
        if line:  # Пропускаем пустые строки
            type_line(line)
    print("Песня завершена!")

# Флаг для остановки
stop_flag = False
current_setting = 1  # Текущая настройка для изменения (1-3)

def change_setting(direction):
    """Изменяет выбранную настройку задержки"""
    global current_setting
    # Циклическое переключение между настройками 1-3
    current_setting = (current_setting % 3) + 1
    update_delays()
    print(f"Выбрана настройка {current_setting} для изменения")

def adjust_delay(amount):
    """Регулирует выбранную задержку"""
    keys = ['char_delay', 'line_delay', 'enter_delay']
    selected = keys[current_setting - 1]
    
    # Изменяем задержку с проверкой на минимальное значение
    new_value = max(0.01, delay_settings[selected] + amount)
    delay_settings[selected] = round(new_value, 3)
    
    print(f"{selected} изменено на {delay_settings[selected]} сек")
    update_delays()

# Настройка горячих клавиш
keyboard.add_hotkey('num 1', run_song)
keyboard.add_hotkey('num 2', lambda: globals().update({'stop_flag': True}))
keyboard.add_hotkey('num 3', lambda: change_setting(1))
keyboard.add_hotkey('num +', lambda: adjust_delay(0.01))
keyboard.add_hotkey('num -', lambda: adjust_delay(-0.01))

# Инструкция
print("Rick Astley - Never Gonna Give You Up Bot")
print("Горячие клавиши:")
print("Num1 - Начать печать песни")
print("Num2 - Остановить печать")
print("Num3 - Выбрать настройку задержки")
print("Num+ - Увеличить выбранную задержку")
print("Num- - Уменьшить выбранную задержку")
update_delays()

# Бесконечный цикл для поддержания работы программы
while True:
    time.sleep(1)