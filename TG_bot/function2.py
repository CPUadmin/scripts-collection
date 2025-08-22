import json
import requests
from Bot_main import CHAT_ID
from telegram import Update
from telegram.ext import ContextTypes
from event_translations import EVENT_TRANSLATIONS

OZON_TRACKING_URL = "https://tracking.ozon.ru/p-api/ozon-track-bff/tracking/{tracking_number}?source=Global"

def get_ozon_status(tracking_number="44612704-0204-1"):
    """Получает и обрабатывает статус посылки с Ozon"""
    try:
        response = requests.get(OZON_TRACKING_URL.format(tracking_number=tracking_number))
        data = response.json()
        
        # Получаем последнее событие
        last_event = data['items'][-1]
        event_name = last_event['event']
        event_time = last_event['moment'].split('T')[0]  # Берем только дату
        
        # Переводим статус
        status_ru = EVENT_TRANSLATIONS.get(event_name, event_name)
        
        # Форматируем результат
        return f"📦 Статус посылки:\n{status_ru} ({event_time})"
    
    except Exception as e:
        return f"⚠️ Ошибка при получении статуса: {str(e)}"

async def trackozon_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /trackozon"""
    status = get_ozon_status()
    await update.message.reply_text(status)

COMMANDS = [("trackozon", trackozon_handler)]