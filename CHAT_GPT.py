import keyboard
import time
from collections import deque

# Карта переходов
move_map = {
    1: {'up': 7, 'down': 4, 'left': 3, 'right': 2},
    2: {'up': 8, 'down': 5, 'left': 1, 'right': 3},
    3: {'up': 9, 'down': 6, 'left': 2, 'right': 1},
    4: {'up': 1, 'down': 7, 'left': 6, 'right': 5},
    5: {'up': 2, 'down': 8, 'left': 4, 'right': 6},
    6: {'up': 3, 'down': 9, 'left': 5, 'right': 4},
    7: {'up': 4, 'down': 1, 'left': 9, 'right': 8},
    8: {'up': 5, 'down': 2, 'left': 7, 'right': 9},
    9: {'up': 6, 'down': 3, 'left': 8, 'right': 7},
}

def press_key(key):
    keyboard.send(key)
    time.sleep(0.02)

def get_path(start, goal):
    queue = deque([(start, [])])
    visited = set()

    while queue:
        current, path = queue.popleft()
        if current == goal:
            return path
        if current in visited:
            continue
        visited.add(current)
        for direction, new_pos in move_map[current].items():
            queue.append((new_pos, path + [direction]))
    return []

# Загрузка кодов из файла
def load_codes(filename):
    codes = []
    with open(filename, "r") as file:
        for line in file:
            code = line.strip()
            if len(code) == 4 and all(ch in '123456789' for ch in code):
                codes.append([int(ch) for ch in code])
    return codes

codes = load_codes("codes.txt")
print(f"Загружено кодов: {len(codes)}")

# Обратный отсчёт
print("Наведи курсор на любую кнопку. Старт через:")
for i in range(3, 0, -1):
    print(i, "...")
    time.sleep(1)
print("🚀 Начинаю подбор\n")

current_pos = 5  # допустим, ты навёлся на 5

for idx, combo in enumerate(codes, 1):
    print(f"[{idx}/{len(codes)}] Пробуем: {combo}")
    for digit in combo:
        path = get_path(current_pos, digit)
        for direction in path:
            press_key(direction)
        press_key('e')
        time.sleep(0.2)
        current_pos = digit
    time.sleep(1.0)  # Ждём сброс
    # По идее, после сброса всегда возвращается в ту же позицию — оставим current_pos как есть

print("\n✅ Все коды перебраны.")
