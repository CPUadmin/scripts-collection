import logging
import os
import json
import importlib
import traceback
import asyncio
from telegram.ext import ApplicationBuilder, CommandHandler
from apscheduler.schedulers.asyncio import AsyncIOScheduler
# Добавьте в начало файла:
import sys
import os

# Добавьте после load_functions():
# Автоматическая перезагрузка модулей
def load_functions(app):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    for file in os.listdir(current_dir):
        if file.startswith("function") and file.endswith(".py"):
            module_name = file[:-3]
            try:
                # Выгружаем модуль, если он уже загружен
                if module_name in sys.modules:
                    del sys.modules[module_name]
                
                module = importlib.import_module(module_name)
                if hasattr(module, "COMMANDS"):
                    for command_name, handler in module.COMMANDS:
                        app.add_handler(CommandHandler(command_name, handler))
                        logging.info(f"✅ Добавлена команда: /{command_name}")
            except Exception as e:
                logging.error(f"⚠️ Не удалось импортировать {module_name}: {e}")
                logging.error(traceback.format_exc())
# === Логирование ===
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler("bot.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

# === Загрузка настроек ===
with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

BOT_TOKEN = config["BOT_TOKEN"]
CHAT_ID = int(config["CHAT_ID"])
AUTOTRACK_SETTINGS = config.get("autotrack", {})
DAILY_TRACKOZON_SETTINGS = config.get("daily_trackozon", {})

# === Команды ===
async def start(update, context):
    await update.message.reply_text(
        "👋 Привет! Я многофункциональный бот.\n\n"
        "Команды:\n"
        "/start — запустить бота\n"
        "/help — помощь\n"
        "/test — проверить работу бота\n"
        "/trackozon — статус посылки OZON\n"
        "/hello вкл — включить приветствие\n"
        "/hello выкл — выключить приветствие"
    )

async def help_command(update, context):
    await update.message.reply_text(
        "📌 Доступные команды:\n"
        "/start — запустить бота\n"
        "/help — помощь\n"
        "/test — проверить работу бота\n"
        "/trackozon — статус посылки OZON\n"
        "/hello вкл — включить приветствие\n"
        "/hello выкл — выключить приветствие"
    )

# === Асинхронная функция для отправки сообщения ===
async def send_trackozon(bot, chat_id):
    try:
        await bot.send_message(chat_id=chat_id, text="/trackozon")
        logging.info(f"✅ Автообновление: /trackozon отправлен.")
    except Exception as e:
        logging.error(f"⚠️ Ошибка при отправке запроса: {e}")

# === Планировщик ===
async def on_startup(app):
    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")

    # Ежедневная задача
    if DAILY_TRACKOZON_SETTINGS.get("enabled", False):
        scheduler.add_job(
            lambda: asyncio.create_task(send_trackozon(app.bot, CHAT_ID)),
            'cron',
            hour=DAILY_TRACKOZON_SETTINGS.get("hour", 10),
            minute=DAILY_TRACKOZON_SETTINGS.get("minute", 0)
        )
        logging.info(f"✅ Ежедневная задача запланирована на {DAILY_TRACKOZON_SETTINGS['hour']}:{DAILY_TRACKOZON_SETTINGS['minute']:02d}.")

    # Интервальная задача
    if AUTOTRACK_SETTINGS.get("enabled", False):
        scheduler.add_job(
            lambda: asyncio.create_task(send_trackozon(app.bot, CHAT_ID)),
            'interval',
            hours=AUTOTRACK_SETTINGS.get("hours", 0),
            minutes=AUTOTRACK_SETTINGS.get("minutes", 0)
        )
        logging.info(f"✅ Автообновление запущено! Интервал: {AUTOTRACK_SETTINGS.get('hours', 0)} ч. {AUTOTRACK_SETTINGS.get('minutes', 0)} мин.")
    else:
        logging.info("⏸️ Автообновление отключено.")

    scheduler.start()
    logging.info("✅ Планировщик запущен!")

# === Загрузка команд из функций ===
def load_functions(app):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    for file in os.listdir(current_dir):
        if file.startswith("function") and file.endswith(".py"):
            module_name = file[:-3]
            try:
                module = importlib.import_module(module_name)
                if hasattr(module, "COMMANDS"):
                    for command_name, handler in module.COMMANDS:
                        app.add_handler(CommandHandler(command_name, handler))
                        logging.info(f"✅ Добавлена команда: /{command_name}")
            except Exception as e:
                logging.error(f"⚠️ Не удалось импортировать {module_name}: {e}")
                logging.error(traceback.format_exc())

# === Основной запуск ===
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).post_init(on_startup).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))

    load_functions(app)

    logging.info("🚀 Бот запущен и готов к работе!")
    app.run_polling()

if __name__ == "__main__":
    main()

# Добавь в конец файла:

async def execute_command(command: str):
    """Выполняет команду напрямую"""
    mock_update = Update(update_id=0, message=Message(
        message_id=0,
        date=datetime.now(),
        chat=Chat(id=CHAT_ID, type='private'),
        text=command
    ))
    
    if command == "/trackozon":
        await trackozon_handler(mock_update, None)
    elif command == "/hello_now":
        await hello_now_handler(mock_update, None)
    # ... добавь другие команды