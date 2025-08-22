import time
import keyboard
import mouse
from pynput.keyboard import Controller, Key

# Инициализация контроллера клавиатуры
pynput_keyboard = Controller()

# Текст, который нужно ввести
text_to_type = "Valuable Piano"

def run_macro():
    # 1. Зажимаем Tab на 1 секунду
    keyboard.press('tab')
    time.sleep(1)
    keyboard.release('tab')
    
    # 2. Стираем лишний текст
    for _ in range(20):
        keyboard.press_and_release('backspace')
        time.sleep(0.02)
    
    # 3. Печатаем текст
    for char in text_to_type:
        pynput_keyboard.press(char)
        pynput_keyboard.release(char)
        time.sleep(0.02)  # Небольшая задержка между символами (похоже на реальный ввод)
    
    # 4. Кликаем ЛКМ
    mouse.click('left')
    time.sleep(0.3)

    # 5. Нажимаем Enter
    pynput_keyboard.press(Key.enter)
    pynput_keyboard.release(Key.enter)

print("Макрос готов! Нажимай Num1 для выполнения.")

# Ждём нажатия Num1
while True:
    if keyboard.is_pressed('num 1'):
        run_macro()
        time.sleep(0.5)
