import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher

from src.services.rag_service import RAGService
from src.db.database import init_db
from src.handlers import commands, documents, chat

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
rag_service = RAGService(api_key=GEMINI_API_KEY)

# Реєстрація роутерів
dp.include_router(commands.router)
dp.include_router(documents.router)
dp.include_router(chat.router)

async def main():
    await init_db()
    print("Бот запущений із модульною структурою!")
    # Передаємо rag_service через workflow_data для доступу в хендлерах
    await dp.start_polling(bot, rag_service=rag_service)

if __name__ == "__main__":
    asyncio.run(main())