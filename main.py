import asyncio
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart

from src.services.rag_service import RAGService

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
rag_service = RAGService(api_key=GEMINI_API_KEY)

@dp.message(CommandStart())
async def start_handler(message: types.Message):
    await message.answer("Привіт! Я корпоративний AI-асистент. Задай мені питання стосовно регламенту компанії.")

@dp.message()
async def query_handler(message: types.Message):
    await message.bot.send_chat_action(chat_id=message.chat.id, action="typing")
    answer = rag_service.answer_question(message.text)
    await message.answer(answer)

async def main():
    print("Бот успішно запущений!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())