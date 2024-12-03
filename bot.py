import os
import random
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from huify import huify
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
PORT = int(os.getenv("PORT", 8080))

# Вероятности событий
# Хорошо бы нормально вероятности подкрутить, но рот их ебать и так работает
PROCESS_PROBABILITY = 0.7  # Вероятность обработки сообщения (0.0 - никогда, 1.0 - всегда)
RESPONSE_PROBABILITY = 0.7  # Вероятность ответа случайной фразой вместо хуефикации

# Загрузка списка фраз из файла RESPONSES_FILE, который ниже
def load_responses(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Файл {file_path} не найден. Добавьте файл с фразами.")
        return []

RESPONSES_FILE = "responses.txt"
RESPONSES = load_responses(RESPONSES_FILE)

async def start(update: Update, context):
    await update.message.reply_text("Привет! Я хуевый бот. Напиши текст, и я либо хуефицирую его, либо отвечу фразой!")

async def handle_message(update: Update, context):
    # Если сообщение является ответом на другое сообщение, всегда отвечаем
    if update.message.reply_to_message:
        if random.random() <= RESPONSE_PROBABILITY and RESPONSES:  # Вероятность ответа случайной фразой
            random_response = random.choice(RESPONSES)
            await update.message.reply_text(random_response)
        else:  # Иначе хуефикация
            user_text = update.message.text
            huified_text = huify(user_text)
            await update.message.reply_text(huified_text)
        return

    if random.random() <= PROCESS_PROBABILITY:  # Вероятность обработки сообщения
        if random.random() <= RESPONSE_PROBABILITY and RESPONSES:  # Вероятность ответа случайной фразой
            random_response = random.choice(RESPONSES)
            await update.message.reply_text(random_response)
        else:  # Иначе хуефикация
            user_text = update.message.text
            huified_text = huify(user_text)
            await update.message.reply_text(huified_text)
    else:
        print(f"Сообщение пропущено: {update.message.text}") # pm2 logs

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start)) # Обработчик старта
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)) # Обработчик сообщений

    print(f"Бот запущен на порту {PORT}")
    app.run_polling()

if __name__ == "__main__":
    main()