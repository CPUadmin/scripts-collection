import tkinter as tk
from tkinter import messagebox
import threading
import time

# Глобальные переменные
failed_attempts = 0
disconnected_attempts = 0
max_attempts = 3
block_time = 600  # 10 минут в секундах
last_disconnect_time = 0
mac_address = "48:8F:4C:FD:10:54"
device_connected = False  # Моделируем, подключено ли устройство
attempting_to_connect = False  # Флаг, который отслеживает попытки подключения
stop_connection_attempts = False  # Флаг для остановки попыток подключения
connection_thread = None  # Переменная для хранения потока попытки подключения

# Функция для имитации подключения устройства
def device_connect(force=False):
    global device_connected
    if not force:
        # Показать всплывающее окно для подтверждения насильного подключения
        response = messagebox.askyesno("Подтверждение", "Вы уверены, что хотите насильно подключить устройство?")
        if not response:
            print("Ошибка: устройство не подключено")
            return
    device_connected = True
    update_status()

# Функция для имитации отключения устройства
def device_disconnect():
    global device_connected
    device_connected = False
    update_status()

# Функция для обновления статуса индикатора и текста
def update_status():
    if device_connected:
        status_label.config(text="Устройство подключено", fg="green")
        status_circle.config(bg="green")
    elif stop_connection_attempts:
        status_label.config(text="Попытка подключения остановлена", fg="yellow")
        status_circle.config(bg="yellow")
    else:
        status_label.config(text="Устройство отключено", fg="red")
        status_circle.config(bg="red")

# Функция для выполнения попытки подключения
def attempt_connection():
    global failed_attempts, disconnected_attempts, last_disconnect_time, attempting_to_connect, stop_connection_attempts

    while not stop_connection_attempts:
        if device_connected:
            failed_attempts = 0  # сбрасываем неудачные попытки
            print(f"Устройство подключено: {mac_address}")
        else:
            failed_attempts += 1
            print(f"Неудачная попытка подключения, попыток: {failed_attempts}")

        if failed_attempts >= max_attempts:
            disconnected_attempts += 1
            print(f"Неудачные попытки подключения: {disconnected_attempts}")

        if failed_attempts >= max_attempts:
            print(f"Превышено количество неудачных попыток, начинаем блокировку на 10 минут.")
            update_status()
            time.sleep(block_time)  # Блокировка на 10 минут
            print(f"Блокировка завершена, устройство может попытаться подключиться снова.")
            failed_attempts = 0  # Сброс счетчика неудачных попыток

        if disconnected_attempts >= max_attempts:
            print(f"Превышено количество отключений, начинаем блокировку на 10 минут.")
            update_status()
            time.sleep(block_time)  # Блокировка на 10 минут
            print(f"Блокировка завершена, устройство может попытаться подключиться снова.")
            disconnected_attempts = 0  # Сброс счетчика отключений

        time.sleep(2)  # Интервал между попытками подключения

# Функция для начала/остановки попыток подключения
def start_connection_attempts():
    global attempting_to_connect, stop_connection_attempts, connection_thread

    if not attempting_to_connect:
        stop_connection_attempts = False
        attempting_to_connect = True
        connection_thread = threading.Thread(target=attempt_connection)
        connection_thread.daemon = True  # Завершается при закрытии программы
        connection_thread.start()
        start_button.config(text="Остановить попытки подключения")
    else:
        stop_connection_attempts = True
        attempting_to_connect = False
        connection_thread.join()  # Ждем завершения потока
        start_button.config(text="Запустить попытки подключения")

# Функция для завершения работы скрипта
def quit_program():
    root.quit()

# Создаем окно с интерфейсом
root = tk.Tk()
root.title("MikroTik Connection Control")

# Метка для статуса
status_label = tk.Label(root, text="Статус: Ожидание подключения", font=("Arial", 14))
status_label.pack(pady=10)

# Круглый индикатор статуса
status_circle = tk.Label(root, text="•", font=("Arial", 30), fg="red")
status_circle.pack()

# Кнопка для подключения устройства
connect_button = tk.Button(root, text="Подключить устройство", command=lambda: device_connect(force=True), width=20)
connect_button.pack(pady=5)

# Кнопка для отключения устройства
disconnect_button = tk.Button(root, text="Отключить устройство", command=device_disconnect, width=20)
disconnect_button.pack(pady=5)

# Кнопка для начала/остановки попыток подключения
start_button = tk.Button(root, text="Запустить попытки подключения", command=start_connection_attempts, width=20)
start_button.pack(pady=5)

# Кнопка для завершения работы программы
quit_button = tk.Button(root, text="Завершить работу", command=quit_program, width=20)
quit_button.pack(pady=5)

# Запуск главного цикла интерфейса
root.mainloop()
