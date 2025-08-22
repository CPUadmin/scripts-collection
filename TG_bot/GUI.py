import tkinter as tk
import requests
import json
import threading
from importlib import import_module
from tkinter import messagebox

# Загружаем настройки
with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)
BOT_TOKEN = config["BOT_TOKEN"]
CHAT_ID = config["CHAT_ID"]

class BotController:
    def __init__(self, root):
        self.root = root
        self.root.title("OZON Bot Controller")
        self.root.geometry("600x500")
        self.root.configure(bg="#f0f8ff")
        
        # Заголовок
        tk.Label(root, text="Управление Ozon Ботом", 
                font=("Arial", 16, "bold"), bg="#f0f8ff").pack(pady=10)
        
        # Фрейм для кнопок функций
        functions_frame = tk.LabelFrame(root, text="Доступные функции", 
                                      bg="#f0f8ff", font=("Arial", 12))
        functions_frame.pack(pady=10, padx=15, fill="x")
        
        # Динамическая загрузка функций
        self.load_functions(functions_frame)
        
        # Лог действий
        log_frame = tk.LabelFrame(root, text="Журнал действий", 
                                bg="#f0f8ff", font=("Arial", 12))
        log_frame.pack(pady=10, padx=15, fill="both", expand=True)
        
        self.log = tk.Text(log_frame, height=10, state='disabled', bg="white")
        self.log.pack(pady=10, padx=10, fill="both", expand=True)
        
        # Кнопка очистки лога
        tk.Button(root, text="Очистить журнал", command=self.clear_log,
                 bg="#ff6b6b", fg="white").pack(pady=5)
    
    def load_functions(self, frame):
        """Динамически загружает функции из модулей function*"""
        try:
            for i in range(1, 10):  # Поддерживаем до 9 функций
                module_name = f"function{i}"
                try:
                    module = import_module(module_name)
                    
                    # Создаем кнопку для функции
                    btn = tk.Button(frame, text=f"⚡ Запустить function{i}",
                                   command=lambda m=module: self.execute_function(m),
                                   bg="#4ecdc4", fg="white", font=("Arial", 10))
                    btn.pack(pady=5, padx=10, fill="x")
                    
                except ImportError:
                    break  # Прекращаем, когда модули закончатся
                    
        except Exception as e:
            self.add_log(f"⚠️ Ошибка загрузки функций: {str(e)}")
    
    def execute_function(self, module):
        """Выполняет функцию из модуля"""
        threading.Thread(target=self._run_function, args=(module,), daemon=True).start()
    
    def _run_function(self, module):
        """Запускает функцию в отдельном потоке"""
        try:
            func_name = getattr(module, "COMMANDS")[0][0]
            self.add_log(f"🚀 Запуск функции: {func_name}")
            
            # Пробуем получить результат через специальный метод
            try:
                result_func = getattr(module, f"get_{func_name}_result", None)
                if result_func:
                    result = result_func()
                    self._send_message(result)
                    self.add_log(f"✅ Результат отправлен: {result}")
                else:
                    # Если специального метода нет, используем обработчик
                    handler = getattr(module, f"{func_name}_handler")
                    self._send_telegram_command(f"/{func_name}")
                    self.add_log(f"📨 Команда отправлена: /{func_name}")
            except Exception as e:
                self.add_log(f"⚠️ Ошибка выполнения: {str(e)}")
                
        except Exception as e:
            self.add_log(f"🚨 Критическая ошибка: {str(e)}")
    
    def _send_message(self, text):
        """Отправляет сообщение в Telegram"""
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        requests.post(url, data={
            "chat_id": CHAT_ID,
            "text": text,
            "parse_mode": "HTML"
        })
    
    def _send_telegram_command(self, command):
        """Отправляет команду в Telegram"""
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        requests.post(url, data={
            "chat_id": CHAT_ID,
            "text": command
        })
    
    def add_log(self, message):
        """Добавляет запись в лог"""
        self.root.after(0, self._update_log, message)
    
    def _update_log(self, message):
        """Обновляет лог (вызывается из основного потока)"""
        self.log.config(state='normal')
        self.log.insert('end', message + "\n")
        self.log.see('end')
        self.log.config(state='disabled')
    
    def clear_log(self):
        """Очищает лог"""
        self.log.config(state='normal')
        self.log.delete(1.0, 'end')
        self.log.config(state='disabled')

if __name__ == "__main__":
    root = tk.Tk()
    app = BotController(root)
    root.mainloop()