from Bot_main import CHAT_ID
from telegram import Update
from telegram.ext import ContextTypes
import datetime

async def hello_now_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отправляет приветствие с текущим временем"""
    current_time = datetime.datetime.now().strftime("%H:%M")
    await update.message.reply_text(f"👋 Привет! Сейчас {current_time}")

async def get_hello_message():
    """Возвращает приветственное сообщение (для GUI)"""
    current_time = datetime.datetime.now().strftime("%H:%M")
    return f"👋 Приветствие отправлено в {current_time}"

COMMANDS = [("hello_now", hello_now_handler)]