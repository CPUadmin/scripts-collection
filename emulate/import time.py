import time

# Параметры конфигурации
MAX_FAILURES = 3  # Максимальное количество отключений подряд
BLOCK_TIME = 900  # Время блокировки (15 минут) в секундах
SLEEP_TIME = 120  # Время ожидания перед повторной проверкой (2 минуты)

# Переменные состояния устройства
device_connected = True  # Статус устройства (True = подключено, False = отключено)
failed_count = 0  # Счетчик отключений
is_blocked = False  # Статус блокировки устройства

# Эмуляция действий
def emulate_connect():
    """Эмулирует подключение устройства."""
    global device_connected
    device_connected = True
    print("Устройство подключено.")

def emulate_disconnect():
    """Эмулирует отключение устройства."""
    global device_connected
    device_connected = False
    print("Устройство отключено.")

def block_device():
    """Блокирует устройство на определенное время."""
    global is_blocked, failed_count
    is_blocked = True
    failed_count = 0  # Сброс счетчика отключений
    print(f"Устройство заблокировано на {BLOCK_TIME} секунд.")
    time.sleep(BLOCK_TIME)  # Имитация блокировки
    is_blocked = False
    print("Устройство разблокировано.")

# Основной цикл проверки
def monitor_device():
    global failed_count, is_blocked

    while True:
        if is_blocked:
            print("Устройство заблокировано. Ожидание...")
            time.sleep(SLEEP_TIME)
            continue

        if not device_connected:
            failed_count += 1
            print(f"Отключение устройства. Счетчик ошибок: {failed_count}/{MAX_FAILURES}")

            if failed_count >= MAX_FAILURES:
                block_device()
            else:
                print(f"Устройство не подключено. Сон на {SLEEP_TIME} секунд...")
                time.sleep(SLEEP_TIME)
        else:
            failed_count = 0
            print("Устройство подключено. Счетчик ошибок сброшен.")
            time.sleep(5)  # Проверка каждые 5 секунд

# Эмуляция управления
if __name__ == "__main__":
    import threading

    # Запускаем мониторинг устройства в отдельном потоке
    monitor_thread = threading.Thread(target=monitor_device, daemon=True)
    monitor_thread.start()

    # Симуляция управления подключением устройства
    while True:
        print("\nДействия:")
        print("1. Подключить устройство")
        print("2. Отключить устройство")
        print("3. Выход")
        choice = input("Выберите действие: ")

        if choice == "1":
            emulate_connect()
        elif choice == "2":
            emulate_disconnect()
        elif choice == "3":
            print("Выход из программы.")
            break
        else:
            print("Некорректный ввод. Попробуйте снова.")
