import time
import keyboard
from pynput.keyboard import Controller, Key

# Инициализация контроллера клавиатуры
keyboard_controller = Controller()

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

def type_line(line):
    # Нажимаем Enter перед строкой
    keyboard_controller.press(Key.enter)
    keyboard_controller.release(Key.enter)
    time.sleep(0.1)
    
    # Печатаем строку
    for char in line:
        keyboard_controller.press(char)
        keyboard_controller.release(char)
        time.sleep(0.05)  # Задержка между символами
    
    # Нажимаем Enter после строки
    keyboard_controller.press(Key.enter)
    keyboard_controller.release(Key.enter)
    time.sleep(0.1)

def run_song():
    print("Начало печати песни...")
    for line in song_lyrics:
        if stop_flag:
            print("Печать остановлена")
            return
        if line:  # Пропускаем пустые строки
            type_line(line)
    print("Песня завершена!")

# Флаг для остановки
stop_flag = False

def on_num1():
    global stop_flag
    if not stop_flag:
        run_song()

def on_num2():
    global stop_flag
    stop_flag = True
    print("Остановка по запросу...")

# Настройка горячих клавиш
keyboard.add_hotkey('num 1', on_num1)
keyboard.add_hotkey('num 2', on_num2)

print("Бот готов! Нажмите Num1 для начала печати, Num2 для остановки.")
print("Rick Astley - Never Gonna Give You Up")

# Бесконечный цикл для поддержания работы программы
while True:
    time.sleep(1)
    stop_flag = False  # Сбрасываем флаг остановки после завершения