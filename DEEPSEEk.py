import keyboard
import time
from collections import deque

# Предварительно вычисленные пути между всеми цифрами
precomputed_paths = {
    1: {1: [], 2: ['right'], 3: ['left'], 4: ['down'], 5: ['down', 'right'], 
        6: ['down', 'left'], 7: ['up'], 8: ['up', 'right'], 9: ['up', 'left']},
    2: {1: ['left'], 2: [], 3: ['right'], 4: ['down', 'left'], 5: ['down'], 
        6: ['down', 'right'], 7: ['up', 'left'], 8: ['up'], 9: ['up', 'right']},
    3: {1: ['right'], 2: ['left'], 3: [], 4: ['down', 'right'], 5: ['down', 'left'], 
        6: ['down'], 7: ['up', 'right'], 8: ['up', 'left'], 9: ['up']},
    4: {1: ['up'], 2: ['up', 'right'], 3: ['up', 'left'], 4: [], 5: ['right'], 
        6: ['left'], 7: ['down'], 8: ['down', 'right'], 9: ['down', 'left']},
    5: {1: ['up', 'left'], 2: ['up'], 3: ['up', 'right'], 4: ['left'], 5: [], 
        6: ['right'], 7: ['down', 'left'], 8: ['down'], 9: ['down', 'right']},
    6: {1: ['up', 'right'], 2: ['up', 'left'], 3: ['up'], 4: ['right'], 5: ['left'], 
        6: [], 7: ['down', 'right'], 8: ['down', 'left'], 9: ['down']},
    7: {1: ['down'], 2: ['down', 'right'], 3: ['down', 'left'], 4: ['up'], 
        5: ['up', 'right'], 6: ['up', 'left'], 7: [], 8: ['right'], 9: ['left']},
    8: {1: ['down', 'left'], 2: ['down'], 3: ['down', 'right'], 4: ['up', 'left'], 
        5: ['up'], 6: ['up', 'right'], 7: ['left'], 8: [], 9: ['right']},
    9: {1: ['down', 'right'], 2: ['down', 'left'], 3: ['down'], 4: ['up', 'right'], 
        5: ['up', 'left'], 6: ['up'], 7: ['right'], 8: ['left'], 9: []},
}

def press_key(key):
    keyboard.send(key)
    time.sleep(0.001)  # Уменьшил задержку в 20 раз

def load_codes(filename):
    with open(filename) as f:
        return [[int(ch) for ch in line.strip()] for line in f 
                if len(line.strip()) == 4 and line.strip().isdigit()]

codes = load_codes("codes.txt")
print(f"Загружено кодов: {len(codes)}")

# Быстрый обратный отсчёт
print("Старт через 3 секунды...")
time.sleep(3)
print("🚀 Старт!\n")

current_pos = 5
start_time = time.time()

for idx, combo in enumerate(codes, 1):
    if idx % 100 == 0:  # Вывод прогресса каждые 100 комбинаций
        print(f"[{idx}/{len(codes)}] {combo}")
    
    for digit in combo:
        for direction in precomputed_paths[current_pos][digit]:
            press_key(direction)
        keyboard.send('e')
        current_pos = digit
        time.sleep(0.02)  # Уменьшил задержку между цифрами
    
    time.sleep(1.0)  # Уменьшил время ожидания сброса

total_time = time.time() - start_time
print(f"\n✅ Готово! Время выполнения: {total_time:.1f} сек")
print(f"Средняя скорость: {len(codes)/total_time:.1f} комб/сек")