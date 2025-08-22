import json
import requests
from Bot_main import CHAT_ID
from telegram import Update
from telegram.ext import ContextTypes

async def test_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Тестовая функция для проверки работы бота"""
    await update.message.reply_text("✅ Бот работает исправно!")

async def get_test_result():
    """Возвращает тестовое сообщение (для GUI)"""
    return "✅ Система функционирует нормально"

COMMANDS = [("test", test_handler)]